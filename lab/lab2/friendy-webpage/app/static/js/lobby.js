

const keyDict = {};
const avatar = {
  el: document.querySelector("#avatar"),
  x: 200,
  y: 100,
  speed: 2,
  move() {
    this.el.style.transform = `translate(${this.x}px, ${this.y}px)`;
  }
};

const updateKeyDict = (ev) => {
    const k = ev.code;
    if (/^Arrow\w+/.test(k)) { // If is arrow
      ev.preventDefault();
      keyDict[k] = ev.type === "keydown"; // set boolean true / false
    }
};

const objects = document.querySelectorAll(".object");
const collisionStatus = new Array(objects.length).fill(false);
let showingAlert = false; // new flag variable

const hoverMessages = [
    "hi",   // message for object 1
    "hello", // message for object 2
    "good"  // message for object 3
    // add more messages for other objects as needed
];

const checkCollisions = () => {
    for (let i = 0; i < objects.length; i++) {
      const object = objects[i];
      const objectRect = object.getBoundingClientRect();
      const avatarRect = avatar.el.getBoundingClientRect();

        if (
            avatarRect.left < objectRect.right &&
            avatarRect.right > objectRect.left &&
            avatarRect.top < objectRect.bottom &&
            avatarRect.bottom > objectRect.top &&
            !collisionStatus[i]
        ) {

        // <<test behavior> Collision detected! Show a message on the object
        //  object.setAttribute("data-tooltip", hoverMessages[i]);
        //  collisionStatus[i] = true;

            collisionStatus[i] = true;

            // Fetch the room details from the database using the room ID
            const roomId = object.dataset.roomId;
            const url = `http://192.168.10.3:31098/api/v1/room/${roomId}`;
            fetch(url)
                .then(response => response.json())
                .then(data => {
                // Show the message on the object
                const message = `${data.roomname}: ${data.roomdetail}`;
                object.setAttribute("data-tooltip", message);
                showingAlert = true;

                // Hide the message after a delay
                setTimeout(() => {
                    object.removeAttribute("data-tooltip");
                    showingAlert = false;                        //allow new messages to be displayed.
                }, 2000);
                })
                .catch(error => {
                    console.error(error);
                });

    } 
        else if (
            avatarRect.left >= objectRect.right ||
            avatarRect.right <= objectRect.left ||
            avatarRect.top >= objectRect.bottom ||
            avatarRect.bottom <= objectRect.top
        ) {
                // No collision detected! Remove the message on the object
                object.removeAttribute("data-tooltip");
                collisionStatus[i] = false;
        }
    }
};


let alreadyAsked = false; // 将标志变量移动到全局作用域
let alreadyRedirected = false; // 添加一个用于跳转的标志变量

const update = () => {
  if (!showingAlert) { // check if alert is not showing
    // Determine move distance to account diagonal move: 1/Math.sqrt(2) = ~0.707
    let dist =
      keyDict.ArrowUp && (keyDict.ArrowLeft || keyDict.ArrowRight) ||
      keyDict.ArrowDown && (keyDict.ArrowLeft || keyDict.ArrowRight) ? 0.707 : 1;

    dist *= avatar.speed;

    if (keyDict.ArrowLeft) {
      avatar.x -= dist;
      if (avatar.x < -50 && !alreadyAsked) {
        if (confirm('即將前往討論空間，是否進入？')) {
          window.location.href = "http://127.0.0.1:5500/index.html";
        }
        alreadyAsked = true; // 设置标志变量为 true
        return;
      }
    }

    const screenWidth = window.innerWidth;
    const threshold = 0.35; 

    if (keyDict.ArrowRight) {
      avatar.x += dist;
      if (avatar.x > screenWidth * threshold && !alreadyRedirected) {
        window.location.href = "http://localhost:3000/"; // 在物体到达界面右边的20%时进行页面跳转到 YouTube
        alreadyRedirected = true; // 设置标志变量为 true
        return;
      }
    }

    const screenHeight = window.innerHeight;
    const scrollPosition = window.scrollY || window.pageYOffset; // 获取当前滚动位置
    const fullHeight = document.documentElement.scrollHeight; // 获取整个页面的高度
    
    const threshold2 = fullHeight * 0.65  + scrollPosition;

    if (keyDict.ArrowDown) {
      avatar.y += dist;
      if (avatar.y >= threshold2 && !alreadyRedirected) {
        window.location.href = "http://google.com.tw"; // 在物体到达页面下方的50%时进行页面跳转到指定网址
        alreadyRedirected = true; // 设置标志变量为 true
        return;
      }
    }

    // Reset alreadyRedirected if avatar's y position is less than the threshold
    if (avatar.y <= threshold) {
      alreadyRedirected = false;
    }

    // Reset alreadyAsked if avatar's x position is greater than 0
    if (avatar.x > 0) {
      alreadyAsked = false;
    }

    if (keyDict.ArrowUp) avatar.y -= dist;
    if (keyDict.ArrowDown) avatar.y += dist;
    avatar.move();
    checkCollisions();
  }
};


