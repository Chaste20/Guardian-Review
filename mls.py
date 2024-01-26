import pandas as pd
import pickle


def predict_reviews(df_reviews):
    # Load pre-trained model
    model = pickle.load(open('Data/model.pkl', 'rb'))

    # Load reviews data from 'reviews.csv'
    #csv_filename = 'reviews.csv'
   # df = pd.read_csv(csv_filename)

    # Perform preprocessing and feature extraction steps as needed

    # Make predictions using the pre-trained model
    result = model.predict(df_reviews['Description'])  # Adjust column name as needed

    # Assuming binary classification (positive/negative)
    # Adjust the logic based on your specific model and use case
    percentage = sum(result) / len(result) * 100

    return f"is: {percentage:.2f}%"
