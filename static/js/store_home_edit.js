document.addEventListener("DOMContentLoaded", function () {
    const templateContainer = document.getElementById("template-container");
    const showTemplatesBtn = document.getElementById("show-templates-btn");
    const templateBoxes = document.querySelectorAll(".template-box");
    const selectedTemplate = document.getElementById("selected-template");

    // 템플릿 버튼 클릭 시 선택지 표시
    showTemplatesBtn.addEventListener("click", function () {
        templateContainer.style.display = templateContainer.style.display === "none" ? "block" : "none";
    });

    // 템플릿 선택 기능
    templateBoxes.forEach(box => {
        box.addEventListener("click", function () {
            // 선택한 템플릿 적용
            selectedTemplate.textContent = this.getAttribute("data-template");

            // 선택지 숨기기
            templateContainer.style.display = "none";
        });
    });
});