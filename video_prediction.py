import cv2
import torch
import os
from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import *  
import torchvision
import natsort


model =torch.hub.load("WongKinYiu/yolov7", 'custom', 'yolov7_training.pt')
model.eval()

# Choose only 'person' and 'bird' classes from coco.yaml
model.classes = [0, 14]

def get_prediction_video(video_path):
    # Load the video file
    cap = cv2.VideoCapture(video_path)

    #Split video into frames for YOLOv7 to identify objects on each frame
    frame_list = []
    while True:
        ret, frame = cap.read()

        # Break the loop if we have reached the end of the video
        if not ret:
            break

        # Append the frame to the list
        frame_list.append(frame)

    # Release the video capture object
    cap.release()

    # Predict results from list of frames 
    results = model(frame_list[:50], size=640)  # includes NMS

    # Save frames with bounding boxes into a file
    results.save()

    # Print frames results
    results.print()


# Function to convert frames into videos 
def compile_video(frame_folder, output_video_path):
    
    # Get a list of all image files in the frame folder sorted in natural order
    # Remember to "import natsort"
    frame_files = natsort.natsorted([os.path.join(frame_folder, file) for file in os.listdir(frame_folder) if file.endswith(('.png', '.jpg', '.jpeg', '.bmp'))])

    # Check frame folder is empty
    if not frame_files:
        print(f"No image files found in {frame_folder}")
        return

    # Read the first frame to get its dimensions (assuming all frames have the same dimensions)
    first_frame = cv2.imread(frame_files[0])
    height, width, _ = first_frame.shape

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use other codecs like 'XVID' or 'MJPG' if needed
    out = cv2.VideoWriter(output_video_path, fourcc, 30, (width, height))  # 30 is the frames per second (adjust as needed)

    # Write each frame to the output video
    for frame_file in frame_files:
        print(frame_file)
        frame = cv2.imread(frame_file)
        
        out.write(frame)

    # Release the VideoWriter object
    out.release()

    print(f"Video saved as {output_video_path}")


video_path = '/Users/tanyu/Desktop/project_env/04100011_CT03.MP4'  
get_prediction_video(video_path = video_path)


frame_folder = '/Users/tanyu/Desktop/project_env/runs/hub/exp6'
output_video_path = 'output_video.mp4'
compile_video(frame_folder = frame_folder, output_video_path = output_video_path)