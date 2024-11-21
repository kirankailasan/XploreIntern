document.addEventListener("DOMContentLoaded", function() { 
    // Get the modal
    var modal = document.getElementById("login-modal");

    // Get the button that opens the modal
    var loginBtns = document.querySelectorAll("#login-btn");

    loginBtns.forEach(btn => {
        btn.onclick = function() {
            modal.style.display = "block";
        }
    });

    // Get the <span> element that closes the modal
    var closeBtn = document.querySelector(".close");

    closeBtn.onclick = function() {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }
});
function toggleNav() {
    var navLinks = document.getElementById("navLinks");
    navLinks.classList.toggle("active");
}