document.addEventListener("DOMContentLoaded", function() {
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
});
