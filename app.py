import io
import os
import json
import torch
import natsort
import cv2
from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import *  
from threading import Thread



app = Flask(__name__)
app.secret_key = '123123qwe'  # Change this to a secure secret key

# Define the directory where uploaded videos will be stored
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



model =torch.hub.load("WongKinYiu/yolov7", 'custom', 'yolov7_training.pt')
model.eval()
model.classes = [0, 14]
video_path_ls =[]

  
### Global Variables
video_processing_progress = 0  # Global variable to track progress
frame_splitting_limit = 10
model_prediction_and_frame_splitting_limit = 80
compile_video_limit = 100 - model_prediction_and_frame_splitting_limit 

# Function to Split Frames and Get Model Prediction
def get_prediction_video(model, video_path):
    global video_processing_progress
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

    # Update Loading Bar from Frame Splitting
    update_progress(frame_splitting_limit)


    # Predict results from list of frames 
    results = model(frame_list[:50], size=640) 

    # Save frames with bounding boxes into a file
    results.save()

    # Print frames results
    results.print()

    # Update Loading Bar from Model Prediction & Frame Splitting
    video_processing_progress = model_prediction_and_frame_splitting_limit



   



# Function to convert frames into videos 
def compile_video(frame_folder, output_video_path):
    global video_processing_progress

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
    fourcc = cv2.VideoWriter_fourcc(*'H264')  # You can use other codecs like 'XVID' or 'MJPG' if needed
    out = cv2.VideoWriter(output_video_path, fourcc, 30, (width, height),  True)  # 30 is the frames per second (adjust as needed)

    increment = compile_video_limit/len(frame_files)
    # Write each frame to the output video
    for frame_file in frame_files:
        print(frame_file)
        frame = cv2.imread(frame_file)
        
        out.write(frame)

        video_processing_progress += increment

    # Release the VideoWriter object
    out.release()

    print(f"Video saved as {output_video_path}")

    video_processing_progress = 100



# Function to predict video and update progress
def predict_and_compile(user_input, output_video_path):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], user_input)
    get_prediction_video(model, filepath)
    runs_folder = '/Users/tanyu/Desktop/project_env/runs/hub/'
    latest_exp = natsort.natsorted([os.path.join(runs_folder, file) for file in os.listdir(runs_folder)])
    frame_folder = latest_exp[-1]
    compile_video(frame_folder=frame_folder, output_video_path=output_video_path)
    


@app.route('/')  
def main():  
    return render_template("index.html")  


@app.route('/result', methods=['GET'])
def result():
    # Retrieve prediction_results from the session
    output_video_name = session.get('output_video_name', None)

    return render_template("prediction_results.html", video_filename = output_video_name)


def update_progress(progress):
    global video_processing_progress
    video_processing_progress = progress

def get_progress():
    global video_processing_progress
    return video_processing_progress

@app.route('/check_progress', methods=['GET'])
def check_progress():
    progress = get_progress()
    return jsonify({'progress': progress})


# To Retrieve Embedded Video
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        filename = f.filename
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        session['filename'] = filename
        
        # output_video_name = user_input[:-4] + '_predicted.MP4'
        output_video_name = 'output_video.MP4'
        output_video_path = os.path.join(app.config['UPLOAD_FOLDER'], output_video_name)
        session['output_video_name'] = output_video_name
        # Start processing video in a separate thread
        video_thread = Thread(target=predict_and_compile, args=(session['filename'], output_video_path))
        video_thread.start()
        return render_template("loading.html")




if __name__ == '__main__':
    app.run()



