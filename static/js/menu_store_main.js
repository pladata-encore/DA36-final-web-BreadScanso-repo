document.addEventListener("DOMContentLoaded", function () {
    const selectAllCheckbox = document.getElementById("select-all");
    const rowCheckboxes = document.querySelectorAll(".row-checkbox");
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");
    const rows = document.querySelectorAll(".store-menu-table tbody tr");
    const deleteBtn = document.getElementById("delete-btn");
    const confirmDeleteBtn = document.getElementById("confirm-delete-btn");
    const deleteConfirmModal = new bootstrap.Modal(document.getElementById("deleteConfirmModal"));
    const newRegisterBtn = document.getElementById("new-register-btn");

    // 전체 선택 체크박스 상태 변경 시
    selectAllCheckbox.addEventListener("change", function () {
        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });
    });

    // 개별 체크박스 상태 변경 시
    rowCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function () {
            // 개별 체크박스 상태 변경 시 추가 동작 없음
        });
    });

    // 행 클릭 시 /menu/store/menu_info 이동 (체크박스를 제외한 부분 클릭 시)
    rows.forEach(row => {
        row.addEventListener("click", function (event) {
            // 클릭한 요소가 체크박스이면 이동하지 않음
            if (event.target.type === "checkbox") return;

            // 체크박스 외의 영역 클릭 시 이동
            window.location.href = "/menu/store/menu_info";
        });
    });

    // 검색 폼 제출 시 검색 기능
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

    // 메뉴 신규 등록 페이지 이동
    newRegisterBtn.addEventListener("click", function () {
        window.location.href = "/menu/store/new_menu"; // 이동할 URL 설정
    });

    // 삭제 버튼 클릭 시 모달 표시
    deleteBtn.addEventListener("click", function () {
        const checkedRows = document.querySelectorAll(".row-checkbox:checked");

        if (checkedRows.length === 0) {
            alert("삭제할 제품을 선택하세요.");
        } else {
            deleteConfirmModal.show();
        }
    });

    // 모달에서 삭제 버튼 클릭 시 선택된 행 삭제
    confirmDeleteBtn.addEventListener("click", function () {
        const checkedRows = document.querySelectorAll(".row-checkbox:checked");

        checkedRows.forEach((checkbox) => {
            checkbox.closest("tr").remove(); // 선택된 행 삭제
        });

        // 모달 닫기
        deleteConfirmModal.hide();
    });
});
