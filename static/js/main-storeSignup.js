document.addEventListener("DOMContentLoaded", function() {
    let userIdInput = document.getElementById("user_id");
    let userIdResult = document.getElementById("username-check-result");
    let checkUsernameBtn = document.getElementById("check-username-btn");
    let signupBtn = document.querySelector("button[type='submit']"); // 회원가입 버튼

    let isIdValid = false;  // 아이디 조건 만족 여부
    let isIdUnique = false; // 중복 체크 완료 여부

    // 아이디 유효성 검사 (영소문자+숫자 4~12자리)
    userIdInput.addEventListener("input", function() {
        let userId = userIdInput.value;
        let regex = /^[a-z0-9]{4,12}$/;

        if (!regex.test(userId)) {
            userIdResult.style.color = "red";
            userIdResult.innerText = "아이디는 영소문자/숫자 4~12자리여야 합니다.";
            isIdValid = false;
        } else {
            userIdResult.style.color = "green";
            userIdResult.innerText = "사용 가능한 아이디입니다.";
            isIdValid = true;
        }

        isIdUnique = false;  // 새 아이디 입력 시 중복 체크 다시
        checkSignupButton();
    });

    // 중복 확인 버튼 클릭 시 AJAX 요청
    checkUsernameBtn.addEventListener("click", function() {
        let userId = userIdInput.value;

        if (!isIdValid) {
            alert("아이디 조건을 먼저 충족해주세요.");
            return;
        }

        fetch(`/main/check_user_id/?user_id=${userId}`)
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
                checkSignupButton();
            })
            .catch(error => console.error("Error:", error));
    });

    // '중복확인' 해야 가입 버튼 누를 수 있음.
    function checkSignupButton() {
        if (isIdValid && isIdUnique) {
            signupBtn.disabled = false;
        } else {
            signupBtn.disabled = true;
        }
    }

    // 비밀번호 유효성 검사 (영문+숫자+특수문자 4~12자리)
    let passwordInput = document.getElementById("password1");
    let passwordResult = document.getElementById("password-check-result");

    passwordInput.addEventListener("input", function() {
        let password = passwordInput.value;
        let regex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[\W_]).{4,12}$/;

        if (!regex.test(password)) {
            passwordResult.style.color = "red";
            passwordResult.innerText = "영문자+숫자+특수문자 4~12자리여야 합니다.";
        } else {
            passwordResult.style.color = "green";
            passwordResult.innerText = "사용 가능한 비밀번호입니다.";
        }
    });

    // 비밀번호 확인 (password1 == password2)
    let passwordConfirmInput = document.getElementById("password2");
    let passwordConfirmResult = document.getElementById("password-match-result");

    passwordConfirmInput.addEventListener("input", function() {
        let password1 = passwordInput.value;
        let password2 = passwordConfirmInput.value;

        if (password1 === password2) {
            passwordConfirmResult.style.color = "green";
            passwordConfirmResult.innerText = "비밀번호가 동일합니다.";
        } else {
            passwordConfirmResult.style.color = "red";
            passwordConfirmResult.innerText = "비밀번호가 동일하지 않습니다.";
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
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

    emailDomainSelect.addEventListener("change", function() {
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
});
