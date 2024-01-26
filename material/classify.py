import pandas as pd
import spacy
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


# Load pre-trained spaCy model
nlp = spacy.load("en_core_web_sm")

# Load and preprocess the CSV file
def load_data(file_path):
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['Title', 'Description'])
    return df

# Tokenize and vectorize text using spaCy
def tokenize_and_vectorize(text):
    doc = nlp(text)
    return [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]

# Train a simple Naive Bayes classifier
def train_classifier(X, y):
    vectorizer = CountVectorizer(tokenizer=tokenize_and_vectorize)
    X_vectorized = vectorizer.fit_transform(X)

    classifier = MultinomialNB()
    classifier.fit(X_vectorized, y)

    return vectorizer, classifier

# Evaluate the classifier
def evaluate_classifier(vectorizer, classifier, X_test, y_test):
    X_test_vectorized = vectorizer.transform(X_test)
    predictions = classifier.predict(X_test_vectorized)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    # Replace 'your_model.csv' with the path to your CSV file
    file_path = './reviews.csv'

    # Load data
    df = load_data(file_path)

    # Encode labels
    label_encoder = LabelEncoder()
    df['Description'] = label_encoder.fit_transform(df['Description'])

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df['Title'], df['Description'], test_size=0.2, random_state=42)

    # Train the classifier
    vectorizer, classifier = train_classifier(X_train, y_train)

    # Evaluate the classifier
    evaluate_classifier(vectorizer, classifier, X_test, y_test)
