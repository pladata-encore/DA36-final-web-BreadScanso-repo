document.addEventListener('DOMContentLoaded', function() {
    // 세션 스토리지에서 데이터 가져오기
    const productDictionary = JSON.parse(sessionStorage.getItem("productDictionary") || "{}");
    const totalQuantity = sessionStorage.getItem("totalQuantity") || 0;
    const totalPrice = parseInt(sessionStorage.getItem("totalPrice") || "0");
    const usedPoints = parseInt(sessionStorage.getItem("usedPoints") || "0");
    const finalPrice = parseInt(sessionStorage.getItem("finalPrice") || "0");

    console.log("세션 스토리지 데이터:", {
        productDictionary,
        totalQuantity,
        totalPrice,
        usedPoints,
        finalPrice
    });

    // 주문 테이블 업데이트
    const orderTable = document.getElementById("order-table");

    // 테이블이 비어있는지 확인
    if (orderTable && Object.keys(productDictionary).length > 0) {
        // 테이블에 데이터 채우기
        orderTable.innerHTML = ''; // 기존 내용 초기화
        Object.keys(productDictionary).forEach(itemName => {
            const product = productDictionary[itemName];
            const row = `
            <tr>
                <td>${product.korName}</td>
                <td>${product.price.toLocaleString()}원</td>
                <td>${product.quantity}</td>
                <td>${product.totalAmount.toLocaleString()}원</td>
            </tr>
            `;
            orderTable.innerHTML += row;
        });

        // 총 수량과 금액 업데이트
        document.getElementById("totalQuantity").textContent = `${totalQuantity}개`;
        document.getElementById("totalPrice").textContent = `${totalPrice.toLocaleString()}원`;

        // 포인트 사용 정보가 있는 경우 표시
        const usedPointsElement = document.getElementById("usedPoints");
        const finalAmountElement = document.getElementById("final_amount");

        if (usedPointsElement && usedPoints > 0) {
            usedPointsElement.textContent = `${usedPoints.toLocaleString()}원`;
        }

        // 최종 결제 금액 표시
        if (finalAmountElement) {
            const finalAmount = finalPrice > 0 ? finalPrice : Math.max(totalPrice - usedPoints, 0);
            finalAmountElement.textContent = `${finalAmount.toLocaleString()}원`;
        }
    } else {
        console.error("주문 테이블을 찾을 수 없거나 상품 데이터가 없습니다.");
        if (orderTable) {
            orderTable.innerHTML = '<tr><td colspan="4">주문 내역이 없습니다.</td></tr>';
        }
    }

    // CSRF 토큰 가져오기 함수
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

    // 결제 버튼 클릭 이벤트 추가
    document.querySelectorAll('.blue-button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            // 세션 스토리지에서 데이터 가져오기
            const productDictionary = JSON.parse(sessionStorage.getItem("productDictionary") || "{}");
            const phoneNum = sessionStorage.getItem("phone_num") || "";
            const finalAmount = parseInt(document.getElementById("final_amount").textContent.replace(/[^0-9]/g, ""));
            const paymentMethod = this.textContent.includes("카드") ? "credit" : "simple";

            // 서버로 전송할 데이터
            const paymentData = {
                phone_num: phoneNum,
                final_amount: finalAmount,
                payment_method: paymentMethod,
                products: productDictionary
            };

            console.log("결제 요청 데이터:", paymentData);

            // 서버에 결제 완료 요청
            fetch("/kiosk/complete_payment/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify(paymentData)
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.message || "서버 오류가 발생했습니다.");
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    window.location.href = "/kiosk/payment_completed/";
                } else {
                    alert("결제 처리 중 오류가 발생했습니다: " + data.message);
                }
            })
            .catch(error => {
                console.error("결제 처리 중 오류:", error);
                alert("결제 처리 중 오류가 발생했습니다: " + error.message);
            });
        });
    });
});