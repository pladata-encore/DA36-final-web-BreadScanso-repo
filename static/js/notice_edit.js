$(document).ready(function() {
    var uploadedImageUrl = null;
    var store = $('#notice-form').data('store') || 'A';

    $('#save-btn').on('click', function(event) {
        event.preventDefault();
        console.log("저장 버튼 클릭됨");

        const title = $('#id_title').val().trim();
        const content = $('#id_content').val().trim();

        if (!title) {
            alert("제목을 입력해주세요.");
            return;
        }
        if (!content) {
            alert("내용을 입력해주세요.");
            return;
        }

        $('#saveConfirmModal').modal('show');
    });

    $('#confirm-save-btn').on('click', async function() {
        console.log("모달 확인 버튼 클릭됨");

        const pinned = $('#id_pinned').is(':checked');
        const title = $('#id_title').val().trim();
        const content = $('#id_content').val().trim();
        const notice_id = $('[name=notice_id]').val();

        const parser = new DOMParser();
        const doc = parser.parseFromString(content, 'text/html');
        const img = doc.querySelector('img');
        uploadedImageUrl = img ? img.src : null;

        const noticeData = {
            notice_id: notice_id,
            pinned: pinned,
            title: title,
            content: content,
            store: store,
            notice_image: uploadedImageUrl
        };

        try {
            const response = await fetch('/notice/store/notice_save/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
                },
                body: JSON.stringify(noticeData)
            });

            const data = await response.json();
            if (data.success) {
                alert('공지사항이 수정되었습니다.');
                window.location.href = `/notice/store/notice_info/${data.notice_id}/`;
            } else {
                alert('저장 실패: ' + data.message);
            }
        } catch (error) {
            alert('저장 중 오류가 발생했습니다.');
            console.error(error);
        } finally {
            $('#saveConfirmModal').modal('hide');
        }
    });
});