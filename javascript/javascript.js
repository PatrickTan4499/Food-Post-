

gapi.load('auth2', function() {
  auth2 = gapi.auth2.init({
    client_id: 'CLIENT_ID.apps.googleusercontent.com',
    fetch_basic_profile: false,
    scope: 'profile'
  });

//allows the dropdown menu to dropdown
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}
// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
