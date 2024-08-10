import text2emotion as te

text = "I was asked to sign a third party contract a week out from stay. If it wasn't an 8 person group that took a lot of wrangling I would have cancelled the booking straight away. Bathrooms - there are no stand alone bathrooms. Please consider this - you have to clear out the main bedroom to use that bathroom. Other option is you walk through a different bedroom to get to its en-suite. Signs all over the apartment - there are signs everywhere - some helpful - some telling you rules. Perhaps some people like this but It negatively affected our enjoyment of the accommodation. Stairs - lots of them - some had slightly bending wood which caused a minor injury."

emotions_dict = te.get_emotion(text)

print(emotions_dict)

def get_top_two_emotions(emotions):
    # Sort the dictionary by values in descending order
    sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
    
    # Return the keys of the first two items
    return [sorted_emotions[0][0], sorted_emotions[1][0]]


top_two_emotions = get_top_two_emotions(emotions_dict)

print(top_two_emotions)
