# Image Metadata Viewer (Flask)
![alt text](https://files.catbox.moe/f11xqf.jpg)

A simple Flask web app to extract and display image metadata (EXIF), including GPS latitude/longitude when available. Upload a photo in the browser and see its metadata rendered in a friendly format.


## Features

- Upload a JPG/PNG image and view its EXIF metadata
- Extracts GPS coordinates and converts them to decimal degrees (latitude/longitude)
- Cleans tricky EXIF value types (bytes, rational numbers, lists, dicts) for display
- Deletes the uploaded file immediately after processing; no images are stored on disk
- Minimal UI using a single page (`/`)


## Tech stack

- Python, Flask
- Pillow (PIL) for image/EXIF parsing
- HTML/CSS/JS served from `templates/` and `static/`


## Quickstart (Windows / PowerShell)

Prerequisites: Python 3.10+ installed and available on PATH.


## How to use

1. Visit the homepage.
2. Choose an image (JPG/PNG typically have EXIF; screenshots often do not).
3. Submit the form. The app:
   - Saves the file temporarily to `uploads/`
   - Reads EXIF using Pillow
   - Extracts/normalizes values (including GPS to decimal degrees)
   - Immediately deletes the file
   - Renders the metadata on the same page

Note: Not all images contain EXIF metadata. If the image lacks EXIF, the output may be empty or minimal.


## Project structure

```
app.py               # Flask app: single route for GET/POST upload + rendering
metadata.py          # EXIF utilities, GPS extraction and value normalization
requirements.txt     # Python dependencies
static/              # JS, CSS
templates/           # Jinja templates (index.html)
uploads/             # Temp folder for uploads (files are deleted after reading)
```


## Deployment notes

- Production WSGI (Linux):

```bash
pip install -r requirements.txt
```

```bash
gunicorn -w 2 -b 0.0.0.0:8000 app:app
```


## Troubleshooting

- "cannot identify image file": The file might not be a supported image, or it’s corrupted. Try a standard JPEG from a camera/phone.
- No GPS data: Many images don’t include location data (e.g., screenshots). Ensure location services were enabled when the photo was taken.
- PowerShell cannot run Activate.ps1: Temporarily allow scripts in the current session:
- Permissions on `uploads/`: Ensure the app has permission to create and delete files in the project directory.


## Security considerations

- Uploaded files are saved with a sanitized name and deleted immediately after processing.
- This sample does not enforce file size limits or content-type validation. For production, consider:
  - Max upload size via Flask config / reverse proxy
  - Content-type and extension checks
  - Scanning files or using in-memory processing only

