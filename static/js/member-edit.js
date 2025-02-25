document.addEventListener('DOMContentLoaded', function() {
    // 기존 이메일 관련 코드는 그대로 유지
    const emailId = document.getElementById('email_id');
    const emailDomain = document.getElementById('email_domain');
    const emailCustom = document.getElementById('email_custom');
    const emailFull = document.getElementById('email_full');

    function updateEmail() {
        const domain = emailDomain.value === '직접입력' ? emailCustom.value : emailDomain.value;
        emailFull.value = emailId.value + '@' + domain;
    }

    emailId.addEventListener('input', updateEmail);
    emailDomain.addEventListener('change', function() {
        if (this.value === '직접입력') {
            emailCustom.classList.remove('d-none');
            emailCustom.addEventListener('input', updateEmail);
        } else {
            emailCustom.classList.add('d-none');
            updateEmail();
        }
    });

    // 폼 제출 처리 수정
    const form = document.getElementById('memberEditForm');
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // 기본 제출 동작 중지
        updateEmail();

        // FormData 객체 생성
        const formData = new FormData(this);

        // AJAX를 사용하여 폼 데이터 전송
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 성공 시 모달 표시
                const modal = new bootstrap.Modal(document.getElementById('signupSuccessModal'));
                modal.show();
            } else {
                // 실패 시 에러 메시지 표시
                alert(data.error || '수정 중 오류가 발생했습니다.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('수정 중 오류가 발생했습니다.');
        });
    });
});

function setAge(age) {
    document.getElementById('ageDropdownBtn').textContent = age;
    document.getElementById('age_group').value = age;
}

function setSex(sex) {
    document.getElementById('sexDropdownBtn').textContent = sex;
    document.getElementById('gender').value = sex;
}