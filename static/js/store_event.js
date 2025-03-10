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

// 행 클릭 시 페이지 이동 (체크박스 열 제외)
    rows.forEach(row => {
        row.addEventListener("click", function (event) {
            const target = event.target;

            // 체크박스 자체를 클릭한 경우
            if (target.classList.contains("row-checkbox")) {
                // 체크박스 클릭 시 기본 동작 유지 (자동으로 체크 상태 변경됨)
                event.stopPropagation(); // tr 클릭 이벤트 방지
                return;
            }

            // 체크박스 열(컬럼)을 클릭한 경우
            if (target.closest(".checkbox-column")) {
                const checkbox = target.closest(".checkbox-column").querySelector(".row-checkbox");
                if (checkbox) {
                    checkbox.checked = !checkbox.checked;
                }
                event.stopPropagation(); // tr 클릭 이벤트 방지
                return;
            }

            // 체크박스 열이 아닌 경우에만 페이지 이동
            const event_id = row.querySelector("td:nth-child(2)").textContent.trim();
            // 해당 제품 정보로 이동
            window.location.href = `/store/store_event_info/${event_id}/`;
        });
    });

// 필터링
document.addEventListener('DOMContentLoaded', function() {
    // 필터 변경 시 폼 제출
    document.getElementById('store-filter').addEventListener('change', function() {
        console.log('Store filter changed:', this.value); // 디버깅용
        document.getElementById('search-form').submit();
    });

    document.getElementById('show-filter').addEventListener('change', function() {
        console.log('Show filter changed:', this.value); // 디버깅용
        document.getElementById('search-form').submit();
    });

    document.getElementById('finish-filter').addEventListener('change', function() {
        console.log('Finish filter changed:', this.value); // 디버깅용
        document.getElementById('search-form').submit();
    });
});