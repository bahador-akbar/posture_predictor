from flask import Flask, render_template, Response
import cv2
from posture_detector import PostureDetector
from datetime import datetime
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask import send_file

app = Flask(__name__)
detector = PostureDetector()
bad_posture_count = 0
total_frames = 0

# اگر فایل لاگ وجود نداشت، ایجاد کن
if not os.path.exists('logs/posture_log.csv'):
    with open('logs/posture_log.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Posture'])

def gen_frames():
    global bad_posture_count, total_frames

    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            total_frames += 1
            frame, posture = detector.detect(frame)

            # ذخیره در لاگ
            with open('logs/posture_log.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), posture])

            # شمارش وضعیت بد
            if posture == 'Bad':
                bad_posture_count += 1

            ret , buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    if total_frames == 0:
        bad_percentage = 0
    else:
        bad_percentage = round((bad_posture_count / total_frames) * 100, 2)
    return render_template('index.html', bad=bad_percentage)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/report')
def report():
    try:
        df = pd.read_csv('logs/posture_log.csv')
        df['Time'] = pd.to_datetime(df['Time'])
        df['Hour'] = df['Time'].dt.hour
        hourly_report = df.groupby(['Hour', 'Posture']).size().unstack().fillna(0)

        # رسم نمودار
        fig, ax = plt.subplots()
        hourly_report.plot(kind='bar', stacked=True, ax=ax, color={'Good': 'green', 'Bad': 'red'})
        plt.title("Hourly Posture Report")
        plt.xlabel("Hour of Day")
        plt.ylabel("Number of Frames")
        plt.tight_layout()

        # تبدیل به تصویر Base64 برای نمایش
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template('report.html', plot_url=plot_url)

    except Exception as e:
        return f"<h3>Error in generating report: {str(e)}</h3>"


@app.route('/download')
def download_csv():
    path = "logs/posture_log.csv"
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)