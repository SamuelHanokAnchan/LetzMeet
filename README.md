# Friend Meetup Scheduler

A simple web application built with Flask that allows friends to schedule meetups by finding overlapping free time slots.

## Features

- Submit your name, day of the week, and available time range
- View all submitted availability entries
- Automatically calculates overlapping time slots for each day
- Simple and intuitive interface
- Easy setup and deployment

## Project Structure

```
friend-meetup-scheduler/
│
├── app.py                  # Main Flask application
├── availability_data.json  # Data storage file (created automatically)
├── templates/
│   └── index.html         # HTML template for the application
└── README.md              # This file
```

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone this repository or download the files

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required packages:
   ```bash
   pip install flask
   ```

## Running Locally

1. Make sure you're in the project directory and your virtual environment is activated

2. Create a templates directory and place the index.html file inside it:
   ```bash
   mkdir templates
   # Now copy index.html into the templates directory
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

4. Open your web browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## Deployment Options

### Deploying to PythonAnywhere (Free Option)

1. Sign up for a free account at [PythonAnywhere](https://www.pythonanywhere.com/)

2. Upload your files:
   - Go to the "Files" tab
   - Create necessary directories and upload your files

3. Set up a new web app:
   - Go to the "Web" tab
   - Click "Add a new web app"
   - Choose "Flask" and select the appropriate Python version
   - Set the path to your Flask app: `/home/yourusername/path/to/app.py`

4. Add your virtual environment path if you're using one

5. Configure the WSGI file to point to your application

### Deploying to Heroku

1. Create a `requirements.txt` file:
   ```bash
   pip freeze > requirements.txt
   ```

2. Create a `Procfile` with the following content:
   ```
   web: gunicorn app:app
   ```

3. Add gunicorn to your requirements:
   ```bash
   pip install gunicorn
   echo "gunicorn==21.2.0" >> requirements.txt
   ```

4. Create a new Heroku app and deploy using Git or the Heroku CLI

### Deploying to Render (Free Option)

1. Sign up for a free account at [Render](https://render.com/)

2. Create a new Web Service
   - Connect your repository or upload files
   - Choose Python as the environment
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `gunicorn app:app`

## Customization

- You can customize the appearance by modifying the CSS in the `index.html` file
- To add more features, modify the Flask application in `app.py`

## Notes

- This application uses a simple JSON file for data storage, which is suitable for demonstration or personal use
- For production use with multiple users, consider using a proper database like SQLite, PostgreSQL, or MongoDB

## License

This project is released under the MIT License.