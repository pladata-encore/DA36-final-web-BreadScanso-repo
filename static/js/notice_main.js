document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");

    // 모든 제목 열에 클릭 이벤트 추가
    const titles = document.querySelectorAll('.notice-title');
    titles.forEach(title => {
        title.addEventListener('click', function() {
            const noticeId = this.getAttribute('data-notice-id');
            // Django URL 패턴에 맞게 notice_detail 페이지로 이동
            window.location.href = `/notice/${noticeId}/`;
        });
    });

    // 검색 기능: 제목만 검색
    searchForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const searchTerm = searchInput.value.toLowerCase().trim();
        const rows = document.querySelectorAll('tbody tr');

        rows.forEach(row => {
            const titleCell = row.querySelector('.notice-title');
            const titleText = titleCell.textContent.toLowerCase();
            row.style.display = titleText.includes(searchTerm) ? "" : "none";
        });
    });
});