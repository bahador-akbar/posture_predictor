# 🧍‍♂️️ Real-Time Posture Detection System A real-time posture detection web app built with *OpenCV, Flask, and Python. This application uses computer vision to analyze posture via webcam feed and provides a visual report along with real-time bad posture alerts. --- ## 🚀 Features - 📸 Real-time video feed using webcam - ✅ Classifies posture as Good or Bad - 📈 Generates hourly posture report (bar chart) - 📥 Logs posture data in CSV format - 🔔 Plays an alert sound when bad posture is detected (optional) - 🌐 Web-based interface using Flask --- ## 🛠️ Technologies Used - Python - OpenCV - Flask - Matplotlib - Pandas - HTML/CSS (Flask Templates) --- ## 📁 Project Structure 

├── app.py # Main Flask application ├── posture_detector.py # Posture detection logic ├── templates/ │ ├── index.html # Main UI │ └── report.html # Report view ├── static/ │ └── alert.mp3 # Optional sound alert ├── logs/ │ └── posture_log.csv # Logged posture data

--- ## ▶️ How to Run 1. Clone the repository: ```bash git clone https://github.com/bahador-akbar/posture-predictor.git cd posture-detector-app 

Install dependencies:

pip install -r requirements.txt 

Run the Flask app:

python app.py 

Open your browser and go to:

http://127.0.0.1:5000 

📊 Report View

Access /report to see a bar chart of posture status grouped by hours of the day.

📥 Download CSV

Access /download to download the posture data as a CSV file.

✅ To Do

Improve model accuracy using deep learning

Add user login system

Extend analytics features

Mobile responsive UI

📸 Screenshots

(Add images of your interface here if available)

🔒 License

This project is licensed under the MIT License.

👤 Author

Developed by [Akbar Bahador].

Feel free to connect and contribute!
