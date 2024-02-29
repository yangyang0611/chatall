// function  registered() {
//     alert("注冊成功");
// }

function exit(){
    if (confirm("確定離開房間嗎？") == true) {
        document.location.href="/welcome";
    }
}

document.querySelectorAll(".cp_img").forEach(function(imgContainer) {
    imgContainer.addEventListener("click", function(event) {
      var button = event.target.closest("button");
      if (button) {
        var id = button.id;
        console.log(id); // or do something else with the ID
      }
    });
  });
  
  
  


  
  
  
  
// document.querySelector("#files").addEventListener("change", (e) => {
//     if (window.File && window.FileReader && window.FileList && window.Blob) {
//       const files = e.target.files;
//       const output = document.querySelector("#result");
  
//       for (let i = 0; i < files.length; i++) { // corrected typo here
//         if (!files[i].type.match("image")) continue;
//         const picReader = new FileReader();
//         picReader.addEventListener("load", function (event) {
//           const picFile = event.target;
//           const div = document.createElement("div");
//           div.innerHTML = `<img class="thumbnail" src="${picFile.result}" title="${picFile.name}"/>`;
//           output.appendChild(div);
//         });
//         picReader.readAsDataURL(files[i]);
//       }
//     } else {
//       alert("Your browser does not support the File API");
//     }
//   });
  
  

// // set var
// $("#form input[name='date']").attr("value", $.format.date(new Date(), 'yyyy-MM-dd'));
// $("#form input[name='time']").attr("value", window.sessionStorage.getItem("time"));
// $("#form input[name='room']").attr("value", window.sessionStorage.getItem("room"));
// $("#form input[name='username']").attr("value", window.localStorage.getItem("username"));

// $("#form input[id='username_register']").attr("value", window.sessionStorage.getItem("username_register"));
// $("#form input[name='password_register']").attr("value", window.sessionStorage.getItem("password_register"));

// $("#form input[name='input_roomname']").attr("value", window.localStorage.getItem("input_roomname"));
// $("#form input[name='input_roomdetail']").attr("value", window.localStorage.getItem("input_roomdetail"));
// $("#form input[name='input_maxpeople']").attr("value", window.localStorage.getItem("input_maxpeople"));


// // web init
// let date = new Date();
// window.sessionStorage.setItem("date", $.format.date(date, 'yyyy-MM-dd'));
// $("date").text(window.sessionStorage.getItem("date"));
// $("time").text(window.sessionStorage.getItem("time"));
// $("park").text(window.sessionStorage.getItem("park"));
// $("username").text(window.localStorage.getItem("username"));
// $("password").text(window.localStorage.getItem("password"));
// $("status").text(window.sessionStorage.getItem("status"));

// $("username_register").text(window.sessionStorage.getItem("username_register"));
// $("password_register").text(window.sessionStorage.getItem("password_register"));

// $("input_roomname").text(window.sessionStorage.getItem("input_roomname"));
// $("input_roomdetail").text(window.sessionStorage.getItem("input_roomdetail"));
// $("input_maxpeople").text(window.sessionStorage.getItem("input_maxpeople"));




// // select time
// $("button[name='select_time']").click(function(){
//     console.log(window.sessionStorage.getItem("date"));
//     console.log(window.sessionStorage.getItem("time"));
// });

// // time
// settimebtn();
// function settimebtn(){
//     for(var i = 0; i < 24; i++) {
//         var hr = date.getHours();
//         $(`button[name='time${i}']`).removeClass("btn_orange text-white");
//         if (hr < i) $(`button[name='time${i}']`).addClass("btn-outline-dark");
//         else {
//             $(`button[name='time${i}']`).attr({"disabled":""});
//             $(`button[name='time${i}']`).addClass("btn-outline-secondary");
//         }
//     }
// }
// function timebtn_click(name){
//     settimebtn();
//     window.sessionStorage.setItem("time", `${name.split('time')[1]}:00`);
//     $(`button[name='${name}']`).addClass("btn_orange text-white");
//     console.log(window.sessionStorage.getItem("date"));
//     console.log(window.sessionStorage.getItem("time"));
// }

