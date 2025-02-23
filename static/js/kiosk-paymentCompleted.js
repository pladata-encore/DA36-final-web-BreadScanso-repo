document.addEventListener("DOMContentLoaded", function () {
    let earnedPointsElem = document.getElementById("earned_point"); // 적립된 포인트 요소
    let finalPointElem = document.getElementById("final_point"); // 보유 포인트 요소

    // 숫자 변환 함수 (쉼표 제거 후 정수 변환)
    function parseNumber(text) {
        return parseInt(text.replace(/,/g, ""), 10) || 0;
    }

    function updatePoints() {
        const finalAmount = sessionStorage.getItem("final_amount");  // 최종 결제 금액 가져오기
        const points = sessionStorage.getItem("points"); // 기존 보유 포인트 가져오기
        const use_points = sessionStorage.getItem("use_points"); // 사용한 포인트 가져오기

        console.log("최종 결제 금액:", finalAmount);
        console.log("기존 보유 포인트:", points);
        console.log("사용한 포인트:", use_points);

        let remainingPoints = points - use_points;
        console.log("사용후 남은 포인트:", remainingPoints);

        let earnedPoints = 0;
        if (finalAmount) {
            earnedPoints = Math.floor(finalAmount * 0.05); // 적립 포인트 계산 (5%)
            earnedPointsElem.textContent = earnedPoints.toLocaleString(); // 천 단위 쉼표 적용
            console.log("적립된 포인트:", earnedPoints);
        }

        // 사용후 남은 포인트 + 적립 포인트 = 새로운 보유 포인트
        let finalPoints = remainingPoints + earnedPoints;
        finalPointElem.textContent = finalPoints.toLocaleString(); // 천 단위 쉼표 적용
        console.log("최종 보유 포인트:", finalPoints);
    }

    // 페이지 로드 시 자동 업데이트
    updatePoints();
});

