from flask import Flask, render_template, request, jsonify, session, g, redirect, url_for, session

import requests

import os

import json

from datetime import datetime, timedelta

from dateutil.parser import parse

from werkzeug.utils import secure_filename

from flask import Flask

from flask import request

import sqlite3



app = Flask(__name__,

            static_url_path="/static")

app.secret_key = "group2secretkey"

username = "default_username"





# @app.route("/api")

# def my_api():

#     """

#     My API

#     ---

#     get:

#       description: Get some data

#       responses:

#         200:

#           description: A successful response

#     """

#     return 'Hello, world!'



# @app.route("/api/spec")

# def spec():

#     swag = swagger(app)

#     swag['info']['version'] = "1.0"

#     swag['info']['title'] = "My API"

#     return jsonify(swag)







@app.route("/")

def initial():

    return render_template("index.html")



@app.before_request

def set_username():

    g.username = username



@app.before_request

def set_userid():

    g.userid = ""



@app.before_request

def set_friendy_code():

    g.friendy_code = ""



# @app.before_request

# def set_country():

#     g.country = country



@app.route("/user_register", methods=["GET", "POST"])

def user_register():

    # global username

    # global userid

    

    # # get data from web

    # username = request.form["username"]

    # password = request.form["password"]

    # print(username)

    # print(password)

    # print(type(username))

    # print(type(password))



    # # Check if username and password are not empty

    # if not username or not password:

    #     return "Username or password is missing", 400

    

    # # sent data to db to compare

    # url="http://192.168.10.4:30180/api/v1/user"

    # data = {

    #     "username": username,

    #     "userpassword": password

    # }



    # print(data)

    # response = requests.post(url, json=data)



    # # Print the response status code and text

    # print(response.status_code)

    # print(response.text)



    # # Extract ID from response and save to localStorage

    # g.userid = json.loads(response.text)["id"]

    # session["userid"] = g.userid

    # print(g.userid)



    return render_template("user_register.html", username=username)



@app.route("/user_login", methods=["GET", "POST"])

def user_login():

    global userid

    global friendy_code 

    global username

    global country

    global email

    # global profile_pic



    if request.method == "POST":

        # get data from user_register web

        username = request.form["username"]

        password = request.form["password"]

        country = request.form["country"]

        email = request.form["email"]



        print(username)

        print(password)

        print(country)

        print(email)



        # Check if username and password are not empty

        if not username or not password:

            return "Username or password is missing", 400

        

      



        # profile_pics = {}

        # for playerId in ["player1", "player2", "player3"]:

        #     if request.form.get("profile_pic_" + playerId):

        #         profile_pics[playerId] = request.form.get("profile_pic_" + playerId)

            



        # sent data to db

        url="http://192.168.10.4:30180/api/v2/user_profile"

        data = {

            "name": username,

            "password": password,

            "email": email,

            "profile_picture": None,

            "caption": None,

            "country": country,

        }

        # Redirect to the user_login.html page or any other desired page

       

        print(data)

        response = requests.post(url, json=data)



        print(response.status_code)

        print(response.text)



        if response != 0:

        

            # Extract ID from response and save to localStorage

            userid = json.loads(response.text)["user_id"]

            session["userid"] = userid

            print(userid)



            friendy_code = json.loads(response.text)["friendy_code"]

            session["friendy_code"] = friendy_code

            print(friendy_code)



            return redirect(url_for("user_login"))



        else:

            return "Error inserting user profile into the database", 500



    return render_template("user_login.html")



@app.route("/room_list")

def room_list():

    return render_template("room_list.html")





@app.route("/check_all")

def check_all():

    return render_template("check_all.html")





@app.route("/pending_finish")

def pending_finish():

    # input_roomname = request.form["input_roomname"]

    # input_roomdetail = request.form["input_roomdetail"]

    # input_maxpeople = request.form["input_maxpeople"]



    # return render_template("pending_finish.html",input_roomname = input_roomname,input_roomdetail = input_roomdetail,input_maxpeople = input_maxpeople)



    return render_template("pending_finish.html")



