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

    // 테이블에 데이터 채우기
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
        const finalAmount = finalPrice || Math.max(totalPrice - usedPoints, 0);
        finalAmountElement.textContent = `${finalAmount.toLocaleString()}원`;
        }

        console.log("최종 결제 금액:", finalAmount);

});