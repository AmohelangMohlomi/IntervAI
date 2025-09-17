document.getElementById("get-feedback").addEventListener("click", async function () {
    const userAnswer = document.getElementById("text-answer").value.trim();
    const question = document.querySelector(".question-text").textContent.trim();

    if (!userAnswer) {
        alert("Please type your answer or speak it before getting feedback.");
        return;
    }

    try {
        const response = await fetch("/get_feedback", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ 
                question, 
                answer: userAnswer,
                category: "technical"  
            })
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
