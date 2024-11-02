import os
import tempfile
import time
from typing import Dict
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.models.model_utils import select_model, load_model_weights
from app.services.video_service import VideoService
from app.services.frame_service import FrameService
from app.utils.logging_config import setup_logging
from app.constants import NUM_CLASSES, TRAFFIC_CLASSES, EFNET_INPUT_SHAPE, EFNET

router = APIRouter()

# Model initialization
input_shape = EFNET_INPUT_SHAPE
num_classes = NUM_CLASSES
model_name = EFNET
classes = TRAFFIC_CLASSES
model = select_model(model_name, input_shape, num_classes)
model.set_weights(load_model_weights(model_name))

# Setup logging
server_logger, model_logger = setup_logging()

# Response model for video prediction
class PredictionResponse(BaseModel):
    counts: Dict[str, int]
    total_time: float
    average_frame_time: float
    total_frames_processed: int
    metadata: dict

# Response model for frame prediction
class FramePredictionResponse(BaseModel):
    prediction: str
    metadata: dict

@router.get("/health/")
async def health_check():
    # Health check endpoint
    return {"status": "Healthy"}

@router.get("/model-info/")
async def model_info():
    # Endpoint to retrieve model information
    return {"model_name": model_name, "input_shape": input_shape, "num_classes": num_classes, "traffic_classes": classes}

@router.get("/traffic-classes/")
async def traffic_classes():
    # Endpoint to get the list of traffic classes
    return {"classes": classes}

@router.post("/predict-video/", response_model=PredictionResponse)
async def predict_video(file: UploadFile = File(...)):
    # Predict traffic from a video file
    if not file.filename.endswith(('.mp4', '.avi', '.mov')):
        model_logger.error("Invalid file format received.")
        return JSONResponse(content={"message": "Invalid file format"}, status_code=400)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        video_file_path = temp_video.name
        temp_video.write(file.file.read())  # Write uploaded video to temporary file

    request_received_time = time.time()
    try:
        video_service = VideoService(model)
        prediction_results = video_service.process_video(video_file_path, target_fps=1)  # Process the video
    except Exception as e:
        model_logger.error(f"Error during video processing: {str(e)}")
        return JSONResponse(content={"message": "Error during video processing", "error": str(e)}, status_code=500)
    finally:
        try:
            os.remove(video_file_path)  # Clean up temporary video file
        except Exception as e:
            model_logger.error(f"Error deleting temporary video file: {str(e)}")

    response_sent_time = time.time()
    metadata = {
        "request_received_time": request_received_time,
        "response_sent_time": response_sent_time,
        "processing_duration": prediction_results["total_time"]
    }

    # Return prediction results
    return JSONResponse(content={
        "counts": prediction_results["predictions_count"],
        "total_time": prediction_results["total_time"],
        "average_frame_time": prediction_results["frame_time"],
        "total_frames_processed": prediction_results["total_frames"],
        "metadata": metadata
    })

@router.post("/predict-image/", response_model=FramePredictionResponse)
async def predict_frame(file: UploadFile = File(...)):
    # Predict traffic from a single frame image
    if not file.filename.endswith(('.jpg', '.jpeg', '.png')):
        model_logger.error("Invalid file format received.")
        return JSONResponse(content={"message": "Invalid file format"}, status_code=400)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_frame:
        frame_file_path = temp_frame.name
        temp_frame.write(file.file.read())  # Write uploaded frame to temporary file

    request_received_time = time.time()
    try:
        frame_service = FrameService(model)
        label, frame_metadata = frame_service.process_frame(frame_file_path=frame_file_path)  # Process the frame
    except Exception as e:
        model_logger.error(f"Error during frame processing: {str(e)}")
        return JSONResponse(content={"message": "Error during frame processing", "error": str(e)}, status_code=500)
    finally:
        try:
            os.remove(frame_file_path)  # Clean up temporary frame file
        except Exception as e:
            model_logger.error(f"Error deleting temporary frame file: {str(e)}")

    response_sent_time = time.time()
    metadata = {
        "request_received_time": request_received_time,
        "response_sent_time": response_sent_time,
    }

    # Return frame prediction result
    return JSONResponse(content={
        "prediction": label,
        "metadata": metadata
    })
