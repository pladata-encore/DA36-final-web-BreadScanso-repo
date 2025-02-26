// 모달 확인 버튼 누르면 저장
document.addEventListener('DOMContentLoaded', function() {
    const confirmSaveBtn = document.getElementById('confirm-save-btn');
    const menuForm = document.getElementById('menu-form');

    confirmSaveBtn.addEventListener('click', function() {
        // 폼 제출
        menuForm.submit();
    });

    // 이미지 미리보기 기능
    const fileInput = document.getElementById('file-input');
    const preview = document.getElementById('preview');

    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.addEventListener('load', function() {
                preview.src = reader.result;
            });
            reader.readAsDataURL(file);
        }
    });

    // 취소 버튼 누르면 목록 화면으로 이동
    const cancelBtn = document.getElementById('cancel-btn');
    cancelBtn.addEventListener('click', function() {
        window.location.href = "/store/";
    });
});