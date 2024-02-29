from fastapi import APIRouter, Request, Header, HTTPException, UploadFile
from models.users import new_v2_user_profile, v2_user
from models.users import user_picture as UserPicture
from internal.db import get_conn
from internal.db import create_user_profile as db_create_userprofile
from internal.db import get_user_profile as db_get_user_profile
from internal.db import delete_user_profile as db_delete_user_profile
from internal.db import update_user_photos_num as db_update_userimage_num
from internal.db import get_user_publice_info as db_get_user_publice_info
from internal.redis import get_conn as get_redis_conn
from internal.logger import create_logger

import aioredis
from PIL import Image
from starlette.responses import StreamingResponse

import random, string, io

router = APIRouter(
    prefix="/api/v2"
)

logger = create_logger("router.user.v2")
# RhyTccxMKJ ndqyiRBPqw
@router.post("/user_profile", status_code=201, tags=["user", "v2"])
async def create_user_profile(req: new_v2_user_profile):
    logger.info("Handle user profile create request")
    
    req_dict = req.dict()
    
    # Generate caption
    user_code = ''.join(random.choice(string.ascii_letters) for x in range(10))
    
    user_profile = v2_user(name=req_dict["name"], password=req_dict["password"], email=req_dict["email"], profile_picture=req_dict["profile_picture"], caption=req_dict["caption"], friend_code=user_code, country=req_dict["country"], num_photos_uploaded=1)
    
    conn = get_conn()
    status, val = db_create_userprofile(conn, user_profile)
    if status != 0:
        logger.error(val)
        raise HTTPException(500, detail=val)
    
    # init user state for match feature
    logger.info("Init user match status to default")
    try:
        redis_conn = get_redis_conn()
        await redis_conn.sadd("users:normal", user_code)
        await redis_conn.set(f"user:{user_code}:status", "default")
    except Exception as e:
        logger.warning(str(e))
        
    finally:
       await redis_conn.close()

    return {"user_id": val, "caption": user_code}

@router.get("/user_profile/{user_id}", status_code=200, tags=["user", "v2"])
async def get_user_profile(user_id: int):
    logger.info("Handle user profile get request")

    try:    
        conn = get_conn()
        name, email, profile_picture, caption, friend_code, country, num_photos_uploaded = db_get_user_profile(conn, user_id)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(500, detail=str(e) + ", check if user exist")
    finally:
        conn.close()

    return {"username": name, "email": email, "profile_picture": profile_picture, "caption": caption, "friend_code": friend_code, "country": country, "num_photos_uploaded": num_photos_uploaded}

@router.delete("/user_profile/{user_id}", status_code=204, tags=["user", "v2"])
async def delete_user_profile(user_id: int):
    logger.info("Handle delete user profile request")
    try:
        conn = get_conn()
        status, msg = db_delete_user_profile(conn, user_id)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(500, detail=str(e))
    finally:
        conn.close()
        
    return

@router.post("/user_picture/{user_id}", status_code=201, tags=["user", "v2"])
async def create_user_image(user_id: int, img: UploadFile):
    logger.info("Create user picture")
    link = ''.join(random.choice(string.ascii_letters) for x in range(10))
    user_picture = UserPicture(user_id=user_id, picture=img, url=link)
    
    contents = await img.read()
    
    try:
        # connect redis db
        redis_conn = get_redis_conn()
        await redis_conn.hset("images", link, contents)
        await redis_conn.sadd(f"user_images:{user_id}", link)
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    finally:
        # Close the Redis connection
        await redis_conn.close()
    conn = get_conn()
    status, msg = db_update_userimage_num(conn, user_id=user_id, offset=1)
    if status != 0:
        logger.error("Failed to update user image num: " + msg)
    
    return {"link": link}

@router.get("/user_picture/{user_id}/{img_id}", status_code=200, tags=["user", "v2"])
async def get_single_user_image(img_id: str, user_id: int):
    logger.info("Get user picture with image id")
    image_data = None
    
    try:
        # connect redis db
        redis_conn = await get_redis_conn()
        image_data = await redis_conn.hget("images", img_id)
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    finally:
        # Close the Redis connection
        await redis_conn.close()
        
    if image_data is None:
        raise HTTPException(404, detail="Image not found")
    
    # Convert the image data to a PIL Image object
    image = Image.open(io.BytesIO(image_data))

    # Return the image as a response
    img_io = io.BytesIO()
    image.save(img_io, format='PNG')
    img_io.seek(0)

    return StreamingResponse(content=img_io, media_type="image/png")

@router.get("/user_picture/{user_id}", status_code=200, tags=["user", "v2"])
async def get_all_user_images(user_id: int):
    logger.info("Get user images with given user id")
    image_ids = None
    
    try:
        # connect redis db
        redis_conn = await get_redis_conn()
        image_ids = await redis_conn.smembers(f"user_images:{user_id}")
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    finally:
        # Close the Redis connection
        await redis_conn.close()
        
    if image_ids is None:
        raise HTTPException(404, detail="Image not found")
    
    # Convert the image IDs from bytes to integers
    image_ids = [image_id.decode() for image_id in image_ids]

    return {"user_id": user_id, "image_ids": image_ids}