@app.route("/rules")

def rules():

    return render_template("rules.html")



@app.route("/room/", methods=["POST", "GET"])

def room():

    

    username = request.form["username"]

    password = request.form["password"]



    # g.username = username 

    session["username"] = username



    url=f"http://192.168.10.4:30180/api/v2/admin/user_profile/{username}"

    

    response = requests.get(url)

    print(response.status_code)

    print(response.text)



    if response.status_code == 200:

        user_data = response.json()

        user_id = user_data["id"]

        session["user_id"] = user_id

        print(user_id)

        return render_template("room.html", username=username)

    elif response.status_code == 404:

        return "User does not exist"

    else:

        return "Error retrieving user profile from the database"

    



    # print(data)

    # response = requests.post(url, json=data)



    # # Print the response status code and text

    # print(response.status_code)

    # print(response.text)



    # # Extract ID from response and save to localStorage

    # g.userid = json.loads(response.text)["id"]

    # session["userid"] = g.userid

    # print(g.userid)



    # return render_template("room.html", username=username)





@app.route("/create_room/" , methods = ["POST", "GET"])

def create_room():

    username = session.pop("username", None)

    session["username"] = username



    return render_template("create_room.html", username = username)



# Create a connection to the SQLite database

# conn = sqlite3.connect('local_database.db')

# cursor = conn.cursor()



# # Create a table if it doesn't exist

# cursor.execute('''CREATE TABLE IF NOT EXISTS rooms

#                   (ownerId INT, roomName TEXT, descript TEXT, `limit` INT)''')



DATABASE = 'local_database.db'



def get_db():

    db = getattr(g, '_database', None)

    if db is None:

        db = g._database = sqlite3.connect(DATABASE)

    else:

        try:

            db.execute('SELECT 1')

        except sqlite3.ProgrammingError:

            db = g._database = sqlite3.connect(DATABASE)

    return db









# Create the rooms table if it doesn't exist

