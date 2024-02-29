// Get references to the input field, search button, and add friend div
var inputField = document.getElementById('friendy_code');
console.log(friendy_code)

var searchButton = document.getElementById('search');
var addFriendDiv = document.querySelector('.add_friend');

// Add event listener to search button
searchButton.addEventListener('click', function() {
  // Get the user code entered by the user
  var userCode = inputField.value;
  console.log(userCode)

  // Fetch user data from the API
  fetch('http://192.168.10.4:30180/api/v2/friendy_code/' + userCode)
    .then(function(response) {
      return response.json();
      console.log(response.json);
    })
    .then(function(userData) {
      // Display user data in the user-details div
      var userDetailsDiv = document.querySelector('.user-details');
      
      userDetailsDiv.innerHTML = '<p>Name: ' + userData.name + '</p>' +
                                  '<p>Email: ' + userData.email + '</p>';

      // Add friend button
      var addFriendButton = document.createElement('button');
      addFriendButton.innerText = 'Add Friend';
      addFriendButton.classList.add('btn', 'btn-lg', 'btn-primary');
      addFriendButton.addEventListener('click', function() {
        // Save friend data to the API
        fetch('http://192.168.10.4:30180/api/v2/{friendy_code}/match', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            userId: userData.id
          })
        })
        .then(function(response) {
          if (response.ok) {
            // Redirect to chat page
            window.location.href = 'chat.html';
          } else {
            console.error('Error saving friend data:', response.statusText);
          }
        })
        .catch(function(error) {
          console.error('Error saving friend data:', error);
        });
      });

      // Display add friend button in the add-friend div
      addFriendDiv.appendChild(addFriendButton);
    })
    .catch(function(error) {
      console.error('Error fetching user data:', error);
    });
});
