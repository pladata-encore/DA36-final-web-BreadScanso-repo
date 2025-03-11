    document.addEventListener('DOMContentLoaded', function() {
        // 세션 스토리지에서 데이터 가져오기
        const productDictionary = JSON.parse(sessionStorage.getItem("productDictionary") || "{}");
        const totalQuantity = parseNumber(sessionStorage.getItem("totalQuantity") || "0");
        const usedPoints = parseNumber(sessionStorage.getItem("usedPoints") || "0");
        const totalAmount = parseNumber(sessionStorage.getItem("totalAmount") || "0");
        // 비회원주문시 finalAmount를 totalAmount로 설정
        let finalAmount = parseNumber(sessionStorage.getItem("finalAmount") || "0");
        if (finalAmount === 0 && totalAmount > 0) {
            finalAmount = totalAmount;
    }

    console.log("제품 딕셔너리 전체 내용:", productDictionary);
    Object.keys(productDictionary).forEach(key => {
        console.log(`제품 ${key}의 item_id:`, productDictionary[key].item_id);
    });

        function parseNumber(text) {
            if (typeof text !== 'string') return parseInt(text) || 0;
            return parseInt(text.replace(/,/g, ""), 10) || 0;
        }

        // 주문 테이블 업데이트
        const orderTable = document.getElementById("order-table");
        if (orderTable && Object.keys(productDictionary).length > 0) {
            orderTable.innerHTML = ''; // 기존 내용 초기화
            Object.keys(productDictionary).forEach(itemName => {
                const product = productDictionary[itemName];
                const row = `
                <tr>
                    <td>${product.korName}</td>
                    <td>${product.price.toLocaleString()}원</td>
                    <td>${product.quantity}</td>
                    <td>${product.totalPrice.toLocaleString()}원</td>
                </tr>
                `;
                orderTable.innerHTML += row;
            });

            document.getElementById("totalQuantity").textContent = `${totalQuantity}개`;
            document.getElementById("totalAmount").textContent = `${totalAmount.toLocaleString()}원`;

            const usedPointsElement = document.getElementById("usedPoints");
            const finalAmountElement = document.getElementById("finalAmount");

            if (usedPointsElement && usedPoints > 0) {
                usedPointsElement.textContent = `${usedPoints.toLocaleString()}원`;
            }

            if (finalAmountElement) {
                const finalAmount_ = finalAmount > 0 ? finalAmount : Math.max(totalAmount - usedPoints, 0);
                finalAmountElement.textContent = `${finalAmount_.toLocaleString()}원`;
            }
        } else {
            console.error("주문 테이블을 찾을 수 없거나 상품 데이터가 없습니다.");
            if (orderTable) {
                orderTable.innerHTML = '<tr><td colspan="4">주문 내역이 없습니다.</td></tr>';
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

        // 결제 버튼 클릭 이벤트
        document.querySelectorAll('.sandybrown-button').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                // db 업데이트 후 다음 페이지로 넘어가도록 수정
                if (e.currentTarget.parentElement.tagName === 'A') {
                    e.currentTarget.parentElement.onclick = function(e) {
                        e.preventDefault();
                        return false;
                    };
                }

                // 1. 세션 스토리지에서 데이터 가져오기
                const phoneNum = sessionStorage.getItem("phone_num") || "";
                const points = parseNumber(sessionStorage.getItem("points") || "0");
                const usedPoints = parseNumber(sessionStorage.getItem("usedPoints") || "0");
                // 2. earnedPoints와 finalPoints 미리 계산
                const earnedPoints = Math.floor(finalAmount * parseFloat(earningRate));
                const finalPoints = points + earnedPoints - usedPoints;
                console.log(points, earnedPoints, usedPoints, finalPoints);
                // earnedPoints 세션에 저장
                sessionStorage.setItem("earnedPoints", earnedPoints);
                // finalPoints 세션에 저장
                sessionStorage.setItem("finalPoints", finalPoints);

                // 3. 서버로 보낼 데이터 구성 (fetch 요청 전에 미리 만듦)
                const paymentData = {
                    phone_num: phoneNum,
                    final_amount: finalAmount,
                    used_points: usedPoints,
                    earned_points: earnedPoints,
                    points: finalPoints,
                    products: productDictionary,
                    total_count: totalQuantity,
                    payment_method: button.textContent.includes("간편") ? "epay" : "credit"
                };

                console.log("결제 요청 데이터:", paymentData);


                // 4. 서버에 결제 완료 요청
                fetch("/kiosk/complete_payment/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCSRFToken()  // CSRF 토큰이 제대로 넘어가고 있는지 확인
                    },
                    body: JSON.stringify(paymentData)  // paymentData가 올바르게 전송되고 있는지 확인
                })
                .then(response => {
                    console.log("서버 응답 상태:", response.status);  // 서버 응답 상태 코드 출력

                    if (!response.ok) {
                        console.log("응답이 OK가 아님. 서버 에러 발생");  // 응답이 성공적이지 않을 때
                        return response.json().then(data => {
                            console.error("서버에서 반환된 에러 메시지:", data.message);
                            throw new Error(data.message || "서버 오류가 발생했습니다.");
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("서버에서 받은 응답 데이터:", data);  // 서버로부터 받은 응답 데이터를 출력

                    if (data.success) {
                        console.log("결제 완료! payment_completed 페이지로 리디렉션");  // 결제 성공 시
                        window.location.href = "/kiosk/payment_completed/";
                    } else {
                        console.log("결제 실패. 메시지:", data.message);  // 결제 실패 시
                        alert("결제 처리 중 오류가 발생했습니다: " + data.message);
                    }
                })
                .catch(error => {
                    console.error("결제 처리 중 오류:", error);  // 에러 발생 시 출력
                    alert("결제 처리 중 오류가 발생했습니다: " + error.message);
                });
            });
        });
    });
