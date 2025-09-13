from transformers import pipeline

qa = pipeline("question-answering", model="google-bert/bert-large-uncased")

text1 = "Intel® Core™ Ultra 9 Processor 185H (24MB Cache, up to 5.1 GHz, 16 cores, 18 core, 22 Threads)"
text2 = "Intel Core i7 14650HX (16 cores 24 threads, max clock speed can reach 5.2GHz with Turbo boost, 30MB Intel® Smart Cache)"


questions = [
    "What is the cache size?",
    "What is the boost clock speed?",
    "How many cores?",
    "How many threads?",
]

for text in (text1, text2):
    print(f"\nInput: {text}\n")
    for q in questions:
        result = qa(question=q, context=text)
        print(f"{q}: {result['answer']}")
