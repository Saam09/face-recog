from flask import Flask, render_template, request, redirect, url_for
import cv2
import os

app = Flask(__name__)
camera = cv2.VideoCapture(0)


def capture_frame():
    # Read a frame from the camera
    _, frame = camera.read()
    return frame


def generate_frames():
    while True:
        frame = capture_frame()

        # Convert the frame to JPEG format
        _, jpeg = cv2.imencode('.jpg', frame)

        # Yield the frame as an HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        # Do something with the entered URL if needed

        return redirect(url_for('video_feed'))
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture', methods=['POST'])
def capture():
    frame = capture_frame()

    # Specify the path to the 'static/img' folder
    img_folder = os.path.join(app.root_path, 'static', 'img')

    # Save the captured frame as an image inside the 'static/img' folder
    img_path = os.path.join(img_folder, 'captured_image.jpg')
    cv2.imwrite(img_path, frame)
    
    return 'Image captured successfully!'


if __name__ == '__main__':
    app.run(debug=True)
