document.addEventListener('DOMContentLoaded', function () {

    // 전체 선택/해제 체크박스 이벤트 처리
    document.getElementById('select-all').addEventListener('change', function () {
        let checkboxes = document.querySelectorAll('.row-checkbox');
        checkboxes.forEach(function (checkbox) {
            checkbox.checked = document.getElementById('select-all').checked;
        });
    });

    // 각 행의 체크박스 상태 변경 시, '전체 선택' 체크박스 상태를 업데이트
    let rowCheckboxes = document.querySelectorAll('.row-checkbox');
    rowCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            let allChecked = true;
            rowCheckboxes.forEach(function (checkbox) {
                if (!checkbox.checked) {
                    allChecked = false;
                }
            });
            document.getElementById('select-all').checked = allChecked;
        });
    });

    // 재고 수정 버튼 클릭 시 모달 열기
    document.querySelectorAll('.btn-warning').forEach(button => {
        button.addEventListener('click', function (event) {
            const row = event.target.closest('tr');
            const rowId = row.querySelector('td:nth-child(2)').innerText;
            const rowName = row.querySelector('td:nth-child(3)').innerText;
            const storeName = row.querySelector('td:nth-child(4)').innerText;
            const stockCell = row.querySelector('td:nth-child(5)');
            const currentStock = stockCell.innerText;

            // 모달에 기존 값 설정
            document.getElementById('editIngredientName').value = rowName;
            document.getElementById('editStore').value = storeName;
            document.getElementById('editStock').value = currentStock;

            const modalElement = document.getElementById('editModal');
            const editModal = new bootstrap.Modal(modalElement, {
                backdrop: 'static',
                keyboard: false
            });

            editModal.show();

            // 저장 버튼 클릭 시
            document.getElementById('saveChangesButton').onclick = function () {
                const newIngredientName = document.getElementById('editIngredientName').value;
                const newStore = document.getElementById('editStore').value;
                const newStock = document.getElementById('editStock').value;

                if (newIngredientName && newStore && newStock !== "" && !isNaN(newStock)) {
                    updateStock_ingredient(rowId, newIngredientName, newStore, newStock, stockCell);
                    editModal.hide();
                } else {
                    alert('유효한 값을 입력해주세요.');
                }
            };
        });
    });

    // 삭제 버튼 클릭 시
    document.getElementById("delete-selected").addEventListener("click", async function () {
        const selectedIds = Array.from(document.querySelectorAll(".row-checkbox:checked"))
            .map(checkbox => checkbox.closest("tr").querySelector("td:nth-child(2)").textContent.trim());

        if (selectedIds.length === 0) {
            alert("삭제할 항목을 선택해주세요.");
            return;
        }

        if (!confirm(`선택한 ${selectedIds.length}개의 재료를 삭제하시겠습니까?`)) {
            return;
        }

        try {
            const response = await fetch("ingredient/delete-ingredients/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({ ingredient_ids: selectedIds }),
            });

            const data = await response.json();
            if (data.success) {
                alert("삭제가 완료되었습니다.");
                window.location.reload();
            }
        } catch (error) {
            alert("삭제 중 오류가 발생했습니다.");
        }
    });
});

// CSRF 토큰 가져오기 함수
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// 재고 정보 업데이트 함수
function updateStock_ingredient(ingredientID, newIngredientName, newStore, newStock, stockCell) {
    fetch('product/update_stock_ingredient/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            'ingredient_id': ingredientID,
            'new_ingredient_name': newIngredientName,
            'new_store': newStore,
            'new_stock': newStock
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const row = stockCell.closest('tr');
            row.querySelector('td:nth-child(3)').innerText = newIngredientName;
            row.querySelector('td:nth-child(4)').innerText = newStore;
            stockCell.innerText = newStock;
            alert('재료 정보가 변경되었습니다.');
        }
    })
    .catch(error => {
        alert("서버 오류 발생");
    });
}

const newRegisterBtn = document.getElementById("new-register-btn");
newRegisterBtn.addEventListener("click", function () {
    window.location.href = "/stock/ingredient/new";  // 신규 등록 페이지로 이동
});

