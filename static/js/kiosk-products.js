document.addEventListener('DOMContentLoaded', function() {
    // 페이지 로드시 세션 스토리지 초기화
    sessionStorage.removeItem("productDictionary");
    sessionStorage.removeItem("totalQuantity");
    sessionStorage.removeItem("totalPrice");
    sessionStorage.removeItem("usedPoints");
    sessionStorage.removeItem("finalPrice");
    console.log('세션 스토리지가 초기화되었습니다.');

// 웹캠 설정
    const video = document.getElementById("webcam");
    const captureBtn = document.getElementById("capture-btn");
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    const NGROK_URL = "https://dbc3-175-121-129-72.ngrok-free.app/predict/";

    let productDictionary = {};

// 한글명 매핑 함수
    function getKoreanName(engName) {
        const nameMapping = {
            "bagel": "베이글",
            "croissant": "크루아상",
            "whitebread": "식빵",
            "redbeanbread": "단팥빵",
            "pizzabread": "피자빵",
            "saltbread": "소금빵",
            "custardcreambread": "슈크림빵",
            "soboro": "소보로"
        };
        return nameMapping[engName] || engName;
    }

// 웹캠 시작
    async function startWebcam() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({video: true});
            video.srcObject = stream;
        } catch (error) {
            console.error("🚨 웹캠 접근 실패:", error);
            alert("웹캠을 사용할 수 없습니다. 브라우저 설정을 확인하세요.");
        }
    }

// 리셋 버튼 이벤트
    document.getElementById('reset-order-btn').addEventListener('click', function () {
// 주문 테이블 비우기
        document.getElementById('order-table').innerHTML = '';
// 총 수량과 총 금액 초기화
        document.getElementById('total-quantity').textContent = '0개';
        document.getElementById('total-price').textContent = '0원';
// 제품 딕셔너리 초기화
        productDictionary = {};
// 세션 스토리지 초기화
        sessionStorage.removeItem("productDictionary");
        sessionStorage.removeItem("totalQuantity");
        sessionStorage.removeItem("totalPrice");
    });

// 테이블 업데이트 함수
    function updateOrderTable() {
        const orderTable = document.getElementById("order-table");
        const totalQuantityElement = document.getElementById("total-quantity");
        const totalPriceElement = document.getElementById("total-price");
        // 테이블 초기화
        orderTable.innerHTML = "";
        let totalQuantity = 0;
        let totalPrice = 0;

        Object.keys(productDictionary).forEach(itemName => {
            const product = productDictionary[itemName];
            totalQuantity += product.quantity;
            totalPrice += product.totalAmount;
            const row = `
            <tr>
                <td>${product.korName}</td>
                <td>${product.price.toLocaleString()}원</td>
                <td>${product.quantity}</td>
                <td>${product.totalAmount.toLocaleString()}원</td>
            </tr>
        `;
            orderTable.innerHTML += row;
        });

        // 총 수량과 금액 업데이트
        totalQuantityElement.innerHTML = `${totalQuantity}개`;
        totalPriceElement.innerHTML = `${totalPrice.toLocaleString()}원`;

        // 세션 스토리지에 데이터 저장
        sessionStorage.setItem("productDictionary", JSON.stringify(productDictionary));
        sessionStorage.setItem("totalQuantity", totalQuantity);
        sessionStorage.setItem("totalPrice", totalPrice);

    }

// 촬영 버튼 이벤트
    captureBtn.addEventListener("click", async () => {
        captureBtn.disabled = true;
        captureBtn.textContent = "🔄 추론 중...";

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL("image/jpeg");

        try {
            const response = await fetch(NGROK_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({image: imageData}),
                mode: "cors"
            });

            const responseText = await response.text();
            if (!responseText) throw new Error("빈 응답이 왔습니다");

            const results = JSON.parse(responseText);
            console.log("📌 추론 결과:", results);

            // 상품 데이터를 테이블에 추가
            results.forEach(result => {
                if (result?.name && result?.confidence) {
                    const engName = result.name;
                    const korName = getKoreanName(engName);
                    const price = menu_data[engName]?.price || 0;


                    if (productDictionary[engName]) {
                        productDictionary[engName].quantity += 1;
                        productDictionary[engName].totalAmount =
                            productDictionary[engName].quantity * productDictionary[engName].price;
                    } else {
                        productDictionary[engName] = {
                            korName: korName,
                            price: price,
                            quantity: 1,
                            totalAmount: price
                        };
                    }
                }
            });

            // 테이블 업데이트
            updateOrderTable();

        } catch (error) {
            console.error("🚨 에러:", error);
        } finally {
            captureBtn.disabled = false;
            captureBtn.textContent = "📸 촬영";
        }
    });

    startWebcam();
});