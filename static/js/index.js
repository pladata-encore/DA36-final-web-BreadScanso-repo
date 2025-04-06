// 메인홈 캐러셀
setTimeout(function() {
    let messageBox = document.getElementById("signup-message");
    if (messageBox) {
        messageBox.style.transition = "opacity 0.5s";
        messageBox.style.opacity = "0";
        setTimeout(() => messageBox.remove(), 500);
    }
}, 5000); // 5초 나타나고 사라지게 했음
