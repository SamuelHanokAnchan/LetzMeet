# Friend Meetup Scheduler

![MIT License](https://img.shields.io/badge/License-MIT-green.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple)

A lightweight web application to solve the age-old problem of finding common free time slots among friends for meetups and events.


## 🌟 Features

- **Multi-day Selection**: Users can select multiple days of availability at once
- **Week Planning**: Schedule across three different time frames - Current Week, Next Week, or Week After Next
- **Full Day Option**: Quick selection for entire day availability
- **Overlap Detection**: Automatically finds and displays common available time slots
- **Mobile Friendly**: Responsive design works seamlessly on phones, tablets, and desktops
- **Real-time Feedback**: Clear visual indication of when everyone is available
- **User Management**: Easily add or remove individual availability entries

## 🚀 Live Demo

Check out the live demo: [Friend Meetup Scheduler](https://friend-meetup-scheduler.onrender.com)

## 💻 Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **Hosting**: Render (Free Tier)

## 📋 Usage

1. Enter your name
2. Select the week you're available
3. Choose one or more days of the week
4. Enter your available time range (or select "Available all day")
5. Click "Add Availability"

The app will automatically find and display overlapping time slots - times when everyone is free. When all participants have a common time slot, a special notification appears.

## 🛠️ Installation and Setup

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/friend-meetup-scheduler.git
cd friend-meetup-scheduler

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Then visit `http://127.0.0.1:5000` in your browser.

### Deployment

The application is ready to deploy on platforms like Render, Heroku, or PythonAnywhere:

```bash
# Make sure requirements.txt is up to date
pip freeze > requirements.txt
```

For Render, you can simply connect your GitHub repository and the platform will automatically detect and deploy your Flask application.

## 📝 How It Works

The Friend Meetup Scheduler uses a simple algorithm to find overlapping availability:

1. Each user submits their available days and time ranges
2. For each day, the app finds the latest start time and earliest end time among all users
3. If the latest start time is before the earliest end time, there's an overlap
4. Common time slots are displayed, grouped by day and week
5. When all users have a common time, a special notification is shown

Data is stored in a simple JSON file, making this application lightweight and easy to deploy.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Bootstrap](https://getbootstrap.com/) - UI framework
- [Font Awesome](https://fontawesome.com/) - Icons
- [Render](https://render.com/) - Hosting platform

---

Made with ❤️ to solve real-world scheduling problems
