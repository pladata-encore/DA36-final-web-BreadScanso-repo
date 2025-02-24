document.addEventListener("DOMContentLoaded", function () {
    // 테이블 정렬 기능
    function sortTable() {
        const table = document.querySelector('.stock-product-table tbody');
        const rows = Array.from(table.rows);
        let currentDirection = table.dataset.direction || 'asc';

        rows.sort((rowA, rowB) => {
            const stockA = parseInt(rowA.cells[5].textContent); // 재고수량 열 (index 5)
            const stockB = parseInt(rowB.cells[5].textContent);

            if (currentDirection === 'asc') {
                return stockA - stockB; // 오름차순
            } else {
                return stockB - stockA; // 내림차순
            }
        });

        rows.forEach(row => table.appendChild(row));  // 테이블에 정렬된 rows를 추가
        table.dataset.direction = currentDirection === 'asc' ? 'desc' : 'asc';

        const icon = document.querySelector('.stock-product-table th:nth-child(5) i'); // 5번째 열, 재고수량 열
        if (currentDirection === 'asc') {
            icon.classList.remove('bi-sort-down-alt');
            icon.classList.add('bi-sort-up-alt');
        } else {
            icon.classList.remove('bi-sort-up-alt');
            icon.classList.add('bi-sort-down-alt');
        }
    }

    // 매장 필터링 및 카테고리 필터링 기능
    function filterStore() {
        const storeValue = document.getElementById('store-filter').value;
        const categoryValue = document.getElementById('category-filter').value;
        const url = new URL(window.location.href);

        if (storeValue) {
            url.searchParams.set('store', storeValue);
        } else {
            url.searchParams.delete('store');
        }

        if (categoryValue) {
            url.searchParams.set('category', categoryValue);
        } else {
            url.searchParams.delete('category');
        }

        window.location.href = url;
    }

    // 전체 선택 체크박스 이벤트 처리
    function selectAllCheckboxes() {
        const selectAllCheckbox = document.getElementById('select-all');
        selectAllCheckbox.addEventListener('change', function() {
            let checkboxes = document.querySelectorAll('.row-checkbox');
            checkboxes.forEach(function(checkbox) {
                checkbox.checked = selectAllCheckbox.checked;
            });
        });

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
    }

    // 재고 수정
    function updateStockFunction() {
        document.querySelectorAll('.btn-warning').forEach(button => {
            button.addEventListener('click', function(event) {
                const button = event.target;
                if (!button || !button.closest('tr')) return;

                const row = button.closest('tr'); // 버튼이 포함된 행
                const rowId = row.querySelector('td:nth-child(2)').innerText; // 제품 ID
                const rowName = row.querySelector('td:nth-child(3)').innerText; // 제품명
                const stockCell = row.querySelector('td:nth-child(6)'); // 재고 셀
                const currentStock = stockCell.innerText; // 현재 재고 수량

                const newStock = prompt(`${rowName}의 새로운 재고를 입력하세요:`, currentStock);

                if (newStock !== null && !isNaN(newStock)) {
                    updateStock(rowId, newStock, stockCell); // 재고 업데이트 함수 호출
                }
            });
        });
    }

    function updateStock(itemId, newStock, stockCell) {
        fetch('product/update_stock/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ 'item_id': itemId, 'new_stock': newStock })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`stock-${itemId}`).innerText = newStock;
                alert('재고가 변경되었습니다.');
            } else {
                alert('재고 변경에 실패하였습니다.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('서버 오류가 발생했습니다.');
        });
    }

    function getCSRFToken() {
        let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        return csrfToken;
    }

    // 모든 이벤트 리스너 설정
    function setEventListeners() {
        sortTable(); // 테이블 정렬 기능
        filterStore(); // 매장 필터링
        selectAllCheckboxes(); // 전체 선택 체크박스
        updateStockFunction(); // 재고 수정 기능
    }

    setEventListeners();
});
