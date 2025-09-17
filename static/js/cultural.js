document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("start-recording").addEventListener("click", function () {
        alert("Recording started... (hook into your speech recognition logic here)");
    });

    document.getElementById("get-feedback").addEventListener("click", async function () {
        const userAnswer = document.getElementById("text-answer").value.trim();
        const question = document.querySelector(".question-text").textContent.trim();

        if (!userAnswer) {
            alert("Please type your answer or speak it before getting feedback.");
            return;
        }

        try {
            // Show some feedback to user while waiting (optional)
            // For example: disable button or show spinner

            const response = await fetch("/get_feedback", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ question, answer: userAnswer })
            });

            const data = await response.json();

            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            } else if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                alert("Failed to get feedback.");
            }

        } catch (error) {
            console.error("Error getting feedback:", error);
            alert("Something went wrong while getting feedback.");
        }
    });

    document.getElementById("save-interview").addEventListener("click", function () {
        alert("💾 Saving your interview... (hook up to backend save logic)");
    });

    document.getElementById("go-home").addEventListener("click", function () {
        window.location.href = "/home";
    });
});
