
#  <img src="https://user-images.githubusercontent.com/64935590/222929027-1c4d7267-7475-49b8-aace-079e33a2ded0.png" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" style="margin: 0px 0px -12px 0px;  display: inline;" width="100" height="50" /> <span style="display: inline; ">Gadid project</span>

### Team members

| Team members   | Role |
| ----------- | ----------- |
| Shatha alyousef | EDA, Encoding , Random Forest algorithm, classification report, README File Arrangement |
| Alaa Qadri  | Face similarity model, Eyeglass Detection model, background color identification model, Deployment by Django |
|Amjad| | Idea, men model, Data collection, Data annotation, EDA, VGG16, loss function 

### Introduction

It is a project related to renewing the image of the electronic national identity, so that through this project it is possible to verify the percentage of similarity of the image added by the user to the previous image registered in the civil status to ensure that the image is of the same person. Also, we created a model that checks the dress conditions for men and women. If the image matches the previous conditions, it is approved and renewed electronically without manual verification.

### Dataset Overview

- Hijab Dataset 

It is a collection of pictures of veiled girls, with approximately 5,000 pictures Also, pictures of girls without a veil, and nearly 5,000 pictures

- Traditional Saudi dress Dataset 

For men clothes classification we collected around 1500 images with Saudi tradition clothes and without.

### Proposed Algorithms

- vgg16 algorithm
VGG16 is object detection and classification algorithm which is able to classify 1000 images of 1000 different categories with 92.7% accuracy. It is one of the popular algorithms for image classification and is easy to use with transfer learning

- LFW (Labeled Faces in the Wild) DataSet 
It is a collection of pictures of men and women faces, with approximatly 13k pictures. 

- Custom DataSet
It is a web scrapping and manual selection for arab persons, we collected around 1.5k men and women faces, 30 images for each person.

- MeGlass Dataset
It is a collection of pictures of person who wear glasses and person without, it contains approximatly 33k with glasses and 14k without them.

- Celeba DataSet
It is a collection of pictures of person who wear glasses and person without, it contains approximatly 13k with glasses and 189k without them.


### Final Results and conclusion

 Model name   | Accuracy |
| ----------- | ----------- |
| Hijab model | 96% |
| Traditional Saudi dress model | 92.7% |
| Face similarity model | 97.3% |
| Eyeglass detection model | 99.0% |

Based on the results of the accuracy, we can say that this project can automate the process of verifying the photos of renewing the national identity photo

