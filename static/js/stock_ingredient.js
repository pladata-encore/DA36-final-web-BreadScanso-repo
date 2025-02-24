// 테이블 정렬 기능
function sortTable() {
    const table = document.querySelector('.stock-ingredient-table tbody');
    const rows = Array.from(table.rows);
    let currentDirection = table.dataset.direction || 'asc';
    // 재고수량을 기준으로 정렬
    rows.sort((rowA, rowB) => {
        const stockA = parseInt(rowA.cells[4].textContent); // 재고수량 열
        const stockB = parseInt(rowB.cells[4].textContent);

        if (currentDirection === 'asc') {
            return stockA - stockB; // 오름차순
        } else {
            return stockB - stockA; // 내림차순
        }
    });
    rows.forEach(row => table.appendChild(row));  // 테이블에 정렬된 rows를 추가
    // 정렬 상태 업데이트
    table.dataset.direction = currentDirection === 'asc' ? 'desc' : 'asc';

    // 아이콘 업데이트
    const icon = document.querySelector('.stock-ingredient-table th:nth-child(5) i'); // 5번째 열, 재고수량 열
    if (table.dataset.direction === 'asc') {
        icon.classList.remove('bi-sort-down-alt');
        icon.classList.add('bi-sort-up-alt');
    } else {
        icon.classList.remove('bi-sort-up-alt');
        icon.classList.add('bi-sort-down-alt');
    }
}


// 매장 필터링 기능
function filterStore() {
    var storeValue = document.getElementById('store-filter').value;
    var url = new URL(window.location.href);

    // store 파라미터를 추가하거나 업데이트
    if (storeValue) {
        url.searchParams.set('store', storeValue);
    } else {
        url.searchParams.delete('store');
    }
    // 페이지 리로드하여 필터링된 데이터를 불러옵니다.
    window.location.href = url;
}


// 전체 선택/해제 체크박스 이벤트 처리
document.getElementById('select-all').addEventListener('change', function() {
    // 모든 체크박스를 선택하거나 해제
    let checkboxes = document.querySelectorAll('.row-checkbox');
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = document.getElementById('select-all').checked;
    });
});

// 각 행의 체크박스 상태 변경 시, '전체 선택' 체크박스 상태를 업데이트
let rowCheckboxes = document.querySelectorAll('.row-checkbox');
rowCheckboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        let allChecked = true;
        rowCheckboxes.forEach(function(checkbox) {
            if (!checkbox.checked) {
                allChecked = false;
            }
        });
        document.getElementById('select-all').checked = allChecked;
    });
});

// ========================================================================

// 재고 수정

// 'btn-warning' 버튼 클릭 시
document.querySelectorAll('.btn-warning').forEach(button => {
    button.addEventListener('click', function(event) {
        const button = event.target;
        if (!button || !button.closest('tr')) return;

        const row = button.closest('tr'); // 버튼이 포함된 행
        const rowId = row.querySelector('td:nth-child(2)').innerText; // 제품 ID
        const rowName = row.querySelector('td:nth-child(3)').innerText; // 제품명
        const storeName = row.querySelector('td:nth-child(4)').innerText; // 매장
        const stockCell = row.querySelector('td:nth-child(5)'); // 재고
        const currentStock = stockCell.innerText; // 현재 재고 수량

        // 모달에 기존 값 설정
        document.getElementById('editIngredientName').value = rowName;
        document.getElementById('editStore').value = storeName;
        document.getElementById('editStock').value = currentStock;

        // 모달 요소 가져오기
        const modalElement = document.getElementById('editModal');

        // 모달 열기
        const editModal = new bootstrap.Modal(modalElement, {
            backdrop: 'static', // 백드롭 클릭 방지
            keyboard: false     // ESC 키 방지
        });

        editModal.show();

        // aria-hidden 자동 제거 및 포커스 설정
        modalElement.addEventListener('shown.bs.modal', function () {
            modalElement.removeAttribute('aria-hidden');
            document.getElementById('editStock').focus();
        });

        // 저장 버튼 클릭 시
        document.getElementById('saveChangesButton').onclick = function() {
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
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            const row = stockCell.closest('tr');
            row.querySelector('td:nth-child(3)').innerText = newIngredientName;
            row.querySelector('td:nth-child(4)').innerText = newStore;
            stockCell.innerText = newStock;
            alert('재료 정보가 변경되었습니다.');
        } else {
            const row = stockCell.closest('tr');
            row.querySelector('td:nth-child(3)').innerText = newIngredientName;
            row.querySelector('td:nth-child(4)').innerText = newStore;
            stockCell.innerText = newStock;
            console.log('서버 응답:', data);
        }
    })
    .catch(error => {
        const row = stockCell.closest('tr');
        row.querySelector('td:nth-child(3)').innerText = newIngredientName;
        row.querySelector('td:nth-child(4)').innerText = newStore;
        stockCell.innerText = newStock;
        console.error('Error:', error);
    });
}

// ====================================================================

// 삭제

document.addEventListener("DOMContentLoaded", function () {
    const deleteButton = document.getElementById("delete-selected");
    deleteButton.addEventListener("click", async function () {
        // 선택된 항목 ID 수집
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



// CSRF 토큰 가져오기 함수 (이 부분이 eventListener 바깥으로 이동해야 함)
function getCSRFToken() {
    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}
