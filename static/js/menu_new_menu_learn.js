document.addEventListener('DOMContentLoaded', function() {
    const menuForm = document.getElementById('menu-form');
    const fileInput = document.getElementById('file-input');
    const zipInput = document.getElementById('zip-input');
    const previewContainer = document.getElementById('preview-container');
    const learnBtn = document.getElementById('learn-btn');
    const confirmLearnBtn = document.getElementById('confirm-learn-btn');
    const cancelBtn = document.getElementById('cancel-btn');

    // 이미지 미리보기 (여러 장)
    fileInput.addEventListener('change', function() {
        previewContainer.innerHTML = ''; // 기존 미리보기 초기화
        const files = this.files;

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.addEventListener('load', function() {
                    const img = document.createElement('img');
                    img.src = reader.result;
                    previewContainer.appendChild(img);
                });
                reader.readAsDataURL(file);
            }
        }
    });

    // ZIP 파일 업로드 시 알림
    zipInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file && file.type === 'application/zip') {
            alert('ZIP 파일이 선택되었습니다: ' + file.name);
        } else {
            alert('유효한 ZIP 파일을 선택해주세요.');
            this.value = ''; // 잘못된 파일 선택 시 초기화
        }
    });

    // 학습 확인 버튼 클릭 시 폼 제출
    confirmLearnBtn.addEventListener('click', function() {
        const itemId = confirmLearnBtn.getAttribute('data-item-id');
        window.location.href = `/menu/store/menu_info/${itemId}`;
    });

    // 취소 버튼 클릭 시 이전 화면으로 이동
    cancelBtn.addEventListener('click', function() {
        // item_id를 가져와서 메뉴 정보 페이지로 이동
        const itemId = confirmLearnBtn.getAttribute('data-item-id');
        window.location.href = `/menu/store/menu_info/${itemId}`;
    });
});