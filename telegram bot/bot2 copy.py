import os
import subprocess
import requests
import telebot
import librosa
import urllib
from pydub import AudioSegment
import io
import numpy as np
import tensorflow as tf
import pickle
from tensorflow import keras
from iteration_utilities import flatten
from keras.models import load_model
import joblib
bot_token = 'INSERT BOT TOKKEN HERE'
bot = telebot.TeleBot(bot_token)

# Load the model from the file
scaler = pickle.load(open('/Users/mohammed_alrajeh/Desktop/Bootcamp/Projects/final-project/telegram_bot/scaler2_5-V4.pkl', 'rb'))
model = tf.keras.models.load_model('/Users/mohammed_alrajeh/Desktop/Bootcamp/Projects/final-project/telegram_bot/ANN-2_5-V4.h5',compile=False)
model.compile()

class_names = ['عبدالله البعيجان','علي الحذيفي','عبدالرحمن السديس','بندر بليلة','ماهر المعيقلي','محمد ايوب','ناصر القطامي','سعد الغامدي','سعود الشريم','ياسر الدوسري','عبدالباري الثبيتي','محمد اللحيدان']
links = ['https://youtu.be/6tKLtFObeWc','https://youtu.be/iqwNmV5Yxu8',
 'https://youtu.be/upQI4flFz4k','https://youtu.be/F5GO6Hz_Hyg',
 'https://youtu.be/JsS6MujjOG4','https://youtu.be/7lJnKt-09BI',
 'https://youtu.be/cfPh6oLBwn4','https://youtu.be/STXWcU6eGCI',
 'https://youtu.be/hmrnO3_E4UA','https://youtu.be/NoN8oOO7Pps',
 'https://youtu.be/h3c4EfSd_sA','https://youtu.be/EXe8Vq_z3g8']


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message,"مرحبا بك في بوت من القارئ، سجل رسالة صوتية لقارئ لمعرفة أسمه")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, 'يرجى تسجيل رسالة صوتيه لمعرفة اسم القارئ')

def features_extractor(file):
    X, sample_rate = librosa.load(file, res_type='kaiser_fast' )
    print(sample_rate)
    mfccs_features = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=128)
    mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
    return mfccs_scaled_features


@bot.message_handler(content_types=['voice'])
def telegram_bot(message,bot_token=bot_token):
    # insert audio
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    audio_segment = AudioSegment.from_file(io.BytesIO(downloaded_file))
    # Convert the AudioSegment to a WAV file
    wav_file = io.BytesIO()
    audio_segment.export(wav_file, format='wav')
    wav_file.seek(0)
    print(wav_file)

    prediction_feature= features_extractor(wav_file)
    prediction_feature = np.array(prediction_feature)
    prediction_feature = scaler.transform(prediction_feature.reshape(1 , -1))

    pred = model.predict(prediction_feature)
    index = np.argmax(pred)
    sorted_indices = np.argsort(pred)
    next_two_indices = sorted_indices[0][::-1][1:3].tolist()

    long_message = 'اسم القارئ هو: '+class_names[index]+'\n\n'+'وهذه بعض اسماء القراء المشابهين له:'+'\n'+\
        class_names [next_two_indices[0]]+'\n'+class_names[next_two_indices[1]]+'\n\n'+'------------------------------------'+'\n\n'\
            'رابط لتلاوة من القرآن الكريم بصوت القارئ'+links[index]

    bot.reply_to(message,long_message)

bot.infinity_polling()