def create_rooms_table():

    conn = get_db()

    cursor = conn.cursor()

     # Drop the existing "rooms" table (if it exists)
    cursor.execute("DROP TABLE IF EXISTS rooms")

    # Create the new "rooms" table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            room_name TEXT,
            room_detail TEXT,
            max_people INTEGER
        )
    """)



    conn.commit()

    cursor.close()

    conn.close()





@app.route("/create_room_finish/" , methods = ["GET", "POST"])

def create_room_finish():

    create_rooms_table()  # Create the rooms table if it doesn't exist



    username = session.pop("username", None)

    session["username"] = username

    

    user_id = session.pop("user_id", None)

    session["user_id"] = user_id



    # userid = session.get("userid")

    print("user_id is " + str(user_id))





    input_roomname = request.form["input_roomname"]

    input_maxpeople = int(request.form["input_maxpeople"])

    input_roomdetail = request.form["input_roomdetail"]

    print("input_roomname is " + input_roomname)

    print("input_maxpeople is" + str(input_maxpeople))

    print("input_roomdetail is " + input_roomdetail)



     # Get the database connection

    conn = get_db()

    cursor = conn.cursor()



   # Check if the user_id column already exists in the rooms table

    cursor.execute("PRAGMA table_info(rooms)")

    columns = cursor.fetchall()

    column_names = [column[1] for column in columns]



    if "user_id" not in column_names:

        # Add the user_id column to the existing table

        cursor.execute("ALTER TABLE rooms ADD COLUMN user_id INTEGER")



     # Save the data locally in the SQLite database

    cursor.execute("INSERT INTO rooms (user_id, room_name, room_detail, max_people) VALUES (?, ?, ?, ?)",

                   (user_id, input_roomname, input_roomdetail, input_maxpeople))

    conn.commit()





     # Get the inserted room ID

    room_id = cursor.lastrowid

    print(room_id)



    # Close the connection

    cursor.close()

    conn.close()



    # Convert room_id to JSON

    room_id_json = json.dumps({"room_id": room_id})

    print(room_id_json)



    return render_template("create_room_finish.html", room_id=room_id, input_roomname=input_roomname, input_maxpeople=input_maxpeople, input_roomdetail=input_roomdetail, username=username)



@app.route("/rooms/<int:room_id>")

def get_room(room_id):

    conn = get_db()

    cursor = conn.cursor()



    cursor.execute("SELECT * FROM rooms WHERE room_id = %s", (room_id,))

    room_data = cursor.fetchone()



    cursor.close()

    conn.close()



    if room_data is None:

        return jsonify(error="Room not found"), 404



    room = {

        "room_id": room_data[0],

        "user_id": room_data[1],

        "room_name": room_data[2],

        "room_detail": room_data[3],

        "max_people": room_data[4]

    }



    return jsonify(room)



    # if request.method == "POST":

    #     # Get the room_id from the request data

    #     room_id = request.form.get("room_id")



    #     # Check if the room_id is provided

    #     if room_id is None:

    #         return jsonify({"error": "Room ID is missing"})



    #     # Get the database connection

    #     conn = get_db()

    #     cursor = conn.cursor()



    #     # Retrieve the room data from the database

    #     cursor.execute("SELECT * FROM rooms WHERE room_id = ?", (room_id,))

    #     room_data = cursor.fetchone()



    #     # Close the connection

    #     cursor.close()

    #     conn.close()



    #     if room_data:

    #         # Prepare the response data

    #         response_data = {

    #             "room_id": room_data[0],

    #             "user_id": room_data[1],

    #             "room_name": room_data[2],

    #             "room_detail": room_data[3],

    #             "max_people": room_data[4]

    #         }

    #         # Return the response as JSON

    #         return jsonify(response_data)

    #     else:

    #         # Room not found

    #         return jsonify({"error": "Room not found"})

    # else:

    #     # Handle unsupported HTTP methods

    #     return jsonify({"error": "Invalid request method"})







    # # sent data to db

    # url="http://192.168.10.4:30180/api/v1/room"

    # data = {

    #     "ownerId": user_id,

    #     "roomName": request.form["input_roomname"],

    #     "descript": request.form["input_roomdetail"],

    #     "limit": request.form["input_maxpeople"]

    # }

    # response = requests.post(url, json=data)



    # print(response.status_code)

    # print(response.text)



    # # returned_ownerId, returned_roomame, returned_maxpeople = DB.createRoom(conn, input_roomname, input_maxpeople, 5)

    # return render_template("create_room_finish.html", input_roomname = input_roomname, input_maxpeople = input_maxpeople, input_roomdetail = input_roomdetail, username = username)



@app.route("/select_room")

def select_room():

    # username = session.pop("username", None)

    return render_template("select_room.html", username = username)





@app.route("/welcome")

def welcome():

    return render_template("welcome.html")



@app.route("/enter_room")

def enter_room():

    return render_template("enter_room.html")



@app.route("/pricing")

def pricing():

    return render_template("pricing.html")



@app.route("/icon")

def icon():

    return render_template("icon.html")



@app.route("/lobby", methods=["GET"])

def lobby_get():

    return render_template("lobby.html")



@app.route("/lobby", methods=["POST"])

def lobby_post():

    room_id = None

    if request.method == "POST":

        room_id = request.form.get("room_id")

        print(room_id)

    

    return render_template("lobby.html", room_id=room_id)



@app.route("/profile")

def profile():

    user_id = session.pop("user_id", None)

    session["user_id"] = user_id



    # get from db

    url=f"http://192.168.10.4:30180/api/v2/user_profile/{user_id}"

    response = requests.get(url)

    data = response.json()



    username = data.get("username")

    country = data.get("country")

    friend_code = data.get("friend_code")



    # update caption in db

    url=f"http://192.168.10.4:30180/api/v2/user_profile"

    new_caption = request.form.get("caption")

    if new_caption:

        data = {

            "caption": new_caption

        }

        response = requests.put(url, json=data)

        if response.status_code == 200:

            print("Caption updated successfully.")



    return render_template("profile.html", username=username, country=country, friend_code=friend_code)

    # return render_template("profile.html")



# @app.route("/chat")

# def chat():

#     return render_template("chat.html")



@app.route("/add_friend")

def add_friend():

    return render_template("add_friend.html")



@app.route("/chatroom")

def chatroom():

    return render_template("chatroom.html")



# @app.route("/chat2")

# def chat2():

#     return render_template("chat2.html")



# @socketio.on('connect')

# def handle_connect():

#     print('Client connected')



# @socketio.on('disconnect')

# def handle_disconnect():

#     print('Client disconnected')



# @socketio.on('chat message')

# def handle_message(data):

#     print(f'Received message: {data}')

#     emit('chat message', data, broadcast=True)



@app.route("/shop")

def shop():

    return render_template("shop.html")



@app.route("/add_me")

def add_me():

    return render_template("add_me.html")



@app.route("/recommend")

def recommend():

    return render_template("recommend.html")

    

@app.route("/myfriend")

def myfriend():

    username = session.get("username")

    session["username"] = username

    print(username)



    return render_template("myfriend.html", username=username)



@app.route("/shopping_bag")

def shopping_bag():

    return render_template("shopping_bag.html")



@app.route("/random")

def random():

    return render_template("random.html")





if __name__ == "__main__":

    # app.run(debug=True)

    # socketio.run(app)

    app.run(host="0.0.0.0", port="5001", debug=True)



# # data init

# room_list = ["房間A", "房間B", "房間C", "房間D", "房間E", "房間F"]

# room_json = {

#     "光復前門地停": 1315,

#     "管院地停": 114,

#     "雲屏地停": 174,

#     "修齊地停": 444,

#     "都計地停": 302,

#     "成功地停": 813,

#     "三系館地停": 689,

#     "奇美樓地停": 538,

#     "生科大樓地停": 453,

#     "理學院樓地停": 754,

#     "管院平面": 331,

#     "光復平面": 333,

#     "新圖平面": 114,

#     "土木及水利平面": 319,

#     "自强平面": 482,

#     "勝後平面": 1181,

#     "力行平面": 500,

#     "成杏平面": 601,

# }



# data_path = os.path.join("static", "data")

# if not os.path.exists(data_path):

#     os.makedirs(data_path)



# reserve_path = os.path.join(data_path, "reserve.json")

# if not os.path.exists(reserve_path):

#     with open(reserve_path, "w", encoding="utf-8") as f:

#         f.write(json.dumps({}, ensure_ascii=False))



# block_path = os.path.join(data_path, "block.json")

# if not os.path.exists(block_path):

#     with open(block_path, "w", encoding="utf-8") as f:

#         f.write(json.dumps({}, ensure_ascii=False))



# total_path = os.path.join(data_path, "total.json")

# if not os.path.exists(total_path):

#     with open(total_path, "w", encoding="utf-8") as f:

#         f.write(json.dumps(room_json, ensure_ascii=False))



# # read data





# def check_in_reserve(room, username):

#     with open(reserve_path, "r", encoding="utf-8") as f:

#         reserve_json = json.loads(f.readline())



#     if f"{room}_{username}" in reserve_json:

#         return True, reserve_json

#     else:

#         return False, reserve_json





# def check_block(username):

#     with open(block_path, "r", encoding="utf-8") as f:

#         block_json = json.loads(f.readline())



#     if username in block_json:

#         return block_json[username]["count"], block_json

#     else:

#         return 0, block_json





# def check_total(room):

#     with open(total_path, "r", encoding="utf-8") as f:

#         total_json = json.loads(f.readline())



#     if room in total_json:

#         return total_json[room], total_json

#     else:

#         return 0, total_json



# # 資料儲存格式

# # mode : (r)eserve

# #        (p)ark

# #        (l)eave

# # reserve.json[room_username] = {

# #     "date": ,

# #     "time": ,

# #     "timestamp": ,

# #     "mode": ,

# # }

# # total.json[room] = count

# # block.json[username] = {

# #     "count": ,

# #     "until": ,

# # }



# # 假設前提

# # 一個停車場只有一筆資料

# # 被封鎖後一個星期無法再預約，已預約的不取消

# # 剩餘量 == 總量 (相同意思)

# # 停超過24小時會被記錄

# # 一個星期後消除黑名單

# # 檢查輸入資料檢查(username)

# # 保存車牌(username)資料



# # 新增預約           - insert

# # 取消預約           - remove

# # 查詢預約           - select

# # 查詢總量(剩餘量)   - select_total

# # 查詢黑名單         - select_block

# # 更新狀態(車牌辨識) - update_mode

# # 自動               - check

# # - 自動校正         - check_all

# #                     (insert_block, release_total, update_reserve, remove_block)

# # - 自動提醒         - check_reserve



# # function





# @app.route("/insert", methods=["POST"])

# def insert():

#     """

