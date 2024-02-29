document.querySelector("#files").addEventListener("change", (e) => {
    if (window.File && window.FileReader && window.FileList && window.Blob) {
      const files = e.target.files;
      const output = document.querySelector("#result");
  
      for (let i = 0; i < files.length; i++) {
        if (!files[i].type.match("image")) continue;
        const picReader = new FileReader();
        picReader.addEventListener("load", function (event) {
          const picFile = event.target;
          const div = document.createElement("div");
          div.innerHTML = `<img class="thumbnail" src="${picFile.result}" title="${picFile.name}"/>`;
          output.appendChild(div);
  
          // send the image to the server
          const formData = new FormData();
          formData.append("image", files[i]);
          fetch("http://192.168.10.3:31098/api/v1/user/pic", {
            method: "POST",
            body: formData,
          });
        });
        picReader.readAsDataURL(files[i]);
      }
    } else {
      alert("Your browser does not support the File API");
    }
  });

  // retrieve the images from the server
fetch("http://192.168.10.3:31098/api/v1/user/profile/pic")
.then((response) => response.json())
.then((images) => {
  const output = document.querySelector("#result");
  images.forEach((image) => {
    const div = document.createElement("div");
    div.innerHTML = `<img class="thumbnail" src="${image.url}" title="${image.name}"/>`;
    output.appendChild(div);
  });
});


$(document).ready(function() {
    $('#edit_caption').click(function(event) {
      event.preventDefault();
      var newCaption = prompt('Enter new caption:'); // prompt user to enter new caption
      if (newCaption !== null) { // check if user clicked "Cancel"
        $('#caption').text(newCaption); // update caption text in the HTML

        // make AJAX call to update caption in the database
        $.ajax({
          url: 'http://192.168.10.4:30180/api/v2/user_profile',
          type: 'POST',
          data: { caption: newCaption },
          success: function(response) {
            console.log('Caption updated successfully.');
          },
          error: function(xhr, status, error) {
            console.error('Error updating caption:', error);
          }
        });
      }
    });
  });


// retrieve initial caption from database

  $(document).ready(function() {
    $.ajax({
      url: 'https://example.com/api/get_caption',
      type: 'GET',
      success: function(response) {
        $('#caption').text(response.caption); // update caption text in the HTML
      },
      error: function(xhr, status, error) {
        console.error('Error retrieving caption:', error);
      }
    });
  
    // add click event listener to "Edit" button
    $('#edit_caption').click(function(event) {
      // same code as before to update caption and make AJAX call to API
    });
  });
