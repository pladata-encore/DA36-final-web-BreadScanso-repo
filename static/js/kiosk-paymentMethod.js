const use_points = sessionStorage.getItem("use_points");  // 사용한 적립금 가져오기
    console.log("사용한 포인트:", use_points);  // 콘솔 확인
    if (use_points) {
        document.getElementById("use_points").textContent = parseInt(use_points).toLocaleString();
    }