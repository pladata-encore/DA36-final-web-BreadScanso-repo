document.addEventListener("DOMContentLoaded", function () {
    let inputField = document.getElementById("points-input");
    let minPoints = parseInt(document.getElementById("min-points").innerText);
    let maxPoints = parseInt(document.getElementById("max-points").innerText.replace(/,/g, ""), 10);
    let maxPrice = parseInt(document.getElementById("max-price").innerText.replace(/,/g, ""), 10);

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

        if (inputPoints < minPoints) {
            alert(`최소 사용 포인트는 ${minPoints}P 입니다.`);
            return;
        } else if (inputPoints > maxPoints) {
            alert(`사용 가능한 포인트를 초과했습니다.`);
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