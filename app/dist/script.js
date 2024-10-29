// Code to handle the client-side functionality of the application
(function($) {
    "use strict";

    // Cursor movement
    document.getElementsByTagName("body")[0].addEventListener("mousemove", function(n) {
        t.style.left = n.clientX + "px";
        t.style.top = n.clientY + "px";
        e.style.left = n.clientX + "px";
        e.style.top = n.clientY + "px";
        i.style.left = n.clientX + "px";
        i.style.top = n.clientY + "px";
    });
    var t = document.getElementById("cursor"),
        e = document.getElementById("cursor2"),
        i = document.getElementById("cursor3");

    function n(t) {
        e.classList.add("hover");
        i.classList.add("hover");
    }

    function s(t) {
        e.classList.remove("hover");
        i.classList.remove("hover");
    }
    s();
    for (var r = document.querySelectorAll(".hover-target"), a = r.length - 1; a >= 0; a--) {
        o(r[a]);
    }

    function o(t) {
        t.addEventListener("mouseover", n);
        t.addEventListener("mouseout", s);
    }

    // Background image movement
    var pos = 0;
    if ($(window).width() > 1200) {
        window.setInterval(function() {
            pos++;
            document.getElementsByClassName('moving-image')[0].style.backgroundPosition = pos + "px 0px";
        }, 18);
    }

    // Switch light/dark theme
    $(".switch").on('click', function() {
        if ($("body").hasClass("light")) {
            $("body").removeClass("light");
            $(".switch").removeClass("switched");
        } else {
            $("body").addClass("light");
            $(".switch").addClass("switched");
        }
    });

    $(document).ready(function() {

        // Hero case study images
        $('.slide-buttons li').on('mouseenter', function() {
            const index = $(this).index() + 1;
            $('.slide-buttons li.active').removeClass('active');
            $('.hero-center-section.show').removeClass("show");
            $(`.hero-center-section:nth-child(${index})`).addClass("show");
            $(this).addClass('active');
        });
        $('.slide-buttons li:nth-child(1)').trigger('mouseenter');
    });

    // Function to handle selection of transformation
    function selectTransformation(element) {
        console.log("Transformation selected:", element.textContent.trim()); // Debugging line

        const previouslySelected = document.querySelector(".section-dropdown-sub a.selected");
        if (previouslySelected) {
            previouslySelected.classList.remove("selected");
        }
        element.classList.add("selected");

        const imageEnhancementLabel = document.getElementById("image-enhancement-label");
        imageEnhancementLabel.innerHTML = element.textContent.trim() + ' <i class="uil uil-arrow-down"></i>';

        // Store selected transformation globally
        window.selectedTransformation = element.textContent.trim();
    }
    window.selectTransformation = selectTransformation;

    // Image upload and submission functionality
    // Image upload and submission functionality
document.getElementById("submit-button").addEventListener("click", async function() {
    const fileInput = document.getElementById("file-upload");
    const processedImage = document.getElementById("processed-image");
    const originalImage = document.getElementById("original-image");
    const tvShowSlider = document.getElementById("tv-show-slider");
    const instructions = document.getElementById("instructions");
    const imageContainer = document.getElementById("image-container");
	const sideButtons = document.getElementById("side-buttons");

    if (fileInput.files.length === 0) {
        alert("Please upload an image.");
        return;
    }

    // Check if a transformation was selected
    if (!window.selectedTransformation) {
        alert("Please select a transformation.");
        return;
    }
    const transformation = window.selectedTransformation;

	// Hide the side buttons
    if (sideButtons) {
        sideButtons.style.display = "none";
    }

    const file = fileInput.files[0];
    const url = URL.createObjectURL(file);
    originalImage.src = url;
    originalImage.style.display = "block";

    tvShowSlider.style.display = "none";
    instructions.style.display = "none"; // Hide the instructions text

    const formData = new FormData();
    formData.append("file", file);
    formData.append("transformation", transformation);

    try {
        const response = await fetch("/process-image", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const blob = await response.blob();
            const processedUrl = URL.createObjectURL(blob);
            processedImage.src = processedUrl;
            processedImage.style.display = "block";

            // Display the image container after successful submission
            imageContainer.style.display = "flex";
        } else {
            alert("Failed to process the image. Please try again.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    }
});

})(jQuery);
