document.addEventListener('DOMContentLoaded', function() {

    // console.log('DOMContentLoaded@kiosk-usePoint.js totalAmount:', totalAmount);
    // 세션 스토리지에서 데이터 가져오기
    const totalPrice = parseInt(sessionStorage.getItem("totalPrice") || "0");
    const totalAmount = parseInt(sessionStorage.getItem("totalAmount") || "0");
    const memberPoints = parseInt(sessionStorage.getItem("points") || "0");
    const phoneNum = sessionStorage.getItem("phone_num") || "";
    
    // 회원 정보가 없으면 회원 확인 페이지로 리다이렉트
    if (!phoneNum) {
        alert("회원 정보가 없습니다. 회원 확인 페이지로 이동합니다.");
        window.location.href = "/kiosk/phonenumber/";
        return;
    }
    
    // 페이지에 정보 표시
    const $totalAmount = document.getElementById('totalAmount');
    $totalAmount.textContent = totalAmount.toLocaleString();
    document.getElementById('points').textContent = memberPoints.toLocaleString();
    
    // 최대 사용 가능 포인트 계산 (총 결제 금액과 보유 포인트 중 작은 값)
    const maxPoints = Math.min(memberPoints, totalAmount);
    document.getElementById('max-points').textContent = maxPoints.toLocaleString();
    
    console.log("세션 저장된 포인트:", memberPoints);
    console.log("사용 가능한 최대 포인트:", maxPoints);
    
    // 최소 사용 포인트
    const minPoints = parseInt(document.getElementById('min-points').textContent.replace(/,/g, ''), 10) || 1000;
});

// 키패드 숫자 추가 함수
function addNumber(num) {
    const input = document.getElementById('points-input');
    const currentValue = input.value.replace(/,/g, '');
    
    // 첫 입력이거나 현재 값이 0인 경우 대체, 아니면 추가
    if (currentValue === '0') {
        input.value = num.toString();
    } else {
        input.value = (currentValue + num).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
}

// 입력 초기화 함수
function clearInput() {
    document.getElementById('points-input').value = '0';
}

// 마지막 숫자 삭제 함수
function deleteLast() {
    const input = document.getElementById('points-input');
    const currentValue = input.value.replace(/,/g, '');
    
    if (currentValue.length <= 1) {
        input.value = '0';
    } else {
        input.value = currentValue.slice(0, -1).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
}

// 포인트 사용 확인 함수
function confirmPoints(usePoints = false) {
    console.log("포인트 사용 여부:", usePoints);

    const pointsInput = parseInt(document.getElementById('points-input').value.replace(/,/g, ''));
    const memberPoints = parseInt(sessionStorage.getItem("points") || "0");
    const totalAmount = parseInt(sessionStorage.getItem("totalAmount") || "0");
    const maxPoints = parseInt(document.getElementById('max-points').textContent.replace(/,/g, ''));
    const minPoints = parseInt(document.getElementById('min-points').textContent.replace(/,/g, ''));
    
    sessionStorage.setItem("usedPoints", 0); // 기본값
    
    if(usePoints){

        // 입력값 검증
        if (isNaN(pointsInput) || pointsInput < minPoints) {
            alert(`최소 ${minPoints.toLocaleString()}P 이상 사용해야 합니다.`);
            return;
        }

        if (pointsInput > maxPoints) {
            alert(`최대 ${maxPoints.toLocaleString()}P까지만 사용 가능합니다.`);
            return;
        }

        if (pointsInput > totalAmount) {
            alert(`결제 금액을 초과했습니다.`);
            return;
        }
        // 사용할 포인트 세션 스토리지에 저장
        sessionStorage.setItem("usedPoints", pointsInput.toString());
    }
    
    
    // 최종 결제 금액 계산 (주문 총액 - 사용 포인트)
    const finalAmount = totalAmount - pointsInput;
    console.log("최종 결제 금액:", finalAmount);
    sessionStorage.setItem("finalAmount", finalAmount.toString());
    console.log(sessionStorage.getItem("finalAmount"));
    
    alert(`${pointsInput.toLocaleString()}P를 사용합니다.`);
    
    // 결제 방식 선택 페이지로 이동
    window.location.href = "/kiosk/payment_method/";
}