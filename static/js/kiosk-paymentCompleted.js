document.addEventListener("DOMContentLoaded", function () {
    let earnedPointsElem = document.getElementById("earnedPoints");
    let finalPointsElem = document.getElementById("finalPoints");

    // 세션 스토리지의 모든 키 출력 (디버깅용)
    console.log("세션 스토리지 내용:");
    for (let i = 0; i < sessionStorage.length; i++) {
        const key = sessionStorage.key(i);
        console.log(`${key}: ${sessionStorage.getItem(key)}`);
    }

    // 세션 스토리지에서 회원 전화번호 가져오기
    const phoneNum = sessionStorage.getItem("phone_num") || "";

    // 비회원인 경우 (전화번호가 없는 경우)
    if (!phoneNum) {
        console.log("비회원 주문입니다. 포인트 적립을 건너뜁니다.");

        // 포인트 관련 요소 숨기기
        const pointElements = document.querySelectorAll("p:has(#earnedPoints), p:has(#finalPoints)");
        pointElements.forEach(elem => {
            elem.style.display = "none";
        });

        // 비회원 메시지 추가
        const completedMsg = document.querySelector("h3.mb-3");
        if (completedMsg) {
            const nonMemberMsg = document.createElement("p");
            nonMemberMsg.textContent = "비회원은 포인트가 적립되지 않습니다.";
            nonMemberMsg.style.color = "#888";
            completedMsg.after(nonMemberMsg);
        }

        return; // 함수 종료
    }

    function parseNumber(text) {
        if (typeof text !== 'string') return parseInt(text) || 0;
        return parseInt(text.replace(/,/g, ""), 10) || 0;
    }

function updatePoints() {
    // 세션 스토리지에서 데이터 가져오기
    const totalPrice = parseNumber(sessionStorage.getItem("totalPrice") || "0");
    const finalPrice = parseNumber(sessionStorage.getItem("finalPrice") || "0");
    const usedPoints = parseNumber(sessionStorage.getItem("usedPoints") || "0");
    const points = parseNumber(sessionStorage.getItem("points") || "0");
    // 서버에서 계산된 적립 포인트 가져오기
    const earnedPoints = parseNumber(sessionStorage.getItem("earnedPoints") || "0");

    // 최종 결제 금액 계산 (finalPrice가 없으면 totalPrice - usedPoints 사용)
    const finalAmount = finalPrice || Math.max(totalPrice - usedPoints, 0);

    console.log("최종 결제 금액:", finalAmount);
    console.log("기존 보유 포인트:", points);
    console.log("사용한 포인트:", usedPoints);
    console.log("적립된 포인트:", earnedPoints);
    console.log("전화번호:", phoneNum);

    // 최종 보유 포인트 계산
    let remainingPoints = points - usedPoints;
    let finalPoints = remainingPoints + earnedPoints;

    // HTML 요소 업데이트
    if (earnedPointsElem) earnedPointsElem.textContent = earnedPoints.toLocaleString();
    if (finalPointsElem) finalPointsElem.textContent = finalPoints.toLocaleString();

    // 서버에 최종 보유 포인트 업데이트 요청
    fetch("/kiosk/update_points/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({
            phone_num: phoneNum,
            final_points: finalPoints,
            final_amount: finalAmount  // 최종 결제 금액 추가
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("포인트 업데이트 응답:", data);
        if (data.success) {
            console.log("포인트가 정상적으로 적립되었습니다.");
        } else {
            console.error("포인트 업데이트 실패:", data.message);
        }
    })
    .catch(error => {
        console.error("포인트 업데이트 중 오류 발생:", error);
    });
}

    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            document.cookie.split(";").forEach(cookie => {
                let [name, value] = cookie.trim().split("=");
                if (name === "csrftoken") {
                    cookieValue = decodeURIComponent(value);
                }
            });
        }
        return cookieValue;
    }

    updatePoints();
});