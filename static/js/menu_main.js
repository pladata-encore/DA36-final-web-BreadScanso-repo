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

    // 임의 제품 리스트
    const products = [
        {id: 1, name: 'Bagel', image: '/static/images/bagel.jpg', description: '쫄깃한 베이글', nutrition: '칼로리: 250kcal', allergy: '글루텐', price: '3,000원', tag: 'Best'},
        {id: 2, name: 'Croissant', image: '/static/images/croissant.jpg', description: '바삭한 크루아상', nutrition: '칼로리: 300kcal', allergy: '우유, 글루텐', price: '3,500원', tag: 'New'},
        {id: 3, name: 'Custard Cream Bread', image: '/static/images/custardcreambread.png', description: '달콤한 커스터드 크림빵', nutrition: '칼로리: 350kcal', allergy: '우유, 계란', price: '4,000원'},
        {id: 4, name: 'Loaf Bread', image: '/static/images/loafbread.jpg', description: '부드러운 식빵', nutrition: '칼로리: 270kcal', allergy: '글루텐', price: '2,500원'},
        {id: 5, name: 'Macaron', image: '/static/images/product1.jpg', description: '달콤한 마카롱', nutrition: '칼로리: 150kcal', allergy: '계란, 견과류', price: '2,000원'},
        {id: 6, name: 'Pizza Bread', image: '/static/images/pizzabread.jpg', description: '맛있는 피자 브레드', nutrition: '칼로리: 400kcal', allergy: '글루텐, 유제품', price: '4,500원'},
        {id: 7, name: 'Red Bean Bread', image: '/static/images/redbeanbread.jpg', description: '달콤한 팥빵', nutrition: '칼로리: 320kcal', allergy: '글루텐', price: '3,200원'},
        {id: 8, name: 'Salt Bread', image: '/static/images/saltbread.jpg', description: '짭짤한 소금빵', nutrition: '칼로리: 280kcal', allergy: '글루텐', price: '2,800원'},
        {id: 9, name: 'Soboro', image: '/static/images/soboro.jpg', description: '고소한 소보로빵', nutrition: '칼로리: 350kcal', allergy: '글루텐, 우유', price: '3,300원'},
        {id: 10, name: 'White Bread', image: '/static/images/whitebread.jpg', description: '담백한 화이트 브레드', nutrition: '칼로리: 260kcal', allergy: '글루텐', price: '2,800원'},
        {id: 11, name: 'Croissant', image: '/static/images/croissant.jpg', description: '바삭한 크루아상', nutrition: '칼로리: 300kcal', allergy: '우유, 글루텐', price: '3,500원', tag: 'New'},
        {id: 12, name: 'Custard Cream Bread', image: '/static/images/custardcreambread.png', description: '달콤한 커스터드 크림빵', nutrition: '칼로리: 350kcal', allergy: '우유, 계란', price: '4,000원'},
        {id: 13, name: 'Loaf Bread', image: '/static/images/loafbread.jpg', description: '부드러운 식빵', nutrition: '칼로리: 270kcal', allergy: '글루텐', price: '2,500원'},
        {id: 14, name: 'Macaron', image: '/static/images/product1.jpg', description: '달콤한 마카롱', nutrition: '칼로리: 150kcal', allergy: '계란, 견과류', price: '2,000원'},
        {id: 15, name: 'Pizza Bread', image: '/static/images/pizzabread.jpg', description: '맛있는 피자 브레드', nutrition: '칼로리: 400kcal', allergy: '글루텐, 유제품', price: '4,500원'},
        {id: 16, name: 'Red Bean Bread', image: '/static/images/redbeanbread.jpg', description: '달콤한 팥빵', nutrition: '칼로리: 320kcal', allergy: '글루텐', price: '3,200원'},
        {id: 16, name: 'Salt Bread', image: '/static/images/saltbread.jpg', description: '짭짤한 소금빵', nutrition: '칼로리: 280kcal', allergy: '글루텐', price: '2,800원'},
        {id: 18, name: 'Soboro', image: '/static/images/soboro.jpg', description: '고소한 소보로빵', nutrition: '칼로리: 350kcal', allergy: '글루텐, 우유', price: '3,300원'},
        {id: 19, name: 'White Bread', image: '/static/images/whitebread.jpg', description: '담백한 화이트 브레드', nutrition: '칼로리: 260kcal', allergy: '글루텐', price: '2,800원'},
        {id: 20, name: 'Bagel', image: '/static/images/bagel.jpg', description: '쫄깃한 베이글', nutrition: '칼로리: 250kcal', allergy: '글루텐', price: '3,000원', tag: 'Best'}
    ];

    products.sort((a, b) => a.name.localeCompare(b.name));  // 가나다 순 정렬

    let displayedProducts = 0;

    function showProductDetails(id) {
        location.href = `/menu/product_detail/${id}`
    }

    // 제품 표시
    function displayProducts() {
        const productGrid = document.getElementById('productGrid');
        const productsToShow = products.slice(displayedProducts, displayedProducts + 10);

        productsToShow.forEach(product => {
            console.log(product)
            const productItem = document.createElement('div');
            productItem.className = 'product-item';
            productItem.innerHTML = `
                <div>
                    <img src="${product.image}" alt="${product.name}" onclick="location.href = '/menu/product_detail/${product.id}'">
                    ${product.tag ? `<div class="tag">${product.tag}</div>` : ''}
                </div>
                <div class="product-name">${product.name}</div>
            `;
            productGrid.appendChild(productItem);
        });

        displayedProducts += productsToShow.length;
        if (displayedProducts >= products.length) {
            document.getElementById('loadMoreBtn').style.display = 'none';
        }
    }

// // Show product details
//     function showProductDetails(productName) {
//         const product = products.find(p => p.name === productName);
//         document.querySelector('.container').style.display = 'none';
//         document.getElementById('productDetails').style.display = 'block';
//
//         document.getElementById('detailName').innerText = product.name;
//         document.getElementById('detailImage').src = product.image;
//         document.getElementById('detailDescription').innerText = product.description;
//         document.getElementById('detailNutrition').innerText = product.nutrition;
//         document.getElementById('detailAllergy').innerText = product.allergy;
//         document.getElementById('detailPrice').innerText = product.price;
//     }

    // // Go back to list
    // function goBackToList() {
    //     document.getElementById('productDetails').style.display = 'none';
    //     document.querySelector('.container').style.display = 'block';
    // }

    // 더보기 버튼
    document.getElementById('loadMoreBtn').addEventListener('click', displayProducts);

    // 첫화면 로드
    window.onload = displayProducts;
});