document.addEventListener("DOMContentLoaded", function () {
    const earnedPoints = sessionStorage.getItem("earnedPoints") || "0";
    const finalPoints = sessionStorage.getItem("finalPoints") || "0";
    const phoneNum = sessionStorage.getItem("phone_num") || "";

    // HTML 요소에 값 설정
    document.getElementById("earnedPoints").textContent = earnedPoints;
    document.getElementById("finalPoints").textContent = finalPoints;

    // 비회원인 경우 (전화번호가 없는 경우)
    if (!phoneNum) {
        console.log("비회원 주문입니다. 포인트 적립을 건너뜁니다.");

        // 포인트 관련 요소 숨기기
        const pointParagraphs = document.querySelectorAll("p");
        pointParagraphs.forEach(elem => {
            if (elem.querySelector("#earnedPoints") || elem.querySelector("#finalPoints")) {
                elem.style.display = "none";
            }
        });

        // 비회원용 메시지 출력
        const completedMsg = document.querySelector("h3.mb-3");
        if (completedMsg) {
            const nonMemberMsg = document.createElement("p");
            nonMemberMsg.textContent = "비회원은 포인트가 적립되지 않습니다.";
            nonMemberMsg.style.color = "#888";
            completedMsg.after(nonMemberMsg);
        }

        return;
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
});