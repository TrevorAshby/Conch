import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np

from transformers import BertTokenizer, BertModel
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

processor = AutoProcessor.from_pretrained("openai/whisper-tiny")
model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-tiny")

utterances = [[
    "Move this file to the Documents folder.",
    "I want to move the file called report.pdf to the Desktop.",
    "Can you move the file in the Downloads folder to the Pictures folder?",
    "Please move the file that I just opened to the Music folder.",
    "How do I move the file in the Recycle Bin to the Videos folder?",
    "Move the file with today\’s date to the Backup folder.",
    "Show me how to move the file in the Dropbox folder to the OneDrive folder.",
    "Move all the files in the Work folder to the Personal folder.",
    "What is the easiest way to move the file in the Google Drive folder to the iCloud folder?",
    "Move the file that I just downloaded to the USB drive."]]

def record_audio(duration=5, samplerate=16000):
    print("start talking")
    myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    myrecording = np.transpose(myrecording)
    print("done recording")
    return myrecording

def detect_spoken(myrecording):
    input_features = processor(myrecording[0], sampling_rate=16000, return_tensors="pt").input_features
    predicted_ids = model.generate(input_features)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    print("the model thought you said: ", transcription)
    return transcription

if __name__ == "__main__":
    duration = 5  # seconds
    fs = 16000
    print("start talking")
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    myrecording = np.transpose(myrecording)
    print("done recording")
    print(myrecording)
    print(myrecording.shape)

    #plt.plot(myrecording)
    #plt.savefig('./myplot.png')

    input_features = processor(myrecording[0], sampling_rate=16000, return_tensors="pt").input_features 

    # generate token ids
    predicted_ids = model.generate(input_features)
    # decode token ids to text
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    print(transcription)

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained("bert-base-uncased")
    encoded_input = tokenizer(transcription, return_tensors='pt')
    output = model(**encoded_input)
    print(output.keys())
    print(output["last_hidden_state"].shape)