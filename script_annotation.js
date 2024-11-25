document.getElementById('annotation-button').addEventListener('click', function() {
    document.getElementById('annotation-modal').style.display = 'block';
});

var modal = document.getElementById('annotation-modal');
var closeButton = document.querySelector('.Close');

closeButton.addEventListener('click', function(){
    modal.style.display = 'none';
});

window.addEventListener('click', function(event){
    if (event.target == modal) {
        modal.style.display = 'none';
    }
});