#     新增預約

#     - [要求輸入] room, username, date, time

#     - [回傳格式] 

#     成功: {

#         "room": ,

#         "username": ,

#         "date": ,

#         "time": ,

#     },

#     失敗: str

#     - [讀取檔案] reserve, total, block

#     - [寫入檔案] reserve, total

#     - [特別功能]

#     檢查黑名單,

#     檢查重複預約,

#     檢查剩餘量

#     """

#     obj = request.get_json()

#     print(obj)



#     in_reserve, reserve_json = check_in_reserve(obj["room"], obj["username"])

#     block_count, block_json = check_block(obj["username"])

#     left_count, total_json = check_total(obj["room"])



#     if block_count >= 3:

#         until = datetime.fromtimestamp(

#             block_json[obj["username"]]["until"]).strftime("%Y-%m-%d")

#         status = "fail"

#         result = f"block until {until}"



#     elif in_reserve:

#         time = reserve_json[f"{obj['room']}_{obj['username']}"]["time"]

#         status = "fail"

#         result = f"already reserve on {time}"



#     elif left_count == 0:

#         status = "fail"

#         result = f"No space left in {obj['room']}"



#     else:

#         reserve_json[f"{obj['room']}_{obj['username']}"] = {

#             "date": obj["date"],

#             "time": obj["time"],

