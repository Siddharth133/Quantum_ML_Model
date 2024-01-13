from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np

class_names = ['Clams', 'Corals', 'Crabs', 'Dolphin', 'Eel', 'Fish', 'Jelly Fish', 'Lobster', 'Nudibranchs', 'Octopus', 'Otter', 'Penguin', 'Puffers', 'Sea Rays', 'Sea Urchins', 'Seahorse', 'Seal', 'Sharks', 'Shrimp', 'Squid', 'Starfish', 'Turtle_Tortoise', 'Whale']

class QuantumLikeLayer(tf.keras.layers.Layer):

    def _init_(self, num_qubits, trainable=True):
        super(QuantumLikeLayer, self)._init_(trainable=trainable)
        self.num_qubits = num_qubits
        self.hadamard_gate = self.create_hadamard_gate()
        self.cz_gate = self.create_cz_gate()

    def create_hadamard_gate(self):
        H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=np.float64)
        hadamard_full = H
        for _ in range(1, self.num_qubits):
            hadamard_full = np.kron(hadamard_full, H)
        return tf.linalg.LinearOperatorFullMatrix(hadamard_full)

    def create_cz_gate(self):
        CZ = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]], dtype=np.float64)
        cz_full = CZ
        for _ in range(2, self.num_qubits):
            cz_full = np.kron(cz_full, np.eye(2, dtype=np.float64))
        return tf.linalg.LinearOperatorFullMatrix(cz_full)

    def call(self, inputs):
        inputs = tf.cast(inputs, tf.float64)
        state = self.hadamard_gate.matvec(inputs)
        state = self.cz_gate.matvec(state)
        return state
image_height = 299
image_width = 299

train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

path = "dataset"
batch_size = 20
training_data = train_datagen.flow_from_directory(
    path,
    target_size=(image_height, image_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

validation_data = val_datagen.flow_from_directory(
    path,
    target_size=(image_height, image_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)


inception_model = Sequential()
pretrained_model = tf.keras.applications.InceptionV3(include_top=False,
                                                     input_shape=(image_height, image_width, 3),
                                                     pooling='avg',
                                                     weights='imagenet')
for layer in pretrained_model.layers[:-4]:
    layer.trainable = False


num_qubits = 11
inception_model.add(pretrained_model)
inception_model.add(Flatten())
inception_model.add(Dense(2**num_qubits, activation='relu'))
inception_model.add(Dropout(0.5))  # Dropout added
inception_model.add(QuantumLikeLayer)
inception_model.add(Dense(512, activation='relu'))
inception_model.add(Dense(23, activation='softmax'))  # Number of classes

# Compile the model
inception_model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=['accuracy'])

# Early Stopping and Model Checkpointing
early_stopping = EarlyStopping(monitor='val_loss', patience=5)
model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_accuracy', save_best_only=True)

epochs = 5
history = inception_model.fit(
    training_data,
    validation_data=validation_data,
    epochs=epochs,
    callbacks=[early_stopping, model_checkpoint]
)


img_path = 'dataset/Corals/10465606544_52913a3632_o.jpg'
img = image.load_img(img_path, target_size=(299, 299))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)


predictions = inception_model.predict(img_array)
predicted_class = np.argmax(predictions, axis=1)
print(predicted_class)
print(class_names[predicted_class[0]])