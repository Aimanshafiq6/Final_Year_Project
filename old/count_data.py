def count_emotion_responses(data):
    # Initialize a dictionary to store counts of yes and no responses for each emotion
    emotion_counts = {}
    
    for entry in data:
        emotion = entry["emotion"]
        response = entry["response"]
        
        if emotion not in emotion_counts:
            emotion_counts[emotion] = {"Yes": 0, "No": 0}
        
        if response == "Yes":
            emotion_counts[emotion]["Yes"] += 1
        elif response == "No":
            emotion_counts[emotion]["No"] += 1
    
    return emotion_counts

# Sample data
data = [
    {
        "question": "Were you surprised by the announcement?",
        "emotion": "surprise",
        "response": "Yes"
    },
    {
        "question": "Did the surprise party make you happy?",
        "emotion": "surprise",
        "response": "Yes"
    },
    {
        "question": "Are you scared of heights?",
        "emotion": "fear",
        "response": "Yes"
    },
    {
        "question": "Do you worry about the future?",
        "emotion": "fear",
        "response": "Yes"
    },
    {
        "question": "Are you afraid of the dark?",
        "emotion": "fear",
        "response": "Yes"
    },
    {
        "question": "Are you annoyed by the traffic?",
        "emotion": "anger",
        "response": "Yes"
    },
    {
        "question": "Did you have a disagreement with someone?",
        "emotion": "anger",
        "response": "Yes"
    },
    {
        "question": "Are you frustrated with your work situation?",
        "emotion": "anger",
        "response": "Yes"
    },
    {
        "question": "Did someone make you upset today?",
        "emotion": "anger",
        "response": "Yes"
    },
    {
        "question": "Are you angry about the recent news?",
        "emotion": "anger",
        "response": "Yes"
    },
    {
        "question": "Do you feel lonely sometimes?",
        "emotion": "sadness",
        "response": "Yes"
    },
    {
        "question": "Are you feeling down because of the weather?",
        "emotion": "sadness",
        "response": "Yes"
    },
    {
        "question": "Do you miss someone right now?",
        "emotion": "sadness",
        "response": "Yes"
    },
    {
        "question": "Did something upset you recently?",
        "emotion": "sadness",
        "response": "Yes"
    },
    {
        "question": "Are you feeling sad today?",
        "emotion": "sadness",
        "response": "Yes"
    },
    {
        "question": "Did you have a good day today?",
        "emotion": "happiness",
        "response": "Yes"
    },
    {
        "question": "Are you looking forward to the weekend?",
        "emotion": "happiness",
        "response": "Yes"
    },
    {
        "question": "Do you feel satisfied with your achievements?",
        "emotion": "happiness",
        "response": "Yes"
    },
    {
        "question": "Did you enjoy your vacation?",
        "emotion": "happiness",
        "response": "Yes"
    },
    {
        "question": "Are you happy with your current job?",
        "emotion": "happiness",
        "response": "Yes"
    },
    {
        "question": "Did the unexpected gift delight you?",
        "emotion": "surprise",
        "response": "Yes"
    },
    {
        "question": "Were you shocked by the sudden change?",
        "emotion": "surprise",
        "response": "Yes"
    },
    {
        "question": "Did the news catch you off guard?",
        "emotion": "surprise",
        "response": "Yes"
    },
    {
        "question": "Are you concerned about your safety?",
        "emotion": "fear",
        "response": "Yes"
    },
    {
        "question": "Do you feel anxious about your health?",
        "emotion": "fear",
        "response": "No"
    }
]

def calculate_percentage_responses(emotion_counts):
    percentage_responses = {}
    
    for emotion, counts in emotion_counts.items():
        total_responses = counts["Yes"] + counts["No"]
        if total_responses > 0:
            percentage_yes = (counts["Yes"] / total_responses) * 100
        else:
            percentage_yes = 0.0
        
        percentage_responses[emotion] = round(percentage_yes, 2)
    
    return percentage_responses
# Calculate and print the emotion response counts
emotion_response_counts = count_emotion_responses(data)
print(emotion_response_counts)

# Example data
emotion_counts = {
    'surprise': {'Yes': 5, 'No': 0},
    'fear': {'Yes': 4, 'No': 1},
    'anger': {'Yes': 5, 'No': 0},
    'sadness': {'Yes': 5, 'No': 0},
    'happiness': {'Yes': 5, 'No': 0}
}

# Calculate percentages
percentage_responses = calculate_percentage_responses(emotion_counts)
print(percentage_responses)

def normalize_percentages(percentage_responses):
    total_percentage = sum(percentage_responses.values())
    normalized_percentages = {emotion: (percentage / total_percentage) * 100 for emotion, percentage in percentage_responses.items()}
    return normalized_percentages

print(normalize_percentages(percentage_responses))