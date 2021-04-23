# Nudity detection
 1. The purpose of this project is to detect images which are NSFW i.e images exposing private parts of "Homo sapiens". Further it can be used to delete/reject such images.  
 2. This app uses YOLOv3 custom trainned model for detecting.
 3. I have used 1000's of images for the training purpose.
 4. Training is done for 4000 iterations, you can add additional datasets and train the model for better results. 
 5. To use it in realtime application, this project is made in flask so that it can be consumed as an API for several applications and platforms like Telegram.  
 
 ## Installation
 First clone the repo and install required packages by
 `pip install -r requirements.txt`  
 thats it! The app is ready to run on flask.
 
 ## Usage
 Run the API by  
 `python app.py`
 The flask runs on port 8080 with local IP address  
 
 ## API Usage
 Read the API Documentation for API usage  
 https://github.com/aravind-tronix/Nudity-detection/blob/main/API.md  
 
 ## Live version of the API
 Here is the live webapp which uses the API to detect nudity from a image  
 https://deeplearnai.ml/nsfw_detector

## Issues
This error is raises in certain OS like windows 10 and 7  
PermissionError after using cv2.imread on certain files/OS. This prevents deletion of the image file after the process is done. 
