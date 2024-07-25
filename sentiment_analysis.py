from textblob import TextBlob
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# analyze sentiments in a single review
def analyze_single_sentiment(review):
    try:
        blob = TextBlob(review)
        score = blob.sentiment.polarity
        sentiment = "Neutral" if score == 0 else "Positive" if score > 0 else "Negative"
        return sentiment
    except Exception as e:
        print("An error occurred:", str(e))
        return "Error"


# analyze sentiments in a csv file
def sentiment_analysis_product(file):
    try:
        data = pd.read_csv(file)
        
        # clean data
        nan_mask = data.isna()
        data = data.dropna()
        
        # get numerical ratings
        ratings = data.get(["review_rating"])
        ratings = ratings.values.tolist()
        
        # count per ratings
        rates = [1,2,3,4,5]
        count_r = [ratings.count([1]), ratings.count([2]), ratings.count([3]), ratings.count([4]), ratings.count([5])]
        
        # get reviews    
        reviews = data.get(["review_body"])
        reviews = reviews.values.tolist()
        
        # sentiment analysis
        sentiments = [ ]
        for text in reviews:
            sentiment = analyze_single_sentiment(text[0])
            sentiments.append(sentiment)
        
        n = len(sentiments)
        
        # counting sentiments
        counts = (sentiments.count("Positive")*100/n, sentiments.count("Neutral")*100/n, sentiments.count("Negative")*100/n)
        
        return counts

    except Exception as e:
        print("An error occurred:", str(e))
        return (0, 0, 0)  # Return default values or handle the error appropriately

    