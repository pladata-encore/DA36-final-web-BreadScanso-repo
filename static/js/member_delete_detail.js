// 팝업창
document.addEventListener("DOMContentLoaded", function () {
    let form = document.querySelector("form");
    let confirmButton = document.getElementById("confirmButton"); // 첫번째 팝업창 띄우는 버튼
    let finalConfirmButton = document.getElementById("finalConfirmButton"); // 두번째 팝업창 띄우는 버튼
    let goHomeButton = document.getElementById("goHomeButton"); // 홈으로 이동 버튼

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // 기본 폼 제출 방지

        // 회원탈퇴 첫번째 표시
        let firstModal = new bootstrap.Modal(document.getElementById("confirmSuccessModal"));
        firstModal.show();
    });

    finalConfirmButton.addEventListener("click", function () {
        // 첫번째 팝업창 닫기
        let firstModal = bootstrap.Modal.getInstance(document.getElementById("confirmSuccessModal"));
        firstModal.hide();

        // 두번째 팝업창 표시
        let secondModal = new bootstrap.Modal(document.getElementById("finalModal"));
        secondModal.show();
    });

    goHomeButton.addEventListener("click", function () {
        window.location.href = "/";  // 홈 페이지로 이동
    });
});

// 체크박스
document.getElementById("otherReasonCheckbox").addEventListener("change", function() {
    let otherReasonText = document.getElementById("otherReasonText");
    if (this.checked) {
        otherReasonText.style.display = "block"; // 체크되면 입력창 표시
    } else {
        otherReasonText.style.display = "none";  // 체크 해제되면 숨김
        otherReasonText.value = "";  // 입력값 초기화
    }
});
