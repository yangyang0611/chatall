const users = [];

// Join user to chat
function userJoin(id, username, room) {
  const user = { id, username, room };

  users.push(user);

  return user;
}

// Get current user
function getCurrentUser(id) {
  return users.find(user => user.id === id);
}

// User leaves chat
function userLeave(id) {

  // findIndex: find the number of index of userid {x: "xx", x: "xx"}
  const index = users.findIndex(user => user.id === id);

  if (index !== -1) {

    // splice: remove index from list, return [0] whixh is user's id
    return users.splice(index, 1)[0];
  }
}

// Get room users
function getRoomUsers(room) {

  // filter: return a list of user information [x,x]
  return users.filter(user => user.room === room);
}

module.exports = {
  userJoin,
  getCurrentUser,
  userLeave,
  getRoomUsers
};
