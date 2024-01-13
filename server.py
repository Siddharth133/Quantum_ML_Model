from flask import Flask, request, render_template
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import io

app = Flask(__name__)


model = load_model('resnet_model')

class_names = ['Clams', 'Corals', 'Crabs', 'Dolphin', 'Eel', 'Fish', 'Jelly Fish', 'Lobster', 'Nudibranchs', 'Octopus', 'Otter', 'Penguin', 'Puffers', 'Sea Rays', 'Sea Urchins', 'Seahorse', 'Seal', 'Sharks', 'Shrimp', 'Squid', 'Starfish', 'Turtle_Tortoise', 'Whale']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        file_stream = io.BytesIO(file.read())
        img = image.load_img(file_stream, target_size=(227, 227))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.

        predictions = model.predict(img_array)
        print("Predictions:", predictions)  # Debugging line

        predicted_class = np.argmax(predictions, axis=1)
        print("Predicted Class Index:", predicted_class[0])  # Debugging line
        print(class_names)
        if predicted_class.size == 0:
            return "Could not classify the image"

        if predicted_class[0] >= len(class_names):
            return "Class index out of range"

        return class_names[predicted_class[0]]


if __name__ == '__main__':
    app.run(debug=True)
