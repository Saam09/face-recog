import os
import base64
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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

    # Generate a unique filename for the captured frame
    filename = "captured_frame.jpg"
    counter = 1
    while os.path.exists(os.path.join("static", "img", filename)):
        filename = f"captured_frame_{counter}.jpg"
        counter += 1

    # Save the captured frame to the static/img folder
    with open(os.path.join("static", "img", filename), "wb") as f:
        f.write(image_bytes)

    return "Image saved"


if __name__ == "__main__":
    app.run()
