document.addEventListener("DOMContentLoaded", function() {
  const changeAvatarButton = document.getElementById("change-avatar-button");
  const avatarPopup = document.getElementById("avatar-popup");

  changeAvatarButton.addEventListener("click", function() {
    avatarPopup.style.display = "block";
  });

  // Sử dụng AJAX để xử lý việc tải lên ảnh đại diện và cập nhật ảnh đại diện hiển thị
  const avatarForm = document.getElementById("avatar-form");
  const userAvatar = document.getElementById("user-avatar");

  avatarForm.addEventListener("submit", function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    // Thực hiện AJAX request để tải lên ảnh đại diện mới
    fetch("{% url 'update_avatar' %}", {
      method: "POST",
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        // Ẩn popup
        avatarPopup.style.display = "none";

        // Cập nhật ảnh đại diện trong template
        userAvatar.src = data.avatar_url;
      })
      .catch(error => {
        console.error("Error:", error);
      });
  });
});
