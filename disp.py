# tkinterのインポート
import tkinter as tk
from PIL import Image, ImageTk
import random
import sys

# 表示するウィンドウの幅と高さ
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600

SENSOR_DISTANCE = 9

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

def repeat_image(kw):
    """
    画像を読み込む
    """
    rnd = random.randint(0,3)
    print(imglist[rnd])

    kw['canvas'].itemconfig(kw['item'], image=imglist[rnd])

    root.after(3000, repeat_image, kw)

def define_image():
    img = Image.open('sample.jpg')
    img = ImageTk.PhotoImage(img)

    img2 = Image.open('sample2.jpg')
    img2 = ImageTk.PhotoImage(img2)

    img3 = Image.open('sample3.jpg')
    img3 = ImageTk.PhotoImage(img3)

    img4 = Image.open('sample4.jpg')
    img4 = ImageTk.PhotoImage(img4)

    global imglist
    imglist = [img, img2, img3, img4]

'''
def reading(sensor):
    import time
    import RPi.GPIO as GPIO
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
'''

def reading(sensor):
    rnd = random.randint(0,10)
    return rnd

def check_phone():
    dis = reading(0)
    print('phone distance : ' + str(dis))
    if SENSOR_DISTANCE > dis:
        boot_flag = True
        print('phone available')

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

if __name__ == "__main__":
    global boot_flag
    transcribe_words = []


    # rootメインウィンドウの設定
    root = Window('メインウィンドウ')
    root.setSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    root.disableMaximum()
    #root.attributes('-fullscreen', True)

    check_phone()

    # rootメインウィンドウのグリッドを 1x1 にする
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # メインフレームの作成と設置
    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")

    # 各種ウィジェットの作成
    label1_frame = tk.Label(main_frame, text="メインウィンドウ")
    button_change = tk.Button(main_frame, text="Go to frame1", command=lambda:change_window(sub_frame),width=10,height=10, bg="#80ff80")

    define_image()

    # 各種ウィジェットの設置
    label1_frame.pack(side=tk.TOP)
    button_change.pack(side=tk.TOP)

    # アプリフレームの作成と設置
    sub_frame = tk.Frame(root)
    sub_frame.grid(row=0, column=0, sticky="nsew")

    # 各種ウィジェットの作成
    label1_frame_app = tk.Label(sub_frame, text="アプリウィンドウ")
    button_change_frame_app = tk.Button(sub_frame, text="メインウィンドウに移動", command=lambda:change_window(main_frame))

    # 各種ウィジェットの設置
    label1_frame_app.pack()
    button_change_frame_app.pack()

    #Canvasの作成
    canvas = tk.Canvas(sub_frame, bg = "black" ,width=656, height=656)
    item = canvas.create_image(0, 0, image=imglist[0],anchor='nw')
    #Canvasを配置
    canvas.pack()

    kw = {
        "canvas": canvas,
        "item": item
    }

    # mainframeを前面にする
    main_frame.tkraise()

    root.after(3000, repeat_image, kw)
    root.mainloop()