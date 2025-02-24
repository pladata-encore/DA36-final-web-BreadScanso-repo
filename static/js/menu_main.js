document.addEventListener("DOMContentLoaded", function () {
    let bestCarouselIndex = 0;
    const track = document.querySelector(".best-carousel-track");
    const items = document.querySelectorAll(".best-carousel-item");
    const totalItems = items.length;
    const visibleItems = 5; // 한 번에 보이는 아이템 수
    const itemWidth = 100 / visibleItems; // 한 장의 이동 폭 (5개씩 보여주기 위해)
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");

    function moveBestCarousel(direction) {
        bestCarouselIndex += direction;
        const moveX = -(bestCarouselIndex * itemWidth);
        track.style.transition = "transform 0.5s ease-in-out";
        track.style.transform = `translateX(${moveX}%)`;

        setTimeout(() => {
            if (bestCarouselIndex >= totalItems - visibleItems) {
                const firstItem = track.firstElementChild;
                track.appendChild(firstItem);
                bestCarouselIndex--;
                track.style.transition = "none";
                track.style.transform = `translateX(${-(bestCarouselIndex * itemWidth)}%)`;
            } else if (bestCarouselIndex < 0) {
                const lastItem = track.lastElementChild;
                track.prepend(lastItem);
                bestCarouselIndex++;
                track.style.transition = "none";
                track.style.transform = `translateX(${-(bestCarouselIndex * itemWidth)}%)`;
            }
        }, 500);
    }

    window.moveBestCarousel = moveBestCarousel;
    setInterval(() => moveBestCarousel(1), 5000);

    // 제품 표시 기능
    let displayedProducts = 0;
    const itemsData = Array.from(document.querySelectorAll('.col'));
    const productGrid = document.getElementById('productGrid');
    const loadMoreBtn = document.getElementById('loadMoreBtn');

    function displayProducts() {
        const productsToShow = itemsData.slice(displayedProducts, displayedProducts + 10);
        productsToShow.forEach(product => {
            product.style.display = 'block';
        });

        displayedProducts += productsToShow.length;
        if (displayedProducts >= itemsData.length) {
            loadMoreBtn.style.display = 'none';
        }
    }

    loadMoreBtn.addEventListener('click', displayProducts);
    itemsData.forEach((product, index) => {
        product.style.display = index < 10 ? 'block' : 'none';
    });

    document.querySelectorAll(".product-card, .best-carousel-item").forEach(element => {
        element.addEventListener("click", function () {
            const item_id = this.getAttribute("data-id");
            if (item_id) {
                location.href = `/menu/product_detail/${item_id}`;
            }
        });

        element.addEventListener("mouseenter", function () {
            this.style.transform = "scale(1.05)";
            this.style.zIndex = "10";
            this.style.position = "relative";
        });

        element.addEventListener("mouseleave", function () {
            this.style.transform = "scale(1)";
            this.style.zIndex = "1";
            this.style.boxShadow = "none";
        });
    });

    document.querySelectorAll(".best-carousel-item img").forEach(img => {
        img.addEventListener("click", function () {
            const parent = this.closest(".best-carousel-item");
            const item_id = parent.getAttribute("data-id");

            if (item_id) {
                location.href = `/menu/product_detail/${item_id}`;
            }
        });
    });

    searchForm.addEventListener("submit", function (event) {
        event.preventDefault(); // 폼 전송 방지
        const searchTerm = searchInput.value.trim().toLowerCase();

        let found = false; // 검색 결과가 있는지 확인하는 변수

        itemsData.forEach(product => {
            const productName = product.querySelector(".card-title").textContent.trim().toLowerCase();

            if (productName.includes(searchTerm)) {
                product.style.display = "block"; // 검색어가 포함된 경우 표시
                found = true;
            } else {
                product.style.display = "none"; // 포함되지 않으면 숨김
            }
        });

        // 검색 결과가 없으면 메시지 표시
        if (!found) {
            productGrid.innerHTML = `<div class="text-center mt-3"><strong>검색 결과가 없습니다.</strong></div>`;
        }

        // 검색 후 '더보기' 버튼 숨기기
        loadMoreBtn.style.display = "none";
    });
});
