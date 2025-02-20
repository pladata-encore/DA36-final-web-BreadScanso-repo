document.addEventListener("DOMContentLoaded", function () {
    let signupForm = document.querySelector("form");  // 폼 선택
    let confirmButton = document.getElementById("confirmButton"); // 확인 버튼

    signupForm.addEventListener("submit", function (event) {
        event.preventDefault(); // 기본 폼 제출 방지

        // 비밀번호변경 완료 팝업창 표시
        let modal = new bootstrap.Modal(document.getElementById("signupSuccessModal"));
        modal.show();

        // 확인 버튼 클릭 시 비밀번호변경 페이지 화면으로 이동
        confirmButton.addEventListener("click", function () {
            onclick="location.href='{% url 'member_pw' %}'";  // 비밀번호변경 페이지로 이동
        });
    });
});