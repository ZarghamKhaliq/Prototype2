import nltk
import csv
import pandas
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import StratifiedKFold, cross_val_score, train_test_split
import string
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

import datefinder
from gtts import gTTS
import os

import imaplib
import email
import email.header
import time
import datetime
from threading import Thread

from DAL import DAL
from meeting import meeting
import datetime as dt
import calendar

def next_weekday(weekday):
    currentDate=dt.datetime.now()
    year=currentDate.year
    month=currentDate.month
    day=currentDate.day
    d = dt.date(year, month, day)
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: 
        days_ahead += 7
    return d + dt.timedelta(days_ahead)


def split_into_lemmas_(sentence):
    wordnet_lemmatizer = WordNetLemmatizer()
    porter_stemmer = PorterStemmer()
    exclude = set(string.punctuation)
    sentence = ''.join(ch for ch in sentence if ch not in exclude)
    sentence= sentence.lower()
    tokens = nltk.word_tokenize(sentence)
    tokens=[porter_stemmer.stem(word) for word in tokens]
    return [wordnet_lemmatizer.lemmatize(word) for word in tokens]

def response(msg):

    tts = gTTS(text='you have a '+msg+'request', lang='en')
    tts.save("response.mp3")
    os.system("response.mp3")


def classify(mail):

    #transorfmming and filtering input data
    print (mail)
    bow4 = bow_transformer.transform([mail])

    mail=split_into_lemmas_(mail)
    tfidf4 = tfidf_transformer.transform(bow4)


    prediction=meeting_detector.predict(tfidf4)[0]
    print ('predicted:',prediction )
    if(prediction!='ham'):
        print('meeting')
        #response(prediction)
        return True
    
    return False


# Use 'INBOX' to read inbox.  Note that whatever folder is specified,
# after successfully running this script all emails in that folder
# will be marked as read.


class MyThread(Thread):
    def __init__(self, mail):
        ''' Constructor. '''
        Thread.__init__(self)
        self.val = mail

    def run(self):
        while True:
            process_mailbox(self.val)
            #print ("loop completed")
            time.sleep(5)

def run():
    

    EMAIL_ACCOUNT = "l144083@lhr.nu.edu.pk"
#    EMAIL_ACCOUNT = email
    PASSWORD = "15987415"
#    PASSWORD = pw

    mail = imaplib.IMAP4_SSL('imap.gmail.com')

    mail.login(EMAIL_ACCOUNT, PASSWORD)

    mail.list()
    mail.select('inbox')

    print('login ho gya hai...')
    vehshithread=MyThread(mail)

    vehshithread.start()

    vehshithread.join()


def process_mailbox(mail):

    mail.list()
    mail.select('inbox')

    result, data = mail.uid('search', None, "UNSEEN")  # (ALL/UNSEEN)
    i = len(data[0].split())

    for x in range(i):
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        # result, email_data = conn.store(num,'-FLAGS','\\Seen')
        # this might work to set flag to seen, if it doesn't already
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        # Header Details
        date_tuple = email.utils.parsedate_tz(email_message['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            local_message_date = "%s" % (str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
        subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

        # Body details
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)

                body=body.decode('utf-8')
                #classifying the upcoming mail
                print('--------------')
                print(body)
                if(classify(body)):
                
                    
                    name=subject
                    date=next_weekday(1) # 0=monday
                    part=email_from
                    
                    count=0
                    match=datefinder.find_dates(body);
                    
                    for m in match:
                        count=count+1
                        
                    if count>0:
                        date=m.date()
                        print(date)
                        print(date.weekday())
                        
                    slots=dal.getFreeSlots(date)
                    
                    print(len(slots))
                    if(len(slots)!=0):
                        print("inserting")
                        m=meeting(name,part,date,slots[0])
                        dal.insert_meeting(m)
                    
            else:
                continue




#################################

messages = pandas.read_csv('dataSet', sep='\t', quoting=csv.QUOTE_NONE, names=["label", "message"])

msg_train, msg_test, label_train, label_test = train_test_split(messages['message'], messages['label'], test_size=0,
                                                                    random_state=0)

    # print(msg_train)


   # Training the Classifier
bow_transformer = CountVectorizer(analyzer=split_into_lemmas_).fit(msg_train)
bow_transformer.min_df = 0.5

print(len(bow_transformer.vocabulary_))

messages_bow = bow_transformer.transform(msg_train)
tfidf_transformer = TfidfTransformer().fit(messages_bow)
messages_tfidf = tfidf_transformer.transform(messages_bow)

    # providing data and labels to the classifier
meeting_detector = MultinomialNB().fit(messages_tfidf, label_train)

##########################################################

dal=DAL()
run()