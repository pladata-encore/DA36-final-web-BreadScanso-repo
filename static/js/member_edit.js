document.querySelector("#memberEditForm").addEventListener("submit", function (event) {
    event.preventDefault();  // 기본 폼 제출 동작을 막기

    let form = new FormData(this);
    console.log([...form]);  // 전송되는 데이터를 콘솔에 출력

    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch("/member/edit/", {
        method: "POST",
        body: form,
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // 서버 응답을 콘솔에 출력
        if (data.success) {
            $('#signupSuccessModal').modal('show');
        } else {
            alert("수정에 실패했습니다.");
        }
    })
    .catch(error => console.error("Error:", error));
});



// 연령대
function setAge(age) {
    document.getElementById("ageDropdownBtn").textContent = age;
}

// 성별
function setSex(sex) {
    document.getElementById("sexDropdownBtn").textContent = sex;
}

// 이메일 선택란 설정
document.addEventListener('DOMContentLoaded', function() {
    const emailId = document.getElementById('email_id');
    const emailDomain = document.getElementById('email_domain');
    const emailCustom = document.getElementById('email_custom');
    const emailFull = document.getElementById('email_full');

    // 이메일 도메인이 리스트에 없는 경우 처리
    {% if member.email %}
        const emailParts = "{{ member.email }}".split('@');
        if (emailParts.length === 2) {
            const domain = emailParts[1];
            if (!['naver.com', 'gmail.com', 'daum.net'].includes(domain)) {
                emailDomain.value = '직접입력';
                emailCustom.classList.remove('d-none');
                emailCustom.value = domain;
            }
        }
    {% endif %}

    // 이메일 값 업데이트 함수
    function updateEmail() {
        const domain = emailDomain.value === '직접입력' ? emailCustom.value : emailDomain.value;
        emailFull.value = emailId.value + '@' + domain;
    }

    // 이벤트 리스너 등록
    emailId.addEventListener('input', updateEmail);
    emailDomain.addEventListener('change', function() {
        if (this.value === '직접입력') {
            emailCustom.classList.remove('d-none');
            emailCustom.value = '';
        } else {
            emailCustom.classList.add('d-none');
        }
        updateEmail();
    });
    emailCustom.addEventListener('input', updateEmail);

    // 초기 이메일 값 설정
    updateEmail();
});
// document.addEventListener("DOMContentLoaded", function () {
//     let emailIdInput = document.getElementById("email_id");
//     let emailDomainSelect = document.getElementById("email_domain");
//     let emailCustomInput = document.getElementById("email_custom");
//     let emailFullInput = document.getElementById("email_full");
//
//     function updateEmail() {
//         let emailId = emailIdInput.value.trim();
//         let domain = emailDomainSelect.value;
//
//         if (domain === "직접입력") {
//             domain = emailCustomInput.value.trim();
//         }
//
//         emailFullInput.value = emailId && domain ? `${emailId}@${domain}` : "";
//     }
//
//     emailIdInput.addEventListener("input", updateEmail);
//     emailDomainSelect.addEventListener("change", function () {
//         if (this.value === "직접입력") {
//             emailCustomInput.classList.remove("d-none");
//         } else {
//             emailCustomInput.classList.add("d-none");
//             emailCustomInput.value = "";
//         }
//         updateEmail();
//     });
//     emailCustomInput.addEventListener("input", updateEmail);
// });

// 아이디 중복 확인
function checkUser_id() {
    const user_id = document.querySelector('input[name="user_id"]').value;
    const resultElement = document.getElementById('user_id-result');

    if (!user_id) {
        resultElement.textContent = '아이디를 입력해주세요.';
        resultElement.style.color = 'red';
        return;
    }

    // AJAX 요청
    fetch(`/check-user-id/?user_id=${encodeURIComponent(user_id)}`)
        .then(response => response.json())
        .then(data => {
            resultElement.textContent = data.message;
            resultElement.style.color = data.available ? 'green' : 'red';

            // 결과를 폼에 저장 (선택사항)
            const form = document.getElementById('memberEditForm');
            form.dataset.idChecked = data.available;
        })
        .catch(error => {
            console.error('Error:', error);
            resultElement.textContent = '중복 확인 중 오류가 발생했습니다.';
            resultElement.style.color = 'red';
        });
}

// 폼 제출 시 중복 확인 여부 체크 (선택사항)
document.getElementById('memberEditForm').addEventListener('submit', function(e) {
    if (this.dataset.idChecked !== 'true') {
        e.preventDefault();
        alert('아이디 중복 확인을 해주세요.');
        return false;
    }
});

// 아이디 입력 필드 변경 시 중복 확인 상태 초기화
document.querySelector('input[name="user_id"]').addEventListener('input', function() {
    const form = document.getElementById('memberEditForm');
    form.dataset.idChecked = 'false';
    document.getElementById('user_id-result').textContent = '';
});
// function checkUser_id() {
//     var user_id = document.getElementById("user_id").value;
//     var resultElement = document.getElementById("user_id-result");
//
//     fetch("/check-user_id/", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/x-www-form-urlencoded",
//             "X-CSRFToken": getCSRFToken()
//         },
//         body: "user_id=" + encodeURIComponent(user_id)
//     })
//         .then(response => response.json())
//         .then(data => {
//             if (data.exists) {
//                 resultElement.innerText = "이미 사용 중인 아이디입니다.";
//                 resultElement.style.color = "red";
//             } else {
//                 resultElement.innerText = "사용 가능한 아이디입니다!";
//                 resultElement.style.color = "green";
//             }
//         });
// }
//
// // CSRF 토큰 가져오기 (Django 보안 정책 대응)
// function getCSRFToken() {
//     return document.cookie.split("; ")
//         .find(row => row.startsWith("csrftoken="))
//         ?.split("=")[1];
// }

// 팝업창
document.addEventListener("DOMContentLoaded", function () {
    let signupForm = document.querySelector("form");  // 폼 선택
    let confirmButton = document.getElementById("confirmButton"); // 확인 버튼

    signupForm.addEventListener("submit", function (event) {
        event.preventDefault(); // 기본 폼 제출 방지

        // 회원정보수정 완료 팝업창 표시
        let modal = new bootstrap.Modal(document.getElementById("signupSuccessModal"));
        modal.show();

        // 확인 버튼 클릭 시 회원정보수정페이지 화면으로 이동
        confirmButton.addEventListener("click", function () {
            window.location.href = '{% url "member:member_page" %}' // 회원정보수정페이지로 이동
        });
    });
});
