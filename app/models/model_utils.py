# model_utils.py

import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0, InceptionV3
import pickle
import os
from dotenv import load_dotenv

load_dotenv()

local_model_path = os.getenv("LOCAL_MODEL_PATH")

# Define model paths
MODEL_PATHS = {
    "EFNET": local_model_path,
}

def select_model(model_name, input_shape, num_classes):
    """
    Select and create a model architecture based on the specified model name.

    Args:
        model_name (str): The name of the model to create, e.g., "EFNET" or "INCEPTv3".
        input_shape (tuple): The input shape for the model.
        num_classes (int): The number of output classes for the model.

    Returns:
        tf.keras.Model: The compiled model with the specified architecture and output classes.
    """
    if model_name == "EFNET":
        base_model = EfficientNetB0(include_top=False, weights=None, input_shape=input_shape)
    elif model_name == "INCEPTv3":
        base_model = InceptionV3(include_top=False, weights=None, input_shape=input_shape)
    else:
        raise ValueError(f"Model '{model_name}' not recognized.")

    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])

    return model

def load_model_weights(model_name):
    """
    Load the model weights from a file for a specified model.

    Args:
        model_name (str): The name of the model to load weights for, e.g., "EFNET".

    Returns:
        list: The loaded weights for the model.

    Raises:
        ValueError: If the weights file for the specified model is not found.
    """
    model_path = MODEL_PATHS.get(model_name)
    if model_path is None or not os.path.exists(model_path):
        raise ValueError(f"Weights file for '{model_name}' not found.")

    with open(model_path, 'rb') as f:
        weights = pickle.load(f)
    return weights
