document.addEventListener("DOMContentLoaded", function () {
    let bestCarouselIndex = 0;
    const track = document.querySelector(".best-carousel-track");
    const items = document.querySelectorAll(".best-carousel-item");
    const totalItems = items.length;
    const visibleItems = 5; // 한 번에 보이는 아이템 수
    const itemWidth = 100 / visibleItems; // 한 장의 이동 폭 (5개씩 보여주기 위해)

    function moveBestCarousel(direction) {
        bestCarouselIndex += direction;

        // 이동 거리 계산
        const moveX = -(bestCarouselIndex * itemWidth);

        // 이동 애니메이션 적용
        track.style.transition = "transform 0.5s ease-in-out";
        track.style.transform = `translateX(${moveX}%)`;

        // 끝까지 가면 처음으로 자연스럽게 이어지게 만들기
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

    // 전역에서 함수 호출 가능하도록 설정
    window.moveBestCarousel = moveBestCarousel;

    // 5초마다 자동 이동
    setInterval(() => moveBestCarousel(1), 5000);

    // 제품 표시 기능
    let displayedProducts = 0;
    const itemsData = Array.from(document.querySelectorAll('.col'));  // 모든 제품 가져오기
    const productGrid = document.getElementById('productGrid');
    const loadMoreBtn = document.getElementById('loadMoreBtn');

    function displayProducts() {
        const productsToShow = itemsData.slice(displayedProducts, displayedProducts + 10);

        productsToShow.forEach(product => {
            product.style.display = 'block';  // 제품 보이게 설정
        });

        displayedProducts += productsToShow.length;

        if (displayedProducts >= itemsData.length) {
            loadMoreBtn.style.display = 'none';  // 모든 제품이 표시되면 버튼 숨김
        }
    }

    // 더보기 버튼 클릭 시 제품 추가 표시
    loadMoreBtn.addEventListener('click', displayProducts);

    // 초기 10개만 보이게 설정
    itemsData.forEach((product, index) => {
        product.style.display = index < 10 ? 'block' : 'none';
    });

    // 카드 및 캐러셀 아이템 클릭 시 상세 페이지로 이동
    document.querySelectorAll(".product-card, .best-carousel-item").forEach(element => {
        element.addEventListener("click", function () {
            const item_id = this.getAttribute("data-id");
            if (item_id) {
                location.href = `/menu/product_detail/${item_id}`;
            }
        });

        // hover 효과 추가
        element.addEventListener("mouseenter", function () {
            this.style.transform = "scale(1.05)";
            this.style.zIndex = "10";
            this.style.position = "relative";
            this.style.boxShadow = "0px 4px 10px rgba(0, 0, 0, 0.2)";
        });

        element.addEventListener("mouseleave", function () {
            this.style.transform = "scale(1)";
            this.style.zIndex = "1";
            this.style.boxShadow = "none";
        });
    });

    // 캐러셀 내부의 이미지 클릭 시에도 부모의 data-id로 이동 가능하게 수정
    document.querySelectorAll(".best-carousel-item img").forEach(img => {
        img.addEventListener("click", function () {
            const parent = this.closest(".best-carousel-item");
            const item_id = parent.getAttribute("data-id");

            if (item_id) {
                location.href = `/menu/product_detail/${item_id}`;
            }
        });
    });
});

