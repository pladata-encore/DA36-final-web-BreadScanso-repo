// 테이블 정렬 기능
function sortTable() {
    const table = document.querySelector('.stock-ingredient-table tbody');
    const rows = Array.from(table.rows);
    let currentDirection = table.dataset.direction || 'asc';
    // 재고수량을 기준으로 정렬
    rows.sort((rowA, rowB) => {
        const stockA = parseInt(rowA.cells[4].textContent); // 재고수량 열 (index 5)
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