#             "timestamp": parse(f"{obj['date']}T{obj['time']}").timestamp(),

#             "mode": "r",

#         }

#         with open(reserve_path, "w", encoding="utf-8") as f:

#             f.write(json.dumps(reserve_json, ensure_ascii=False))



#         total_json[obj['room']] -= 1

#         with open(total_path, "w", encoding="utf-8") as f:

#             f.write(json.dumps(total_json, ensure_ascii=False))



#         status = "success"

#         result = obj



#     return {"status": status, "opt": "insert", "result": result}





# @app.route("/remove", methods=["POST"])

# def remove():

#     """

#     取消預約

#     - [要求輸入] room, username

#     - [回傳格式] 

#     成功: {

#         "room": ,

#         "username": ,

#         "date": ,

#         "time": ,

#     },

#     失敗: str

#     - [讀取檔案] reserve, total

#     - [寫入檔案] reserve, total

#     - [特別功能]

#     檢查是否可以取消預約(mode:r)

#     """

#     obj = request.get_json()

#     print(obj)



#     in_reserve, reserve_json = check_in_reserve(obj["room"], obj["username"])

#     left_count, total_json = check_total(obj["room"])



#     if in_reserve and reserve_json[f"{obj['room']}_{obj['username']}"]["mode"] == "r":

#         status = "success"

#         result = {

#             "room": obj["room"],

#             "username": obj["username"],

#             "date": reserve_json[f"{obj['room']}_{obj['username']}"]["date"],

