from transformers import pipeline
def emotional_analysis(text):
    classifier = pipeline("text-classification",model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True)
    prediction = classifier(text, )
    score=0
    label=''
    for i in prediction[0]:
        scores=i['score']
        if scores>score:
            score=scores
            label=i['label']
    if label=='':
        return 0
    else:
        return label
