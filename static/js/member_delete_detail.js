document.addEventListener("DOMContentLoaded", function () {
    let form = document.querySelector("form");
    let confirmButton = document.getElementById("confirmButton");
    let finalConfirmButton = document.getElementById("finalConfirmButton");
    let submitDeleteFormButton = document.getElementById("submitDeleteForm");

    // 첫 번째 탈퇴 버튼 클릭 시 첫 번째 모달 표시
    if (confirmButton) {
        confirmButton.addEventListener("click", function (event) {
            event.preventDefault(); // 기본 폼 제출 방지
            let firstModal = new bootstrap.Modal(document.getElementById("confirmSuccessModal"));
            firstModal.show();
        });
    }

    // 첫 번째 모달의 확인 버튼 클릭 시 두 번째 모달 표시
    if (finalConfirmButton) {
        finalConfirmButton.addEventListener("click", function () {
            let firstModal = bootstrap.Modal.getInstance(document.getElementById("confirmSuccessModal"));
            if (firstModal) firstModal.hide();

            let secondModal = new bootstrap.Modal(document.getElementById("finalModal"));
            secondModal.show();
        });
    }

    // 두 번째 모달의 확인 버튼 클릭 시 폼 실제 제출
    if (submitDeleteFormButton) {
        submitDeleteFormButton.addEventListener("click", function () {
            let form = document.getElementById("deleteForm"); // 폼 ID 지정
            if (form) {
                form.submit(); // 폼 제출 실행
            } else {
                console.error("폼을 찾을 수 없습니다.");
            }
        });
    }
});


// 체크박스
    document.getElementById("otherReasonCheckbox").addEventListener("change", function () {
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