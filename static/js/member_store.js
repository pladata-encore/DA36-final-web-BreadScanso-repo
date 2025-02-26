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

// 전체 선택/해제 체크박스 이벤트 처리
    document.getElementById('select-all').addEventListener('change', function () {
        let checkboxes = document.querySelectorAll('.row-checkbox');
        checkboxes.forEach(function (checkbox) {
            checkbox.checked = document.getElementById('select-all').checked;
        });
    });

    // 각 행의 체크박스 상태 변경 시, '전체 선택' 체크박스 상태를 업데이트
    let rowCheckboxes = document.querySelectorAll('.row-checkbox');
    rowCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            let allChecked = true;
            rowCheckboxes.forEach(function (checkbox) {
                if (!checkbox.checked) {
                    allChecked = false;
                }
            });
            document.getElementById('select-all').checked = allChecked;
        });
    });

    // 회원정보 수정 버튼 클릭 시 모달 열기
document.querySelectorAll('.edit-member-btn').forEach(button => {
    button.addEventListener('click', function (event) {
        const row = event.target.closest('tr');
        const rowId = row.querySelector('td:nth-child(3)').innerText;  // 아이디
        const Name = row.querySelector('td:nth-child(2)').innerText;   // 이름
        const PhoneNum = row.querySelector('td:nth-child(4)').innerText; // 휴대폰 번호
        const Email = row.querySelector('td:nth-child(7)').innerText;  // 이메일

        // 모달창에 값 설정
        document.getElementById('editName').value = Name;
        document.getElementById('editPhoneNum').value = PhoneNum;
        document.getElementById('editEmail').value = Email;

        const modalElement = document.getElementById('editModal');
        const editModal = new bootstrap.Modal(modalElement, {
            backdrop: 'static',
            keyboard: false
        });

        editModal.show();

        // 저장 버튼 클릭 시
        document.getElementById('saveChangesButton').onclick = function () {
            const newName = document.getElementById('editName').value;
            const newPhoneNum = document.getElementById('editPhoneNum').value;
            const newEmail = document.getElementById('editEmail').value;

            // 이메일 유효성 검사 (간단한 정규식 사용)
            const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
            if (newName && newPhoneNum && newEmail && emailPattern.test(newEmail)) {
                updateMember_store(rowId, newName, newPhoneNum, newEmail);
                editModal.hide();
            } else {
                alert('유효한 값을 입력해주세요.');
            }
        };
    });
});


            // document.getElementById('saveChangesButton').onclick = function () {
            //     const newName = document.getElementById('editName').value;
            //     const newPhoneNum = document.getElementById('editPhoneNum').value;
            //     const newEmail = document.getElementById('editEmail').value;

            // // 이메일 유효성 검사 (간단한 정규식 사용)
            // const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
            // if (newName && newPhoneNum && newEmail !== "" && emailPattern.test(newEmail)) {
            //     updateMember_store(rowId, newName, newPhoneNum, newEmail);
            //     editModal.hide();

            // if (newName && newPhoneNum && newEmail !== "" && !isNaN(newEmail)) {
            //     updateMember_store(newName, newPhoneNum, newEmail);
            //     editModal.hide();
            //         } else {
            //             alert('유효한 값을 입력해주세요.');
            //         }
            //     };
            // });
        });

        // 삭제 버튼 클릭 시
        document.getElementById("delete-selected").addEventListener("click", async function () {
            const selectedIds = Array.from(document.querySelectorAll(".row-checkbox:checked"))
                .map(checkbox => checkbox.closest("tr").querySelector("td:nth-child(3)").textContent.trim());  // 아이디 열이 3번째 열입니다

            if (selectedIds.length === 0) {
                alert("삭제할 회원을 선택해주세요.");
                return;
            }

            if (!confirm(`선택한 회원의 정보를 삭제하시겠습니까?`)) {
                return;
            }

            try {
                const response = await fetch("/store/delete_member/", {  // URL 경로 수정
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCSRFToken(),
                    },
                    body: JSON.stringify({member_ids: selectedIds}),
                });

                const data = await response.json();
                if (data.success) {
                    alert("삭제가 완료되었습니다.");
                    window.location.reload();
                } else {
                    alert("삭제 실패: " + (data.message || "알 수 없는 오류가 발생했습니다."));
                }
            } catch (error) {
                console.error("Error:", error);
                alert("삭제 중 오류가 발생했습니다.");
            }
        });


        // CSRF 토큰 가져오기 함수
            function getCSRFToken() {
                return document.querySelector('[name=csrfmiddlewaretoken]').value;
            }


