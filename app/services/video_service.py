import cv2
import numpy as np
import threading
import queue
from keras.preprocessing.image import img_to_array
from keras.applications.efficientnet import preprocess_input
import time
from app.utils.logging_config import setup_logging
from app.constants import TRAFFIC_CLASSES

server_logger, model_logger = setup_logging()

class VideoService:
    def __init__(self, model):
        self.model = model
        if not hasattr(self.model, "predict"):
            raise ValueError("The model does not have a 'predict' method.")  # Ensure model has predict method
        self.classes = TRAFFIC_CLASSES
        self.frame_queue = queue.Queue(maxsize=10)  # Initialize a queue for frames

    def frame_extractor(self, video_file_path: str, target_fps: int = 1):
        cap = cv2.VideoCapture(video_file_path)  # Open the video file
        if not cap.isOpened():
            model_logger.error(f"Failed to open video file: {video_file_path}")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second of the video
        frame_interval = int(fps / target_fps) if target_fps <= fps else 1  # Calculate frame interval
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()  # Read a frame from the video
            if not ret:
                break  # Exit loop if no more frames are available
            if frame_count % frame_interval == 0:
                frame_resized = cv2.resize(frame, (229, 229))  # Resize frame for the model
                frame_array = img_to_array(frame_resized)  # Convert frame to array
                self.frame_queue.put(preprocess_input(frame_array))  # Preprocess and queue the frame
            frame_count += 1
        cap.release()  # Release the video capture object

    def process_video(self, video_file_path: str, target_fps: int = 1):
        extractor_thread = threading.Thread(target=self.frame_extractor, args=(video_file_path, target_fps))  # Start frame extraction
        extractor_thread.start()
        predictions_list = []
        total_time = 0
        frame_count = 0

        while extractor_thread.is_alive() or not self.frame_queue.empty():
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()  # Get a frame from the queue
                frame = np.expand_dims(frame, axis=0)  # Expand dimensions for model input
                start_time = time.time()
                prediction = self.model.predict(frame)  # Predict the class for the frame
                end_time = time.time()

                class_id = np.argmax(prediction)  # Get the predicted class ID
                label = self.classes[class_id]  # Map class ID to label
                predictions_list.append(label)  # Append the prediction to the list

                frame_time = end_time - start_time
                total_time += frame_time  # Accumulate total time taken
                frame_count += 1  # Increment frame count

        extractor_thread.join()  # Wait for the extraction thread to finish

        total_frames = len(predictions_list)  # Total number of frames processed
        predictions_count = {cls: predictions_list.count(cls) for cls in self.classes}  # Count predictions for each class

        return {
            "predictions": predictions_list,
            "total_time": total_time,
            "frame_time": total_time / frame_count if frame_count > 0 else 0,  # Average frame processing time
            "total_frames": total_frames,
            "predictions_count": predictions_count  # Count of predictions per class
        }
