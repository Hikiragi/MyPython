document.addEventListener("DOMContentLoaded", function() {
    var downloadButton = document.getElementById("download-button");
    if (downloadButton) {
        downloadButton.addEventListener("click", function() {
          // Запросите список ссылок для скачивания у вашего приложения Flask
          fetch('/materials')
            .then(response => response.json())
            .then(data => {
              // Очистите предыдущие ссылки для скачивания
              var downloadLinks = document.getElementById("download-links");
              downloadLinks.innerHTML = "";
              // Создайте новые ссылки для скачивания
              for (var i = 0; i < data.length; i++) {
                var link = document.createElement("a");
                link.href = data[i][1];
                link.download = data[i][0].split("/").pop();
                link.innerHTML = data[i][0].split("/").pop();
                downloadLinks.appendChild(link);
                downloadLinks.appendChild(document.createElement("br"));
              }
              // Откройте мини окно
              var modal = document.getElementById('downloadModal');
              var downloadModal = document.getElementById("downloadModal");
              downloadModal.style.display = "block";
              var closeButton = document.querySelector('.Close');
              closeButton.addEventListener('click', function(){
                downloadModal.style.display = "none";
              });
              window.addEventListener('click', function(event){
                    if (event.target == modal) {
                        modal.style.display = 'none';
                    }
               });
            });
        });
    }
});