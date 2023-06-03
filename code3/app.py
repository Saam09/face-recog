import os
import base64
import face_recognition
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Load the face images and encode them
known_faces = []
faces_dir = "static/faces"
for filename in os.listdir(faces_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(faces_dir, filename)
        face_image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(face_image)[0]
        known_faces.append(face_encoding)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")
        # You can perform any necessary processing with the URL here

        # Redirect to the "Face Authentication" page and pass the URL as a parameter
        return redirect(url_for("face_authentication", url=url))

    return render_template("index.html")


@app.route("/face-authentication")
def face_authentication():
    url = request.args.get("url")
    # Access the URL passed as a parameter and display it on the page

    return render_template("face_authentication.html", url=url)


@app.route("/save-image", methods=["POST"])
def save_image():
    data = request.get_json()
    image_data = data["image"]

    # Decode base64 image data
    image_bytes = base64.b64decode(image_data.split(",")[1])

    # Set the filename for the captured frame
    filename = "captured_frame.jpg"

    # Save the captured frame to the static/img folder, overwriting the existing file
    with open(os.path.join("static", "img", filename), "wb") as f:
        f.write(image_bytes)

    # Perform face matching logic here
    result = perform_face_matching(filename)

    # Redirect to the result page and pass the matching result as a parameter
    return redirect(url_for("result", result=result))


@app.route("/result")
def result():
    result = request.args.get("result")
    # Display the face matching result on the result page

    return render_template("result.html", result=result)


def perform_face_matching(filename):
    # Load the captured frame
    captured_frame = face_recognition.load_image_file(
        os.path.join("static", "img", filename)
    )
    captured_encodings = face_recognition.face_encodings(captured_frame)

    if len(captured_encodings) > 0:
        captured_encoding = captured_encodings[0]

        # Compare the captured frame encoding with the known face encodings
        matches = face_recognition.compare_faces(known_faces, captured_encoding)
        if any(matches):
            return "Match"
        else:
            return "No Match"
    else:
        return "No Faces Detected"


if __name__ == "__main__":
    app.run()
