    document.getElementById("date_button").addEventListener("click", function() {
        let startDate = new Date(document.getElementById("startDate").value);
        let endDate = new Date(document.getElementById("endDate").value);
        let rows = document.querySelectorAll(".table tbody tr");

        rows.forEach(row => {
            let dateCell = row.querySelector("td:first-child");
            if (dateCell) {
                let purchaseDate = new Date(dateCell.innerText);
                if (purchaseDate >= startDate && purchaseDate <= endDate) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }
            }
        });
    });

    document.querySelectorAll(".dropdown-item").forEach(item => {
item.addEventListener("click", function () {
    const selectedMethod = this.textContent.trim() === "카드" ? "credit" : "epay";
    window.location.href = `?payment_method=${selectedMethod}`;
});
});