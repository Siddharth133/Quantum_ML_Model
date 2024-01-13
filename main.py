from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np


# Inception Model Implementation

inception_model = load_model('inception_model')
class_names = ['Clams', 'Corals', 'Crabs', 'Dolphin', 'Eel', 'Fish', 'Jelly Fish', 'Lobster', 'Nudibranchs', 'Octopus', 'Otter', 'Penguin', 'Puffers', 'Sea Rays', 'Sea Urchins', 'Seahorse', 'Seal', 'Sharks', 'Shrimp', 'Squid', 'Starfish', 'Turtle_Tortoise', 'Whale']
img = image.load_img('dataset/Sea Urchins/10032795986_14e543bbca_o.jpg', target_size=(299, 299))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.
predictions = inception_model.predict(img_array)
predicted_class = np.argmax(predictions, axis=1)
print(predicted_class)
print(class_names[predicted_class[0]])


