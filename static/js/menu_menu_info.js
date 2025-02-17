document.addEventListener("DOMContentLoaded", function () {
    const cancelBtn = document.getElementById("cancel-btn");
    const editMenuBtn = document.getElementById("edit-menu-btn");
    const listBtn = document.getElementById("list-btn");

    // 삭제 버튼
    if (cancelBtn) {
        cancelBtn.addEventListener("click", function () {
            window.location.href = "/menu/store/";
        });
    }

    // 수정 버튼
    if (editMenuBtn) {
        editMenuBtn.addEventListener("click", function () {
            window.location.href = "/menu/store/menu_edit";
        });
    }

    // 목록 버튼
    if (listBtn) {
        listBtn.addEventListener("click", function () {
            window.location.href = "/menu/store/";
        });
    }
});
