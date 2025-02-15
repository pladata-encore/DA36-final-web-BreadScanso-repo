const fileInput = document.getElementById('file-input');
const preview = document.getElementById('preview');


// 파일 업로드 후 이미지 미리보기
fileInput.addEventListener('change', function(event) {
    const file = event.target.files[0];  // 선택한 파일
    if (file) {
        const reader = new FileReader();  // FileReader 객체 생성
        reader.onload = function(e) {
            preview.src = e.target.result;  // 미리보기 이미지 설정
            preview.style.display = 'block';  // 이미지 보이게 하기
            fileInput.style.display = 'none';  // 파일 업로드 칸 숨기기
        };
        reader.readAsDataURL(file);  // 파일을 URL로 읽음
    }
});

// 취소 버튼 누르면 목록 화면으로 이동
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("cancel-btn").addEventListener("click", function () {
        window.location.href = "/menu/store/";  // 취소 시 이전 화면으로 이동
    });
});

// 저장 버튼 누르면 메뉴관리 상세 페이지로 이동
document.getElementById("confirm-save-btn").addEventListener("click", function () {
    window.location.href = "/menu/store/menu_info";  // 확인을 누르면 menu_info 페이지로 이동
});
