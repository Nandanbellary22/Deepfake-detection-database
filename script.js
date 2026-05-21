document.addEventListener("DOMContentLoaded", function () {
    console.log("Deepfake Detection System Loaded");

    const cards = document.querySelectorAll(
        ".stat-card, .premium-panel, .feature-card, .workflow-box"
    );

    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.08}s`;
    });

    const buttons = document.querySelectorAll(
        ".btn-submit, .btn-custom, .btn-primary"
    );

    buttons.forEach((button) => {
        button.addEventListener("mouseenter", function () {
            button.style.transform = "translateY(-3px) scale(1.02)";
        });

        button.addEventListener("mouseleave", function () {
            button.style.transform = "translateY(0) scale(1)";
        });
    });

    const fileInput = document.querySelector("input[type='file']");

    if (fileInput) {
        fileInput.addEventListener("change", function () {
            if (fileInput.files.length > 0) {
                showToast("File selected: " + fileInput.files[0].name);
            }
        });
    }

    const forms = document.querySelectorAll("form");

    forms.forEach((form) => {
        form.addEventListener("submit", function () {
            const submitButton = form.querySelector("button[type='submit']");

            if (submitButton) {
                submitButton.innerHTML =
                    '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
            }
        });
    });
});

function showToast(message) {
    const toast = document.createElement("div");

    toast.className = "custom-toast";
    toast.innerHTML = `
        <i class="fa-solid fa-circle-check"></i>
        <span>${message}</span>
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("show-toast");
    }, 100);

    setTimeout(() => {
        toast.classList.remove("show-toast");

        setTimeout(() => {
            toast.remove();
        }, 400);
    }, 3000);
}
