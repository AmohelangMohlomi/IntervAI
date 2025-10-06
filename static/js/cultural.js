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
                category: "cultural"  
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
 document.getElementById("go-home").addEventListener("click", function () {
        window.location.href = "/home";
    });

document.getElementById("start-recording").addEventListener("click", async function () {
    try {
        const response = await fetch("/start_recording", {
            method: "POST"
        });

        const data = await response.json();

        if (data.status === "Recording started") {
            const recordingId = data.recording_id;

            alert("Recording started. Please speak.");

            // Wait before polling for result (adjust delay based on silence threshold)
            setTimeout(async () => {
                const res = await fetch(`/get_transcription?recording_id=${recordingId}`);
                const transcriptionData = await res.json();

                if (transcriptionData.transcription) {
                    document.getElementById("text-answer").value = transcriptionData.transcription;
                } else if (transcriptionData.status === "pending") {
                    alert("Still processing. Please try again in a few seconds.");
                } else {
                    alert("No audio transcription available.");
                }
            }, 7000);  // 7 seconds for silence threshold + recognition time
        }
    } catch (error) {
        console.error("Recording failed:", error);
        alert("An error occurred while starting recording.");
    }
});
