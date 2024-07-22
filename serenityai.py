import pandas as pd
import time
import re
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# Load pre-split datasets with corrected delimiter
train = pd.read_csv("train.csv", delimiter=';')
test = pd.read_csv("test.csv", delimiter=';')

# Verify columns
print("Train columns:", train.columns)
print("Test columns:", test.columns)

# Use correct column names
X_train = train['message']
y_train = train['label']
X_test = test['message']
y_test = test['label']

# Vectorize the text data
vectorizer = TfidfVectorizer(max_df=0.9).fit(X_train)
X_train = vectorizer.transform(X_train)
X_test = vectorizer.transform(X_test)
print(X_train.shape)

# Encode the labels
encoder = LabelEncoder().fit(y_train)
y_train = encoder.transform(y_train)
y_test = encoder.transform(y_test)

# Train a logistic regression model
model = LogisticRegression(C=0.1, class_weight='balanced')
model.fit(X_train, y_train)
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)
print("Training Accuracy : ", accuracy_score(y_train, y_pred_train))
print("Testing Accuracy  : ", accuracy_score(y_test, y_pred_test))

# Continue with the rest of the code...


negative = 0
positive = 0

def intent(message):
    for words in intents.keys():
        pattern = re.compile('|'.join([syn for syn in intents[words]]))
        match = pattern.search(message)
        if match:
            return words
    return 'default'

def respond(message):
    word = intent(message)
    return responses[word]

def score(name):
    sc = 0
    for k in dictionary.keys():
        sc += dictionary[k] * s[k]
    print("Your mental assessment score is ", sc)
    if sc >= 0 and sc <= 5:
        print(bot.format("Please make sure that you keep checking in with me. What's your mood now after opening up?"))
        message = input().lower()
        m_intent = intent(message)
        if m_intent == 'depression':
            depression(name)
        elif m_intent == 'anxiety':
            anxiety(name)
        elif m_intent == 'sleeping_disorder':
            sleeping_disorder(name)
        elif m_intent == 'paranoia':
            paranoia(name)
        elif m_intent == 'personality_disorder':
            personality_disorder(name)
        elif m_intent == 'substance_abuse':
            substance_abuse(name)
        elif m_intent == 'happy':
            time.sleep(1)
            print(bot.format("Please ask me for help whenever you feel like it! I'm always online."))
        else:
            extreme(name)
    elif sc >= 6 and sc <= 15:
        extreme(name)

def extreme(name):
    print(bot.format("We're really sorry to know that and for further assistance we would try to connect you with our local assistance who is available 24/7"))
    time.sleep(1)
    print(bot.format("Here are the details", name))
    print(bot.format("Contact Jeevan Suicide Prevention Hotline"))
    print(bot.format("Address: 171, Ambiga Street Golden George Nagar, Nerkundram, Chennai, Tamil Nadu 600107"))
    print(bot.format("Number: 044 2656 4444"))

def quiz(name):
    global dictionary
    time.sleep(1)
    print(bot.format("Now we're starting with a small assessment and hopefully at the end of the assessment, we'll be able to evaluate your mental health"))
    print()
    time.sleep(0.8)
    print(bot.format("To respond please type the following answer depending upon your choice"))
    print("A. not at all")
    print("B. several days")
    print("C. more than half a day")
    print("D. all the days")
    print()
    time.sleep(1)
    print("Now we'll be starting with the quiz, type okay if you're ready!")
    inp = input().lower()
    if inp == 'okay':
        for sentence in questions:
            time.sleep(1)
            print(bot.format(sentence))
            resp = input().lower()
            if resp in dictionary:
                dictionary[resp] = dictionary[resp] + 1
            else:
                print("Invalid response. Please choose A, B, C, or D.")
    else:
        greet()
    print()
    time.sleep(1)
    print("Thank you for taking the assessment!")
    for k in dictionary.keys():
        print(k, dictionary[k])
    score(name)

def predict_(x):
    tfidf = vectorizer.transform([x])
    preds = model.predict(tfidf)
    probab = model.predict_proba(tfidf)[0][preds]
    print(preds, probab)
    feeling(preds, probab)
    return preds

def feeling(pred, probab):
    global negative, positive
    if pred == 0 or pred == 1 or pred == 4:
        negative = negative + 1
        if probab >= 0.5:
            time.sleep(1)
            print(bot.format("Oh, sorry to hear that!"))
        else:
            time.sleep(1)
            print(bot.format("Okay, thanks for sharing."))
    else:
        positive = positive + 1
        if probab >= 0.5:
            time.sleep(1)
            print(bot.format("That's great to hear!"))
        else:
            time.sleep(1)
            print(bot.format("Okay, thanks for sharing."))

def classification(pred):
    if pred == 0 or pred == 1 or pred == 4:
        return 0
    else:
        return 1

def depression(name):
    print(bot.format("Hello {0}, it's good to know that you're comfortable opening up about depression.".format(name)))
    time.sleep(1)
    print(bot.format("We would try to assist you by taking a small quiz to further evaluate your mental health condition"))
    print(bot.format("Would that be okay?"))
    inp = input().lower()
    if inp == 'yes':
        quiz(name)
    else:
        extreme(name)

def greet():
    print("BOT: What is your name?")
    name = input().lower()
    print(bot.format("Hey {0}!".format(name)))
    time.sleep(1)
    print(bot.format("How are you feeling today?"))
    inp = input().lower()
    pred = predict_(inp)
    label = classification(pred)
    if label == 0:
        depression(name)
    else:
        time.sleep(1)
        print(bot.format("Thanks for sharing {0}".format(name)))

if __name__ == "__main__":
    greet()
