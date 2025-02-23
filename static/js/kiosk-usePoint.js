document.addEventListener("DOMContentLoaded", function () {
    let inputField = document.getElementById("points-input");
    let minPoints = parseInt(document.getElementById("min-points").innerText);
    let maxPrice = parseInt(document.getElementById("max-price").innerText.replace(/,/g, ""), 10);

    const points = sessionStorage.getItem("points");  // 저장된 적립금 가져오기
    console.log("세션 저장된 포인트:", points);  // 콘솔 확인

    if (points) {
        document.getElementById("points").textContent = parseInt(points).toLocaleString();
    }

    // 최대 사용 가능한 적립금 계산 (결제 금액 또는 보유 포인트 중 적은 값을 선택)
    let maxPoints = Math.min(parseInt(points) || 0, maxPrice);
    console.log("사용 가능한 최대 포인트:", maxPoints);  // 콘솔 확인
    document.getElementById("max-points").textContent = formatNumber(maxPoints);


    function addNumber(num) {
        let currentValue = inputField.value.replace(/,/g, ""); // 쉼표 제거
        if (currentValue === "0") currentValue = ""; // 처음 입력 시 0 제거
        let newValue = currentValue + num; // 숫자 추가
        inputField.value = formatNumber(newValue); // 천 단위 쉼표 적용
    }

    function clearInput() {
        inputField.value = "0"; // 전체 삭제 후 0으로 설정
    }

    function deleteLast() {
        let currentValue = inputField.value.replace(/,/g, ""); // 쉼표 제거
        if (currentValue.length > 1) {
            inputField.value = formatNumber(currentValue.slice(0, -1)); // 마지막 숫자 삭제
        } else {
            inputField.value = "0"; // 값이 한 자리만 남았다면 0으로 초기화
        }
    }

    function formatNumber(num) {
        return num ? parseInt(num).toLocaleString() : "0"; // 빈 값이면 0으로 처리
    }

    function confirmPoints() {
        let inputPoints = parseInt(inputField.value.replace(/,/g, "")); // 입력 값 (쉼표 제거)
        sessionStorage.setItem("use_points", inputPoints);

        if (inputPoints < minPoints) {
            alert(`최소 사용 포인트는 ${minPoints}P 입니다.`);
            return;
        } else if (inputPoints > maxPoints) {
            alert(`사용 가능한 포인트를 초과했습니다. 최대 사용 가능 포인트는 ${maxPoints}P입니다.`);
            return;
        } else if (inputPoints > maxPrice) {
            alert(`결제 금액을 초과했습니다.`);
            return;
        } else {
            alert(`${inputPoints}P를 사용합니다.`);
            window.location.href = "/kiosk/payment_method";
        }
    }

    // 전역에서 사용 가능하도록 함수 등록
    window.addNumber = addNumber;
    window.clearInput = clearInput;
    window.deleteLast = deleteLast;
    window.confirmPoints = confirmPoints;
});