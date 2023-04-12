#import speech_recognition as sr
import transformers
import numpy as np
#from transformers import pipeline

from transformers import BertTokenizer, BertModel
import torch
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained("bert-base-uncased")

#r = sr.Recognizer()

import pyttsx3
engine = pyttsx3.init()

import random

# intents = ['DIRECTIVE','INFO_REQUEST','CONV_INQUIRY','CONV_OFFER',
#             'APPROVAL','DISAPPROVAL']

intents = ['DIRECTIVE','INFO_REQUEST','CONV_INQUIRY','CONV_OFFER',
            'APPROVAL','DISAPPROVAL']
#intents2 = ['directive', 'info request', 'conversation inquiry', 'conversation offer', 'approval', 'disapproval']

utterances = {'DIRECTIVE':["Turn on the lights"
                            "Open the door",
                            "Go right at the intersection",
                            "Buy some cupcakes while you're at the store",
                            "Would you turn the lights down please",
                            "Stop",
                            "Stop right there",
                            "Please don't do that again",
                            "Turn up the volume",
                            "Add milk to the shopping list, would you",
                            "Eat your vegetables",
                            "Don\'t knock over the vase",
                            "Can you pour me a glass of milk please",
                            "I want you to paint this wall blue"],
            'INFO_REQUEST':["How far away is the moon",
                            "What is a mars rover",
                            "Can you tell me where Colorado is",
                            "How many legs does a spider have",
                            "Tell me how to use a piano",
                            "Do you know who Benjamin Franklin is",
                            "Who was maralyn monroe",
                            "Name the ten largest animals on earth",
                            "why are butterflies so colorful",
                            "give me the current Dow Jones index",
                            "Tomorrows weather what will it be like",
                            "Jim Henson was the voice of which famous frog puppet",
                            "What should you do if your best friend is choking",
                            "If I am traveling to New Hampshire which freeway should I take",],
            'CONV_INQUIRY':["What\'s your name",
                            "Do you have a favorite movie",
                            "Who is your favorite actor",
                            "How\'s it going",
                            "Are you a fan of Stephen King",
                            "Will it snow tomorrow, do you think",
                            "Tell me your thoughts on polymorphism",
                            "What\'s your opinion on global warming",
                            "Okay, but what's your spirit animal",
                            "Have you ever watched Gone With the Wind",
                            "What would you do if you had a million dollars",
                            "Did you know that my favorite color is green",
                            "Would you like to play chess",],
            'CONV_OFFER':["My name is Jarvis",
                            "I am a student in Dr. Fulda\'s CS 401R class",
                            "I don\'t know much about geology but I think rocks are cool",
                            "If you gave me a cookie I would probably eat it",
                            "Pizza is my favorite food",
                            "My favorite movie is \"While You Were Sleeping\"",
                            "I am very fond of kittens",
                            "Be careful, I\'m highly trained in Karate, Ju Jitsu, and other cool terms",
                            "I like cats",
                            "I cannot stand the taste of broccoli",
                            "You would be surprised at how many movies I\'ve seen",],
            'APPROVAL':["That\'s great",
                        "awesome",
                        "I\'m glad to hear it",
                        "hey cool",
                        "hahaha",
                        "that\'s funny",
                        "I like that",],
            'DISAPPROVAL':["that\'s wrong",
                        "i am unhappy",
                        "you suck",
                        "why won\'t you listen to me you stupid robot",
                        "i\'m sad now",
                        "stop, just stop",
                        "no no no no no",
                        "i hate this",]}

#classifier = pipeline("zero-shot-classification",model="facebook/bart-large-mnli")


def calculateCosineSimilarity(textinput, model_in, tokenizer_in, utterances=["this is the place", "are we there yet", "arrived"]):
    with torch.no_grad():
        # calculate the embedding of the input text
        encoded_input = tokenizer_in(textinput.lower(), return_tensors='pt')
        input_output = model_in(**encoded_input)
        
        # set the input first dim as the max_dim, used for padding
        in_dim1_shape = input_output.last_hidden_state.shape[1]
        max_dim = in_dim1_shape

        utters_output = []
        for utter in utterances:
            encoded_input = tokenizer_in(utter.lower(), return_tensors='pt')
            utter_output = model_in(**encoded_input)
            utters_output.append(utter_output.last_hidden_state)

            # check to see if dim 1 embedding of each utterance is longer than input, if so, set new max
            if utter_output.last_hidden_state.shape[1] > max_dim:
                max_dim = utter_output.last_hidden_state.shape[1]
        
        # pad input embedding and utterances to match max dim
        in_out = torch.nn.functional.pad(input_output.last_hidden_state, (0, 0, 0, (max_dim - in_dim1_shape)))
        for i in range(len(utters_output)):
            utters_output[i] = torch.nn.functional.pad(utters_output[i],  (0, 0, 0, (max_dim - utters_output[i].shape[1])))

        # calculate the cosine similarity of the input to the utterances
        cosi = torch.nn.CosineSimilarity(dim=0)

        the_sum = []
        for utter in utters_output:
            the_sum.append(torch.sum(cosi(in_out, utter)).item())

        the_sum = sorted(the_sum, reverse=True)
        return sum(the_sum[0:3])/3


def detectIntent(text, utterances_in, intents_in):
    # Your intent classification code goes here.
    #
    # (feel free to define and call as many
    #  subsidiary functions as you like.)
    #detectedIntent = random.choice(intents)
    #return detectedIntent

    #return classifier(text, intents2, multi_label=True)['labels'][0]
    intentions = []

    for utter_key in utterances_in.keys():
        utter = utterances_in[utter_key]
        cosim = calculateCosineSimilarity(text, model, tokenizer, utter)
        intentions.append(cosim)

    calc_intents = np.array(intentions)
    print(calc_intents)
    return intents_in[np.argmax(calc_intents)]
    

def respond(text):
    detectedIntent = detectIntent(text, utterances_in=utterances)

    # Code to customize your response based
    # on the detected intent goes here.

    #response = "I don't know what to say about that. " + detectedIntent
    response = "Okay, I will " + detectedIntent
    return response


#if __name__=='__main__':
    #with sr.Microphone() as source:
    #    audio = r.listen(source)
    #    print("Start talking...")
    #    audio = r.record(source, duration=5)
    #    text = r.recognize_google(audio)
    #    response = respond(text)
    #    engine.say(response)
    #    engine.runAndWait()