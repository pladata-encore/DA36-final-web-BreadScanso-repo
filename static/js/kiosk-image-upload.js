const fileInput = document.getElementById('file-input');
const preview = document.getElementById('preview');
const resetBtn = document.getElementById('reset-btn');


// 파일 업로드 후 이미지 미리보기
fileInput.addEventListener('change', function(event) {
    const file = event.target.files[0];  // 선택한 파일
    if (file) {
        const reader = new FileReader();  // FileReader 객체 생성
        reader.onload = function(e) {
            preview.src = e.target.result;  // 미리보기 이미지 설정
            preview.style.display = 'block';  // 이미지 보이게 하기
            fileInput.style.display = 'none';  // 파일 업로드 칸 숨기기
            resetBtn.style.display = 'block';  // 다시 스캔 버튼 보이기
        };
        reader.readAsDataURL(file);  // 파일을 URL로 읽음
    }
});

// 다시 스캔 버튼 클릭 시 파일 업로드 칸 다시 보이기
resetBtn.addEventListener('click', function() {
    fileInput.style.display = 'block';  // 파일 업로드 칸 보이기
    fileInput.value = '';  // 이전 파일값 초기화
    preview.style.display = 'none';  // 미리보기 이미지 숨기기
    resetBtn.style.display = 'none';  // 다시 스캔 버튼 숨기기
});