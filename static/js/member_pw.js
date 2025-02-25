document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector('form');
    const checkPasswordBtn = document.getElementById("checkPasswordBtn");
    const password1 = document.getElementById("password1");
    const password2 = document.getElementById("password2");
    const password3 = document.getElementById("password3");
    const passwordCheckMessage = document.getElementById("passwordCheckMessage");
    const changePasswordBtn = document.getElementById("changePasswordBtn");
    // const successModal = document.getElementById('signupSuccessModal');
    // const modalConfirmBtn = document.getElementById('modalConfirmBtn');

    // 초기 상태 설정
    password2.disabled = true;
    password3.disabled = true;
    changePasswordBtn.disabled = true;

    // 현재 비밀번호 확인
    checkPasswordBtn.addEventListener("click", function() {
        if (!password1.value) {
            alert('현재 비밀번호를 입력해주세요.');
            return;
        }

        fetch('/member/check_password/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                current_password: password1.value
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.valid) {
                passwordCheckMessage.innerHTML = '<span class="text-success">비밀번호가 일치합니다.</span>';
                password2.disabled = false;
                password3.disabled = false;
                changePasswordBtn.disabled = false;
            } else {
                passwordCheckMessage.innerHTML = '<span class="text-danger">현재 비밀번호가 일치하지 않습니다.</span>';
                password2.disabled = true;
                password3.disabled = true;
                changePasswordBtn.disabled = true;
            }
        });
    });

    // 새 비밀번호 입력 시 유효성 검사
    password2.addEventListener('input', validateNewPassword);
    password3.addEventListener('input', validateNewPassword);

    function validateNewPassword() {
        if (password2.value && password3.value) {
            if (password2.value !== password3.value) {
                changePasswordBtn.disabled = true;
                return;
            }

            // 비밀번호 형식 검사 (영문자, 숫자, 특수문자 포함 4~12자리)
            const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[\W_]).{4,12}$/;
            if (!passwordRegex.test(password2.value)) {
                changePasswordBtn.disabled = true;
                return;
            }

            changePasswordBtn.disabled = false;
        }
    }

    // 폼 제출 처리
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        if (!password1.value || !password2.value || !password3.value) {
            alert('모든 비밀번호 필드를 입력해주세요.');
            return;
        }

        if (password2.value !== password3.value) {
            alert('새 비밀번호가 일치하지 않습니다.');
            return;
        }

        // 서버로 폼 데이터 전송
        fetch(form.action, {
            method: 'POST',
            body: new FormData(form)
        })
        .then(response => response.text())
        .then(() => {
            // 비밀번호 변경 성공 시 모달 표시
            const modal = new bootstrap.Modal(document.getElementById('signupSuccessModal'));
            modal.show();
        });
    });

    // 모달 확인 버튼 클릭 처리
    document.addEventListener("DOMContentLoaded", function () {
        const confirmButton = document.getElementById("confirmButton");

        confirmButton.addEventListener("click", function () {
            const targetUrl = confirmButton.getAttribute("data-url"); // HTML에서 URL 가져오기
            window.location.href = targetUrl;
        });
    });

    // CSRF 토큰 가져오기
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});