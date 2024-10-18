# RealSense D455 Strawberry Maturity Capture

This project enables capturing images using the Intel RealSense D455 RGBD Camera and categorizing strawberries based on their ripeness. The captured images can be saved into separate folders according to the ripeness level, facilitating future machine learning model training.

## Features

- Capture images of strawberries with the Intel RealSense D455 RGBD Camera.
- Classify strawberry maturity into four categories:
  1. **Mature**
  2. **Immature**
  3. **Overripe** (slightly rotten)
  4. **Bitten by insects**
- Store images in different directories based on their classification for easy access during the training process.

## Requirements

To run this program, you will need the following:

- **Python 3.8**
- **OpenCV**: Used for image processing and display.
- **pyrealsense2**: A library to interface with the Intel RealSense cameras.