document.addEventListener('keydown', updateKeyDict);
document.addEventListener('keyup', updateKeyDict);

(function engine() {
  update();
  window.requestAnimationFrame(engine);
}());

// After you get the response from the server
let roomName = response.json().roomName;

// Create a box element with the room name
let $box = $('<div>', {class: 'room-box', text: roomName});

// Append the box element to the container element
$('#room-container').append($box);


// var avatar = document.getElementById("avatar");
// var object1 = document.getElementById("object1");
// var object2 = document.getElementById("object2");

// document.addEventListener("keydown", function(event) {
// 	// Move the avatar with the arrow keys
// 	if (event.code === "ArrowUp") {
// 		avatar.style.top = parseInt(avatar.style.top) - 10 + "px";
// 	}
// 	if (event.code === "ArrowDown") {
//         avatar.style.top = parseInt(avatar.style.top) + 10 + "px";
//     }
//     if (event.code === "ArrowLeft") {
//         avatar.style.left = parseInt(avatar.style.left) - 10 + "px";
//     }
//     if (event.code === 39) {
//         avatar.style.left = parseInt(avatar.style.left) + 10 + "px";
//     }
// });

// object1.addEventListener("click", function() {
// // Show a message when the first object is clicked
// alert("This is an object! Click OK to learn more.");
// });

// object2.addEventListener("click", function() {
// // Navigate to a new page when the second object is clicked
// window.location.href = "https://www.example.com";
// })    



    // var smallPerson = document.getElementById("small-person");
// var object = document.getElementById("object");

// document.addEventListener("keydown", function(event) {
//     if (event.key === "ArrowLeft") { // left arrow key
//       moveLeft();
//     } else if (event.key === "ArrowUp") { // up arrow key
//       moveUp();
//     } else if (event.key === "ArrowRight") { // right arrow key
//       moveRight();
//     } else if (event.key === "ArrowDown") { // down arrow key
//       moveDown();
//     }
// });
  

// object.addEventListener("click", function(event) {
//     object.classList.add("hidden");
//     alert("You clicked the object! Moving to the next page...");
//     window.location.href = "next-page.html";
// });

// function moveLeft() {
//     var leftPos = parseInt(smallPerson.style.left);
//     if (leftPos > 0) {
//         smallPerson.style.left = leftPos - 10 + "px";
//         checkObject();
//     }
// }

// function moveUp() {
//     var topPos = parseInt(smallPerson.style.top);
//     if (topPos > 0) {
//         smallPerson.style.top = topPos - 10 + "px";
//         checkObject();
//     }
// }

// function moveRight() {
//     var leftPos = parseInt(smallPerson.style.left);
//     if (leftPos < 450) {
//         smallPerson.style.left = leftPos + 10 + "px";
//         checkObject();
//     }
// }

// function moveDown() {
//     var topPos = parseInt(smallPerson.style.top);
//     if (topPos < 450) {
//         smallPerson.style.top = topPos + 10 + "px";
//         checkObject();
//     }
// }

// function checkObject() {
//     var smallPersonRect = smallPerson.getBoundingClientRect();
//     var objectRect = object.getBoundingClientRect();
//     if (intersect(smallPersonRect, objectRect)) {
//         object.classList.remove("hidden");
//         object.innerText = "Click me!";
//     }
// }

// function intersect(rect1, rect2) {
//   return !(rect1.right < rect2.left || 
//            rect1.left > rect2.right || 
//            rect1.bottom < rect2.top || 
//            rect1.top > rect2.bottom);
// }
