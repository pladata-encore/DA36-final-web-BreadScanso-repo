document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");
    const deleteBtn = document.getElementById("delete-btn");
    const confirmDeleteBtn = document.getElementById("confirm-delete-btn");
    const deleteConfirmModal = new bootstrap.Modal(document.getElementById("deleteConfirmModal"));
    const newRegisterBtn = document.getElementById("new-register-btn");
    const selectAllCheckbox = document.getElementById("select-all");
    const rowCheckboxes = document.querySelectorAll(".row-checkbox");
    const rows = document.querySelectorAll(".store-menu-table tbody tr");

    // 전체 선택 체크박스 변경
    selectAllCheckbox.addEventListener("change", function () {
        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });
    });

    // 행 클릭 시 페이지 이동 (체크박스 열 제외)
    rows.forEach(row => {
        row.addEventListener("click", function (event) {
            const target = event.target;

            // 체크박스 클릭 시 체크 상태 변경 후 이벤트 전파 방지
            if (target.closest(".checkbox-column")) {
                const checkbox = target.closest(".checkbox-column").querySelector(".row-checkbox");
                if (checkbox) {
                    checkbox.checked = !checkbox.checked;
                }
                event.stopPropagation(); // tr 클릭 이벤트 방지
                return;
            }

            // 체크박스 열이 아닌 경우에만 페이지 이동
            const item_id = row.querySelector("td:nth-child(2)").textContent.trim();

            // Django view URL 패턴에 맞게 변경
            window.location.href = `/menu/store/menu_info/${item_id}/`;
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
        window.location.href = "/menu/store/menu_add"; // 이동할 URL 설정
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
