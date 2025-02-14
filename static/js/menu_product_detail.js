document.addEventListener("DOMContentLoaded", function() {
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


        function getProductIdFromUrl() {
        const pathSegments = window.location.pathname.split('/');
        return parseInt(pathSegments[pathSegments.length - 1]);
    }

    function showProductDetails() {
        const productId = getProductIdFromUrl();
        const product = products.find(p => p.id === productId);

        if (product) {
            document.getElementById('detailImage').src = product.image;
            document.getElementById('detailName').innerText = product.name;
            document.getElementById('detailDescription').innerText = product.description;
            document.getElementById('detailNutrition').innerText = product.nutrition;
            document.getElementById('detailAllergy').innerText = product.allergy;
            document.getElementById('detailPrice').innerText = `판매가: ${product.price}`;

            if (product.tag) {
                const tagElement = document.getElementById('productTag');
                tagElement.innerText = product.tag;
                tagElement.style.display = "inline-block";
                tagElement.style.backgroundColor = product.tag === "Best" ? "#00FFFF" : "#FFEE8C";
                tagElement.style.color = "#000";
                tagElement.style.padding = "5px 10px";
                tagElement.style.borderRadius = "15px";
                tagElement.style.marginBottom = "10px";
            }
        } else {
            console.error("제품 정보를 찾을 수 없습니다.");
        }
    }

    showProductDetails();
});

// 전역 범위로 이동
function goBackToList() {
    window.history.back();
}