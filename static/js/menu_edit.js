document.addEventListener("DOMContentLoaded", function () {
    const saveBtn = document.getElementById("confirm-save-btn");
    const cancelBtn = document.getElementById("cancel-btn");
    const form = document.querySelector("form");  // 폼 요소 가져오기

    // 저장 버튼 클릭 시 폼 제출
    if (saveBtn) {
        saveBtn.addEventListener("click", function () {
            form.submit();  // 폼을 제출하여 DB에 저장
        });
    }

    // 취소 버튼 클릭 시 menu_info 페이지로 이동
    if (cancelBtn) {
        const itemId = cancelBtn.getAttribute("data-item-id");
        if (itemId) {
            cancelBtn.addEventListener("click", function () {
                window.location.href = `/menu/store/menu_info/${itemId}`;
            });
        }
    }
});
