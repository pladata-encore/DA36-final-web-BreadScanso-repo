// 취소 버튼 누르면 목록 화면으로 이동
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("cancel-btn").addEventListener("click", function () {
        window.location.href = "/menu/store/";  // 취소 시 이전 화면으로 이동
    });
});