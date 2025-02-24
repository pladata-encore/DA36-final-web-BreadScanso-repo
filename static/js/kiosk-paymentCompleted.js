document.addEventListener("DOMContentLoaded", function () {
    let earnedPointsElem = document.getElementById("earned_point");
    let finalPointElem = document.getElementById("final_point");

    function parseNumber(text) {
        return parseInt(text.replace(/,/g, ""), 10) || 0;
    }

    function updatePoints() {
        const finalAmount = sessionStorage.getItem("final_amount");
        const points = parseNumber(sessionStorage.getItem("points") || "0");
        const usePoints = parseNumber(sessionStorage.getItem("use_points") || "0");
        const phoneNum = sessionStorage.getItem("phone_num"); // 회원 전화번호 가져오기

        // 핸드폰 번호가 0이 아니면 회원으로 간주
        if (phoneNum !== "0" && phoneNum !== null) {
            document.getElementById("points-section").style.display = "block";
            document.getElementById("final-points").style.display = "block";
        } else {
            document.getElementById("points-section").style.display = "none";
            document.getElementById("final-points").style.display = "none";
        }

        console.log("최종 결제 금액:", finalAmount);
        console.log("기존 보유 포인트:", points);
        console.log("사용한 포인트:", usePoints);
        console.log("전화번호:", phoneNum);

        let remainingPoints = points - usePoints;
        let earnedPoints = finalAmount ? Math.floor(finalAmount * 0.05) : 0;
        let finalPoints = remainingPoints + earnedPoints;

        earnedPointsElem.textContent = earnedPoints.toLocaleString();
        finalPointElem.textContent = finalPoints.toLocaleString();

        console.log("적립된 포인트:", earnedPoints);
        console.log("최종 보유 포인트:", finalPoints);

        // 서버에 최종 보유 포인트 업데이트 요청
        if (phoneNum) {
            fetch("/kiosk/update_points/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({
                    phone_num: phoneNum,
                    final_points: finalPoints,
                }),
            })
            .then(response => response.json())
            .then(data => {
                console.log("포인트 업데이트 응답:", data);
                if (data.success) {
                    alert("포인트가 정상적으로 적립되었습니다.");
                } else {
                    alert("포인트 업데이트 실패: " + data.message);
                }
            })
            .catch(error => {
                console.error("포인트 업데이트 중 오류 발생:", error);
                alert("서버 오류로 인해 포인트 업데이트에 실패했습니다.");
            });
        }
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

