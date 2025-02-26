document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector('form');
    const checkPasswordBtn = document.getElementById("checkPasswordBtn");
    const password1 = document.getElementById("password1");

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
                changePasswordBtn.disabled = false;
            } else {
                passwordCheckMessage.innerHTML = '<span class="text-danger">현재 비밀번호가 일치하지 않습니다.</span>';
                changePasswordBtn.disabled = true;
            }
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
