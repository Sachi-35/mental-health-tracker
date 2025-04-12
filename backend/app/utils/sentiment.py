from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the VADER sentiment intensity analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the provided text using VADER.
    Returns a dictionary of sentiment scores (positive, neutral, negative, and compound).
    """
    return analyzer.polarity_scores(text)
