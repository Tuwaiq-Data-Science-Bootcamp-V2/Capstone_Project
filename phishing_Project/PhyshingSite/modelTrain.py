import pandas as pd
import re
import nltk
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
nltk.download('stopwords') 
nltk.download('punkt')
import pickle
from sklearn.model_selection import train_test_split

emailSMSData = pd.read_csv('arabic-english-text.csv') #latin-1 is saperated encoding method for special characters

emailSMSData.drop('Unnamed: 0',axis=1, inplace=True)

emailSMSData.drop_duplicates(inplace=True)

# Replace ham with 0 and spam 1
emailSMSData = emailSMSData.replace('spam', 1)
emailSMSData = emailSMSData.replace('ham', 0)


def cleanText(text):
    # Create a regular experssion pattern for whitespaces '\s', + means there is one or more charater after the whitespace 
    # ==> as result this pattern remove the whitespace at the begining of string
    whitespace = re.compile(r"\s+") 


    # Create a regular experssion pattern for web addresses 
    # (?i) ==> for case insinstive
    # (s) ==> means either http or https
    # \/\/ ==> means douple slash 
    #[a-z0-9.~_\-\/]+ ==> means set of characters between a-z and 0-9, . except newlines , ~_ include underscore and \, + one or more characters
    web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")

    # Create a regular experssion pattern for users ids
    # (?i) ==> for case insinstive 
    # @ ==> means contains @ character
    # [a-z0-9_]+ ==> means contains characters a to z and digits 0 to 9 and underscore
    user = re.compile(r"(?i)@[a-z0-9_]+")

    # to replace the . in text with empty string
    text = text.replace('.', '')

    # Apply the whitespace pattern into the text using sub
    text = whitespace.sub(' ', text)

    # Apply web addreses pattern into the text using sub
    text = web_address.sub('', text)

    # Apply user pattern into the text using pattern
    text = user.sub('', text)
    text = re.sub(r"\[[^()]*\]", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r'[^\w\s]','',text)
    text = re.sub(r"(?:@\S*|#\S*|http(?=.*://)\S*)", "", text)
    return text.lower()
emailSMSData.Text =  [cleanText(item) for item in emailSMSData.Text]
#print(spam_data)


tokenizer = Tokenizer(oov_token='<OOV>')
tokenizer.fit_on_texts(emailSMSData.Text)
vocab = tokenizer.word_index 
vocabCount = len(vocab)+1 
textSequences = tokenizer.texts_to_sequences(emailSMSData.Text)
finalDataFrame = pad_sequences(textSequences, padding='pre', maxlen=171) 
target = emailSMSData.target
dim = finalDataFrame.shape[1] 

xTrain, xTest, yTrain,yTest = train_test_split(finalDataFrame, target, test_size=0.2, random_state=0)

model = tf.keras.models.Sequential() #sequential why??
model.add(tf.keras.layers.Embedding(input_dim=vocabCount, output_dim=32, input_length=dim))
model.add(tf.keras.layers.GlobalAveragePooling1D())
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(xTrain, yTrain, epochs=10, shuffle=True)

y_pred = model.predict(xTest)
print()
print('Evaluate the mode')
eval = model.evaluate(xTest, yTest)
print('Test Loss: ', eval[0])
print('Test Accuracy: ', eval[1])
model.save('messagesModele') # To save deep learning model we use save instead of pkile.dump
pickle.dump(tokenizer, open("messagesTokenizer.pkl", "wb")) # We save tokenizer so we can use it in the website

loadedModel = tf.keras.models.load_model('messagesModele')
tokeize= pickle.load(open('messagesTokenizer.pkl','rb'))
text = "Hi my name is Munirah"
processedText = cleanText(text)
finalText = pad_sequences(tokeize.texts_to_sequences([processedText]), padding='pre', maxlen=171)
loadedModel.predict(finalText)

if loadedModel.predict(finalText) > 0.5:
    print(loadedModel.predict(finalText),'Spam')
else:
    print(loadedModel.predict(finalText),'Ham')