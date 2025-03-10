console.log('event_list.js loaded...');

// 검색창
document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");
    const rows = document.querySelectorAll(".table tbody tr");


    searchForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const searchTerm = searchInput.value.toLowerCase();

        rows.forEach(row => {
            const cells = row.querySelectorAll("td");
            let rowText = "";
            cells.forEach(cell => {
                rowText += cell.textContent.toLowerCase();
            });
            row.style.display = rowText.includes(searchTerm) ? "" : "none";
        });
    });
});

// 클릭시 이벤트 상세 페이지로 이동
document.querySelectorAll(".event-card").forEach(card => {
    // 제품 클릭 시 상세 페이지 이동
    card.addEventListener("click", function() {
        const event_id = this.getAttribute("data-id");
        if (event_id) {
            location.href = `/event/event_detail/${event_id}`;
        }
    });

    // hover 효과
    card.addEventListener("mouseenter", function () {
        this.style.transform = "scale(1.1)";
        this.style.zIndex = "10";
        this.style.transition = "transform 0.3s ease-in-out";
    });

    card.addEventListener("mouseleave", function () {
        this.style.transform = "scale(1)";
        this.style.zIndex = "1";
        this.style.transition = "transform 0.3s ease-in-out";
    });
});

