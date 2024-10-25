document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var formData = new FormData(this);
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        var resultDiv = document.getElementById('result');
        if (data.error) {
            resultDiv.innerHTML = `<p class="error">${data.error}</p><p>${data.details}</p>`;
        } else {
            resultDiv.innerHTML = `<p class="success">${data.message}</p><p>${data.details}</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
