import sys
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import text2emotion as te


def get_two_max_val_emotions(emotion):
    max1=0
    max2=0
    name1 = ""
    name2 = ""
    for k,v in emotion.items():
     if v >= max1:
         name2 = name1
         name1 = k
         max2 = max1
         max1 = v
    return {name1:max1,name2:max2}


def main():
    analysis = SentimentIntensityAnalyzer() 
    text = input("Enter text\n:")
    
    sentiment_dict = analysis.polarity_scores(text)

    print("The sentiment of the text is:")    
    if sentiment_dict['compound'] >= 0.05:
        print("\nThe feedback is positive")
    elif sentiment_dict['compound'] <= -0.05:
        print("\nThe feedback is negative")
    else:
        print("\nThe feedback is neutral")

    emotions_found = te.get_emotion(text)
    print(emotions_found)
    print("The emotions Expressed here are:")
    topemotions = get_two_max_val_emotions(emotions_found)
    print(topemotions)
    for k in topemotions.keys():
        print(k,end=" ")


def analysis(text_inst):
    analysis_obj = SentimentIntensityAnalyzer()
    data = {}
    sentiment_dict = analysis_obj.polarity_scores(text_inst)
    sentiment_got = ''
    if sentiment_dict['compound'] >= 0.05:
        sentiment_got = sentiment_got + 'positive'
    elif sentiment_dict['compound'] <= -0.05:
        sentiment_got = sentiment_got + 'negative'
    else:
        sentiment_got = sentiment_got + 'neutral'
    data = {
        "sentiment":sentiment_got
    }

    emotions_found = te.get_emotion(text_inst)
    data.update(get_two_max_val_emotions(emotions_found))

    return data;


if __name__ == '__main__':
    main()


