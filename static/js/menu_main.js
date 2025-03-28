document.addEventListener("DOMContentLoaded", function () {
    // 매장 선택 확인
    const storeSelected = document.getElementById('selectStore') && document.getElementById('selectStore').value;
    const storeSelect = document.getElementById('storeSelect') && document.getElementById('storeSelect').value;
    const isStoreSelected = storeSelected || storeSelect;

    // 매장 미선택 시
    if (!isStoreSelected) {
        // 해당 요소가 존재하는지 확인 후 초기화
        if (document.querySelector(".new-carousel-track")) {
            setupCarousel(
                ".new-carousel-track",
                ".new-carousel-btn.left",
                ".new-carousel-btn.right",
                ".new-carousel-item"
            );
        }

        if (document.querySelector(".product-carousel-track")) {
            setupCarousel(
                ".product-carousel-track",
                ".product-carousel-btn.left",
                ".product-carousel-btn.right",
                ".product-carousel-item"
            );
        }
    } else {
        // 매장 선택 시
        if (document.querySelector(".best-carousel-track")) {
            setupCarousel(
                ".best-carousel-track",
                ".best-carousel-btn.left",
                ".best-carousel-btn.right",
                ".best-carousel-item"
            );
        }

        // 매장 선택 시에만 더보기 기능 초기화
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        if (loadMoreBtn) {
            const productItems = document.querySelectorAll('.col');
            let displayedProducts = 0;
            const itemsPerLoad = 10;

            // 처음에는 첫 10개만 표시하고 나머지는 숨김
            productItems.forEach((product, index) => {
                if (index < itemsPerLoad) {
                    product.style.display = 'block';
                    displayedProducts++;
                } else {
                    product.style.display = 'none';
                }
            });

            // 제품이 10개 이하면 더보기 버튼 숨김
            if (productItems.length <= itemsPerLoad) {
                loadMoreBtn.style.display = 'none';
            }

            // 더보기 버튼 클릭 이벤트
            loadMoreBtn.addEventListener('click', function() {
                let count = 0;
                for (let i = displayedProducts; i < productItems.length; i++) {
                    if (count < itemsPerLoad) {
                        productItems[i].style.display = 'block';
                        count++;
                        displayedProducts++;
                    } else {
                        break;
                    }
                }

                // 모든 제품을 표시했으면 더보기 버튼 숨김
                if (displayedProducts >= productItems.length) {
                    loadMoreBtn.style.display = 'none';
                }
            });
        }
    }

    // 제품 클릭시 제품 상세 페이지로 이동
    document.querySelectorAll(".new-carousel-item, .product-carousel-item, .best-carousel-item, .product-card").forEach(element => {
        element.addEventListener("click", function() {
            const item_id = this.getAttribute("data-id");
            if (item_id) {
                location.href = `/menu/product_detail/${item_id}`;
            }
        });

        // hover 효과
        element.addEventListener("mouseenter", function () {
            this.style.transform = "scale(1.1)";
            this.style.zIndex = "10";
            this.style.transition = "transform 0.3s ease-in-out";
        });

        element.addEventListener("mouseleave", function () {
            this.style.transform = "scale(1)";
            this.style.zIndex = "1";
            this.style.transition = "transform 0.3s ease-in-out"
        });
    });

    // 캐러셀 설정 함수 (무한 스크롤 적용)
    function setupCarousel(carouselTrackSelector, btnLeftSelector, btnRightSelector, itemClass) {
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
        const btnLeft = document.querySelectorAll(btnLeftSelector);
        const btnRight = document.querySelectorAll(btnRightSelector);

        if (totalItems <= visibleItems) {
            btnLeft.forEach(btn => btn.style.display = "none");
            btnRight.forEach(btn => btn.style.display = "none");
            return;
        }

        btnLeft.forEach(btn => {
            btn.addEventListener("click", () => {
                moveCarousel(-1);
            });
        });

        btnRight.forEach(btn => {
            btn.addEventListener("click", () => {
                moveCarousel(1);
            });
        });

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

    // 검색 기능
    const searchForm = document.getElementById('search-form');
    const bestSection = document.querySelector('.best-section');
    const productItems = document.querySelectorAll('.col');
    const loadMoreBtn = document.getElementById('loadMoreBtn');

    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault(); // 기본 폼 제출 방지
            const searchInput = this.querySelector('input[name="search"]');
            const searchTerm = searchInput.value.trim().toLowerCase();

            // 검색어가 있으면 필터링
            if (searchTerm) {
                let hasResults = false;
                productItems.forEach(item => {
                    const itemName = item.textContent.toLowerCase();
                    if (itemName.includes(searchTerm)) {
                        item.style.display = 'block';
                        hasResults = true;
                    } else {
                        item.style.display = 'none';
                    }
                });

                if (bestSection) {
                    bestSection.style.display = hasResults ? 'none' : 'block';
                }
                if (loadMoreBtn) {
                    loadMoreBtn.style.display = hasResults ? 'none' : 'block';
                }
            } else {
                resetDisplay();
            }
        });
    }

    // 표시 초기화 함수
    function resetDisplay() {
        let displayedProducts = 0;
        const itemsPerLoad = 10;

        productItems.forEach((item, index) => {
            if (loadMoreBtn && index < itemsPerLoad) {
                item.style.display = 'block';
                displayedProducts++;
            } else if (loadMoreBtn) {
                item.style.display = 'none';
            } else {
                item.style.display = 'block';
            }
        });

        if (bestSection) {
            bestSection.style.display = 'block';
        }
        if (loadMoreBtn) {
            loadMoreBtn.style.display = productItems.length > itemsPerLoad ? 'block' : 'none';
        }
    }

    // 페이지 로드 시 초기화 (URL 유지)
    window.addEventListener('load', function() {
        // URL은 유지하고 검색 결과만 초기화
        resetDisplay();
    });

    // NEW 태그 타이머 설정
    function setupNewTagTimers() {
        const newTags = document.querySelectorAll('.new-tag-main');
        const now = new Date(); // 현재 시간

        newTags.forEach(tag => {
            const createdAt = new Date(tag.getAttribute('data-created-at')); // 등록 시점
            const durationSeconds = parseInt(tag.getAttribute('data-new-duration-seconds')) || 3600; // 지속 시간 (초)
            const durationMs = durationSeconds * 1000; // 밀리초로 변환
            const elapsedMs = now - createdAt; // 경과 시간
            const remainingMs = durationMs - elapsedMs; // 남은 시간

            if (remainingMs <= 0) {
                // 이미 시간이 지난 경우 즉시 숨김
                tag.style.display = 'none';
            } else {
                // 남은 시간 후 숨김
                setTimeout(() => {
                    tag.style.display = 'none';
                }, remainingMs);
            }
        });
    }

    // 페이지 로드 시 타이머 설정
    setupNewTagTimers();

    // 실시간 업데이트 (1초마다 확인)
    setInterval(setupNewTagTimers, 1000);
});