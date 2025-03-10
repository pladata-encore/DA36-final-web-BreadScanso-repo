document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const selectedTemplate = urlParams.get("template");
    const previewContainer = document.getElementById("preview-container");

    if (selectedTemplate) {
        previewContainer.style.display = "grid";
    }

    // "템플릿 선택" 버튼 클릭 시, 다시 첫 화면으로 이동
    document.getElementById("show-templates-btn").addEventListener("click", function () {
        window.location.href = "/store/store_home_edit/";
    });

    // 저장 버튼 클릭 시 동작
    document.getElementById("save-btn").addEventListener("click", function () {
        alert("저장되었습니다!");
    });
});
