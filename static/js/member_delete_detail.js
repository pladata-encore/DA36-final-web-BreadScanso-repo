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

// 회원탈퇴사유 직접입력칸
document.addEventListener("DOMContentLoaded", function () {
    const otherCheckbox = document.getElementById("otherReasonCheckbox");
    const otherText = document.getElementById("otherReasonText");

    // 체크박스 클릭 시 textarea 보이기/숨기기
    otherCheckbox.addEventListener("change", function () {
        if (this.checked) {
            otherText.style.display = "block"; // 보이기
            otherText.focus(); // 입력 가능하도록 포커스
        } else {
            otherText.style.display = "none"; // 숨기기
            otherText.value = ""; // 내용 초기화
        }
    });

    // 입력할 때마다 높이 자동 조절
    otherText.addEventListener("input", function () {
        this.style.height = "auto"; // 높이를 초기화
        this.style.height = this.scrollHeight + "px"; // 내용에 맞춰 높이 조정
    });
});


