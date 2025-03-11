document.addEventListener("DOMContentLoaded", function () {
    const confirmBtn = document.getElementById("confirm-guide-btn");
    const guideConfirmModal = new bootstrap.Modal(document.getElementById("guideConfirmModal"));
    const confirmGuideBtn = document.getElementById("confirm-btn");
    const cancelBtn = document.getElementById("cancel-btn");

    // 모달 표시
    confirmBtn.addEventListener("click", function () {
        guideConfirmModal.show();
    });

    // 모달에서 확인 버튼 클릭 시 신규 제품 등록 페이지로 이동
    if(confirmGuideBtn)
        confirmGuideBtn.addEventListener("click", function () {
            const itemId = confirmGuideBtn.getAttribute("data-item-id");  // 버튼의 data-item-id 값 가져오기
            if (itemId) {
                window.location.href = `/menu/store/new_menu_learn/${itemId}`;
            }
    });

    // 취소 버튼
    if (cancelBtn) {
        cancelBtn.addEventListener("click", function () {
            window.location.href = "/menu/store/";
        });
    }
});