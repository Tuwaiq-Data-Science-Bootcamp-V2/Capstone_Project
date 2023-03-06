# Project Title
### Who is the Reciter (من القارئ)


## Introduction
We have trained Deep Learning model that can accurately classify Quran recitations based on the audio input and return the name of the reciter. The model was later deployed as a Telegram Bot, providing users with the ability to receive automatic classification of Quran recitations through audio input.

## Dataset Overview
The Quran Recitation Audio Classification Dataset is a collection of audio recordings of Quran recitations from various reciters. The dataset consists of folders named after each reciter, with audio files in WAV format inside each folder and we have provided a csv file that contains the path of each file along with it's class. The audio files were recorded by a team in different acoustic environments, providing a diverse range of audio samples for training and testing a deep learning model. Here is a [link](https://www.kaggle.com/datasets/mohammedalrajeh/quran-recitations-for-audio-classification) of dataset in kaggle 

 
## Used Algorithms.
We have used number of deep learning and machine learning algorithms to classifiy the reciters based on the MFCC and we have found that best number of MFCC to extract is 128 and the model that gave us the best result was ANN.

## Final results and Conclusion
We are pleased to report that our deep learning model successfully predicts the name of a Quran reciter with remarkable accuracy using only a brief sound clip. This project has equipped us with the skills necessary to effectively process and analyze audio files, and to refine our algorithm to make informed predictions.

| Model | precision | recall | f1-score |accuracy |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| ANN | 96% | 95% | 95% | 95% |
| RNN | 95% | 96% | 95% | 96% |


## Team members
| Team members      | Role                                                                                                                             |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------|
| Suliman Alsaadan   | collected data manually, apply Deep Learning model , helped in README markdown file and helped in telegram bot.                       |
| Mohammed Alrajeh (LEADER) | collected data manually, created telegram bot, helped in Deep Learning model, created the presentation and helped in README markdown file.|
| Faris Alshammari  | collected data manually, helped in Deep Learning model , helped in telegram bot , and wrote README markdown file.               |

