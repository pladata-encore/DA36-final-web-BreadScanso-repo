document.addEventListener('DOMContentLoaded', function () {
    // 페이지 로드시 세션 스토리지 초기화
    sessionStorage.removeItem("productDictionary");
    sessionStorage.removeItem("totalQuantity");
    sessionStorage.removeItem("totalAmount");
    sessionStorage.removeItem("usedPoints");
    sessionStorage.removeItem("finalAmount");
    sessionStorage.removeItem("earnedPoints");
    sessionStorage.removeItem("phone_num");
    sessionStorage.removeItem("points");
    sessionStorage.removeItem("finalPoints");
    console.log('세션 스토리지가 초기화되었습니다.');

    // 웹캠 설정
    const video = document.getElementById("webcam");
    const captureBtn = document.getElementById("capture-btn");
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    const NGROK_URL = "https://dace-175-121-129-72.ngrok-free.app/predict/";

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
        document.getElementById('order-table').innerHTML = '';
        document.getElementById('totalQuantity').textContent = '0개';
        document.getElementById('totalAmount').textContent = '0원';
        productDictionary = {};
        sessionStorage.removeItem("productDictionary");
        sessionStorage.removeItem("totalQuantity");
        sessionStorage.removeItem("totalAmount");
    });

    // 테이블 업데이트 함수
    function updateOrderTable() {
        const orderTable = document.getElementById("order-table");
        const totalQuantityElement = document.getElementById("totalQuantity");
        const totalAmountElement = document.getElementById("totalAmount");
        orderTable.innerHTML = "";
        let totalQuantity = 0;
        let totalAmount = 0;

        Object.keys(productDictionary).forEach(itemName => {
            const product = productDictionary[itemName];
            totalQuantity += product.quantity;
            totalAmount += product.totalPrice;

            // confidence 값이 70% 미만이면 붉은 글씨로 표시
            const textColor = (product.confidence < 0.6) ? 'style="color: red;"' : '';
            const row = `
                <tr>
                    <td ${textColor}>${product.korName}</td>
                    <td>${product.price.toLocaleString()}원</td>
                    <td>${product.quantity}</td>
                    <td>${product.totalPrice.toLocaleString()}원</td>
                    <td><button class="del-btn" data-item="${itemName}">X</button></td>
                </tr>
            `;
            orderTable.innerHTML += row;
        });

        totalQuantityElement.innerHTML = `${totalQuantity}개`;
        totalAmountElement.innerHTML = `${totalAmount.toLocaleString()}원`;
        sessionStorage.setItem("productDictionary", JSON.stringify(productDictionary));
        sessionStorage.setItem("totalQuantity", totalQuantity);
        sessionStorage.setItem("totalAmount", totalAmount.toString());

        // 삭제 버튼 이벤트
        document.querySelectorAll(".del-btn").forEach(button => {
            button.addEventListener("click", function () {
                const itemName = this.getAttribute("data-item");
                delete productDictionary[itemName];
                updateOrderTable();
            });
        });
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

            const results = await response.json();
            if (!results) throw new Error("빈 응답이 왔습니다");

            // Base64 인코딩된 이미지 받아오기
            const detectedImage = results.image;
            const detectionData = results.data;

            // base64 이미지
            document.getElementById("result-image").src = `data:image/jpeg;base64,${detectedImage}`;
            document.getElementById("result-modal").style.display = "block";


            // 모달 외부 클릭 시 닫기 (선택 사항)
            window.addEventListener("click", function (event) {
                const modal = document.getElementById("result-modal");
                if (event.target === modal) {
                    modal.style.display = "none";
                }
            });

            // 라벨, confidence data
            detectionData.forEach(result => {
                if (result?.name && result?.confidence) {
                    const engName = result.name;
                    const korName = getKoreanName(engName);
                    const price = menu_data[engName]?.price || 0;
                    const item_id = menu_data[engName]?.item_id || null;
                    const confidence = parseFloat(result.confidence); // 문자열에서 숫자로 변환

                    if (productDictionary[engName]) {
                        productDictionary[engName].quantity += 1;
                        productDictionary[engName].totalPrice =
                            productDictionary[engName].quantity * productDictionary[engName].price;
                        // confidence 값이 더 낮은 경우 갱신
                        if (confidence < productDictionary[engName].confidence) {
                            productDictionary[engName].confidence = confidence;
                        }
                    } else {
                        productDictionary[engName] = {
                            korName: korName,
                            price: price,
                            quantity: 1,
                            totalPrice: price,
                            item_id: item_id,
                            confidence: confidence // confidence 값 추가
                        };
                    }
                }
            });

            updateOrderTable();
        } catch (error) {
            console.error("🚨 에러:", error);
        } finally {
            captureBtn.disabled = false;
            captureBtn.textContent = "📸 촬영";
        }
    });

    // 모달 요소
    const modal = document.getElementById("edit-modal");
    const itemSelect = document.getElementById("item-select");
    const quantityInput = document.getElementById("quantity-input");
    const saveItemBtn = document.getElementById("save-item-btn");
    const closeModalBtn = document.getElementById("close-modal-btn");
    const searchInput = document.getElementById("search-input");

    // 품목 목록 채우기
    function populateItemSelect(filter = "") {
        itemSelect.innerHTML = "";
        Object.keys(menu_data).forEach(engName => {
            const korName = getKoreanName(engName);
            if (korName.includes(filter)) {
                const option = document.createElement("option");
                option.value = engName;
                option.textContent = `${korName} - ${menu_data[engName].price}원`;
                itemSelect.appendChild(option);
            }
        });
    }

    // 모달 열기 함수 (수정 모드)
    function openModalForEdit(itemName) {
        modal.style.display = "block";
        populateItemSelect();
        itemSelect.value = itemName;
        quantityInput.value = productDictionary[itemName].quantity;
        saveItemBtn.onclick = () => {
            const newQuantity = parseInt(quantityInput.value);
            productDictionary[itemName].quantity = newQuantity;
            productDictionary[itemName].totalPrice = newQuantity * productDictionary[itemName].price;
            updateOrderTable();
            modal.style.display = "none";
        };
    }

    // 모달 열기 함수 (추가 모드)
    function openModalForAdd() {
        modal.style.display = "block";
        populateItemSelect();
        quantityInput.value = 1;
        saveItemBtn.onclick = () => {
            const selectedItem = itemSelect.value;
            const quantity = parseInt(quantityInput.value);
            if (!productDictionary[selectedItem]) {
                productDictionary[selectedItem] = {
                    korName: getKoreanName(selectedItem),
                    price: menu_data[selectedItem].price,
                    quantity: quantity,
                    totalPrice: menu_data[selectedItem].price * quantity,
                    item_id: menu_data[selectedItem].item_id,
                    confidence: 1.0 // 수동 추가 시 confidence 값 기본 100%
                };
            } else {
                productDictionary[selectedItem].quantity += quantity;
                productDictionary[selectedItem].totalPrice = productDictionary[selectedItem].quantity * productDictionary[selectedItem].price;
            }
            updateOrderTable();
            modal.style.display = "none";
        };
    }

    // 검색 기능
    searchInput.addEventListener("input", () => {
        populateItemSelect(searchInput.value);
    });

    // 모달 닫기
    closeModalBtn.addEventListener("click", () => {
        modal.style.display = "none";
    });

    // 테이블 행 클릭 시 수정 모달 열기
    document.getElementById("order-table").addEventListener("click", (e) => {
        const row = e.target.closest("tr");
        if (row && e.target.tagName !== "BUTTON") { // 삭제 버튼 클릭 제외
            const itemName = Object.keys(productDictionary).find(key => productDictionary[key].korName === row.cells[0].textContent);
            openModalForEdit(itemName);
        }
    });

    // 품목 추가 버튼 이벤트
    document.getElementById("add-item-btn").addEventListener("click", openModalForAdd);

    startWebcam();
});