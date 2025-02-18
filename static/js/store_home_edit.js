document.addEventListener("DOMContentLoaded", function () {
    const templateContainer = document.getElementById("template-container");
    const showTemplatesBtn = document.getElementById("show-templates-btn");
    const templateBoxes = document.querySelectorAll(".template-box");
    const templateEditor = document.getElementById("template-editor");
    const templateInput = document.getElementById("template-input");
    const previewContainer = document.getElementById("preview-container");
    const editMenuBtn = document.getElementById("edit-menu-btn");
    const saveBtn = document.getElementById("save-btn");

    // 템플릿 버튼 클릭 시 선택지 표시/숨김
    showTemplatesBtn.addEventListener("click", function () {
        templateContainer.style.display = templateContainer.style.display === "none" ? "block" : "none";
    });

    // 템플릿 선택 기능
    templateBoxes.forEach(box => {
        box.addEventListener("click", function () {
            // 템플릿 편집창 활성화
            templateEditor.style.display = "block";

            // 기존 선택 초기화
            templateBoxes.forEach(b => b.classList.remove("selected"));
            this.classList.add("selected");

            // 선택한 템플릿 내용을 가져와서 편집창에 설정
            const selectedText = this.getAttribute("data-template");
            templateInput.value = selectedText;
            previewContainer.textContent = selectedText; // 미리보기 업데이트

            // 선택지 숨기기
            templateContainer.style.display = "none";
        });
    });

    // 템플릿 입력창에서 수정할 때 미리보기 업데이트
    templateInput.addEventListener("input", function () {
        previewContainer.textContent = templateInput.value;
    });

    // 수정 버튼
    editMenuBtn.addEventListener("click", function () {
            window.location.href = "#";
    });

    // 저장 버튼
    saveBtn.addEventListener("click", function () {
            window.location.href = "store";
    });
});