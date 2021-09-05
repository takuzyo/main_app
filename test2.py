import sys
import tkinter as tk
from threading import Thread

transcribe_words = []

def receive_words():
    global transcribe_words
    while True:
        line = sys.stdin.readline()
        if 'sentence1' in line:
            transcribe_words.append(line)
        
        if line == "":
            print("break")
            break

def get_words():
    word = None
    if len(transcribe_words):
        word = transcribe_words[0]
        del transcribe_words[0]

    return word


class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()

        master.title("HELLO")
        master.geometry("500x500")

        self.lab = tk.Label(text="aaaaaaaaaaaaaaaaaaaaaaaああああ")
        self.lab.place(x=100, y=200)
        self.x  = 0
        self.i = 100
        master.after(500, self.change)
    
    def change(self):
        self.lab.place(x=self.i, y=300)

        text = get_words()
        if text:
            self.lab['text'] = text
        self.i += 1
        
        self.after(500, self.change)


def main():
    global transcribe_words

    thread = Thread(target = receive_words)
    thread.start()



    root = tk.Tk()

    Application(root).mainloop()



if __name__ == '__main__':
    main()