from flask import Flask, request, render_template_string, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    download_progress = 0
    file_url = None
    message = None

    if request.method == "POST":
        url = request.form.get("url")
        quality = request.form.get("quality")
        is_audio = 'audio' in request.form

        try:
            # Configure yt-dlp options based on input
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',  # Save with title and extension
                'format': 'best' if quality == 'best' else quality,  # Set format based on quality
                'progress_hooks': [lambda d: progress_hook(d, download_progress)]
            }

            # If the user wants to download audio (mp3), set the format accordingly
            if is_audio:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegAudioConvertor',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=True)
                file_name = ydl.prepare_filename(result)

            # Provide a download link for the file
            file_url = f"/download/{file_name}"
            message = "Download ready!"

            return render_template_string(template, message=message, file_url=file_url, download_progress=100)

        except Exception as e:
            # Handle errors
            message = f"Error: {str(e)}"
            return render_template_string(template, message=message, download_progress=0)

    return render_template_string(template, message=message, file_url=file_url, download_progress=download_progress)


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)


def progress_hook(d, download_progress):
    if d['status'] == 'downloading':
        percent = d['downloaded_bytes'] / d['total_bytes'] * 100
        download_progress = round(percent)
        print(f"Download Progress: {download_progress}%")
    return download_progress

# HTML template for the app
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Video Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 20px;
            text-align: center;
        }
        h1 {
            color: #4CAF50;
            margin-bottom: 20px;
        }
        form {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 400px;
            margin: 0 auto;
        }
        input[type="text"], select {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 2px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        input[type="checkbox"] {
            margin-right: 10px;
        }
        button {
            width: 100%;
            padding: 14px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .message {
            color: green;
            font-weight: bold;
            margin-top: 20px;
        }
        .error {
            color: red;
        }
        .download-link {
            margin-top: 20px;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #ddd;
            border-radius: 5px;
            margin: 20px 0;
            display: none;
        }
        .progress-bar div {
            height: 100%;
            width: 0;
            background-color: #4CAF50;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>YouTube Video Downloader</h1>
    <form action="/" method="POST">
        <input type="text" name="url" placeholder="Enter YouTube video URL" required>
        <label for="quality">Select Video Quality:</label>
        <select name="quality" id="quality">
            <option value="best">Best Quality</option>
            <option value="1080p">1080p</option>
            <option value="720p">720p</option>
        </select>
        <label for="audio">
            <input type="checkbox" name="audio" id="audio"> Download as Audio (MP3)
        </label>
        <button type="submit">Download</button>
    </form>

    {% if message %}
        <p class="message">{{ message }}</p>
    {% endif %}
    
    {% if file_url %}
        <div class="download-link">
            <p>Click <a href="{{ file_url }}" download>here</a> to download the file.</p>
        </div>
    {% endif %}

    {% if download_progress %}
        <div class="progress-bar">
            <div style="width: {{ download_progress }}%;"></div>
        </div>
    {% endif %}
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
