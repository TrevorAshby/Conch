from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

model_name = "deepset/roberta-base-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

def detect_slot(text, question):
    # a) Get predictions
    
    QA_input = {
        'question': question,
        'context': text
    }
    res = nlp(QA_input)

    return res

if __name__ == "__main__":
    print("testing QA")
    print(detect_slot("i want to create a new file chimichangas.txt.", "What is the name of the file?"))
    print(detect_slot("Create a new folder named testing 123.", "What is the name of the folder?"))
    print(detect_slot("I want to move the file testing.txt to the folder what I Want.", "What is the name of the folder where the file should be moved?"))
    print(detect_slot("I want to move the file testing.txt to the folder what I Want.", "What is the file name?"))
    print(detect_slot("Take me up a folder.", "Does the user want to go up or down a folder?"))
    print(detect_slot("Go to previous folder.", "Does the user want to go up or down a folder?"))