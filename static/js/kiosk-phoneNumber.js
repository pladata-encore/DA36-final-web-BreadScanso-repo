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
      alert("입력한 번호 : 010-" + phoneDigits.slice(0, 4).join("") + "-" + phoneDigits.slice(4, 8).join("") + " 로 포인트가 적립됩니다.");
      // 여기에 실제 데이터 전송 로직 추가 가능
}


