document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('history-button').addEventListener('click', function() {
        console.log('History button clicked');
        document.getElementById('historyResults').style.display = 'block';
    });

    var modal = document.getElementById('historyResults');
    var closeButton = document.querySelector('.Close');

    closeButton.addEventListener('click', function(){
        document.getElementById('historyResults').style.display = 'none';
    });

    window.addEventListener('click', function(event){
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

});