# Chessboard Detector and Warper

This repository contains a Python script that detects the outer boundary of a chessboard in an image using contour detection, applies a perspective transform to obtain a top-down view, and saves the output as an 800×800 JPEG file. It supports common image formats and is designed to help with image preprocessing tasks for chessboard images.

## Features

- **Chessboard detection:** Uses contour detection to locate the largest quadrilateral (assumed to be the chessboard border).
- **Perspective warping:** Warps the detected board to a top-down view with a resolution of 800×800 pixels.
- **Multi-format support:** Processes images with extensions such as JPG, JPEG, PNG, BMP.
- **Command-line interface:** Easily process multiple images from an input directory and save them to an output directory.

## Input and Output Example

This program transforms images as follows:

**Input Image:**

![IMG_2243](https://github.com/user-attachments/assets/fc5c3fab-2998-4063-b977-5171ae74eea4)


**Output Image:**

![IMG_2243_cropped jpg 17-30-33-664](https://github.com/user-attachments/assets/8c668d15-49a1-4037-bfb6-f6f09a2a698c)


## Installation

### Using Pip

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/chessboard-detector.git
   cd chessboard-detector
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` should include at least:

   ```txt
   opencv-python
   numpy
   ```

### Using Conda

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/chessboard-detector.git
   cd chessboard-detector
   ```

2. **Create a new Conda environment:**

   ```bash
   conda create -n chessboard_env python=3.8 --yes
   conda activate chessboard_env
   ```

3. **Install the required packages using Conda (via conda-forge for up-to-date packages):**

   ```bash
   conda install -c conda-forge opencv numpy
   ```

## Usage

### Configuring and Running the Script

Before running the script, open the `run` file and fill in the correct paths for your input and output directories:

```bash
#!/bin/bash

# Set the paths for your input and output directories.
INPUT_DIR="/path/to/your/input_images"
OUTPUT_DIR="/path/to/your/output_images"

# Name of the Python script file.
SCRIPT_NAME="script.py"

# Run the Python script with the specified directories.
python "$SCRIPT_NAME" --input_dir "$INPUT_DIR" --output_dir "$OUTPUT_DIR"
```

Once the paths are set, make the script executable (only required once):

```bash
chmod +x run
```

Then, execute the script with:

```bash
./run
```

Alternatively, you can run the script manually:

```bash
python script.py --input_dir /path/to/your/input_images --output_dir /path/to/your/output_images
```

The script will search for image files in the input directory, detect the chessboard, warp it to a top-down 800×800 view, and save the processed images with the suffix `_cropped.jpg` in the output directory.

