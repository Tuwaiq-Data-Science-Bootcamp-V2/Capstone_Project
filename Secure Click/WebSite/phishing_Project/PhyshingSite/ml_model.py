from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle


df = pd.read_csv('URL-Data-LASTVER.csv')
X = df.drop(columns=['Unnamed: 0','url','label','result'],axis=1)
y = df['result']

sc = StandardScaler()
X = sc.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, random_state = 20)


urlModel = RandomForestClassifier()
urlModel.fit(X_train, y_train)


pickle.dump(urlModel, open('urlModellass.pkl','wb'))
pickle.dump(sc , open('urlScalerlass.pkl','wb'))