document.addEventListener("DOMContentLoaded", function () {
    const introText = "Initializing IntervAI...";
    const introElement = document.getElementById("intro-text");
    const loadingFill = document.getElementById("loading-fill");
    const mainContent = document.getElementById("main-content");
    const aiIntro = document.getElementById("ai-intro");
    const bgImage = document.getElementById("bg-image");

    let i = 0;
    const speed = 60;

    function typeWriter() {
        if (i < introText.length) {
            introElement.innerHTML += introText.charAt(i);
            const progress = i / introText.length;

            // Update loading bar width
            loadingFill.style.width = `${progress * 100}%`;

            // Gradually reduce blur from 20px to 0, and increase opacity 0.3 to 1
            const blurValue = 20 - progress * 20; // 20 to 0
            const opacityValue = 0.3 + progress * 0.7; // 0.3 to 1

            bgImage.style.filter = `blur(${blurValue}px) brightness(0.5)`;
            bgImage.style.opacity = opacityValue;

            i++;
            setTimeout(typeWriter, speed);
        } else {
            loadingFill.style.width = "100%";

            // Finalize blur & opacity
            bgImage.style.filter = "blur(0px) brightness(0.8)";
            bgImage.style.opacity = "1";

            setTimeout(() => {
                // Add class to body to switch background from image to neon black-blue gradient
                document.body.classList.add("question-active");

                // Hide the intro container
                aiIntro.style.display = "none";

                // Show main content container
                mainContent.classList.remove("hidden");
                mainContent.classList.add("fade-in");
            }, 1000);
        }
    }

    typeWriter();
});
