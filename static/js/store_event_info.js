document.addEventListener("DOMContentLoaded", function () {
    const deleteBtn = document.getElementById("delete-btn");
    const deleteConfirmModal = new bootstrap.Modal(document.getElementById("deleteConfirmModal"));
    const confirmDeleteBtn = document.getElementById("confirm-delete-btn");
    const editEventBtn = document.getElementById("edit-event-btn");
    const listBtn = document.getElementById("list-btn");

    // 삭제 버튼 클릭 시 모달 표시
    deleteBtn.addEventListener("click", function () {
        deleteConfirmModal.show();
    });

    // 모달에서 삭제 확인 버튼 클릭 시 삭제 요청 보내기
    confirmDeleteBtn.addEventListener("click", async function () {
        try {
            const itemId = confirmDeleteBtn.getAttribute("data-event-id");

            if (!eventId) {
                alert("삭제할 이벤트의 ID를 찾을 수 없습니다.");
                return;
            }

            const response = await fetch('/store/event_delete/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({ item_ids: [itemId] }), // 리스트 형태로 전달
            });

            const data = await response.json();

            if (data.success) {
                alert("삭제가 완료되었습니다.");
                window.location.href = "/menu/store/";
            } else {
                alert("삭제 실패: " + (data.message || "알 수 없는 오류 발생"));
            }
        } catch (error) {
            console.error("Error:", error);
            alert("삭제 중 오류가 발생했습니다.");
        }
    });

    // 수정 버튼
    if (editMenuBtn) {
        editMenuBtn.addEventListener("click", function () {
            const itemId = editMenuBtn.getAttribute("data-item-id");  // 버튼의 data-item-id 값 가져오기
            if (itemId) {
                window.location.href = `/menu/store/menu_edit/${itemId}`;
            }
        });
    }

    // 목록 버튼
    if (listBtn) {
        listBtn.addEventListener("click", function () {
            window.location.href = "/menu/store/";
        });
    }
});

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}