// // 회원 정보 업데이트 함수
//     function updateMember_store(memberID, newName, newPhoneNum, newEmail, sex, ageGroup, visitCount, totalSpent, membershipDate, lastVisited, points, profileImage) {
//         fetch('/store/update_member_store/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCSRFToken(),
//             },
//             'member_id': memberID,
//             'new_name': newName,
//             'new_phone_num': newPhoneNum,
//             'new_email': newEmail,
//             'sex': sex,
//             'age_group': ageGroup,
//             'visit_count': visitCount,
//             'total_spent': totalSpent,
//             'membership_date': membershipDate,
//             'last_visited': lastVisited,
//             'points': points,
//             'profile_image': profileImage
//         })
//
//             .then(response => response.json())
//             .then(data => {
//                 if (data.success) {
//                     const row = event.target.closest('tr');
//                     row.querySelector('td:nth-child(2)').innerText = newName;
//                     row.querySelector('td:nth-child(4)').innerText = newPhoneNum;
//                     row.querySelector('td:nth-child(7)').innerText = newEmail;
//                     alert('회원 정보가 변경되었습니다.');
//                 }
//             })
//     // 회원 정보 업데이트 함수 내부
//     then(response => {
//         console.log("Response status:", response.status);
//         return response.json();
//     })
//         .then(data => {
//             console.log("Server response:", data);
//         })
//         .catch(error => {
//             alert("서버 오류 발생");
//         });


// 회원 정보 업데이트 함수
function updateMember_store(memberID, newName, newPhoneNum, newEmail) {
    fetch('/store/update_member_store/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            member_id: memberID,
            new_name: newName,
            new_phone_num: newPhoneNum,
            new_email: newEmail
        })
    })
    .then(response => {
        console.log("Response status:", response.status);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Server response:", data);
        if (data.success) {
            alert('회원 정보가 변경되었습니다.');
            // 페이지 새로고침
            window.location.reload();
        } else {
            alert('회원 정보 변경에 실패했습니다: ' + (data.error || '알 수 없는 오류'));
        }
    })
    .catch(error => {
        console.error("Fetch 에러:", error);
        alert("서버 오류가 발생했습니다: " + error.message);
    });
}

// function updateMember_store(memberID, newName, newPhoneNum, newEmail) {
//     fetch('/store/update_member_store/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': getCSRFToken(),
//         },
//         body: JSON.stringify({
//             member_id: memberID,
//             new_name: newName,
//             new_phone_num: newPhoneNum,
//             new_email: newEmail,
//             sex: sex,
//             age_group: ageGroup,
//             visit_count: visitCount,
//             total_spent: totalSpent,
//             membership_date: membershipDate,
//             last_visited: lastVisited,
//             points: points,
//             profile_image: profileImage
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             // 클릭된 버튼의 부모 <tr> 요소 찾기
//             const row = event.target.closest('tr');
//             row.querySelector('td:nth-child(2)').innerText = newName;
//             row.querySelector('td:nth-child(4)').innerText = newPhoneNum;
//             row.querySelector('td:nth-child(7)').innerText = newEmail;
//             alert('회원 정보가 변경되었습니다.');
//         } else {
//             alert('회원 정보 변경에 실패했습니다.');
//         }
//     })
//     .catch(error => {
//         console.error("Fetch 에러:", error);
//         alert("서버 오류가 발생했습니다.");
//     });
// }




    // const newRegisterBtn = document.getElementById("new-register-btn");
    // newRegisterBtn.addEventListener("click", function () {
    //     window.location.href = "/store/store";  // 이동할 URL 경로
    // });


