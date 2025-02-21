let phoneDigits = [];

function updateDisplay() {
    let formattedNumber = "010-";
    if (phoneDigits.length > 0) {
        formattedNumber += phoneDigits.slice(0, 4).join("");
    }
    if (phoneDigits.length > 4) {
        formattedNumber += "-" + phoneDigits.slice(4, 8).join("");
    }
    document.getElementById("phone-number").innerText = formattedNumber.padEnd(12, "_");
}

function addNumber(num) {
    if (phoneDigits.length < 8) {
        phoneDigits.push(num);
        updateDisplay();
    }
}

function deleteLast() {
    phoneDigits.pop();
    updateDisplay();
}

function clearNumber() {
    phoneDigits = [];
    updateDisplay();
}


function confirm() {
    if (phoneDigits.length < 8) {
        alert("번호를 완성해주세요.");
        return;
    }

    let phoneNumber = "010" + phoneDigits.join("");  // 하이픈 없이 변환
    console.log("요청할 전화번호:", phoneNumber);  // 요청할 전화번호 출력

    // 서버로 전화번호 존재 여부 확인 요청
    fetch(`check-phone/?phone_num=${phoneNumber}`)
        .then(response => response.json())
        .then(data => {
            console.log("서버 응답:", data);  // 서버 응답 확인
            if (data.is_member) {
                alert("입력한 번호 : " + phoneNumber + " 로 포인트가 적립됩니다.");
                window.location.href = "/kiosk/usepoint";  // 포인트 사용 페이지로 이동
            } else {
                alert("회원이 아닙니다.");
            }
        })
        .catch(error => {
            console.error("Error checking phone number:", error);  // 에러 메시지 확인
        });
}




