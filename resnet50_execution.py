import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.python.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
image_height = 227
image_weight = 227
batch_size = 20
path ='dataset'

training_data = tf.keras.preprocessing.image_dataset_from_directory(
    path,
    batch_size = batch_size,
    image_size =(image_height,image_weight),

    shuffle = True,
    seed =123,
    validation_split =0.3,
    subset ='training'

    )


validation_data =tf.keras.preprocessing.image_dataset_from_directory(
    path,
    batch_size = batch_size,
    image_size =(image_height,image_weight),

    shuffle = True,
    seed =123,
    validation_split =0.3,
    subset ='validation'

    )



class QuantumLikeLayer(tf.keras.layers.Layer):
    def __init__(self, num_qubits, trainable=True):
        super(QuantumLikeLayer, self).__init__(trainable=trainable)

        self.num_qubits = num_qubits
        self.hadamard_gate = self.create_hadamard_gate()
        self.cz_gate = self.create_cz_gate()
    def get_config(self):
        config = super(QuantumLikeLayer, self).get_config()
        config.update({
            'num_qubits': self.num_qubits,
        })
        return config
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

num_qubits = 11
quantum_like_layer = QuantumLikeLayer(num_qubits, trainable=False)
input_state = tf.constant(np.ones(2**num_qubits, dtype=np.float64))
output_state = quantum_like_layer(input_state)

resnet_model = Sequential()

pretrained_model = tf.keras.applications.ResNet50(
    include_top=False,
    input_shape=(227, 227, 3),
    pooling='avg',
    classes=23,
    weights='imagenet'
)

for layer in pretrained_model.layers:
    layer.trainable = True

resnet_model.add(pretrained_model)
resnet_model.add(Flatten())

num_qubits = 11
resnet_model.add(Dense(2**num_qubits))

resnet_model.add(quantum_like_layer)
resnet_model.add(Dense(512, activation='relu'))
resnet_model.add(Dense(23, activation='softmax'))


resnet_model.compile(loss='sparse_categorical_crossentropy', optimizer=tf.optimizers.SGD(lr=0.001), metrics=['accuracy'])



epochs=10
history = resnet_model.fit(
  training_data,
  validation_data=validation_data,
  epochs=epochs
)


class_names = training_data.class_names
print(class_names)
img = image.load_img('dataset/Sea Urchins/10032795986_14e543bbca_o.jpg', target_size=(227, 227))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.
predictions = resnet_model.predict(img_array)
predicted_class = np.argmax(predictions, axis=1)
print(predicted_class)
print(class_names[predicted_class[0]])