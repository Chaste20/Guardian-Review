import pandas as pd
import pickle
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline


nltk.download('stopwords')


def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove punctuation and special characters
    text = ''.join(char for char in text if char.isalnum() or char.isspace())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join(word for word in text.split() if word not in stop_words)

    return text
def predict_reviews(df_reviews):
    # Load pre-trained model
    model = pickle.load(open('Data/model.pkl', 'rb'))

    # Load reviews data from 'reviews.csv'
    #csv_filename = 'reviews.csv'
   # df = pd.read_csv(csv_filename)

    # Perform preprocessing and feature extraction steps as needed
    #df_reviews['Cleaned_Description'] = df_reviews['Description'].apply(preprocess_text)
    # Make predictions using the pre-trained model
    result = model.predict(df_reviews['Description'])  # Adjust column name as needed

    # Assuming binary classification (positive/negative)
    # Adjust the logic based on your specific model and use case
    percentage = sum(result) / len(result) * 100

    return f" {percentage:.2f}%"
