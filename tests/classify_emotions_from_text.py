import tensorflow
from transformers import pipeline
from autocorrect import Speller
import transformers
print("--"+str(transformers.is_tf_available()))
classifer = pipeline('text-classification',model='bhadresh-savani/distilbert-base-uncased-emotion')
spell = Speller()

some_text = "hello world my name is Zack, i love scence and progrmming"

corrected_text = spell(some_text)
emotion = classifer(corrected_text)

print(emotion[0]['label'])

