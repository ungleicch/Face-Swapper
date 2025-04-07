# Face Swapper Program

## Overview
This program provides a face swapping feature using computer vision and machine learning techniques. It allows users to select faces from two different images and swap them. The program uses OpenCV, InsightFace, Tkinter, and PIL for image processing and graphical user interface.

## Dependencies
- OpenCV (`cv2`)
- NumPy (`numpy`)
- InsightFace (`insightface`)
- Tkinter (`tkinter`)
- Python Imaging Library (PIL)

## Model Download
- The `inswapper` model used in this program can be downloaded from the following link: [inswapper model](https://drive.google.com/file/d/1krOLgjW2tAPaqV-Bw4YALz0xT5zlb5HF/view)

## Features
- **Face Detection**: Detects faces in images using InsightFace.
- **Face Selection**: Interactive GUI for selecting which faces to swap.
- **Face Swapping**: Swaps selected faces between two images.
- **Image Sharpening**: Applies high boost sharpening to the swapped faces.
- **Image Saving**: Save the result to a file.

## Functions
- `sharpen_highboost(image, alpha, sigma)`: Sharpens the image using high boost filtering.
- `select_face(img_path, app, msg)`: Allows user to select a face from an image.
- `swap_faces(source_img_path, target_img_path, app, swapper)`: Performs the face swapping process.
- `open_file_dialog(title)`: Opens a file dialog for image selection.

## Usage
1. Run the program.
2. Select the source image (the face to be copied).
3. Select the target image (the face to be replaced).
4. Follow the on-screen instructions to select faces and apply the swap.
5. Optionally apply sharpening to the swapped faces.
6. Save the output image.

## Notes
- Ensure all dependencies are installed.
- Font file `Arial.ttf` is required in the program directory for proper GUI display.
- The program uses a Tkinter interface for interaction and OpenCV for image processing.

## Author
~ungleicch
