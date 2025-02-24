function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length, cookie.length);
        }
    }
    return null;  // CSRF 토큰이 없을 경우 null 반환
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("confirm-save-btn").addEventListener("click", function () {
        const formData = new FormData();

        // 제품 기본 정보
        formData.append("item_name", document.getElementById("item_name").value);
        formData.append("category", document.getElementById("category").value);
        formData.append("description", document.getElementById("description").value);
        formData.append("cost_price", document.getElementById("cost_price").value);
        formData.append("sale_price", document.getElementById("sale_price").value);
        formData.append("best", document.getElementById("flexCheckBest").checked ? 1 : 0);
        formData.append("new", document.getElementById("flexCheckNew").checked ? 1 : 0);
        formData.append("show", document.getElementById("flexCheckVisible").checked ? 1 : 0);

        // 영양 정보
        formData.append("nutrition_weight", document.getElementById("nutrition_weight").value);
        formData.append("nutrition_calories", document.getElementById("nutrition_calories").value);
        formData.append("nutrition_sodium", document.getElementById("nutrition_sodium").value);
        formData.append("nutrition_sugar", document.getElementById("nutrition_sugar").value);
        formData.append("nutrition_carbohydrates", document.getElementById("nutrition_carbohydrates").value);
        formData.append("nutrition_saturated_fat", document.getElementById("nutrition_saturated_fat").value);
        formData.append("nutrition_trans_fat", document.getElementById("nutrition_trans_fat").value);
        formData.append("nutrition_protein", document.getElementById("nutrition_protein").value);

        // 알레르기 정보
        formData.append("allergy_wheat", document.querySelector("[name='allergy_wheat']").checked ? 1 : 0);
        formData.append("allergy_milk", document.querySelector("[name='allergy_milk']").checked ? 1 : 0);
        formData.append("allergy_egg", document.querySelector("[name='allergy_egg']").checked ? 1 : 0);
        formData.append("allergy_soybean", document.querySelector("[name='allergy_soybean']").checked ? 1 : 0);
        formData.append("allergy_nuts", document.querySelector("[name='allergy_nuts']").checked ? 1 : 0);
        formData.append("allergy_etc", document.getElementById("allergy_etc").value);


        fetch("/store/menu_save/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),  // CSRF 토큰 추가
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.message.includes("성공")) {
                window.location.href = "/menu/store/menu_info";  // 저장 성공 후 이동
            }
        })
        .catch(error => console.error("Error:", error));
    });
});

const fileInput = document.getElementById('file-input');
const preview = document.getElementById('preview');

// 파일 업로드 후 이미지 미리보기
fileInput.addEventListener('change', function(event) {
    const file = event.target.files[0];  // 선택한 파일
    if (file) {
        const reader = new FileReader();  // FileReader 객체 생성
        reader.onload = function(e) {
            preview.src = e.target.result;  // 미리보기 이미지 설정
            preview.style.display = 'block';  // 이미지 보이게 하기
            fileInput.style.display = 'none';  // 파일 업로드 칸 숨기기
        };
        reader.readAsDataURL(file);  // 파일을 URL로 읽음
    }
});

// 취소 버튼 누르면 목록 화면으로 이동
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("cancel-btn").addEventListener("click", function () {
        window.location.href = "/menu/store/";  // 취소 시 이전 화면으로 이동
    });
});

// 저장 버튼 누르면 메뉴관리 상세 페이지로 이동
document.getElementById("confirm-save-btn").addEventListener("click", function () {
    window.location.href = "/menu/store/menu_info";  // 확인을 누르면 menu_info 페이지로 이동
});
