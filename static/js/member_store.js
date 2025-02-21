// 검색창
document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");
    const rows = document.querySelectorAll(".table tbody tr");


    searchForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const searchTerm = searchInput.value.toLowerCase();

        rows.forEach(row => {
            const cells = row.querySelectorAll("td");
            let rowText = "";
            cells.forEach(cell => {
                rowText += cell.textContent.toLowerCase();
            });
            row.style.display = rowText.includes(searchTerm) ? "" : "none";
        });
    });

// 회원정보db - 표
    document.addEventListener("DOMContentLoaded", function () {
        let editButtons = document.querySelectorAll(".btn-light, .btn-danger");

        // 수정 버튼 클릭 시 동작
        editButtons.forEach(button => {
            button.addEventListener("click", function () {
                toggleButton(this);
            });
        });

// 회원정보 수정 버튼 클릭 시 동작
function toggleButton(button) {
    const row = button.closest('tr'); // 버튼이 속한 행(tr)을 찾음
    const cells = row.querySelectorAll('td'); // 해당 행의 모든 셀을 선택

    if (button.innerText === "수정") {
    button.innerText = "저장"; // 버튼 텍스트 변경
    button.classList.remove("btn-light");
    button.classList.add("btn-secondary");

    // contenteditable을 true로 바꾸어 셀을 수정할 수 있게 함
    cells.forEach(cell => {
    if (cell.dataset.field) { // 데이터 필드가 있는 셀만 수정 가능하도록 처리
    cell.contentEditable = true;
    cell.style.backgroundColor = "#fff"; // 수정 중인 셀 배경색 변경 (선택 사항)
}
});
} else {
    button.innerText = "수정"; // 버튼 텍스트 변경
    button.classList.remove("btn-secondary");
    button.classList.add("btn-light");

    // contenteditable을 false로 바꾸어 셀 수정 마무리
    cells.forEach(cell => {
    if (cell.dataset.field) {
    cell.contentEditable = false;
    cell.style.backgroundColor = ""; // 배경색 원래대로
}
});

    // 수정된 데이터를 서버로 보내는 처리 추가 가능
    saveChanges(row); // 여기서 row 데이터를 서버로 보내거나 처리
}
}

// CSRF Token을 가져오는 함수 (Django에서 사용)
function getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}


// 회원 ID 가져오기
        function saveData(button) {
            let row = button.closest("tr");
            let memberId = row.querySelector("[data-field='member_id']").innerText;

            // 수정된 데이터 가져오기
            let updatedData = {};
            let editableFields = row.querySelectorAll("[data-field]");

            editableFields.forEach(field => {
                updatedData[field.getAttribute("data-field")] = field.innerText.trim();
                field.contentEditable = "false"; // 다시 수정 불가능하게 변경
                field.style.backgroundColor = ""; // 원래 배경색 복원
            });

            console.log("수정된 데이터:", updatedData);

// 회원 ID 서버로 데이터 전송 (AJAX)
            function saveMemberData(row) {
                let memberId = row.querySelector("[data-field='member_id']").innerText;
                let name = row.querySelector("[data-field='name']").innerText;
                let phone_num = row.querySelector("[data-field='phone_num']").innerText;
                let sex = row.querySelector("[data-field='sex']").innerText;
                let age_group = row.querySelector("[data-field='age_group']").innerText;
                let email = row.querySelector("[data-field='email']").innerText;

                let data = {
                    member_id: memberId,
                    name: name,
                    phone_num: phone_num,
                    sex: sex,
                    age_group: age_group,
                    email: email,
                    csrfmiddlewaretoken: "{{ csrf_token }}" // CSRF 토큰 추가
                };

                fetch("/update_member/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": data.csrfmiddlewaretoken
                    },
                    body: JSON.stringify(data)
                })
                    .then(response => response.json())
                    .then(result => {
                        if (result.success) {
                            alert("회원 정보가 성공적으로 수정되었습니다!");
                        } else {
                            alert("수정 실패: " + result.error);
                        }
                    })
                    .catch(error => console.error("에러:", error));
            }

// 버튼 변경
            button.style.display = "none"; // 저장 버튼 숨기기
            let editButton = row.querySelector(".edit-btn");
            editButton.style.display = "inline-block"; // 수정 버튼 다시 보이기
        }

// CSRF 토큰 가져오는 함수 (Django 보안용)
        function getCSRFToken() {
            return document.querySelector("[name=csrfmiddlewaretoken]").value;
        }

// 삭제 요청 보내기
        document.getElementById("finalConfirmButton").addEventListener("click", function () {
            // 실제 삭제 요청을 서버에 보낼 수 있도록 수정 필요
            alert("삭제가 완료되었습니다.");
            window.location.href = "{% url 'member_store' %}"; // 삭제 후 이동할 페이지 설정
        });

// 팝업창 표시
        document.addEventListener("DOMContentLoaded", function () {
            let form = document.querySelector("form");
            // let confirmButton = document.getElementById("confirmButton"); // 첫번째 팝업창 띄우는 버튼
            let finalConfirmButton = document.getElementById("finalConfirmButton"); // 두번째 팝업창 띄우는 버튼
            let goHomeButton = document.getElementById("goHomeButton"); // 홈으로 이동 버튼

            form.addEventListener("submit", function (event) {
                event.preventDefault(); // 기본 폼 제출 방지

                // 회원삭제 첫번째 표시
                let firstModal = new bootstrap.Modal(document.getElementById("deleteConfirmModal"));
                firstModal.show();
            });

            finalConfirmButton.addEventListener("click", function () {
                // 첫번째 팝업창 닫기
                let firstModal = bootstrap.Modal.getInstance(document.getElementById("deleteConfirmModal"));
                firstModal.hide();

                // 두번째 팝업창 표시
                let secondModal = new bootstrap.Modal(document.getElementById("finalModal"));
                secondModal.show();
            });

            goHomeButton.addEventListener("click", function () {
                window.location.href = "/";  // 홈 페이지로 이동
            });
        });
    });
})
