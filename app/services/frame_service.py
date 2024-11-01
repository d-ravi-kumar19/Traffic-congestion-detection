import numpy as np
import cv2
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input
from app.constants import  TRAFFIC_CLASSES


class FrameService:
    def __init__(self, model):
        self.model = model
        self.classes = TRAFFIC_CLASSES

    def process_frame(self, frame_file_path: str):
        """Process a single frame image for traffic congestion prediction."""
        # Read the image from the file path
        frame = cv2.imread(frame_file_path)
        if frame is None:
            raise ValueError("Could not read the image from the given path.")

        # Resize and preprocess frame
        frame_resized = cv2.resize(frame, (229, 229))
        frame_array = img_to_array(frame_resized) / 255.0  # Normalize
        processed_frame = preprocess_input(np.expand_dims(frame_array, axis=0))

        # Make prediction
        prediction = self.model.predict(processed_frame)
        class_id = np.argmax(prediction)
        label = self.classes[class_id]

        return label, {"additional_info": "Example info"}  # Customize additional metadata as needed
