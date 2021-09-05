# tkinterのインポート
import tkinter as tk
from tkinter.constants import FALSE
from PIL import Image, ImageTk
import random
import sys
from threading import Thread
from mystery import Mystery
import time
import re

# 表示するウィンドウの幅と高さ
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600

#センサー距離
SENSOR_DISTANCE = 3

#開始用のセリフ
START_SENTENCE = 'すたーと'

global transcribe_words

class Window(tk.Tk): 
    """
    TKクラスを継承、Windowクラスとする
    """

    def __init__(self, text):
        """
        ウィンドウを生成する（タイトルを指定）
        """
        tk.Tk.__init__(self)
        self.title(text)


    def setSize(self, width, height, isCenter = True):
        """
        サイズを指定、ディスプレイ中央に表示する
        """
        # サイズを指定した文字列
        geometry = "{0}x{1}".format(width, height)

        if isCenter:    # ディスプレイ中央に表示する            
            # ディスプレイの幅と高さを取得
            s_width = self.winfo_screenwidth()
            s_height = self.winfo_screenheight()
            # 表示する左上の座標を算出        
            win_left = int((s_width - width) / 2)
            win_top = int((s_height - height) / 2)
            # 表示位置を指定した文字列を追加
            geometry += "+{0}+{1}".format(win_left, win_top)

        # サイズと表示位置を中央に指定（幅 x 高さ + 左位置 + 上位置）
        self.geometry(geometry)

    def disableMaximum(self):
        """
        最大化を制限する
        """
        self.resizable(False, False)

def change_window(window):
    window.tkraise()

def put_image(frame):
     #Canvasの作成
    
    canvas = tk.Canvas(frame, bg = "black" ,width=897, height=497)
    item = canvas.create_image(0, 0, image=imglist[0],anchor='nw')
    #Canvasを配置
    canvas.pack(expand= True)

    kw = {
        "canvas": canvas,
        "item": item,
    }

    return kw


def define_image():
    """
    画像読み込み
    """
    img = Image.open('./img/start.png')
    img = ImageTk.PhotoImage(img)


    global imglist
    imglist = [img]


def reading(sensor):
    """
    超音波センサーの読み込み
    """


    try:
        import RPi.GPIO as GPIO
    except ModuleNotFoundError:
        return 4
    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BOARD)
    TRIG = 11
    ECHO = 13

    if sensor == 0:
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        GPIO.output(TRIG, GPIO.LOW)
        time.sleep(0.3)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            signaloff = time.time()

        while GPIO.input(ECHO) == 1:
            signalon = time.time()

        timepassed = signalon - signaloff
        distance = timepassed * 17000
        return distance
        GPIO.cleanup()
    else:
        print("Incorrect usonic() function varible.")

def check_phone():
    """
    スマホが装置に置かれたか確認
    """
    dis = reading(0)
    print('phone distance : ' + str(dis))
    if SENSOR_DISTANCE > dis:
        print('phone available')
        return True

def receive_words():
    """
    juliusからの標準入力を受け取り単語を取得
    """
    global transcribe_words
    while True:
        line = sys.stdin.readline()
        if 'sentence1' in line:
            line = re.findall('\>(.*)\<', line)
            line = line[0].replace(" ","")
            transcribe_words.append(line)
        
        if line == "":
            print("receive julius results finish")
            break

def get_words():
    """
    受け取った単語を使えるように
    """
    word = None
    if len(transcribe_words):
        word = transcribe_words[0]
        del transcribe_words[0]

    return word

def check_start(kw):
    """
    開始確認
    """
    phone_able = check_phone()
    word = get_words()

    if phone_able:
        if word ==  START_SENTENCE:
            print('start app')
            sub_frame = App(root)

            change_window(sub_frame)
        else:
            root.after(500, check_start)
    else:
        """
        スマホが置かれてないことを強調する
        """
        global big_start
        big_start = Image.open('img/start2.png')
        big_start = ImageTk.PhotoImage(big_start)

        kw['canvas'].itemconfig(kw['item'], image=big_start)


        root.after(2000, delete_img, kw)

def delete_img(kw):
    kw['canvas'].itemconfig(kw['item'], image=imglist[0])
    root.after(2000, check_start, kw)


class App(tk.Frame):
    def __init__(self, master = None):
        
        super().__init__(master)
        #self.pack()
        self.grid(row=0, column=0, sticky="nsew")

        label1_frame_app = tk.Label(self, text="答えがわかったら叫んでね！")
        label1_frame_app.pack()
        self.mystery = Mystery()

        self.put_image(master)
    
    def put_image(self, master):
        mystery_image = self.mystery.get_mystery()

        global img
        img = Image.open(mystery_image)
        img = ImageTk.PhotoImage(img)

        canvas = tk.Canvas(self, bg = "black" ,width=897, height=497)
        item = canvas.create_image(0, 0, image=img,anchor='nw')
        #Canvasを配置
        canvas.pack(expand = True)

        self.canvas = canvas
        self.item = item

        master.after(500, self.check_voice, master)


    def change_image(self, master):
        #終了判定
        if self.mystery.fin:
            fin_img = Image.open('img/end.png')
            fin_img = ImageTk.PhotoImage(fin_img)

            canvas = tk.Canvas(self, bg = "black" ,width=897, height=497)
            canvas.create_image(0, 0, image=fin_img,anchor='nw')

            #Canvasを配置
            canvas.pack(expand = True)
        else:
            mystery_image = self.mystery.get_mystery()

            global img
            img = Image.open(mystery_image)
            img = ImageTk.PhotoImage(img)

            self.canvas.itemconfig(self.item, image=img)

        master.after(500, self.check_voice, master)
    
    def check_voice(self, master):
        #print(transcribe_words)

        word = get_words()
        flag = self.mystery.check_answer(word)
        if flag:
            self.change_image(master)
        else:
            master.after(500, self.check_voice, master)
    


if __name__ == "__main__":
    transcribe_words = []

    thread = Thread(target = receive_words)
    thread.start()

    # rootメインウィンドウの設定
    root = Window('メインウィンドウ')
    root.setSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    #root.attributes('-fullscreen', True)

    # rootメインウィンドウのグリッドを 1x1 にする
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # メインフレームの作成と設置
    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")

    define_image()
    kw = put_image(main_frame)
    root.after(2000, check_start, kw)

    # アプリフレームの作成と設置

    # mainframeを前面にする
    main_frame.tkraise()

    root.mainloop()