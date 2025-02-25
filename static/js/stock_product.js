// 테이블 정렬 기능
function sortTable() {
    const table = document.querySelector('.stock-product-table tbody');
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
    const icon = document.querySelector('.stock-product-table th:nth-child(5) i'); // 5번째 열, 재고수량 열
    if (currentDirection === 'asc') {
        icon.classList.remove('bi-sort-down-alt');
        icon.classList.add('bi-sort-up-alt');
    } else {
        icon.classList.remove('bi-sort-up-alt');
        icon.classList.add('bi-sort-down-alt');
    }
}

// 재고 수정

document.querySelectorAll('.btn-warning').forEach(button => {
    button.addEventListener('click', function(event) {
        const button = event.target;
        if (!button || !button.closest('tr')) return;

        const row = button.closest('tr'); // 버튼이 포함된 행
        const rowId = row.querySelector('td:nth-child(1)').innerText; // 제품 ID
        const rowName = row.querySelector('td:nth-child(2)').innerText; // 제품명
        const stockCell = row.querySelector('td:nth-child(5)'); // 재고 셀
        const currentStock = stockCell.innerText; // 현재 재고 수량

        const newStock = prompt(`${rowName}의 새로운 재고 값을 입력하세요:`, currentStock);

        if (newStock !== null && !isNaN(newStock)) {
            updateStock(rowId, newStock, stockCell); // 재고 업데이트 함수 호출
        } 
    });
});


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
      // stockCell.innerText = newStock;
      document.getElementById(`stock-${itemId}`).innerText = newStock;
      alert('재고 수량이 업데이트되었습니다.');
    } else {
      alert('재고 수량 업데이트에 실패했습니다.');
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



document.addEventListener('DOMContentLoaded', function () {
    // // 테이블 정렬 기능
    // const table = document.querySelector('.stock-product-table tbody');
    // const icon = document.querySelector('.stock-product-table th:nth-child(5) i'); // 재고수량 열 아이콘

    // // 테이블 정렬 이벤트 처리
    // table.addEventListener('click', function (event) {
    //     if (event.target && event.target.closest('th:nth-child(5)')) { // 5번째 열 클릭 시
    //         const rows = Array.from(table.rows);
    //         let currentDirection = table.dataset.direction || 'asc';
    //
    //         rows.sort((rowA, rowB) => {
    //             const stockA = parseInt(rowA.cells[5].textContent);
    //             const stockB = parseInt(rowB.cells[5].textContent);
    //
    //             return currentDirection === 'asc' ? stockA - stockB : stockB - stockA;
    //         });
    //
    //         rows.forEach(row => table.appendChild(row));  // 정렬된 rows 다시 추가
    //         table.dataset.direction = currentDirection === 'asc' ? 'desc' : 'asc';
    //
    //         // 아이콘 업데이트
    //         if (table.dataset.direction === 'asc') {
    //             icon.classList.remove('bi-sort-down-alt');
    //             icon.classList.add('bi-sort-up-alt');
    //         } else {
    //             icon.classList.remove('bi-sort-up-alt');
    //             icon.classList.add('bi-sort-down-alt');
    //         }
    //     }
    // });

    // 매장 필터링 기능
    document.getElementById('category-filter').addEventListener('input', function () {
        var categoryValue = this.value;
        var url = new URL(window.location.href);

        if (categoryValue) {
            url.searchParams.set('category', categoryValue);
        } else {
            url.searchParams.delete('category');
        }
        window.location.href = url;
    });

    // 재고 수정 버튼 클릭 시 모달 열기
    // document.querySelectorAll('.btn-warning').forEach(button => {
    //     button.addEventListener('click', function (event) {
    //         const row = event.target.closest('tr');
    //         const rowId = row.querySelector('td:nth-child(1)').innerText;
    //         const stockCell = row.querySelector('td:nth-child(5)');
    //         const currentStock = stockCell.innerText;
    //
    //         // 모달에 기존 값 설정
    //         document.getElementById('editStock').value = currentStock;
    //
    //         const modalElement = document.getElementById('editModal');
    //         const editModal = new bootstrap.Modal(modalElement, {
    //             backdrop: 'static',
    //             keyboard: false
    //         });
    //
    //         editModal.show();
    //
    //         // 저장 버튼 클릭 시
    //         document.getElementById('saveChangesButton').onclick = function () {
    //             const newStock = document.getElementById('editStock').value;
    //
    //             if (newStock !== "" && !isNaN(newStock)) {
    //                 updateStock(rowId, newStock, stockCell);
    //                 editModal.hide();
    //             } else {
    //                 alert('유효한 값을 입력해주세요.');
    //             }
    //         };
    //     });
    // });

});

// CSRF 토큰 가져오기 함수
// function getCSRFToken() {
//     return document.querySelector('[name=csrfmiddlewaretoken]').value;
// }

// 재고 정보 업데이트 함수
// function updateStock(itemID, newStock, stockCell) {
//     fetch('product/update_stock/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': getCSRFToken(),
//         },
//         body: JSON.stringify({
//             'item_id': itemID,
//             'new_stock': newStock
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             const row = stockCell.closest('tr');
//             stockCell.innerText = newStock;
//             alert('수량이 변경되었습니다.');
//         }
//     })
//     .catch(error => {
//         alert("서버 오류 발생");
//     });
// }
