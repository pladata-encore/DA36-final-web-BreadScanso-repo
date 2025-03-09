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

// 이벤트 삭제 기능
document.getElementById("delete-selected").addEventListener("click", async function () {
    // 체크된 이벤트 수집
    const selectedIds = Array.from(document.querySelectorAll(".row-checkbox:checked"))
        .map(checkbox => checkbox.closest('tr').querySelector('td:nth-child(2)').innerText);  // 아이디 칼럼에서 값 가져오기

    console.log("선택된 이벤트 ID:", selectedIds);  // 콘솔 로그 확인


    if (selectedIds.length === 0) {
        alert("삭제할 이벤트를 선택해주세요.");
        return;
    }

    if (!confirm(`선택한 이벤트를 삭제하시겠습니까?`)) {
        return;
    }

    try {
        const response = await fetch("/store/delete_store_event/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({event_ids: selectedIds}),
        });

        const data = await response.json();
        if (data.success) {
            alert("삭제가 완료되었습니다.");
            window.location.reload();
        } else {
            alert("삭제 실패: " + data.message);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("삭제 중 오류가 발생했습니다.");
    }
});

// CSRF 토큰 가져오기 함수
    function getCSRFToken() {
        return document.getElementsByName("csrfmiddlewaretoken")[0].value;
    }

