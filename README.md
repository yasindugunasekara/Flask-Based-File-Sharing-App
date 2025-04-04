# FileSharing-App

## Overview
FileSharing-App is a Flask-based file-sharing web application that allows users to upload, preview, and download various file types securely. It supports images, PDFs, text files, videos, and more, with unique file handling to prevent duplication.

## Features
- **Secure File Uploads**: Supports multiple file types with validation.
- **File Preview**: Displays images and provides icons for other file types.
- **Downloadable Files Section**: Lists files available for download.
- **Duplicate File Handling**: Renames files to avoid overwriting.
- **User-Friendly Interface**: Simple and responsive UI for easy file management.

## Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Storage**: Local file system

## Installation
### Prerequisites
- Python 3.x
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/FileSharing-App.git
   cd FileSharing-App
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python app.py
   ```
4. Open your browser and go to `http://localhost:5000`.

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Render the upload form and display files |
| `/upload` | POST | Upload files securely |
| `/get_downloadable_files` | GET | Retrieve downloadable files |
| `/uploads/<filename>` | GET | Serve uploaded files |
| `/downloads/<filename>` | GET | Serve downloadable files |

## How to Use
1. Open the web application in your browser.
2. Click the "Upload" button to select files from your device.
3. View uploaded files with preview support for images and icons for other formats.
4. Download files by clicking the "Download" button next to each file.

## Technology Used
- **Flask**: Backend framework for handling requests and responses.
- **HTML, CSS, JavaScript**: Frontend for user interaction.
- **Werkzeug**: Secure filename handling.
- **OS Module**: File storage and directory management.

## Use Cases
- **Personal File Storage**: Store and access files easily.
- **Team Collaboration**: Share files securely with team members.
- **Document Management**: Manage and retrieve important documents efficiently.
- **Media Sharing**: Upload and share images, videos, and other media files.

