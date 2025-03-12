document.addEventListener("DOMContentLoaded", function () {
    let userIdInput = document.getElementById("user_id");
    let userIdResult = document.getElementById("username-check-result");
    let checkUsernameBtn = document.getElementById("check-username-btn");
    let saveButton = document.querySelector("button[type='submit']");
    let emailIdInput = document.getElementById("email_id");
    let emailDomainSelect = document.getElementById("email_domain");
    let emailCustomInput = document.getElementById("email_custom");
    let emailFullInput = document.getElementById("email_full");

    let isIdValid = false;
    let isIdUnique = false;

    // ✅ 아이디 유효성 검사
    userIdInput.addEventListener("input", function () {
        let userId = userIdInput.value.trim();
        let regex = /^[a-z0-9]{4,12}$/;

        if (!regex.test(userId)) {
            userIdResult.style.color = "red";
            userIdResult.innerText = "아이디는 영소문자/숫자 4~12자리여야 합니다.";
            isIdValid = false;
        } else {
            userIdResult.style.color = "green";
            userIdResult.innerText = "사용 가능한 아이디 형식입니다.";
            isIdValid = true;
        }

        isIdUnique = false;
        checkSaveButton();
    });

    // ✅ 중복 확인 버튼 클릭 시 AJAX 요청
    function checkUsername() {
        let userId = userIdInput.value.trim();

        if (!isIdValid) {
            alert("아이디 조건을 먼저 충족해주세요.");
            return;
        }

        fetch(`/member/check-user-id/?user_id=${encodeURIComponent(userId)}`)
            .then(response => response.json())
            .then(data => {
                if (data.valid) {
                    userIdResult.style.color = "gray";
                    userIdResult.innerText = "사용 가능한 아이디입니다.";
                    isIdUnique = true;
                } else {
                    alert("중복된 아이디입니다.");
                    userIdResult.style.color = "red";
                    userIdResult.innerText = "중복된 아이디입니다.";
                    isIdUnique = false;
                }
                checkSaveButton();
            })
            .catch(error => console.error("Error:", error));
    }

    // 버튼 이벤트에 checkUsername 연결
    checkUsernameBtn.addEventListener("click", checkUsername);

    // ✅ 수정 버튼 활성화 여부 체크
    function checkSaveButton() {
        saveButton.disabled = !(isIdValid && isIdUnique);
    }

    // ✅ 이메일 값 업데이트
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
            emailCustomInput.removeAttribute("disabled");
            emailCustomInput.focus();
        } else {
            emailCustomInput.classList.add("d-none");
            emailCustomInput.setAttribute("disabled", "true");
            emailCustomInput.value = "";
        }
        updateEmail();
    });
    emailCustomInput.addEventListener("input", updateEmail);

    // ✅ AJAX를 통한 폼 제출 처리
    const form = document.getElementById("memberEditForm");
    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            updateEmail();
            console.log("Form submission - Email:", emailFullInput.value);

            const formData = new FormData(this);
            const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            fetch("/member/member_edit/", {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": csrfToken,
                    "X-Requested-With": "XMLHttpRequest"
                },
                credentials: "same-origin"
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const modal = new bootstrap.Modal(document.getElementById("signupSuccessModal"));
                    modal.show();
                } else {
                    alert(data.error || "수정 중 오류가 발생했습니다.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("수정 중 오류가 발생했습니다: " + error.message);
            });
        });
    }
});
