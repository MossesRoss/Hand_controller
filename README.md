# Hand Tracking Python Project

## Description
This project is a Python-based hand tracking system that utilizes the MediaPipe library and other related libraries. It provides real-time hand tracking and gesture recognition capabilities, allowing you to track and analyze hand movements from various sources such as a webcam or recorded videos.

## Features
- **Real-time hand tracking**: The project uses the MediaPipe library to track and locate the positions of the user's hands in real-time.
- **Gesture recognition**: It includes gesture recognition functionality, enabling you to recognize predefined hand gestures such as a thumbs-up or a peace sign.
- **Multiple input sources**: You can use different input sources, such as a webcam or pre-recorded videos, to analyze hand movements.
- **Easy integration**: The project is written in Python, making it easy to integrate into your existing Python projects or applications.
- **Customizable**: You can customize the project to fit your specific needs by adjusting parameters, adding new gestures, or extending the functionality as desired.

## Requirements
To run this project, you need to have the following libraries installed:
- Python (3.7 or higher)
- MediaPipe
- OpenCV
- NumPy

## Installation
1. Clone the repository to your local machine using the following command:
   ```
   git clone https://github.com/MossesRoss/Hand_controller.git
   ```
2. Change into the project directory:
   ```
   cd Hand_controller
   ```

## Usage
1. Make sure you have installed the required libraries mentioned in the 'Requirements' section.
2. Run the following command to execute the hand tracking script:
   ```
   python hand_controller.py
   ```
3. The script will open a window showing the live webcam feed with hand tracking overlays.
4. Perform hand gestures in front of the camera, and the application will track and recognize them in real-time.
5. Depending on the recognized gesture, the script will perform specific actions like controlling brightness or volume.
6. Press 'Q' to quit the application.

## Customization
- **Adding new gestures**: You can add new gestures by modifying the gesture recognition module. This involves defining the new gesture pattern and mapping it to a specific action or command.
- **Adjusting parameters**: Various parameters, such as hand detection confidence threshold or gesture recognition threshold, can be adjusted in the script to achieve optimal performance based on your requirements.
- **Extending functionality**: Feel free to extend the project's functionality by integrating it with other libraries or APIs or by implementing additional features such as hand pose estimation or object interaction.

## Contributions
Contributions to this project are welcome! If you encounter any issues or have suggestions for improvements, please submit them as GitHub issues or create a pull request with your proposed changes.

## License
This project is licensed under the [Apache License 2.0](LICENSE).

## Contact
If you have any questions or inquiries regarding this project, feel free to contact me at mosasross@gmail.com.

Thank you for your interest in this hand tracking Python project! I hope you find it useful and enjoy exploring its capabilities.
