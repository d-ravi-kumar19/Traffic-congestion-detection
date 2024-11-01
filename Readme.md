
# Traffic Congestion Prediction Application

## Overview

This is a traffic congestion prediction application built with FastAPI, leveraging machine learning models to analyze and predict traffic conditions from video inputs. Developed as a group project under the Center of Excellence in AI & ML, it provides a robust API for processing both video and individual frame predictions.

## Features

- Upload video files to predict traffic conditions.
- Upload images to predict traffic conditions from single frames.
- Health check endpoint to verify the status of the application.
- API endpoints to retrieve model information and available traffic classes.

## Tech Stack

- **Backend Framework:** FastAPI
- **Machine Learning Library:** Keras (with TensorFlow backend)
- **Image Processing:** OpenCV
- **Containerization:** Docker
- **Environment Management:** Python 3.9
- **Logging:** Custom logging configuration
- **Deployment:** AWS S3 for model storage (optional)

## Getting Started

### Prerequisites

- Docker installed on your machine.
- Python 3.9 (if you wish to run locally outside Docker).

### Clone the Repository

```bash
git clone https://github.com/d-ravi-kumar19/traffic-congestion-prediction-app.git
cd traffic-prediction-api
```

### Build the Docker Image

```bash
docker build -t traffic-prediction-app .
```

### Run the Docker Container

```bash
docker run -d -p 8000:8000 --name traffic-prediction-api traffic-prediction-app
```

### Access the Application

The application will be accessible at `http://localhost:8000`.

### API Endpoints

- `GET /`: Home page (HTML response).
- `GET /health/`: Check application health.
- `GET /model-info/`: Get information about the model.
- `GET /traffic-classes/`: Retrieve available traffic classes.
- `POST /predict-video/`: Upload a video file to get predictions.
- `POST /predict-image/`: Upload a single image to get predictions.

## Logging

Logs are configured for both server activity and model processing, enabling easy debugging and monitoring.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.