// // select carpark
// $("button[name='select_time']").click(function(){
//     console.log(window.sessionStorage.getItem("date"));
//     console.log(window.sessionStorage.getItem("time"));
//     console.log(window.sessionStorage.getItem("park"));
// });

// // carpark
// setparkbtn("");
// function setparkbtn(name){
//     $.ajax({
//         method: "POST",
//         url: "/select/total",
//         contentType: 'application/json',
//         dataType: "json",
//     })
//     .done(function(result) {
//         console.log(result);
//         var total = result["result"]
//         for(var i = 1; i <= 18; i++) {
//             var parkname = $(`button[name='carpark${i}']`).text().split(' ')[0];
//             var less = total[parkname];
//             $(`button[name='carpark${i}']`).removeClass("btn_orange text-white");
//             $(`button[name='carpark${i}']`).text(`${parkname} (剩餘${less}格)`);
//             if (less > 0) $(`button[name='carpark${i}']`).addClass("btn-outline-dark");
//             else {
//                 $(`button[name='carpark${i}']`).attr({"disabled":""});
//                 $(`button[name='carpark${i}']`).addClass("btn-outline-secondary");
//             }
//             if (name == parkname) {
//                 $(`button[name='carpark${i}']`).addClass("btn_orange text-white");
//             }
//         }
//     })
//     .fail(function() {
//     })
//     .always(function() {
//     });
// }
// function parkbtn_click(name){
//     setparkbtn(name.split(' ')[0]);
//     window.sessionStorage.setItem("park", name.split(' ')[0]);
//     console.log(window.sessionStorage.getItem("date"));
//     console.log(window.sessionStorage.getItem("time"));
//     console.log(window.sessionStorage.getItem("park"));
// }
// $("button[name='select_carpark']").click(function(){
//     console.log("insert on click");
//     $.ajax({
//         method: "POST",
//         url: "/insert",
//         contentType: 'application/json',
//         data: JSON.stringify({
//             "room": window.sessionStorage.getItem("room"),
//             "username": window.localStorage.getItem("username"),
//             "date": window.sessionStorage.getItem("date"),
//             "time": window.sessionStorage.getItem("time"), 
//         }),
//         dataType: "json",
//     })
//     .done(function(result) {
//         console.log(result);
//         window.sessionStorage.setItem("status", result["status"]);
//     })
//     .fail(function() {
//     })
//     .always(function() {
//     });
// });

// // finish
// $("button[name='remove_last']").click(function(){
//     console.log("remove on click");
//     if (confirm("確定刪除此預約嗎？") == true) {
//         $.ajax({
//             method: "POST",
//             url: "/remove",
//             contentType: 'application/json',
//             data: JSON.stringify({
//                 "room": window.sessionStorage.getItem("room"),
//                 "username": window.localStorage.getItem("username"),
//             }),
//             dataType: "json",
//         })
//         .done(function(result) {
//             console.log(result);
//         })
//         .fail(function() {
//         })
//         .always(function() {
//         });
//         document.location.href="/check_all";
//     }
// });

// // exit
// $("button[name='exit']").click(function(){
//     console.log("exit on click");
//     if (confirm("確定離開房間嗎？") == true) {
//         $.ajax({
//             method: "POST",
//             url: "/remove",
//             contentType: 'application/json',
//             data: JSON.stringify({
//                 "room": window.sessionStorage.getItem("room"),
//                 "username": window.localStorage.getItem("username"),
//             }),
//             dataType: "json",
//         })
//         .done(function(result) {
//             console.log(result);
//         })
//         .fail(function() {
//         })
//         .always(function() {
//         });
//         document.location.href="/welcome";
//     }
// });

// // check all
// // setInterval(check, 1000);
// window.onload = check;

// function check() {
//     console.log("check call");
//     $.ajax({
//         method: "POST",
//         url: "/check",
//         contentType: 'application/json',
//         data: JSON.stringify({
//             "username": window.localStorage.getItem("username"),
//         }),
//         dataType: "json",
//     })
//     .done(function(result) {
//         console.log(result);
//         result = result["result"];
//         $("div[class='res_show']").html("");
//         if (result.length == 0){
//             var appendhtml = "<h3 class='text-white'>查無資料</h3>"
//             $("div[class='res_show']").append(appendhtml);
//         }
//         for (let i = 0; i < result.length; i++) {
//             // var img=document.createElement('img');
//             // img.src="/static/images/tickets/smallticket_notready.png";
             
