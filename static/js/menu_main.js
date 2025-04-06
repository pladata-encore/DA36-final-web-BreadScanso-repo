document.addEventListener("DOMContentLoaded", function () {
    // 매장 선택 여부 확인
    const storeSelected = document.getElementById('selectStore')?.value;
    const storeSelect = document.getElementById('storeSelect')?.value;
    const isStoreSelected = storeSelected || storeSelect;

    // 캐러셀 초기화
    if (!isStoreSelected) {
        setupCarousel(".new-carousel-track", ".new-carousel-btn", ".new-carousel-item");
        setupCarousel(".product-carousel-track", ".product-carousel-btn", ".product-carousel-item");
    } else {
        setupCarousel(".best-carousel-track", ".best-carousel-btn", ".best-carousel-item");
        setupLoadMore();
    }

    // 제품 클릭 및 호버 이벤트
    document.querySelectorAll(".new-carousel-item, .product-carousel-item, .best-carousel-item, .product-card").forEach(element => {
        element.addEventListener("click", function() {
            const item_id = this.getAttribute("data-id");
            if (item_id) location.href = `/menu/product_detail/${item_id}`;
        });
        element.addEventListener("mouseenter", function () {
            this.style.transform = "scale(1.05)";
            this.style.zIndex = "10";
            this.style.transition = "transform 0.3s ease-in-out";
        });
        element.addEventListener("mouseleave", function () {
            this.style.transform = "scale(1)";
            this.style.zIndex = "1";
            this.style.transition = "transform 0.3s ease-in-out";
        });
    });

    // 캐러셀 설정 함수
    function setupCarousel(carouselTrackSelector, btnSelector, itemClass) {
        const track = document.querySelector(carouselTrackSelector);
        if (!track) {
            console.error("Track not found:", carouselTrackSelector);
            return;
        }
        let index = 0;
        const items = track.querySelectorAll(itemClass);
        const totalItems = items.length;
        const visibleItems = Math.min(5, totalItems);
        const itemWidth = 100 / visibleItems;
        const btnLeft = document.querySelectorAll(`${btnSelector}.left`);
        const btnRight = document.querySelectorAll(`${btnSelector}.right`);

        if (totalItems <= visibleItems) {
            btnLeft.forEach(btn => btn.style.display = "none");
            btnRight.forEach(btn => btn.style.display = "none");
            return;
        }

        btnLeft.forEach(btn => btn.addEventListener("click", () => moveCarousel(-1)));
        btnRight.forEach(btn => btn.addEventListener("click", () => moveCarousel(1)));

        function moveCarousel(direction) {
            index += direction;
            const moveX = -(index * itemWidth);
            track.style.transition = "transform 0.5s ease-in-out";
            track.style.transform = `translateX(${moveX}%)`;
            setTimeout(() => {
                if (index >= totalItems - visibleItems) {
                    const firstItem = track.firstElementChild;
                    track.appendChild(firstItem);
                    index--;
                    track.style.transition = "none";
                    track.style.transform = `translateX(${-(index * itemWidth)}%)`;
                } else if (index < 0) {
                    const lastItem = track.lastElementChild;
                    track.prepend(lastItem);
                    index++;
                    track.style.transition = "none";
                    track.style.transform = `translateX(${-(index * itemWidth)}%)`;
                }
            }, 500);
        }

        if (!track.dataset.carouselInitialized) {
            setInterval(() => moveCarousel(1), 5000);
            track.dataset.carouselInitialized = true;
        }
    }

    // 더보기 버튼 설정
    function setupLoadMore() {
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        if (!loadMoreBtn) return;

        const productItems = document.querySelectorAll('.col');
        let displayedProducts = 0;
        const itemsPerLoad = 10;

        productItems.forEach((product, index) => {
            product.style.display = index < itemsPerLoad ? 'block' : 'none';
            if (index < itemsPerLoad) displayedProducts++;
        });

        if (productItems.length <= itemsPerLoad) loadMoreBtn.style.display = 'none';

        loadMoreBtn.addEventListener('click', function() {
            let count = 0;
            for (let i = displayedProducts; i < productItems.length && count < itemsPerLoad; i++) {
                productItems[i].style.display = 'block';
                count++;
                displayedProducts++;
            }
            if (displayedProducts >= productItems.length) loadMoreBtn.style.display = 'none';
        });
    }

    // 검색 기능
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const searchInput = this.querySelector('input[name="search"]');
            const searchTerm = searchInput.value.trim().toLowerCase();

            const bestSection = document.querySelector('.best-section');
            const productItems = document.querySelectorAll('.col');

            if (searchTerm) {
                let hasResults = false;
                productItems.forEach(item => {
                    const itemName = item.textContent.toLowerCase();
                    item.style.display = itemName.includes(searchTerm) ? 'block' : 'none';
                    if (itemName.includes(searchTerm)) hasResults = true;
                });
                if (bestSection) bestSection.style.display = hasResults ? 'none' : 'block';
            } else {
                resetDisplay();
            }
        });
    }

    // 카테고리 필터링
    const categoryButtons = document.querySelectorAll('.category-btn');
    categoryButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            filterByCategory(category);
        });
    });

    // 카테고리별 필터링 함수
    function filterByCategory(category) {
        const productItems = document.querySelectorAll('.col');
        const selectedStore = document.getElementById('storeSelect')?.value || '';

        productItems.forEach(item => {
            const itemCategory = item.getAttribute('data-category');
            const itemStore = allItems.find(i => i.pk == item.getAttribute('data-id')).fields.store;
            const matchesStore = selectedStore ? itemStore === selectedStore : true;
            const matchesCategory = category === 'all' || itemCategory === category;
            item.style.display = matchesStore && matchesCategory ? 'block' : 'none';
        });

        // 더보기 버튼 재설정
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        if (loadMoreBtn) {
            loadMoreBtn.style.display = 'block';
            setupLoadMore();
        }
    }

    // 표시 초기화 함수
    function resetDisplay() {
        const productItems = document.querySelectorAll('.col');
        const bestSection = document.querySelector('.best-section');
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        let displayedProducts = 0;
        const itemsPerLoad = 10;

        productItems.forEach((item, index) => {
            item.style.display = loadMoreBtn && index < itemsPerLoad ? 'block' : loadMoreBtn ? 'none' : 'block';
            if (loadMoreBtn && index < itemsPerLoad) displayedProducts++;
        });

        if (bestSection) bestSection.style.display = 'block';
        if (loadMoreBtn) loadMoreBtn.style.display = productItems.length > itemsPerLoad ? 'block' : 'none';
    }

    // NEW 태그 타이머
    function setupNewTagTimers() {
        const newTags = document.querySelectorAll('.new-tag-main');
        const now = new Date();

        newTags.forEach(tag => {
            const createdAt = new Date(tag.getAttribute('data-created-at'));
            const durationSeconds = parseInt(tag.getAttribute('data-new-duration-seconds')) || 3600;
            const remainingMs = (durationSeconds * 1000) - (now - createdAt);

            if (remainingMs <= 0) {
                tag.style.display = 'none';
            } else {
                setTimeout(() => tag.style.display = 'none', remainingMs);
            }
        });
    }

    // 초기화
    window.addEventListener('load', resetDisplay);
    setupNewTagTimers();
});