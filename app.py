from flask import Flask, request, send_from_directory, jsonify, render_template_string
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set upload folder, download folder, and allowed extensions
UPLOAD_FOLDER = "uploads"
DOWNLOAD_FOLDER = "downloads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "bmp", "webp", "pdf", "txt", "docx", "zip", "mp4", "mp3", "wav", "avi", "mov"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_unique_filename(filename):
    """Avoid file overwriting by renaming duplicates"""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(UPLOAD_FOLDER, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename

def get_file_size(filename, folder):
    """Get file size in MB (rounded to 2 decimal places)"""
    size_in_bytes = os.path.getsize(os.path.join(folder, filename))
    size_in_mb = size_in_bytes / (1024 * 1024)
    return f"{size_in_mb:.2f}"

def get_preview_url(filename, folder):
    """Generate the preview for the file (like an image thumbnail or PDF icon)"""
    ext = filename.rsplit(".", 1)[1].lower()
    if ext in {"jpg", "jpeg", "png", "gif", "bmp", "webp"}:
        return f"/{folder}/{filename}"  # Image preview
    elif ext == "pdf":
        return "/static/pdf-icon.png"  # PDF icon
    elif ext in {"txt", "docx", "zip"}:
        return "/static/file-icon.png"  # Generic file icon
    elif ext == "mp4":
        return "/static/video-icon.png"  # Video icon (optional, you can customize as needed)
    else:
        return "/static/file-icon.png"  # Default file icon

@app.route("/")
def upload_form():
    """Render the upload form and display uploaded files"""
    files = os.listdir(UPLOAD_FOLDER)
    file_list = "".join(
        f"<div class='file-card'>"
        f"<div class='file-preview'>"
        f"<img src='{get_preview_url(file, 'uploads')}' alt='Preview' class='preview-image'>"
        f"</div>"
        f"<div class='file-info'>"
        f"<p class='file-name'><a href='/uploads/{file}'>{file}</a></p>"
        f"<p class='file-size'>{get_file_size(file, UPLOAD_FOLDER)} MB</p>"
        f"</div>"
        f"<a href='/uploads/{file}' download><button class='btn-download'>Download</button></a>"
        f"</div>"
        for file in files
    )

    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Upload</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Roboto', sans-serif; background-color: #f4f7fc; text-align: center; padding: 50px 0; }
            h2 { margin-bottom: 20px; color: #333; }
            .container { max-width: 900px; margin: 0 auto; background-color: #fff; border-radius: 10px; padding: 40px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
            input, button { padding: 15px; margin: 10px 0; border-radius: 5px; border: 1px solid #ccc; width: 100%; max-width: 300px; }
            button { background-color: #4CAF50; color: white; cursor: pointer; }
            button:hover { background-color: #45a049; }
            .file-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; margin-top: 30px; }
            .file-card { background: #fff; border-radius: 8px; padding: 20px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); text-align: center; }
            .file-preview { margin-bottom: 10px; }
            .preview-image { width: 100px; height: 100px; object-fit: cover; border-radius: 8px; }
            .file-info { margin-top: 10px; }
            .file-info a { text-decoration: none; color: #333; font-weight: 500; }
            .file-name { margin: 10px 0; font-weight: bold; }
            .file-size { font-size: 0.9em; color: #777; }
            .btn-download { margin-top: 10px; padding: 10px 20px; background-color: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; }
            .btn-download:hover { background-color: #0056b3; }
            .progress-container { width: 100%; height: 20px; background-color: #e0e0e0; border-radius: 10px; margin-top: 30px; display: none; }
            .progress-bar { height: 100%; background-color: #4caf50; width: 0; border-radius: 10px; }
            .error-message { color: red; font-weight: bold; margin-top: 10px; }
            hr { margin: 40px 0; border-top: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Upload Files</h2>
            <form id="uploadForm">
                <input type="file" id="files" name="files" multiple required>
                <button type="submit">Upload</button>
            </form>

            <div id="progress-container" class="progress-container">
                <div id="progress-bar" class="progress-bar"></div>
            </div>

            <div id="error-message" class="error-message"></div>

            <h3>Uploaded Files</h3>
            <div class="file-list" id="file-list">''' + file_list + '''</div>

            <hr>

            <h3>Downloadable Files</h3>
            <button id="downloadableBtn">Show Downloadable Files</button>
            <div class="file-list" id="downloadable-files" style="display:none;"></div>
        </div>

        <script>
            document.getElementById("uploadForm").addEventListener("submit", function(event) {
                event.preventDefault();

                var formData = new FormData();
                var files = document.getElementById("files").files;
                for (var i = 0; i < files.length; i++) {
                    formData.append("files", files[i]);
                }

                var xhr = new XMLHttpRequest();
                xhr.open("POST", "/upload", true);

                xhr.onload = function() {
                    if (xhr.status === 200) {
                        location.reload();  // Reload the page to display new files
                    } else {
                        document.getElementById("error-message").innerHTML = xhr.responseText;
                    }
                };

                xhr.send(formData);
            });

            document.getElementById("downloadableBtn").addEventListener("click", function() {
                var xhr = new XMLHttpRequest();
                xhr.open("GET", "/get_downloadable_files", true);
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        document.getElementById("downloadable-files").style.display = "grid";
                        document.getElementById("downloadable-files").innerHTML = xhr.responseText;
                    } else {
                        alert("Failed to load downloadable files.");
                    }
                };
                xhr.send();
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handles file uploads with security and duplicate filename handling"""
    if "files" not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist("files")
    if not files or all(file.filename == "" for file in files):
        return jsonify({"error": "No selected file"}), 400

    uploaded_files = []
    for file in files:
        if file.filename == "": continue

        if not allowed_file(file.filename):
            return jsonify({"error": f"File type not allowed: {file.filename}"}), 400

        filename = secure_filename(file.filename)
        unique_filename = get_unique_filename(filename)
        file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
        uploaded_files.append(unique_filename)

    return jsonify({"message": "Files uploaded successfully", "files": uploaded_files}), 200

@app.route("/get_downloadable_files")
def get_downloadable_files():
    """Return downloadable files from the downloads folder with previews"""
    download_files = os.listdir(DOWNLOAD_FOLDER)
    file_list = "".join(
        f"<div class='file-card'>"
        f"<div class='file-preview'>"
        f"<img src='{get_preview_url(file, 'downloads')}' alt='Preview' class='preview-image'>"
        f"</div>"
        f"<div class='file-info'>"
        f"<p class='file-name'><a href='/downloads/{file}'>{file}</a></p>"
        f"<p class='file-size'>{get_file_size(file, DOWNLOAD_FOLDER)} MB</p>"
        f"</div>"
        f"<a href='/downloads/{file}' download><button class='btn-download'>Download</button></a>"
        f"</div>"
        for file in download_files
    )
    return file_list

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/downloads/<filename>")
def download_file(filename):
    """Serve downloadable files"""
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
