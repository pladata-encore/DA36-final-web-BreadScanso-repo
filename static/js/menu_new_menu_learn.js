document.addEventListener('DOMContentLoaded', function() {
    const menuForm = document.getElementById('menu-form');
    const fileInput = document.getElementById('file-input');
    const zipInput = document.getElementById('zip-input');
    const previewContainer = document.getElementById('preview-container');
    const learnBtn = document.getElementById('learn-btn');
    const confirmLearnBtn = document.getElementById('confirm-learn-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const clearZipBtn = document.getElementById('clear-zip-btn');

    // 요소 존재 여부 확인
    if (!zipInput) {
        console.error("zip-input 요소를 찾을 수 없습니다. HTML에서 id='zip-input'이 정의되어 있는지 확인하세요.");
        return;
    }
    if (!clearZipBtn) {
        console.error("clear-zip-btn 요소를 찾을 수 없습니다. HTML에서 id='clear-zip-btn'이 정의되어 있는지 확인하세요.");
        return;
    }

    // 이미지 미리보기 및 취소 기능
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            previewContainer.innerHTML = ''; // 기존 미리보기 초기화
            const files = Array.from(this.files);

            files.forEach((file, index) => {
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.addEventListener('load', function() {
                        const previewDiv = document.createElement('div');
                        previewDiv.className = 'preview-item';

                        const img = document.createElement('img');
                        img.src = reader.result;
                        img.className = 'preview-image';

                        const removeBtn = document.createElement('button');
                        removeBtn.textContent = 'X';
                        removeBtn.className = 'remove-btn';
                        removeBtn.type = 'button';

                        removeBtn.addEventListener('click', function() {
                            const newFiles = Array.from(fileInput.files).filter((_, i) => i !== index);
                            const dataTransfer = new DataTransfer();
                            newFiles.forEach(f => dataTransfer.items.add(f));
                            fileInput.files = dataTransfer.files;

                            previewDiv.remove();
                            fileInput.dispatchEvent(new Event('change'));
                        });

                        previewDiv.appendChild(img);
                        previewDiv.appendChild(removeBtn);
                        previewContainer.appendChild(previewDiv);
                    });
                    reader.readAsDataURL(file);
                }
            });
        });
    }

    // ZIP 파일 업로드 시 즉시 검증
    zipInput.addEventListener('change', async function() {
        const file = this.files[0];
        console.log('Selected file:', file);

        if (file) {
            if (typeof file.name !== 'string') {
                console.error('file.name이 문자열이 아닙니다:', file.name);
                alert('유효하지 않은 파일입니다.');
                this.value = '';
                clearZipBtn.style.display = 'none';
                return;
            }

            const isZip = file.name.toLowerCase().indexOf('.zip') === file.name.length - 4;
            if (!isZip) {
                alert('유효한 ZIP 파일을 선택해주세요.');
                this.value = '';
                clearZipBtn.style.display = 'none';
                return;
            }

            // 파일 크기 확인 (최대 500MB)
            const maxSizeInBytes = 500 * 1024 * 1024;
            if (file.size > maxSizeInBytes) {
                alert('ZIP 파일 크기는 최대 500MB까지 가능합니다.');
                this.value = '';
                clearZipBtn.style.display = 'none';
                return;
            }

            // ZIP 파일 내용 검증
            try {
                const result = await validateZipContents(file);
                if (result.valid) {
                    alert('유효한 ZIP 파일이 선택되었습니다: ' + file.name);
                    clearZipBtn.style.display = 'inline-block';
                } else {
                    alert('ZIP 파일은 이미지와 동영상 파일만 포함해야 합니다.\n' + result.message);
                    this.value = '';
                    clearZipBtn.style.display = 'none';
                }
            } catch (error) {
                console.error('ZIP 검증 중 오류:', error);
                alert('ZIP 파일 처리 중 오류가 발생했습니다.');
                this.value = '';
                clearZipBtn.style.display = 'none';
            }
        } else {
            clearZipBtn.style.display = 'none';
        }
    });

    // ZIP 파일 취소 버튼
    clearZipBtn.addEventListener('click', function() {
        zipInput.value = '';
        this.style.display = 'none';
        zipInput.dispatchEvent(new Event('change'));
    });

    // ZIP 파일 내용 검증 함수
    async function validateZipContents(file) {
        try {
            if (typeof JSZip === 'undefined') {
                console.error('JSZip 라이브러리가 로드되지 않았습니다. 클라이언트 검증을 건너뛰고 서버에서 검증합니다.');
                alert('ZIP 검증 라이브러리가 로드되지 않았습니다. 서버에서 추가 검증이 수행됩니다.');
                return { valid: true, message: "JSZip 미로드로 서버 검증에 의존" };
            }

            const zip = new JSZip();
            const zipData = await zip.loadAsync(file);

            const fileEntries = Object.keys(zipData.files);
            console.log('ZIP 파일 내 항목:', fileEntries); // 디버깅 로그

            const validExtensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg',
                                     'mp4', 'mov', 'avi', 'wmv', 'flv', 'mkv', 'webm'];
            let invalidFiles = [];
            let validFilesFound = false;

            for (const filename of fileEntries) {
                if (!zipData.files[filename].dir) {
                    const fileExt = filename.split('.').pop().toLowerCase();
                    console.log(`검증 중인 파일: ${filename}, 확장자: ${fileExt}`);
                    if (validExtensions.includes(fileExt)) {
                        validFilesFound = true;
                    } else {
                        invalidFiles.push(filename);
                    }
                }
            }

            if (!validFilesFound) {
                return {
                    valid: false,
                    message: 'ZIP 파일에 이미지나 동영상 파일이 없습니다.'
                };
            }

            if (invalidFiles.length > 0) {
                return {
                    valid: false,
                    message: `다음 파일들은 허용되지 않습니다: ${invalidFiles.slice(0, 3).join(', ')}${invalidFiles.length > 3 ? ' 외 ' + (invalidFiles.length - 3) + '개' : ''}`
                };
            }

            return { valid: true, message: "모든 파일이 유효합니다." };
        } catch (error) {
            console.error("ZIP 파일 검증 중 오류:", error);
            return { valid: false, message: "ZIP 파일 검증 중 오류가 발생했습니다." };
        }
    }

    // 학습 확인 버튼 클릭 시 파일 업로드
    confirmLearnBtn.addEventListener('click', function() {
        const itemId = confirmLearnBtn.getAttribute('data-item-id');

        const hasImages = fileInput && fileInput.files.length > 0;
        const hasZip = zipInput.files.length > 0;

        if (!hasImages && !hasZip) {
            alert('업로드할 이미지나 ZIP 파일을 선택해주세요.');
            return;
        }

        const formData = new FormData();

        if (hasImages) {
            for (let i = 0; i < fileInput.files.length; i++) {
                formData.append('item_images', fileInput.files[i]);
            }
        }

        if (hasZip) {
            formData.append('item_zip', zipInput.files[0]);
        }

        const modalBody = document.querySelector('.modal-body');
        const originalContent = modalBody.innerHTML;
        modalBody.innerHTML = '업로드 중... <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/menu/store/upload_learning_materials/${itemId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`학습 자료 업로드 완료! ${data.uploaded_count}개의 파일이 업로드되었습니다.`);
                window.location.href = `/menu/store/menu_info/${itemId}`;
            } else {
                alert('업로드 실패: ' + data.message);
                modalBody.innerHTML = originalContent;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('업로드 중 오류가 발생했습니다.');
            modalBody.innerHTML = originalContent;
        });
    });

    // 취소 버튼 클릭 시 메뉴 정보 페이지로 이동
    cancelBtn.addEventListener('click', function() {
        const itemId = confirmLearnBtn.getAttribute('data-item-id');
        window.location.href = `/menu/store/menu_info/${itemId}`;
    });
});