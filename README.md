# UDA-Q Agent (Universal AI Data Quality Evaluator)

<img width="1024" height="338" alt="image" src="https://github.com/user-attachments/assets/3e12c4d2-c64b-4069-8246-cff0d0dc27b7" />


## Prerequisites
- Python 3.8+
- Node.js 16+

## Setup Instructions

### Backend (Django)
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000/api/`.

### Frontend (React)
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173`.

## Usage
1. Open the frontend in your browser.
2. Upload a CSV or Excel file.
3. The Agent will automatically diagnose, fix, and evaluate the dataset.
4. View the report and download the cleaned data.
