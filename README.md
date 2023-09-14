# Commercial Project: BirD
### Updated On: 14 September 2023

## Overview

This project aims to classify animals in motion detected videos captured in Singapore. The methodology used in this project involves exploring the use of YOLOv7 to fine tune the classification model. In addition, data augmentation techniques will be employed to enhance the model's accuracy.

![](https://github.com/Tan-Yu/BirD/blob/main/README%20Content/My%20Movie.gif)


## Methodology

To achieve accurate classification, we are exploring the use of YOLOv7 to fine tune the model. This approach involves training the model on a supervised dataset of common Singaporean animals. Then, by fine tuning the model with frames from the real videos, we can identify real animals in the videos. The use of YOLOv7 allows us to achieve high accuracy and fast processing times.

## Choice of YOLOv7 for Licensing Reasons

### Background

When selecting the computer vision model for our animal classification project, we carefully considered licensing and open-source considerations. While there are several excellent models available for object detection and classification, we decided to use YOLOv7 for the following reasons:

### Licensing Considerations

1. **MIT License:** YOLOv7 is released under the MIT License, which is one of the most permissive open-source licenses available. This license grants us the freedom to use, modify, and distribute the model for both non-commercial and commercial purposes without significant licensing restrictions.

2. **No GPL Dependencies:** YOLOv7's codebase is free from dependencies that use the GNU General Public License (GPL) or other restrictive licenses. This ensures that our entire project remains open and accessible while avoiding any potential licensing conflicts.

3. **Commercial Viability:** Given our project's commercial nature, it was crucial to select a model that aligns with our business goals. YOLOv7's licensing allows us to incorporate it into our commercial product, making it a suitable choice for our needs.

### Flexibility and Performance

Apart from licensing considerations, YOLOv7 offers high performance in object detection and classification tasks. Its architecture is efficient and can handle real-time processing, making it well-suited for our application's requirements.

### Future Compatibility

We anticipate that YOLOv7's permissive licensing and strong community support will ensure its compatibility with future developments in the field of computer vision. This ensures the longevity and sustainability of our project.

By selecting YOLOv7 for our animal classification model, we aim to strike a balance between licensing compliance and robust performance, allowing us to develop a successful commercial project while adhering to open-source principles.


## Data Augmentation

To further enhance the accuracy of the model, we plan to create "fake" night vision videos to train on since the camera has night vision videos. This data augmentation technique will help the model recognize animals in low-light settings, improving its performance.


## User Interface for Video Upload (Using Flask)

### Overview

As part of our project, we needed a way for users to upload videos for classification. To accomplish this, we created a simple and user-friendly web interface using Flask, a Python web framework. This UI allows users to submit videos easily, which are then processed by our animal classification model.

### Implementation Details

Here's how we integrated Flask into our project:

1. **Flask Web Application:** We developed a Flask web application that serves as the frontend for video uploading. This web app provides a user interface where users can select and upload their videos.

2. **HTML Form:** Within our Flask application, we included an HTML form with an input element of type "file." This input element allows users to select video files from their local devices.

3. **File Upload Handling:** We implemented a route in Flask that handles file uploads. When a user selects a video and submits the form, Flask captures the uploaded file and saves it to a designated location on the server.

4. **Processing and Classification:** After the file is uploaded, it can be passed to our animal classification model for processing, as described in the project overview.

### User Experience

Our Flask-based UI enhances the overall user experience by providing an intuitive and accessible way for users to contribute videos to our animal classification project. It simplifies the process of data collection and allows us to leverage user-generated content to improve our model's accuracy.

### Future Enhancements

While our current implementation offers a straightforward way to upload videos, we are continually working to enhance the user interface. Future improvements may include:

- Providing feedback to users during the upload process, such as progress indicators.
- Allowing users to track the status of their uploaded videos.
- Supporting additional file formats and video-related features.
- Users will be able to upload videos in bulk and generate a .CSV report on the animals that were predicted

By using Flask, we have created a flexible foundation for our user interface, enabling us to incorporate these enhancements seamlessly.


## Conclusion

Overall, this project aims to develop a robust animal classification model that can accurately identify animals in motion detected videos captured in Singapore. Through the use of YOLOv7 and data augmentation techniques, we aim to achieve high accuracy and fast processing times.

The integration of Flask into our project has facilitated the video upload process, empowering users to contribute to our animal classification efforts. This collaborative approach improves data diversity and contributes to the overall success of our project.


