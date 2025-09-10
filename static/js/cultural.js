document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("start-recording").addEventListener("click", function () {
        alert("Recording started... (hook into your speech recognition logic here)");
    });

   
    document.getElementById("get-feedback").addEventListener("click", function () {
        const userAnswer = document.getElementById("text-answer").value.trim();

        if (!userAnswer) {
            alert("Please type your answer or speak it before getting feedback.");
            return;
        }

        alert("Analyzing your answer... (hook up to AI feedback engine)");
    });

 
    document.getElementById("save-interview").addEventListener("click", function () {
        alert("💾 Saving your interview... (hook up to backend save logic)");
    });

 
    document.getElementById("go-home").addEventListener("click", function () {
        window.location.href = "/home"; 
    });
});