#             "time": reserve_json[f"{obj['room']}_{obj['username']}"]["time"]

#         }

#         del reserve_json[f"{obj['room']}_{obj['username']}"]

#         with open(reserve_path, "w", encoding="utf-8") as f:

#             f.write(json.dumps(reserve_json, ensure_ascii=False))



#         total_json[obj['room']] += 1

#         with open(total_path, "w", encoding="utf-8") as f:

#             f.write(json.dumps(total_json, ensure_ascii=False))



#     else:

#         status = "fail"

#         result = "no reserve can remove"



#     return {"status": status, "opt": "remove", "result": result}





# @app.route("/select", methods=["POST"])

# def select():

#     """

#     查詢預約

#     - [要求輸入] username

#     - [回傳格式] 

#     成功: list of {

#         "room": ,

#         "username": ,

#         "date": ,

#         "time": ,

#         "mode": ,

#     }

#     - [讀取檔案] reserve

#     - [寫入檔案] 

#     - [特別功能]

#     """

#     obj = request.get_json()

#     print(obj)



#     in_reserve, reserve_json = check_in_reserve("none", "none")



#     result = list()

#     for room in room_list:

#         if f"{room}_{obj['username']}" in reserve_json:

#             result.append({

#                 "room": room,

#                 "username": obj["username"],

#                 "date": reserve_json[f"{room}_{obj['username']}"]["date"],

#                 "time": reserve_json[f"{room}_{obj['username']}"]["time"],

#                 "mode": reserve_json[f"{room}_{obj['username']}"]["mode"]

#             })



#     return {"status": "success", "opt": "select", "result": result}





# @app.route("/select/total", methods=["POST"])

# def select_total():

#     """

#     查詢總量(剩餘量)

#     - [要求輸入] 

#     - [回傳格式] 

#     成功: {

#         "place A": ,

#         "place B": ,

#         ...

#     }

#     - [讀取檔案] total

#     - [寫入檔案] 

#     - [特別功能] 

#     """

#     # obj = request.get_json()

#     # print(obj)



#     left_count, total_json = check_total("none")



#     return {"status": "success", "opt": "select_total", "result": total_json}





# @app.route("/api/v1/user", methods=["POST"])

# def select_block():

#     """

#     查詢黑名單

#     - [要求輸入] username

#     - [回傳格式] 

#     成功: {

#         "username": ,

#         "count": ,

#         "until": ,

#     }

#     - [讀取檔案] block

#     - [寫入檔案] 

#     - [特別功能]

#     轉換時間輸出格式

#     """

#     obj = request.get_json()

#     print(obj)



#     block_count, block_json = check_block(obj["username"])

#     status, level = DB.getUserName(obj["username"])



#     if block_count >= 3:

#         until = datetime.fromtimestamp(

#             block_json[obj["username"]]["until"]).strftime("%Y-%m-%d")

#         result = {

#             "username": obj["username"],

#             "count": block_count,

#             "until": until,

#             "level": level

#         }

#     else:

#         result = {

#             "username": obj["username"],

#             "count": block_count,

#             "until": "",

#             "level": level

#         }



#     return {"status": "success", "opt": "selectblock", "result": result}





# @app.route("/update/mode", methods=["POST"])

# def update_mode():

#     """

#     系統自動更新狀態 (車牌辨識)

#     - [要求輸入] room, username, mode

#     - [回傳格式] 

#     成功: {

#         "room": ,

#         "username": ,

#         "date": ,

#         "time": ,

#         "mode": ,

#     },

#     失敗: str

#     - [讀取檔案] reserve, total

#     - [寫入檔案] reserve, total

#     - [特別功能]

#     檢查是否可以資料可以變更,

#     r -> p, p -> l

#     """

#     obj = request.get_json()

#     print(obj)



#     in_reserve, reserve_json = check_in_reserve(obj["room"], obj["username"])

#     left_count, total_json = check_total(obj["room"])



#     if not in_reserve:

#         status = "fail"

