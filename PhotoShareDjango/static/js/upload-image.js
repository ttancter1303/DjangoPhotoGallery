var dropArea = document.getElementById('drop-area');
var fileInput = document.getElementById('fileInput');

dropArea.addEventListener('dragenter', function(e) {
  e.preventDefault();
  dropArea.classList.add('active');
});

dropArea.addEventListener('dragover', function(e) {
  e.preventDefault();
});

dropArea.addEventListener('dragleave', function(e) {
  e.preventDefault();
  dropArea.classList.remove('active');
});

dropArea.addEventListener('drop', function(e) {
  e.preventDefault();
  dropArea.classList.remove('active');
  var files = e.dataTransfer.files;
  handleFiles(files);
});

fileInput.addEventListener('change', function() {
  var files = fileInput.files;
  handleFiles(files);
});

