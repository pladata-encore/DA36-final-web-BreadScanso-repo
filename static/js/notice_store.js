document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");
    const deleteBtn = document.getElementById("delete-btn");
    const finalConfirmButton = document.getElementById("finalConfirmButton");
    const deleteConfirmModal = new bootstrap.Modal(document.getElementById("deleteConfirmModal"));
    const newRegisterBtn = document.getElementById("new-register-btn");
    const selectAllCheckbox = document.getElementById("select-all");
    const rowCheckboxes = document.querySelectorAll(".row-checkbox");
    const rows = document.querySelectorAll(".store-notice-table tbody tr");

    // 전체 선택 체크박스 변경
    selectAllCheckbox.addEventListener("change", function () {
        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });
    });

    // 검색 기능
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
        window.location.href = "/notice/store/notice_write";
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
    finalConfirmButton.addEventListener("click", async function () {
        const selectedIds = Array.from(document.querySelectorAll(".row-checkbox:checked"))
            .map(checkbox => checkbox.closest("tr").querySelector(".notice-title").getAttribute("data-notice-id"));

        if (selectedIds.length === 0) {
            alert("삭제할 항목을 선택해주세요.");
            return;
        }

        // 요청 데이터 디버깅
        const requestData = { notice_ids: selectedIds };
        console.log("전송할 데이터:", JSON.stringify(requestData));

        try {
            const response = await fetch('/notice/store/notice_delete/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(), // CSRF 토큰 확인
                },
                body: JSON.stringify(requestData) // JSON 직렬화 확인
            });

            // 응답 디버깅
            const text = await response.text();
            console.log("서버 응답:", text);

            const data = JSON.parse(text);
            if (data.success) {
                alert("삭제가 완료되었습니다.");
                window.location.reload();
            } else {
                alert("삭제 실패: " + data.message);
            }
        } catch (error) {
            alert("삭제 중 오류가 발생했습니다: " + error.message);
            console.error("에러 상세:", error);
        } finally {
            deleteConfirmModal.hide(); // 모달 닫기
        }
    });
});

function getCSRFToken() {
    const tokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!tokenElement) {
        console.error("CSRF 토큰을 찾을 수 없습니다.");
        return "";
    }
    return tokenElement.value;
}