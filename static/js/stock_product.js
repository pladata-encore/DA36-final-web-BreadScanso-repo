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
});