//             var appendhtml = `
//                 <form id="form${i}">
//                     <div class="background_ticket container">
//                         <img src="/static/images/tickets/smallticket_countdown.png">
                    
                        
//                             <p name="room" class="all_room">${result[i]["room"]}</p>
//                             <p name="username" class="all_username">${result[i]["username"]}</p>
//                             <p name="date" class="all_date">${result[i]["date"]}</p>
//                             <p name="time" class="all_time">${result[i]["time"]}</p>
//                             <p name="left" class="all_left">預約倒數 ${result[i]["left"]} 分鐘</p>
//                             <p></p>
//                             <button name="res_delete${i}" type="button" class="btn_res btn_orange all_delete" onClick="detelebtn_click(this.name)">取消該筆預約</button>
                        
                        
//                     </div>
//                 </form> 
//             `
//             $("div[class='res_show']").append(appendhtml);
//         }
//     })
//     .fail(function() {
//     })
//     .always(function() {
//     });
// }

// function detelebtn_click(name){
//     if (confirm("確定刪除此預約嗎？") == true) {
//         name = `form${name.split('res_delete')[1]}`;
//         $.ajax({
//             method: "POST",
//             url: "/remove",
//             contentType: 'application/json',
//             data: JSON.stringify({
//                 "room": $(`#${name} p[name='room']`).text(),
//                 "username": $(`#${name} p[name='username']`).text(),
//             }),
//             dataType: "json",
//         })
//         .done(function(result) {
//             console.log(result);
//         })
//         .fail(function() {
//         })
//         .always(function() {
//             check();
//         });
//     }
// }

// // username
// // check input
// $("#form input[name='username']").on("input", function() {
//     let text = $(this).val();
//     $("#form warning[name='username']").text("");
// });

// $("#form button[name='save_username']").click(function() {
//     console.log("save_username on click");
//     console.log($("#username").val())
//     $.ajax({
//         method: "POST",
//         url: "http://192.168.10.3:8501/api/v1/user",
//         contentType: 'application/json',
//         data: JSON.stringify({
//             "username": $("#username").val(),
//             "password": window.localStorage.getItem("password"),
//         }),
//         dataType: "json",
//         success: function(res) {
//             console.log("return from backend")
//             console.log(res)
//             alert(res)
//         }
//     })
//     .done(function(result) {
//         console.log(result);
//         result = result["result"];
//         if (result["count"] >= 3) {
//             $("block").text(`你以累計${result["count"]}違規，直到${result["until"]}`);
//         }
//         else $("block").text(`表現良好繼續維持`);
//     })
//     .fail(function() {
//     })
//     .always(function() {
//     });

//     // window.localStorage.setItem("username", $("#form input[name='username']").val());
//     // console.log(window.localStorage.getItem("username"));
// });

// $("#form button[name='save_register']").click(function() {
//     console.log("save_register on click");
//     console.log($("#username_register").val())
//     if (confirm("注冊成功") == true) {
//         $.ajax({
//             method: "POST",
//             url: "",
//             contentType: 'application/json',
//             data: JSON.stringify({
//                 "username": $("#username_register").val(),
//                 "password": window.localStorage.getItem("password_register"),
//             }),
//             dataType: "json",
//             success: function(res) {
//                 console.log("return from backend")
//                 console.log(res)
//                 alert(res)
//             }
//         })
//         .done(function(result) {
//             console.log(result);
//             result = result["result"];
//             if (result["count"] >= 3) {
//                 $("block").text(`你以累計${result["count"]}違規，直到${result["until"]}`);
//             }
//             else $("block").text(`表現良好繼續維持`);
//         })
//         .fail(function() {
//         })
//         .always(function() {
//         });
//     }
//     // window.localStorage.setItem("username", $("#form input[name='username']").val());
//     // console.log(window.localStorage.getItem("username"));
// });

// // roomdetail
// // check input
// // $("#form input[name='input_maxpeople']").on("input", function() {
// //     const pattern = /{2,100}$/;
// //     const error_message = "請輸入數字";
// //     i