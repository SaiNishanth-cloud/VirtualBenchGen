import os
import time
import cv2
from flask import Flask, render_template, Response, request

app = Flask(__name__)
sub = cv2.createBackgroundSubtractorMOG2()  # create background subtractor


@app.route('/')
def index():
    """Video upload page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    """Video processing and streaming."""
    # Get the uploaded file from the request
    file = request.files['video']

    # Save the uploaded file
    video_path = 'uploaded_video.mp4'
    file.save(video_path)

    return Response(gen(video_path), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen(video_path):
    """Video streaming generator function."""
    cap = cv2.VideoCapture(video_path)

    # Read until video is completed
    while cap.isOpened():
        ret, frame = cap.read()  # import image
        if not ret:  # if video finishes, break the loop
            break

        # Your existing image processing code here...
        fgmask = sub.apply(frame)  # use background subtraction
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # kernel for morphology
        closing = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        dilation = cv2.dilate(opening, kernel)
        retvalbin, bins = cv2.threshold(dilation, 220, 255, cv2.THRESH_BINARY)  # remove shadows
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        minarea = 400
        maxarea = 50000
        for i in range(len(contours)):  # cycle through all contours in the current frame
            if hierarchy[0, i, 3] == -1:  # consider only parent contours (contours not within others)
                area = cv2.contourArea(contours[i])  # area of contour
                if minarea < area < maxarea:  # area threshold for contour
                    # calculate centroid of contour
                    cnt = contours[i]
                    M = cv2.moments(cnt)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    # get bounding points of contour to create rectangle
                    x, y, w, h = cv2.boundingRect(cnt)
                    # create a rectangle around contour
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # print centroid coordinates
                    cv2.putText(frame, str(cx) + "," + str(cy), (cx + 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, .3,
                                (0, 0, 255), 1)
                    cv2.drawMarker(frame, (cx, cy), (0, 255, 255), cv2.MARKER_CROSS, markerSize=8, thickness=3,
                                   line_type=cv2.LINE_8)

        # Encode the processed frame to JPEG format and yield it
        encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame + b'\r\n'
        time.sleep(0.1)

    # Release the video capture and close any open windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
