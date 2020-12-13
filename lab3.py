import nltk
from pathlib import Path
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
from nltk import *
from nltk.corpus import stopwords
from string import punctuation
import tkinter as tk
import math
from gensim.summarization.summarizer import summarize
from rake_nltk import Rake

doc_name = ""
text = ""
result = ""

root=Tk()
space0 = Label(root,text='\n')
aboutButton = Button(root,text='Help',width=8,height=2,bg='light grey')
chooseDocButton=Button(root,text='Select document',width=25,height=2,bg='blue')
detectButton=Button(root,text='Get key words and summarize',width=35,height=2,bg='orange')
resultText = tk.Text(root, state='disabled',width=120, height=25)
saveButton=Button(root,text='Save document',width=25,height=2,bg='green')
space1 = Label(root,text='\n')

def nameOf(path):
    return Path(path).stem

def chooseDocsClicked():
    global doc_name, text
    resultText.delete('1.0', END)
    files = filedialog.askopenfilename(multiple=False)
    splitlist = root.tk.splitlist(files)
    for doc in splitlist:
        doc_name = nameOf(doc)
        text = Path(doc, encoding="UTF-8", errors='ignore').read_text(encoding="UTF-8", errors='ignore')

def extract_keywords_from(text):
    r = Rake(max_length=5)
    r.extract_keywords_from_text(text)
    return ', '.join(r.get_ranked_phrases()[:5])

def get_essay(text):
    sentences = []
    for sentence in nltk.sent_tokenize(text):
        terms = []
        for term in nltk.word_tokenize(sentence):
            if term not in punctuation and term not in stopwords.words('russian') and term not in stopwords.words('german'):
                terms.append(term)
        sentences.append(terms)
    scores = []
    for sentence in sentences:
        score = 0
        for term in sentence:
            score += ((sentence.count(term)/len(sentence)) * 0.5 * (1+((sentence.count(term)/len(sentence))/(max_freq(sentence))))*math.log(len(sentences)/term_count(term, sentences)))
        scores.append(score)
    essay = ""
    for _ in range(int(len(sentences)/3)):
        current_max = max(scores)
        for i in range(len(scores)-1):
            if scores[i] == current_max:
                essay += nltk.sent_tokenize(text)[i]
                scores.remove(current_max)
                break
    return essay

def max_freq(sentence):
    result = 0
    for term in sentence:
        result = max(result,sentence.count(term))
    return result/len(sentence)

def term_count(term, sentences):
    result = 0
    for sentence in sentences:
        if term in sentence:
            result+=1
    return result

def detectClicked():
    global result
    result = ""

    result += "========= ESSAY ON TEXT: =========\n"
    result += get_essay(text)
    result += "\n\n========= SUMMARIZE: =========\n"
    result += summarize(text)
    result += "\n\n========= KEY WORDS: =========\n"
    result += extract_keywords_from(text)
    resultText.configure(state='normal')
    resultText.insert('end', result)
    resultText.configure(state='disabled')

def saveClicked():
    file = open(doc_name + '_result.txt', 'w', encoding="utf8")
    file.write(result)
    file.close()

def aboutButtonClicked():
    messagebox.showinfo("Development of a system for automatic summarization of documents", "Usage: Select document. Then click \"Get key words and summarize\" button.\nYou can also save result.")

aboutButton.config(command=aboutButtonClicked)
chooseDocButton.config(command=chooseDocsClicked)
detectButton.config(command=detectClicked)
saveButton.config(command=saveClicked)

space0.place(x=0, y=0)
aboutButton.place(x = 50, y = 10)
chooseDocButton.place(x = 190, y = 10)
detectButton.place(x = 480, y = 10)
resultText.place(x = 50, y = 80)
saveButton.place(x = 830, y = 10)
space1.place()
root.mainloop()
