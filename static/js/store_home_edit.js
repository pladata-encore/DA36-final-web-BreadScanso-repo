document.addEventListener("DOMContentLoaded", function () {
    const templateBoxes = document.querySelectorAll(".template-box");

    templateBoxes.forEach(box => {
        box.addEventListener("click", function () {
            const selectedTemplate = this.getAttribute("data-template");

            console.log("템플릿 선택됨:", selectedTemplate);

            const detailPageUrl = `/store/store_home_edit_details/?template=${selectedTemplate}`;
            console.log("이동할 URL:", detailPageUrl);

            window.location.href = detailPageUrl;
        });
    });
});
