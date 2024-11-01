// Traffic class name mapping
const trafficClassNames = {
    'congested_traffic': 'Congested Traffic',
    'light_traffic': 'Light Traffic',
    'heavy_traffic': 'Heavy Traffic',
    'moderate_traffic': 'Moderate Traffic',
    'no_traffic': 'No Traffic'
};

document.addEventListener('DOMContentLoaded', () => {
    const videoUploadForm = document.getElementById('upload-form');
    const imageInput = document.getElementById('upload-file-image');
    const imageSubmit = document.getElementById('image-submit');
    const imageFileNameDisplay = document.getElementById('image-file-name');
    const videoInput = document.getElementById('upload-file-video');
    const videoFileNameDisplay = document.getElementById('video-file-name');
    const videoResultDiv = document.getElementById('result');
    const imageProgressBox = document.getElementById('image-progress-box');
    const videoProgressBox = document.getElementById('video-progress-box');

    // Update file name display when an image is selected
    imageInput.addEventListener('change', () => {
        const file = imageInput.files[0];
        imageFileNameDisplay.textContent = file ? `Selected file: ${file.name}` : '';
    });

    // Update file name display when a video is selected
    videoInput.addEventListener('change', () => {
        const file = videoInput.files[0];
        videoFileNameDisplay.textContent = file ? `Selected file: ${file.name}` : '';
    });

    // Handle video upload
    videoUploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        videoProgressBox.style.display = 'block'; // Show the progress box
        updateProgress(0, videoProgressBox); // Initialize progress bar

        const formData = new FormData(videoUploadForm);
        const xhr = new XMLHttpRequest();
        xhr.open('POST', videoUploadForm.action, true);

        // Update progress event
        xhr.upload.addEventListener('progress', (event) => {
            if (event.lengthComputable) {
                const percentage = Math.round((event.loaded / event.total) * 100);
                updateProgress(percentage, videoProgressBox); // Update video progress bar
            }
        });

        xhr.onload = async () => {
            videoProgressBox.style.display = 'none'; // Hide the progress box after completion

            if (xhr.status >= 200 && xhr.status < 300) {
                const data = JSON.parse(xhr.responseText);
                displayVideoPredictionResults(data, videoResultDiv); // Pass videoResultDiv to the function
            } else {
                videoResultDiv.innerHTML = '<h2>Error processing video</h2>';
            }
        };

        xhr.onerror = () => {
            console.error('Error uploading video');
            videoResultDiv.innerHTML = '<h2>Error uploading video</h2>';
            videoProgressBox.style.display = 'none'; // Hide the progress box after completion
        };

        xhr.send(formData); // Send the form data
    });

    // Image prediction functionality
    imageSubmit.addEventListener('click', async (event) => {
        event.preventDefault(); // Prevent default form submission
        const file = imageInput.files[0];
        if (!file) {
            alert('Please select an image.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            imageProgressBox.style.display = 'block'; // Show the progress box
            updateProgress(0, imageProgressBox); // Initialize progress for image

            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/api/v1/predict-image/', true);

            // Update progress event for image
            xhr.upload.addEventListener('progress', (event) => {
                if (event.lengthComputable) {
                    const percentage = Math.round((event.loaded / event.total) * 100);
                    updateProgress(percentage, imageProgressBox); // Update image progress bar
                }
            });

            xhr.onload = () => {
                imageProgressBox.style.display = 'none'; // Hide progress box after completion

                if (xhr.status >= 200 && xhr.status < 300) {
                    const data = JSON.parse(xhr.responseText);
                    displayImagePredictionResults(data);
                } else {
                    alert('Error predicting image.');
                }
            };

            xhr.onerror = () => {
                console.error('Error uploading image');
                alert('Error uploading image');
                imageProgressBox.style.display = 'none'; // Hide progress box
            };

            xhr.send(formData); // Send the form data
        } catch (error) {
            console.error('Error:', error);
            alert('Error uploading image');
        }
    });
});

// Function to update the progress bar
function updateProgress(percentage, progressBox) {
    const progressText = progressBox.querySelector('.progress-percent');
    const progressBar = progressBox.querySelector('.progress-bar');
    progressText.textContent = `${percentage}%`;
    progressBar.style.width = `${percentage}%`; // Update the width for the visual bar
}

// Function to display prediction results for the video
function displayVideoPredictionResults(data, videoResultDiv) {
    const counts = data.counts;
    let highestCountLabel = '';
    let highestCountValue = 0;

    for (const [label, count] of Object.entries(counts)) {
        if (count > highestCountValue) {
            highestCountValue = count;
            highestCountLabel = label;
        }
    }

    // Use the mapping to display the friendly name
    const displayLabel = trafficClassNames[highestCountLabel] || highestCountLabel;

    // Display the results
    videoResultDiv.innerHTML = `<h2>Prediction Results</h2>
                                <p>Most Predicted Traffic Condition: <b>${displayLabel}</b> (${highestCountValue} times)</p>`;
}

// Function to display prediction results for the image
function displayImagePredictionResults(data) {
    const prediction = data.prediction;

    // Display the prediction result
    const predictionText = document.getElementById('prediction-text');
    const predictionResultDiv = document.getElementById('prediction-result');

    const displayLabel = trafficClassNames[prediction] || prediction;

    predictionText.textContent = `${displayLabel}`;
    predictionResultDiv.style.display = 'block'; // Show the prediction result section
}
