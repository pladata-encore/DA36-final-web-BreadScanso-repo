document.addEventListener("DOMContentLoaded", function () {
    let totalAmountElem = document.getElementById("total_amount"); // 총 금액 요소
    let finalAmountElem = document.getElementById("final_amount"); // 최종 결제 금액 요소

    const use_points = sessionStorage.getItem("use_points");  // 사용한 적립금 가져오기
    console.log("사용한 포인트:", use_points);  // 콘솔 확인
    if (use_points) {
        document.getElementById("use_points").textContent = parseInt(use_points).toLocaleString();
    }


    // 숫자 변환 함수 (쉼표 제거 후 정수 변환)
    function parseNumber(text) {
        return parseInt(text.replace(/,/g, ""), 10) || 0;
    }

    function updateFinalAmount() {
        let totalAmount = parseNumber(totalAmountElem.textContent);
        console.log("총 결제 금액:", totalAmount);  // 콘솔 확인

        let finalAmount = Math.max(totalAmount - use_points, 0); // 음수 방지
        finalAmountElem.textContent = finalAmount.toLocaleString(); // 천 단위 쉼표 적용
        sessionStorage.setItem("final_amount", finalAmount);
        console.log("최종 결제 금액:", finalAmount);  // 콘솔 확인

    }

    // 페이지 로드 시 자동 업데이트
    updateFinalAmount();
});

