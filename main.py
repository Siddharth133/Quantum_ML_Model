import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.python.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import tensorflow_quantum as tfq
import tensorflow as tf
import cirq
import sympy
import random
import matplotlib.pyplot as plt
import numpy as np

image_height = 227
image_weight = 227
batch_size = 20
path ='dataset'

training_data = tf.keras.preprocessing.image_dataset_from_directory(
    path,
    batch_size=batch_size,
    image_size=(image_height, image_weight),

    shuffle=True,
    seed=123,
    validation_split=0.3,
    subset='training'

)

validation_data = tf.keras.preprocessing.image_dataset_from_directory(
    path,
    batch_size=batch_size,
    image_size=(image_height, image_weight),

    shuffle=True,
    seed=123,
    validation_split=0.3,
    subset='validation'

)




# Define a simple quantum circuit as your quantum layer
def create_quantum_circuit():
    # Define qubits
    qubits = cirq.GridQubit.rect(1, 5)  # Assuming 5 qubits as per the previous encoding

    # Define a simple circuit
    circuit = cirq.Circuit()
    circuit.append([cirq.H(qubit) for qubit in qubits])  # Apply Hadamard gates
    circuit.append(cirq.CZ(qubits[0], qubits[1]))  # Apply a CZ gate for entanglement

    return circuit


# Create a Keras layer that can apply this quantum circuit to quantum data
class QuantumLayer(tf.keras.layers.Layer):
    def _init_(self, circuit):
        super(QuantumLayer, self)._init_()
        self.circuit = circuit
        self.qubits = cirq.GridQubit.rect(1, 5)
        self.q_model = tfq.layers.PQC(circuit, operators=cirq.Z(self.qubits[-1]))

    def call(self, inputs):
        return self.q_model(inputs)


# Create the quantum circuit
quantum_circuit = create_quantum_circuit()

# Add the quantum layer to your model
quantum_layer = QuantumLayer(quantum_circuit)

resnet_model = Sequential()

pretrained_model= tf.keras.applications.ResNet50(include_top=False,
                   input_shape=(227,227,3),
                   pooling='avg',classes=23,
                   weights='imagenet')
for layer in pretrained_model.layers:
        layer.trainable=False

resnet_model.add(pretrained_model)
resnet_model.add(Flatten())
resnet_model.add(Dense(512, activation='relu'))
resnet_model.add(Dense(23, activation='softmax'))