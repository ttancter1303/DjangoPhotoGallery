const uploadForm = document.getElementById('upload-form');
  const imageInput = document.querySelector('input[type="file"]');
  const uploadedImagePreview = document.getElementById('uploaded-image-preview');

  // Thêm sự kiện 'change' vào trường tệp hình ảnh để hiển thị trước hình ảnh khi người dùng chọn tệp
  imageInput.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
      const reader = new FileReader();

      reader.onload = function (event) {
        uploadedImagePreview.src = event.target.result;
        uploadedImagePreview.style.display = 'block';
      };

      reader.readAsDataURL(file);
    }
  });

  uploadForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    const xhr = new XMLHttpRequest();

    xhr.upload.onprogress = function (event) {
      if (event.lengthComputable) {
        const percentComplete = (event.loaded / event.total) * 100;
        document.getElementById('progress-bar').style.width = percentComplete + '%';
        document.getElementById('progress-percent').textContent = percentComplete.toFixed(2) + '%';
      }
    };

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
        document.getElementById('uploaded-image-preview').src = response.image_url;
        document.getElementById('uploaded-image').style.display = 'block';
        document.getElementById('progress-container').style.display = 'none';
        document.getElementById('success-link').style.display = 'block';
      }
    };

    xhr.open('POST', '{% url 'upload_image' %}', true);
    xhr.send(formData);

    document.getElementById('progress-container').style.display = 'block';
    document.getElementById('progress-bar').style.width = '0%';
    document.getElementById('progress-percent').textContent = '0%';
  });