#         result = f"can not update reserve on {obj['room']}_{obj['username']}"



#     elif obj["mode"] == "p":

#         reserve_json[f"{obj['room']}_{obj['username']}"]["mode"] = "p"

#         with open(reserve_path, "w", encoding="utf-8") as f:

#             f.write(json.dumps(reserve_json, ensure_ascii=False))



#         status = "success"

#         result = {

#             "room": obj["room"],

#             "username": obj["username"],

#             "date": reserve_json[f"{obj['room']}_{obj['username']}"]["date"],

#             "time": reserve_json[f"{obj['room']}_{obj['username']}"]["time"],

#             "mode": "p"

#         }



#     else:  # obj["mode"] == "l"

#         status = "success"

#         result = {

#             "room": obj["room"],

#             "username": obj["username"],

#             "date": reserve_json[f"{obj['room']}_{obj['username']}"]["date"],

#             "time": reserve_json[f"{obj['room']}_{obj['username']}"]["time"],

#             "mode": "l"

#         }



#         del reserve_json[f"{obj['room']}_{obj['username']}"]

#         with open(reserve_path, "w", encoding="utf-8") as f:

#             f.write(json.dumps(reserve_json, ensure_ascii=False))



#         total_json[obj['room']] += 1

#         with open(total_path, "w", encoding="utf-8") as f:

#             f.write(json.dumps(total_json, ensure_ascii=False))



#     return {"status": status, "opt": "update_mode", "result": result}



# # auto function





# @app.route("/check", methods=["POST"])

# def check():

#     """

#     檢查所有

#     - [要求輸入] username

#     - [回傳格式] 

#     成功: list of {

#         "room": ,

#         "username": , 

#         "date": ,

#         "time": ,

#         "left": ,

#     }

#     - [讀取檔案] reserve, total, block

#     - [寫入檔案] reserve, total, block

#     - [特別功能]

#     檢查全部預約狀態,

#     檢查自己預約剩餘時間

#     """

#     obj = request.get_json()

#     print(obj)



#     now = datetime.now()

#     block_count_total, total_json = check_all(now)

#     result = check_reserve(obj["username"], now)



#     return {"status": "success", "opt": "check", "result": result}





# def check_all(now):

#     """

#     檢查全部預約狀態

#     - [要求輸入] now

#     - [回傳格式] 

#     成功: (block_count_total, total)

#     - [讀取檔案] reserve

#     - [寫入檔案] reserve, total, block

#     - [特別功能]

#     檢查逾時未停(mode:r),

#     檢查停超過24H(mode:p),

#     新增黑名單,

#     釋放未停空位,

#     更新過期黑名單

#     """

#     now_ts = now.timestamp()

#     ytd_ts = now_ts - 1*60*60*24

#     in_reserve, reserve_json = check_in_reserve("none", "none")



#     block_count = dict()

#     release_count = dict()

#     release_reserve_key = list()

#     continue_reserve_key = list()

#     for key, value in reserve_json.items():

#         room, username = key.split('_', 1)



#         # 預約未到/預約超過一天

#         if now_ts > value["timestamp"] and value["mode"] == "r":

#             # 違規紀錄

#             if username in block_count:

#                 block_count[username] += 1

#             else:

#                 block_count[username] = 1

#             # 釋放空位/刪除預約

#             if room in release_count:

#                 release_count[room] += 1

#             else:

#                 release_count[room] = 1

#             # 刪除預約

#             release_reserve_key.append(key)



#         # 停超過24H

#         if ytd_ts > value["timestamp"] and value["mode"] == "p":

#             # 違規紀錄

#             if username in block_count:

#                 block_count[username] += 1

#             else:

#                 block_count[username] = 1

#             # 無法釋放空位

#             # 自動重新預約

#             continue_reserve_key.append(key)



#     block_count_total = insert_block(block_count, now_ts)

#     total_json = release_total(release_count)

#     update_reserve(reserve_json, release_reserve_key, continue_reserve_key)

