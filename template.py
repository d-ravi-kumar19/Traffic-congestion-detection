import os

# Define the directory structure
directories = [
    "app",
    "app/api",
    "app/models",
    "app/services",
    "app/utils",
    "logs",
    "uploads",
    "outputs",
    "templates"
]

# Function to create directories
def create_directories():
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)  # Create directory if it doesn't exist
            print(f"Directory '{directory}' created successfully.")
        except Exception as e:
            print(f"Error creating directory '{directory}': {e}")

# Function to create initial files (optional)
def create_initial_files():
    with open("app.py", "w") as f:
        f.write("# Main application file\n")
        f.write("from fastapi import FastAPI\n\n")
        f.write("app = FastAPI()\n\n")
        f.write("@app.get('/')\n")
        f.write("async def home():\n")
        f.write("    return {'message': 'Welcome to the Traffic Congestion Prediction API'}\n")
    
    with open("logging_config.py", "w") as f:
        f.write("# Logging configuration\n")

    with open("model_utils.py", "w") as f:
        f.write("# Model utility functions\n")

    with open("optimized_video_processing.py", "w") as f:
        f.write("# Optimized video processing functions\n")

    print("Initial files created.")

if __name__ == "__main__":
    create_directories()
    create_initial_files()
