
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from textblob import TextBlob
from sentiment_analysis import sentiment_analysis_product, analyze_single_sentiment
from io import StringIO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file = request.files['file']
            df = pd.read_csv(file)
            data = df[['review_rating', 'review_title', 'review_body']]
            data.rename(columns={'review_rating': 'Stars', 'review_title': 'Title', 'review_body': 'Review'}, inplace=True)
            text_content = df.to_csv(index=False)  # Convert DataFrame to CSV string
            positive, neutral, negative = sentiment_analysis_product(StringIO(text_content))

            # for the table
            table = data.to_html()
            plain = '<table border="1" class="dataframe">'
            nice =   '<table class="dataframe w3-table w3-striped w3-bordered w3-border">'
            nicetable = table.replace(plain, nice)

            return render_template('summaryreviews.html', table=nicetable, positive=positive, negative=negative, neutral=neutral)
        except Exception as e:
            error_message = "An error occurred while processing the uploaded file: {}".format(str(e))
            return render_template('error.html', error_message=error_message)

    return render_template('upload_file.html')

@app.route('/input_review', methods=['GET', 'POST'])
def input_review():
    if request.method == 'POST':
        try:
            review = request.form['review']
            sentiment = analyze_single_sentiment(review)
            return render_template('output_review.html', review=review, sentiment=sentiment)
        except Exception as e:
            error_message = "An error occurred while analyzing the review: {}".format(str(e))
            return render_template('error.html', error_message=error_message)

    return render_template('input_review.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    
    
    
