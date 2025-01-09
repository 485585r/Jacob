const record = document.querySelector(".record");
const output = document.querySelector(".output");
const input = document.querySelector(".input")
const vidSrc = document.querySelector("#video-source");



if (navigator.mediaDevices.getUserMedia) {

    let onMediaSetupSuccess = function (stream) {
        const mediaRecorder = new MediaRecorder(stream);
        let chunks = [];

        record.onclick = function() {
            if (mediaRecorder.state == "recording") {
                mediaRecorder.stop();
                record.classList.remove("btn-danger");
                record.classList.add("btn-primary");
            } else {
                mediaRecorder.start();
                record.classList.remove("btn-primary");
                record.classList.add("btn-danger");
            }
        }

        mediaRecorder.ondataavailable = function (e) {
            chunks.push(e.data);
        }

        mediaRecorder.onstop = function () {
            let blob = new Blob(chunks, {type: "audio/webm"});
            chunks = [];

            let formData = new FormData();
            formData.append("audio", blob);

            fetch("/transcribe", {
                method: "POST",
                body: formData
            }).then((response) => response.json())
            .then((data) => {

                input.innerHTML = data.input;
                output.innerHTML = data.output;

                fetch('http://localhost:5000/get-text')
                .then(response => response.json())
                .then(data => {
                    if (data.text) {

                        const videoPlayer = document.getElementById('video-player');


                        // Update the video source
                        vidSrc.src = data.text;

                        // Reload the video player with the new source
                        videoPlayer.load();
                    } else {
                        alert('No video URL returned from the server.');
                    }
                })
                .catch(error => console.error('Error:', error));


            })
        }
    }

    let onMediaSetupFailure = function(err) {
        alert(err);
    }

    navigator.mediaDevices.getUserMedia({ audio: true}).then(onMediaSetupSuccess, onMediaSetupFailure);

} else {
    alert("getUserMedia is not supported in your browser!")
}