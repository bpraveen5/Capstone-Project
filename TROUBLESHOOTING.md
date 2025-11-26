# Troubleshooting "Localhost Refused to Connect"

If you are seeing `ERR_CONNECTION_REFUSED`, it means the web server is not running. This usually happens if the installation failed or the start command encountered an error.

## Step 1: Check the Command Windows
When you ran `run_app.bat`, two black command windows should have opened.
- **Window 1 (Backend)**: Should say `Starting development server at http://127.0.0.1:8000/`
- **Window 2 (Frontend)**: Should say `Local: http://localhost:5173/`

**If these windows closed immediately**, there was an error. Proceed to Step 2.

## Step 2: Run Manually (To see errors)
Try running the commands manually in a terminal (PowerShell or Command Prompt) to see what's going wrong.

### 1. Start Backend
Open a terminal in the `Capstone-Project` folder and run:
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
*If this fails, do you see an error about "python not found" or "pip not recognized"?*

### 2. Start Frontend
Open a **new** terminal in the `Capstone-Project` folder and run:
```bash
cd frontend
npm install
npm run dev
```
*If this fails, do you see an error about "npm not recognized"?*

## Common Issues
1.  **Python/Node not installed**: Ensure you have installed Python and Node.js on your computer.
2.  **Dependencies failed**: Sometimes `npm install` fails due to network issues. Try running it again.
3.  **Port in use**: If port 5173 or 8000 is taken, the startup log will tell you the new port (e.g., 5174).
