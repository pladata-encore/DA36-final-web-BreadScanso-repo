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
    if (phoneDigits.length !== 8) {
        alert("전화번호를 올바르게 입력해주세요.");
        return;
    }

    let phoneNumber = "010" + phoneDigits.join("");  // 하이픈 없이 변환
    console.log("요청할 전화번호:", phoneNumber);

    // 서버로 전화번호 존재 여부 확인 요청
    fetch(`check-phone/?phone_num=${phoneNumber}`)
        .then(response => response.json())
        .then(data => {
            console.log("서버 응답:", data);
            if (data.is_member) {
                alert("입력한 번호 : " + phoneNumber + " 로 포인트가 적립됩니다.");

                console.log("전화번호:", data.phone_num);  // 🔹 회원 전화번호 출력
                console.log("적립금:", data.points);  // 🔹 적립금 출력

                // 📌 sessionStorage에 데이터 저장
                sessionStorage.setItem("phone_num", data.phone_num);
                sessionStorage.setItem("points", data.points);


                window.location.href = "/kiosk/usepoint";
            } else {
                alert("회원이 아닙니다. 비회원은 적립이 불가능합니다. 홈페이지에서 신규 회원가입을 진행해주세요!");
                window.location.href = "/kiosk/payment_method";  // 결제수단 선택 페이지로 이동
            }
        })
        .catch(error => {
            console.error("Error checking phone number:", error);
            alert("서버와 연결할 수 없습니다. 잠시 후 다시 시도해주세요.");
        });
}





