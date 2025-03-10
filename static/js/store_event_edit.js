document.addEventListener("DOMContentLoaded", function () {
    const saveBtn = document.getElementById("confirm-save-btn"); // 모달의 "확인" 버튼
    const cancelBtn = document.getElementById("cancel-btn");
    const form = document.querySelector("form"); // 폼 요소 가져오기
    const eventId = cancelBtn.getAttribute("data-event-id"); // i

    // 모달의 "확인" 버튼 클릭 시 폼 제출
    if (saveBtn) {
        saveBtn.addEventListener("click", function () {
            form.submit(); // 기본 폼 제출로 백엔드에 데이터 전송
        });
    }

    // 취소 버튼 클릭 시 시스템설정-이벤트 페이지로 이동
    if (cancelBtn) {
        cancelBtn.addEventListener("click", function () {
            window.location.href = `/store/store_event/${eventId}`;
        });
    }
});