@router.delete("/user_picture/{user_id}", status_code=204, tags=["user", "v2"])
async def delete_all_user_images(user_id: int):
    logger.info("Clean up user images")
    image_ids = None
    result = 0
    logger.info("Get all user image links from redis")
    try:
        redis_conn = await get_redis_conn()
        image_ids = await redis_conn.smembers(f"user_images:{user_id}")
    except Exception as e:
        logger.error("User doesn't have any image")
        return {"message": "Clean up user associated images successfully"}
    finally:
        await redis_conn.close()
        
    # Convert the image IDs from bytes to strings
    image_ids = [image_id.decode() for image_id in image_ids]

    logger.info("Clean up images")
    # Perform cleanup actions for each image
    try:
        redis_conn = get_redis_conn()
        for image_id in image_ids:
            # Delete the image from your storage (e.g., file system, cloud storage, etc.)
            await redis_conn.hdel("images", image_id)
    except Exception as e:
        logger.error(str(e))
    finally:
        await redis_conn.close()
    
    # Delete the user's images from the Redis Set
    try:
        # connect redis db
        redis_conn = await get_redis_conn()
        result = await redis_conn.delete(f"user_images:{user_id}")
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    finally:
        await redis_conn.close()
    logger.debug(result)
    if result == 0:
        # Return a 404 response if the user or their images were not found
        raise HTTPException(404, detail="User or images not found")

    return {"message": "Clean up user associated images successfully"}

@router.delete("/user_picture/{user_id}/{img_id}", status_code=204, tags=["user", "v2"])
async def delete_single_user_image(img_id: str, user_id: int):
    result = 0
    try:
        # Establish a connection to Redis
        redis_conn = await get_redis_conn()
        # Delete the image from the Redis Hash
        result = await redis_conn.hdel("images", img_id)
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    finally:
        # Close the Redis connection
        await redis_conn.close()

    if result == 0:
        # Return a 404 response if the image was not found
        raise HTTPException(404, detail="Image not found")

    try:
        conn = get_conn()
        status, msg = db_update_userimage_num(conn, user_id, -1)
        if status != 0:
            logger.error("Failed to update user profile uploaded image num field: " + msg)
    except Exception as e:
        logger.error(str(e))
    finally:
        conn.close()
        
    try:
        redis_conn = get_redis_conn()
        await redis_conn.srem(f"user_images:{user_id}", img_id)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(500, detail=str(e))
    finally:
        await redis_conn.close()

    # Return a success message
    return {"message": "Image deleted successfully"}

@router.get("/friendy_code/{code}", status_code=200, tags=["v2", "matches"])
async def get_user_info(code: str):
    name = ""
    country = ""
    try:
        conn = get_conn()
        name, country = db_get_user_publice_info(conn, code)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(500, detail=str(e))
    finally:
        conn.close()
    
    return {"name": name, "country": country}
#DYykODHPOa  QrCjrKCIkc
@router.get("/{friendy_code}/match", status_code=200, tags=["v2", "matches"])
async def get_user_match(friendy_code: str):
    logger.info("Handle user get match request")
    matched_user_friendly_code = ""

    try:
        redis_conn = get_redis_conn()
        
        status = await redis_conn.get(f"user:{friendy_code}:status")
        matched_user = await redis_conn.get(f"user:{friendy_code}:matched_user")

        if status is None:
            return {"status": "User not found."}
        
        if matched_user is None:
            # select a user in matching phase randomly\
            matching_users = await redis_conn.smembers("users:matching")

            # exclude user itself            
            matching_users = {user for user in matching_users if user != friendy_code.encode()}
            
            logger.debug("User in matching phase (excluse user himself): " + matching_users)
            
            if not matching_users:
                if status.decode() == "default":
                    return {"status": "Not in matching"}
                logger.debug("Current user is in " + status.decode())
                logger.debug("No user in matching phase")
                return {"status": "Matching"}
            
            matched_user = random.choice(list(matching_users))
            matched_user_friendly_code = matched_user.decode()
            
            # update users status
            await redis_conn.srem("users:matching", friendy_code)
            await redis_conn.srem("users:matching", matched_user_friendly_code)
            await redis_conn.sadd("users:matched", friendy_code)
            await redis_conn.sadd("users:matched", matched_user_friendly_code)

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(500, detail=str(e))
    
    finally:
        await redis_conn.close()
    
    logger.info("Get matched user public info")
    try:
        conn = get_conn()
        matched_user_name, matched_user_country = db_get_user_publice_info(conn, matched_user_friendly_code)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(500, detail="Fail to get matched user public info: " + str(e))
    finally:
        conn.close()
    
    return {"status": "Matched", "username": matched_user_name, "country": matched_user_country}

@router.post("/{friendy_code}/match", status_code=201, tags=["v2", "matches"])
async def create_user_match(friendy_code: str):
    logger.info("Handle user match request")
    try:
        redis_conn = get_redis_conn()
        await redis_conn.set(f"user:{friendy_code}:status", "matching")
        await redis_conn.sadd("users:matching", friendy_code)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(500, detail=str(e))
    finally:
        await redis_conn.close()
    
    return {"status": "Match request created"}

@router.delete("/{friendy_code}/match", status_code=204, tags=["v2", "matches"])
async def delete_user_match(friendy_code: str):
    logger.info("Handle user match cancel request")
    try:
        redis_conn = get_redis_conn()
        if await redis_conn.get(f"user:{friendy_code}:status") != b"matching":
            return {"status": "User is not in matching state."}
        
        # update user state to default
        await redis_conn.set(f"user:{friendy_code}:status", "default")
        
        return {"status": "Match canceled."}
    
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(500, detail=str(e))

    finally:
        await redis_conn.close()