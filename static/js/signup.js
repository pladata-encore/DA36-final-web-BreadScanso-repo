// 연령대
function setAge(age) {
    document.getElementById("ageDropdownBtn").textContent = age;
}

// 성별
function setSex(sex) {
    document.getElementById("sexDropdownBtn").textContent = sex;
}

//
function checkUsername() {
    var user_id = document.getElementById("user_id").value;
    var resultElement = document.getElementById("user_id-result");

    fetch("/check-user_id/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
        },
        body: "user_id=" + encodeURIComponent(user_id)
    })
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                resultElement.innerText = "이미 사용 중인 아이디입니다.";
                resultElement.style.color = "red";
            } else {
                resultElement.innerText = "사용 가능한 아이디입니다!";
                resultElement.style.color = "green";
            }
        });
}

// CSRF 토큰 가져오기 (Django 보안 정책 대응)
function getCSRFToken() {
    return document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}

<!-- 이메일 선택란 설정 -->
document.addEventListener("DOMContentLoaded", function () {
    let emailIdInput = document.getElementById("email_id");
    let emailDomainSelect = document.getElementById("email_domain");
    let emailCustomInput = document.getElementById("email_custom");
    let emailFullInput = document.getElementById("email_full");

    function updateEmail() {
        let emailId = emailIdInput.value.trim();
        let domain = emailDomainSelect.value;

        if (domain === "직접입력") {
            domain = emailCustomInput.value.trim();
        }

        emailFullInput.value = emailId && domain ? `${emailId}@${domain}` : "";
    }

    emailIdInput.addEventListener("input", updateEmail);
    emailDomainSelect.addEventListener("change", function () {
        if (this.value === "직접입력") {
            emailCustomInput.classList.remove("d-none");
        } else {
            emailCustomInput.classList.add("d-none");
            emailCustomInput.value = "";
        }
        updateEmail();
    });
    emailCustomInput.addEventListener("input", updateEmail);
});

// 팝업창
document.addEventListener("DOMContentLoaded", function () {
    let signupForm = document.querySelector("form");  // 폼 선택
    let confirmButton = document.getElementById("confirmButton"); // 확인 버튼

    // signupForm.addEventListener("submit", function (event) {
    // event.preventDefault(); // 기본 폼 제출 방지  -> 해당 코드 삭제 예정, 제출 방지하고있어 db에 갈 수 없었음

    // 가입 완료 팝업창 표시
    let modal = new bootstrap.Modal(document.getElementById("signupSuccessModal"));
    modal.show();

    // 확인 버튼 클릭 시 홈 화면으로 이동
    confirmButton.addEventListener("click", function () {
    window.location.href = "/";  // 홈 페이지로 이동
});
});
