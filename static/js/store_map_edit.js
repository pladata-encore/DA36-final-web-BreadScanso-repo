document.addEventListener("DOMContentLoaded", function() {
    const saveButton = document.getElementById("save-changes-btn");

    saveButton.addEventListener("click", saveStoreInfo);

    function saveStoreInfo() {
        const storeData = {
            store_address: document.getElementById("address").value,
            store_time: document.getElementById("store_time").value,
            store_notes: document.getElementById("transportation").innerHTML
        };

        fetch("/store/store_map/edit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
                // X-CSRFToken 헤더 제거됨
            },
            body: JSON.stringify(storeData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert("변경 사항이 저장되었습니다.");
                window.location.href = "/store/store_map/";
            } else {
                alert("저장 실패: " + data.message);
            }
        })
        .catch(error => {
            console.error("저장 중 오류 발생:", error);
            alert("저장 중 오류가 발생했습니다.");
        });
    }
});