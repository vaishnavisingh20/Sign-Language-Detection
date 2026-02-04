## Sign Language Detection
Sign Language Detection is a project for detecting and recognizing hand signs (such as alphabet gestures) using computer vision and machine learning. It uses hand keypoint extraction and classification to interpret sign language from real-time video or collected images.
Features

1. Real-time sign gesture detection
2. Uses webcam video input
3. Dataset collection support
4. Hand landmark detection for classification
5. Simple architecture to extend for custom gestures

Repository Structure
Sign-Language-Detection/
├── Data/                # Collected training images or dataset
├── Model/               # Pretrained model (e.g., .h5)
├── Test.py              # Test and inference script
├── data_collection.py   # Script to collect hand gesture images
├── requirements.txt     # List of project dependencies
└── README.md            # This file

Getting Started

These steps will help you run the project locally.

1. Clone the repository
```bash
git clone https://github.com/vaishnavisingh20/Sign-Language-Detection.git
cd Sign-Language-Detection
```
3. Create and activate a Python virtual environment

Windows
```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```
Collecting Gesture Data (Optional)

If the project includes data_collection.py to collect images:
```bash
python data_collection.py
```

Follow on-screen instructions to record hand sign images for training.

Running Inference

After dataset/model setup:
```bash
python Test.py
```

This script should start the webcam and attempt to recognize live gesture input.
