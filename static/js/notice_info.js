document.addEventListener('DOMContentLoaded', function() {
    const deleteBtn = document.getElementById('delete-btn');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    const editBtn = document.getElementById('edit-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const modalElement = document.getElementById('deleteConfirmModal');
    const modal = new bootstrap.Modal(modalElement);

    // 삭제 버튼 클릭 시 모달 열기
    if (deleteBtn) {
        deleteBtn.addEventListener('click', function() {
            modal.show();
        });
    }

    // 모달에서 삭제 확인 버튼 클릭 시 AJAX 요청
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', function() {
            const noticeId = this.getAttribute('data-notice-id');

            fetch('/notice/store/notice_delete/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                },
                body: JSON.stringify({ notice_ids: [noticeId] })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('공지사항이 삭제되었습니다.');
                    window.location.href = '/notice/store/notice';
                } else {
                    alert('삭제 실패: ' + data.message);
                }
                modal.hide();
            })
            .catch(error => {
                alert('오류 발생: ' + error);
                modal.hide();
            });
        });
    }

    // 수정 버튼 클릭 시 notice_edit 페이지로 이동
    if (editBtn) {
        editBtn.addEventListener('click', function() {
            const noticeId = this.getAttribute('data-notice-id');
            window.location.href = `/notice/store/notice_edit/${noticeId}/`;
        });
    }

    // 취소 버튼 클릭 시 모달 닫기
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            modal.hide();
        });
    }
});