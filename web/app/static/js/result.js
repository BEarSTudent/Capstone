window.onload = function() {
const stepTargets = document.querySelectorAll('.step');

    stepTargets[0].classList.remove('active');
    for(let i =0; i<5; i++){
        stepTargets[i].classList.add('prev');
        stepTargets[i].classList.add('last');
    }
    stepTargets[5].classList.add('active');
    stepTargets[5].classList.add('last');
}

document.addEventListener('DOMContentLoaded', (event) => {
    // Get the modal
    var modal = document.getElementById("postModal");

    // Get the button that opens the modal
    var btn = document.getElementById("shareImage");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks the button, open the modal 
    if (btn) {
        btn.onclick = function() {
            modal.style.display = "block";
        }
    }

    // When the user clicks on <span> (x), close the modal
    if (span) {
        span.onclick = function() {
            modal.style.display = "none";
        }
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});