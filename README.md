# ArUco Marker Tool <img src="logo.png" alt="ArUco Marker Tool Logo" width="30"/>

The ArUco Marker Tool is an application built using KivyMD and OpenCV for detecting and visualizing ArUco markers in live camera streams or multimedia files.

#### Warning: Do not try uploading media bigger than 1000 pixels; it may freeze the app or significantly slow performance. Feel free to fork and fix this issue.

## About ArUco markers
https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html

All you need to do is print them out or use them from the templates folder

Generate here: https://chev.me/arucogen/

## Features

- **Live Camera Broadcast:** View real-time camera feed with ArUco marker detection.
- **ArUco Dictionary Selection:** Choose ArUco dictionaries for marker detection.
- **File Management:** Select image or video files for ArUco marker processing.
- **Frame Augmentation:** Augment frames with selected media files.
- **Capture Frames:** Make screenshots by pressing the button in the middle.
  
### Getting Started

- Clone the repository:

   ```bash
   git clone https://github.com/yehorderehus/ArUco-Marker-Tool
   ```

- Optionally, create a virtual environment with name `venv`:

   ```bash
   python -m venv venv
   ```

- ..activate the virtual environment. On Unix or MacOS:
   ```bash
   source venv/bin/activate
   ```
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

- Install dependencies (from the root of the repository)

   ```bash
   pip install -r requirements.txt
   ```

- Run the application. On Unix or MacOS:

   ```bash
   python3 user_app.py
   ```
   On Windows:
   ```bash
   python user_app.py
   ```

### Feedback
Click Rate App in application menu to rate the app. You can also submit experience or report bugs.

### Contributing
Contributions are welcome! Please feel free to submit a Pull Request. This project is intended for demonstration purposes, but in case of right ideas, it may be extended to a full-fledged application.

### License
This project is licensed under the MIT License (pretty default)