#     remove_block(now_ts)

#     return block_count_total, total_json





# def insert_block(block_count, now_ts):

#     """

#     新增黑名單

#     - [要求輸入] block_count, now_ts

#     - [回傳格式] 

#     成功: block_count_total

#     - [讀取檔案] block

#     - [寫入檔案] block

#     - [特別功能]

#     更新黑名單時間

#     """

#     _, block_json = check_block("none")



#     block_count_total = 0

#     for username, count in block_count.items():

#         block_count_total += count

#         if username in block_json:

#             block_json[username] = {

#                 "count": block_json[username]["count"] + count,

#                 "until": now_ts + 1*60*60*24*7,

#             }

#         else:

#             block_json[username] = {

#                 "count": 0 + count,

#                 "until": now_ts + 1*60*60*24*7,

#             }



#     with open(block_path, "w", encoding="utf-8") as f:

#         f.write(json.dumps(block_json, ensure_ascii=False))



#     return block_count_total





# def release_total(release_count):

#     """

#     釋放未停空位(total)

#     - [要求輸入] release_count

#     - [回傳格式] 

#     成功: total_json

#     - [讀取檔案] total

#     - [寫入檔案] total

#     - [特別功能]

#     """

#     left_count, total_json = check_total("none")



#     for room, count in release_count.items():

#         total_json[room] += count



#     with open(total_path, "w", encoding="utf-8") as f:

#         f.write(json.dumps(total_json, ensure_ascii=False))



#     return total_json





# def update_reserve(reserve_json, release_reserve_key, continue_reserve_key):

#     """

#     更新預約狀態

#     - [要求輸入] reserve_json, release_reserve_key, continue_reserve_key

#     - [回傳格式] 

#     成功: reserve_json

#     - [讀取檔案] reserve

#     - [寫入檔案] reserve

#     - [特別功能]

#     釋放未停空位,

#     停超過24H自動重新預約

#     """

#     for key in release_reserve_key:

#         del reserve_json[key]



#     for key in continue_reserve_key:

#         reserve_json[key]["timestamp"] += 1*60*60*24



#     with open(reserve_path, "w", encoding="utf-8") as f:

#         f.write(json.dumps(reserve_json, ensure_ascii=False))



#     return reserve_json





# def remove_block(now_ts):

#     """

#     更新過期黑名單

#     - [要求輸入] now_ts

#     - [回傳格式] 

#     成功: block_json

#     - [讀取檔案] block

#     - [寫入檔案] block

#     - [特別功能]

#     移除到期黑名單

#     """

#     block_count, block_json = check_block("none")



#     remove_block_key = list()

#     for key, value in block_json.items():

#         if now_ts > value["until"]:

#             remove_block_key.append(key)



#     for key in remove_block_key:

#         del block_json[key]



#     with open(block_path, "w", encoding="utf-8") as f:

#         f.write(json.dumps(block_json, ensure_ascii=False))



#     return block_json





# def check_reserve(username, now):

#     """

#     檢查自己預約剩餘時間

#     - [要求輸入] username, now

#     - [回傳格式] 

#     成功: list of {

#         "room": ,

#         "username": , 

#         "date": ,

#         "time": ,

#         "left": ,

#     }

#     - [讀取檔案] reserve

#     - [寫入檔案] 

#     - [特別功能]

#     30分鐘倒數

#     """

#     now_ts = now.timestamp()

#     in_reserve, reserve_json = check_in_reserve("none", "none")



#     result = list()

#     for room in room_list:

#         if f"{room}_{username}" in reserve_json and reserve_json[f"{room}_{username}"]["mode"] == "r":

#             temp = reserve_json[f"{room}_{username}"]

#             left_min = int(temp["timestamp"] - now_ts) // 60

#             if left_min >= 0:

#                 result.append({

#                     "room": room,

#                     "username": username,

#                     "date": temp["date"],

#                     "time": temp["time"],

#                     "left": left_min

#                 })



#     return result







