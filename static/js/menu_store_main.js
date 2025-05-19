document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("search-form");
    const deleteBtn = document.getElementById("delete-btn");
    const confirmDeleteBtn = document.getElementById("confirm-delete-btn");
    const deleteConfirmModal = new bootstrap.Modal(document.getElementById("deleteConfirmModal"));
    const newRegisterBtn = document.getElementById("new-register-btn");
    const selectAllCheckbox = document.getElementById("select-all");
    const rowCheckboxes = document.querySelectorAll(".row-checkbox");
    const rows = document.querySelectorAll(".store-menu-table tbody tr");

    // 검색 폼 제출 시 페이지 1로 리셋
    searchForm.addEventListener("submit", function (event) {
        event.preventDefault();
        let url = new URL(window.location.href);
        const searchInput = document.getElementById("search-input").value.trim();

        if (searchInput) {
            url.searchParams.set("search-input", searchInput);
        } else {
            url.searchParams.delete("search-input");
        }

        // 페이지 파라미터 제거 (백엔드에서 page=1로 처리)
        url.searchParams.delete("page");

        console.log("Search URL:", url.toString());
        window.location.href = url;
    });

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

            // 체크박스 자체를 클릭한 경우
            if (target.classList.contains("row-checkbox")) {
                event.stopPropagation();
                return;
            }

            // 체크박스 열(컬럼)을 클릭한 경우
            if (target.closest(".checkbox-column")) {
                const checkbox = target.closest(".checkbox-column").querySelector(".row-checkbox");
                if (checkbox) {
                    checkbox.checked = !checkbox.checked;
                }
                event.stopPropagation();
                return;
            }

            // 체크박스 열이 아닌 경우에만 페이지 이동
            const item_id = row.querySelector("td:nth-child(2)").textContent.trim();
            window.location.href = `/menu/store/menu_info/${item_id}/`;
        });
    });

    // 필터링 기능
    let filters = ["category-filter", "show-filter", "best-filter", "new-filter"];
    filters.forEach(function (filterId) {
        document.getElementById(filterId).addEventListener("input", function () {
            let url = new URL(window.location.href);
            let filterValue = this.value;

            if (filterValue) {
                url.searchParams.set(this.name, filterValue);
            } else {
                url.searchParams.delete(this.name);
            }

            // 필터 변경 시 페이지 1로 리셋, 검색 쿼리 유지
            url.searchParams.set('page', '1');

            console.log("Filter URL:", url.toString());
            window.location.href = url;
        });
    });

    // 페이지네이션 링크 클릭 시 URL 로그
    document.querySelectorAll(".page-link").forEach(link => {
        link.addEventListener("click", function (event) {
            console.log("Pagination URL:", this.href);
        });
    });

    // 메뉴 신규 등록 페이지 이동
    newRegisterBtn.addEventListener("click", function () {
        window.location.href = "/menu/store/menu_add";
    });

    // 삭제 기능
    deleteBtn.addEventListener("click", function () {
        const selectedIds = document.querySelectorAll(".row-checkbox:checked");
        if (selectedIds.length === 0) {
            alert("삭제할 항목을 선택해주세요.");
            return;
        }
        deleteConfirmModal.show();
    });

    // 모달에서 삭제 확인 버튼 클릭 시 삭제 요청 보내기
    confirmDeleteBtn.addEventListener("click", async function () {
        const selectedIds = Array.from(document.querySelectorAll(".row-checkbox:checked"))
            .map(checkbox => checkbox.closest("tr").querySelector("td:nth-child(2)").textContent.trim());

        if (selectedIds.length === 0) {
            alert("삭제할 항목을 선택해주세요.");
            return;
        }

        try {
            const response = await fetch('/menu/store/menu_delete/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({ item_ids: selectedIds }),
            });

            const data = await response.json();
            if (data.success) {
                alert("삭제가 완료되었습니다.");
                window.location.reload();
            } else {
                alert("삭제 실패: " + data.message);
            }
        } catch (error) {
            alert("삭제 중 오류가 발생했습니다.");
        }
    });
});

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}