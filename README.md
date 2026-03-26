
# Face Attendance System 📸✅

An automated attendance management system using **Face Recognition** and **Computer Vision**. This project identifies individuals from a live camera feed and logs their attendance in real-time.

## 🚀 Features
* **Real-Time Detection:** High-speed face detection and identification.
* **Automated Logging:** Saves attendance data (Name, Date, Time) into a CSV file or Database.
* **Multiple Face Support:** Capable of recognizing multiple registered users simultaneously.
* **Accuracy:** Built on top of the state-of-the-art `face_recognition` library (99.38% accuracy on LFW).

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Libraries:** * `OpenCV`: For image processing and camera handling.
    * `face_recognition`: For facial encoding and matching.
    * `Pandas/NumPy`: For data manipulation.
    * `Tkinter/PyQt` (Optional): For the GUI.

## 📁 Project Structure

- `images/`: Stores images of authorized personnel.
- `attendance.csv`: The output file where attendance is recorded.
- `main.py`: The entry point of the application.
