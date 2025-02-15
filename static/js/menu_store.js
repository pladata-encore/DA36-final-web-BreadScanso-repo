document.addEventListener("DOMContentLoaded", function () {
    const selectAllCheckbox = document.getElementById("select-all");
    const rowCheckboxes = document.querySelectorAll(".row-checkbox");
    const deleteBtn = document.getElementById("delete-btn");
    const deletePopup = document.getElementById("delete-popup");
    const confirmDeleteBtn = document.getElementById("confirm-delete");
    const cancelDeleteBtn = document.getElementById("cancel-delete");
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");
    const rows = document.querySelectorAll("table.store-menu-table tbody tr");
    const newRegisterBtn = document.querySelector(".btn-info");

    let selectedRows = [];


    // 전체 선택 체크
    selectAllCheckbox.addEventListener("change", function () {
        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
            toggleRowSelection(checkbox.closest("tr"), checkbox.checked);
        });
        updateSelectedRows();
    });

    // 개별 선택 체크
    rowCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function () {
            toggleRowSelection(checkbox.closest("tr"), checkbox.checked);
            updateSelectedRows();
        });
    });

    // 개별 선택 시 행 색상 변경
    function toggleRowSelection(row, isSelected) {
        if (row) {
            row.classList.toggle("selected", isSelected);
        }
    }

    // 선택된 행을 배열로 업데이트
    function updateSelectedRows() {
        selectedRows = [];
        rowCheckboxes.forEach((checkbox, index) => {
            if (checkbox.checked) {
                selectedRows.push(index);
            }
        });
    }

    // 삭제 버튼 클릭 시 팝업 열기
    deleteBtn.addEventListener("click", function () {
        if (selectedRows.length > 0) {
            deletePopup.style.display = "flex"; // 팝업창 띄우기
        } else {
            alert("삭제할 항목을 선택해주세요."); // 항목이 선택되지 않았을 경우 알림
        }
    });

    // 예 버튼 클릭 시 삭제
    confirmDeleteBtn.addEventListener("click", function () {
        selectedRows.forEach(rowIndex => {
            const row = rowCheckboxes[rowIndex].closest("tr");
            row.remove(); // 행 삭제
        });
        deletePopup.style.display = "none"; // 팝업창 닫기
        updateSelectedRows(); // 선택된 행 초기화
    });

    // 아니오 버튼 클릭 시 팝업창 닫기
    cancelDeleteBtn.addEventListener("click", function () {
        deletePopup.style.display = "none"; // 팝업창 닫기
    });

    // 검색 폼 제출 시
    searchForm.addEventListener("submit", function (event) {
        event.preventDefault(); // 기본 form 제출을 막음
        const searchTerm = searchInput.value.toLowerCase(); // 검색어 소문자 변환

        // 테이블의 각 행을 순회하며 검색어와 비교
        rows.forEach(row => {
            const cells = row.querySelectorAll("td");
            let rowText = "";
            cells.forEach(cell => {
                rowText += cell.textContent.toLowerCase(); // 모든 셀의 텍스트를 합침
            });

            // 검색어가 행의 텍스트에 포함되면 해당 행을 보여줌
            row.style.display = rowText.includes(searchTerm) ? "" : "none"; // 조건문으로 간결하게 표현
        });
    });

    // 팝업창을 처음에 숨김 처리
    deletePopup.style.display = "none"; // 페이지 로드 시 팝업은 숨김 상태로 설정

    // 메뉴 신규 등록 페이지 이동
    newRegisterBtn.addEventListener("click", function () {
        window.location.href = "/menu/store/new_menu"; // 이동할 URL 설정
    });

});