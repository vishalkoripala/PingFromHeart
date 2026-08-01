Aura Love Heart
================

This small Python application draws an animated heart and displays a user-provided image and message.

Requirements
------------
- Python 3.9+
- Pillow (for image handling)
- (Optional) PyInstaller to create a standalone executable

Quick start (run from source)
-----------------------------
1. Create a virtual environment and install dependencies:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the app (GUI prompts will ask for text and image):

```powershell
python love.py
```

3. Run with command-line arguments (skips GUI prompts):

```powershell
python love.py "Happy Anniversary" "C:\path\to\image.jpg"
```

Run the web app (browser)
------------------------
This repository also includes a small Flask-based web UI so the app can be used from a browser. After creating the virtual environment and installing dependencies (see Quick start), start the web server:

PowerShell (development):

```powershell
$env:FLASK_APP='app.py'
$env:FLASK_ENV='development'
flask run --host=0.0.0.0 --port=5000
```

Or run with Gunicorn for a production-like server:

```powershell
gunicorn app:app -b 0.0.0.0:5000
```

Open `http://localhost:5000` in a browser. The live demo is available at https://pingfromheart.onrender.com


Build a Windows executable
--------------------------
1. Install PyInstaller (already in `requirements.txt`):

```powershell
pip install pyinstaller
```

2. Run the build script:

```powershell
build_exe.bat
```

3. The single-file executable will be in the `dist` folder as `AuraLove.exe`.

Distribution suggestions
------------------------
- Upload the built `AuraLove.exe` to GitHub Releases for easy sharing.
- Include the `requirements.txt` so users can run from source.

Deploy to the web (so anyone can access via browser)
--------------------------------------------------
1. Containerized deployment (recommended): a `Dockerfile` is included. You can build and push the image to GitHub Container Registry (GHCR) or Docker Hub, then configure a host (Render, Railway, Fly.io) to run it.

2. GitHub Actions: a workflow is included at `.github/workflows/build-and-push-image.yml` that builds and publishes an image to GHCR on pushes to `main`.

3. Quick host setup (Render):
	- Create a Render Web Service and connect it to this GitHub repository.
	- Choose "Docker" or "Web Service" and set the start command to use `gunicorn app:app` (port 5000).
	- Render will deploy automatically on pushes.

4. Security: if you expose the server publicly, consider adding rate-limiting, file-size limits, and virus scanning for uploads.

Automated deploy to Render using GitHub Actions
----------------------------------------------
This repo includes a GitHub Actions workflow at `.github/workflows/deploy-to-render.yml` that:

- builds and pushes a Docker image to GHCR on push to `main` and
- triggers a Render deploy via the Render API.

To enable automatic deploys to Render:

1. Create a Render Web Service for a Docker/web service and copy its **Service ID**.
2. Create an API key on Render (Service or Account API Key) and copy it.
3. In your GitHub repository, add two repository secrets:
	- `RENDER_SERVICE_ID` — the Render service ID
	- `RENDER_API_KEY` — your Render API key

When you push to `main`, the workflow will publish the image and trigger a deploy. Your Render service URL will be the public demo link (e.g. `https://your-service.onrender.com`).

Live demo URL
-------------
https://pingfromheart.onrender.com

If you prefer a different host (Fly, Railway, AWS), I can add deployment steps for that provider.

Notes
-----
- The app uses `tkinter` and `turtle` so it runs as a desktop GUI application. It is not a web app.
- For cross-platform packaging consider `pyinstaller` on each target OS (Windows, macOS, Linux).
