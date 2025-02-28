console.log('event_list.js loaded...');

// // 검색창
// searchForm.addEventListener("submit", function (event) {
//         event.preventDefault(); // 폼 전송 방지
//         const searchTerm = searchInput.value.trim().toLowerCase();
//
//         let found = false; // 검색 결과가 있는지 확인하는 변수
//
//         itemsData.forEach(product => {
//             const eventName = product.querySelector(".card-title").textContent.trim().toLowerCase();
//
//             if (eventName.includes(searchTerm)) {
//                 product.style.display = "block"; // 검색어가 포함된 경우 표시
//                 found = true;
//             } else {
//                 product.style.display = "none"; // 포함되지 않으면 숨김
//             }
//         });
//
//         // 검색 결과가 없으면 메시지 표시
//         if (!found) {
//             eventGrid.innerHTML = `<div class="text-center mt-3"><strong>검색 결과가 없습니다.</strong></div>`;
//         }
//
//         // 검색 후 '더보기' 버튼 숨기기
//         loadMoreBtn.style.display = "none";
//     });
