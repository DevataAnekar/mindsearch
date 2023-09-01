import codecs
from deep_translator import GoogleTranslator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get(sentence):
    translated_text = GoogleTranslator(source='auto', target='en').translate(sentence)
    analyzer = SentimentIntensityAnalyzer()
    sentiment_dict = analyzer.polarity_scores(translated_text)

    probability = [sentiment_dict['neg'],sentiment_dict['neu'],sentiment_dict['pos']]


    if sentiment_dict['compound'] >= 0.05 :
        return "Positive"
        
    elif sentiment_dict['compound'] <= - 0.05 :
        return "Negative"

    else:
        return "Neutral"



