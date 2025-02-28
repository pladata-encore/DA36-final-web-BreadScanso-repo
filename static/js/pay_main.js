// 설정한 기간 내의 결제 내역이 검색되도록 설정
document.getElementById("date_button").addEventListener("click", function() {
    // 시작일자, 종료일자 가져오기
    let startDate = new Date(document.getElementById("startDate").value);
    let endDate = new Date(document.getElementById("endDate").value);
    // 테이블 가져오기
    let rows = document.querySelectorAll(".table tbody tr");
    // 결제일자 불러오기
    rows.forEach(row => {
        let dateCell = row.querySelector("td:first-child");
        if (dateCell) {
            let purchaseDate = new Date(dateCell.innerText);
            // purchaseDate가 startDate와 endDate 사이인지 확인
            if (purchaseDate >= startDate && purchaseDate <= endDate) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        }
    });
});


// 결제일자 누르면 상세 페이지 - 새탭으로
document.querySelectorAll(".clickable").forEach(cell => {
    cell.addEventListener("click", function () {
        let paymentRow = this.parentElement;
        let paymentId = paymentRow.getAttribute('data-payment-id');
        if (paymentId) {
            let detailPageUrl = `/details/${paymentId}/`;
            window.open(detailPageUrl, "_blank");
        }
    })
    }
)
// 임시로 만들어놓는 '취소' 버튼 클릭 시 이동할 '취소내역 페이지'
document.getElementById("cancel").addEventListener("click", function () {
    window.location.href = "cancel/";
});


// 결제수단 '카드' '간편결제' 중에 선택하면 해당 내역이 나오게 하는 기능 구현 추가 필요. DB 만들어진 뒤에 설정할 예정.
document.querySelectorAll(".dropdown-item").forEach(item => {
item.addEventListener("click", function () {
    const selectedMethod = this.textContent.trim() === "카드" ? "credit" : "epay";
    window.location.href = `?payment_method=${selectedMethod}`;
});
});