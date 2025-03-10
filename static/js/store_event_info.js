// document.addEventListener("DOMContentLoaded", function () {
//     const deleteBtn = document.getElementById("delete-btn");
//     const deleteConfirmModal = new bootstrap.Modal(document.getElementById("deleteConfirmModal"));
//     const confirmDeleteBtn = document.getElementById("confirm-delete-btn");
//     const editEventBtn = document.getElementById("edit-event-btn");
//     const listBtn = document.getElementById("list-btn");
//
//     // 삭제 버튼 클릭 시 모달 표시
//     deleteBtn.addEventListener("click", function () {
//         deleteConfirmModal.show();
//     });
//
//     // 모달에서 삭제 확인 버튼 클릭 시 삭제 요청 보내기
//     confirmDeleteBtn.addEventListener("click", async function () {
//         try {
//             const eventId = confirmDeleteBtn.getAttribute("data-event-id");
//
//             if (!eventId) {
//                 alert("삭제할 이벤트의 ID를 찾을 수 없습니다.");
//                 return;
//             }
//
//             const response = await fetch('/store/event_delete/', {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                     "X-CSRFToken": getCSRFToken(),
//                 },
//                 body: JSON.stringify({ item_ids: [itemId] }), // 리스트 형태로 전달
//             });
//
//             const data = await response.json();
//
//             if (data.success) {
//                 alert("삭제가 완료되었습니다.");
//                 window.location.href = "/store/store_event/";
//             } else {
//                 alert("삭제 실패: " + (data.message || "알 수 없는 오류 발생"));
//             }
//         } catch (error) {
//             console.error("Error:", error);
//             alert("삭제 중 오류가 발생했습니다.");
//         }
//     });
//
//     // 수정 버튼
//     // if (editEventBtn) {
//     //     editEventBtn.addEventListener("click", function () {
//     //         const eventId = editEventBtn.getAttribute("data-event-id");
//     //         if (eventId) {
//     //             window.location.href = `/store/store_event_edit/${eventId}`;
//     //         }
//     //     });
//     // }
//     if (editEventBtn) {
//     editEventBtn.addEventListener("click", function () {
//         const eventId = editEventBtn.getAttribute("data-event-id");
//         if (eventId) {
//             window.location.href = `/store/store_event_edit/${eventId}`;
//         }
//     });
// }
//
//     // 목록 버튼
//     if (listBtn) {
//         listBtn.addEventListener("click", function () {
//             window.location.href = "/store/store_event/";
//         });
//     }
// });
//
// function getCSRFToken() {
//     return document.querySelector('[name=csrfmiddlewaretoken]').value;
// }

document.addEventListener("DOMContentLoaded", function () {
    const deleteBtn = document.getElementById("delete-btn");
    const deleteConfirmModal = new bootstrap.Modal(document.getElementById("deleteConfirmModal"));
    const confirmDeleteBtn = document.getElementById("confirm-delete-btn");
    const editEventBtn = document.getElementById("edit-event-btn");
    const listBtn = document.getElementById("list-btn");

    // 삭제 버튼 클릭 시 모달 표시
    deleteBtn.addEventListener("click", function () {
        const eventId = deleteBtn.getAttribute("data-event-id");
        if (eventId) {
            confirmDeleteBtn.setAttribute("data-event-id", eventId);
            deleteConfirmModal.show();
        }
    });

    // 모달에서 삭제 확인 버튼 클릭 시 삭제 요청 보내기
    confirmDeleteBtn.addEventListener("click", async function () {
        try {
            const eventId = confirmDeleteBtn.getAttribute("data-event-id");

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
                body: JSON.stringify({ item_ids: [eventId] }), // eventId로 수정
            });

            const data = await response.json();

            if (data.success) {
                alert("삭제가 완료되었습니다.");
                window.location.href = "/store/store_event/";  // 목록 페이지로 이동
            } else {
                alert("삭제 실패: " + (data.message || "알 수 없는 오류 발생"));
            }
        } catch (error) {
            console.error("Error:", error);
            alert("삭제 중 오류가 발생했습니다.");
        }
    });

    // 수정 버튼
    if (editEventBtn) {
        editEventBtn.addEventListener("click", function () {
            const eventId = editEventBtn.getAttribute("data-event-id");
            if (eventId) {
                window.location.href = `/store/store_event_edit/${eventId}`;  // 이벤트 수정 페이지로 이동
            }
        });
    }

    // 목록 버튼
    if (listBtn) {
        listBtn.addEventListener("click", function () {
            window.location.href = "/store/store_event/";  // 목록 페이지로 이동
        });
    }
});

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
