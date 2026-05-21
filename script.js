// ==========================================
// DEEPFAKE DETECTION REPORT SYSTEM
// FRONTEND JAVASCRIPT
// ==========================================

console.log("Deepfake Detection System Loaded Successfully");

// ==========================================
// FAKE AI SCORE GENERATOR
// ==========================================

function generateAIScore() {

    let score = Math.floor(Math.random() * 100) + 1;

    return score;
}

// ==========================================
// SIMULATED AI ANALYSIS
// ==========================================

function simulateAIAnalysis() {

    let score = generateAIScore();

    let message = "";

    if (score >= 80) {

        message =
            "High probability of deepfake content detected.";

    }

    else if (score >= 50) {

        message =
            "Suspicious media detected. Further investigation recommended.";

    }

    else {

        message =
            "Low probability of manipulation detected.";

    }

    alert(

        "AI Detection Score: " +

        score +

        "%\n\n" +

        message
    );
}

// ==========================================
// BUTTON CLICK EFFECT
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    let buttons =
        document.querySelectorAll(".btn-custom, .btn-submit");

    buttons.forEach(function (button) {

        button.addEventListener("mouseenter", function () {

            button.style.transform = "scale(1.03)";
        });

        button.addEventListener("mouseleave", function () {

            button.style.transform = "scale(1)";
        });

    });

});

// ==========================================
// FORM VALIDATION
// ==========================================

function validateForm() {

    let inputs =
        document.querySelectorAll("input[required]");

    for (let input of inputs) {

        if (input.value.trim() === "") {

            alert("Please fill all required fields.");

            return false;
        }
    }

    return true;
}

// ==========================================
// SEARCH FILTER DEMO
// ==========================================

function searchReports() {

    let input =
        document.getElementById("searchInput");

    if (!input) return;

    let filter =
        input.value.toUpperCase();

    let table =
        document.getElementById("reportTable");

    let tr =
        table.getElementsByTagName("tr");

    for (let i = 0; i < tr.length; i++) {

        let td =
            tr[i].getElementsByTagName("td")[1];

        if (td) {

            let txtValue =
                td.textContent || td.innerText;

            if (txtValue.toUpperCase().indexOf(filter) > -1) {

                tr[i].style.display = "";

            }

            else {

                tr[i].style.display = "none";
            }
        }
    }
}

// ==========================================
// NOTIFICATION DEMO
// ==========================================

function showNotification(message) {

    let notification =
        document.createElement("div");

    notification.innerText = message;

    notification.style.position = "fixed";

    notification.style.top = "20px";

    notification.style.right = "20px";

    notification.style.padding = "15px 25px";

    notification.style.background =
        "#2563eb";

    notification.style.color =
        "white";

    notification.style.borderRadius =
        "12px";

    notification.style.boxShadow =
        "0 10px 30px rgba(0,0,0,0.2)";

    notification.style.zIndex =
        "9999";

    document.body.appendChild(notification);

    setTimeout(() => {

        notification.remove();

    }, 3000);
}

// ==========================================
// PAGE LOAD NOTIFICATION
// ==========================================

window.onload = function () {

    showNotification(
        "Deepfake Detection System Loaded"
    );
};