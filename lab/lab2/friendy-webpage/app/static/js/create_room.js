$(document).ready(function() {
    var roomCount = 0; // Counter for room IDs
    
    // Function to create a room box
    function createRoomBox(roomName) {
        roomCount++; // Increment room ID counter
        var roomId = "room" + roomCount; // Generate room ID
        
        // Create room box HTML
        var roomBox = '<div id="' + roomId + '" class="object" data-tooltip="">' + roomName + '</div>';
        
        // Append room box to room container
        $("#room-container").append(roomBox);
    }
    
    // Event handler for the 確認 button click
    $("#create_room").click(function(event) {
        event.preventDefault(); // Prevent form submission
        
        // Get room name input value
        var roomName = $("input[name='input_roomname']").val();
        
        // Create room box
        createRoomBox(roomName);
        
        // Reset input field
        $("input[name='input_roomname']").val("");
    });
});
