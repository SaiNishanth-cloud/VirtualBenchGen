from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
import os

# Create a Flask application
app = Flask(__name__)


# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')


# Define the route for the upload page
@app.route('/upload', methods=['POST'])
def upload():
    # Get the video file from the user
    file = request.files['file']
    # Save the file to a temporary location
    filename = file.filename
    uploads_dir = os.path.join(app.root_path, 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    file_path = os.path.join(uploads_dir, filename)
    file.save(file_path)
    # Read the video file
    cap = cv2.VideoCapture(file_path)
    # Create a background subtraction object
    fgbg = cv2.createBackgroundSubtractorMOG2()
    # Read the first frame
    ret, frame = cap.read()
    # Initialize the background
    fgbg.apply(frame)
    # Loop over the frames
    while True:
        # Read the next frame
        ret, frame = cap.read()
        if not ret:
            break
        # Apply the background subtraction algorithm
        fgmask = fgbg.apply(frame)
        # Detect the pedestrians in the foreground
        contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Draw the contours on the frame
        for contour in contours:
            cv2.drawContours(frame, contour, -1, (0, 255, 0), 2)
        # Check if the frame has valid dimensions
        if frame.shape[0] > 0 and frame.shape[1] > 0:
            # Display the frame
            cv2.imshow('Frame', frame)
        # Check if the user wants to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the VideoCapture object
    cap.release()
    # Close all windows
    cv2.destroyAllWindows()
    # Redirect the user to the results page
    return redirect(url_for('results'))


# Define the route for the results page
@app.route('/results')
def results():
    return "Results page"


if __name__ == '__main__':
    app.run()
