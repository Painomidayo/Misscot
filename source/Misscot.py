import sys
import os
import pyperclip
import requests
from misskey import Misskey
from enum import Enum
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image

root = Tk()
a = 1

#マスコットwindow
root.title('misscot')
win_width = 102
win_height = 162
w = root.winfo_screenwidth()        #画面の幅を取得
h = root.winfo_screenheight()       #画面の高さを取得
x = w - win_width
y = h - win_height - 20
root.geometry(str(win_width) + 'x' + str(win_height) + '+'+str(x)+'+'+str(y))
root.resizable(False,False)     #サイズ変更不可
root.config(bg='white')
root.attributes('-topmost',True)        #最前列表示
root.wm_protocol(name = 'WM_DELETE_WINDOW',func='delfimc')
root.overrideredirect(boolean=True)     #タイトルバーをTrueで消す
root.attributes('-transparentcolor','white')      #白色を透過


#画像を表示
#実行ファイルからの絶対パスを取得
if getattr(sys,'frozen',False):
    script_dir = sys._MEIPASS
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir,"FLAG_BLOB.png")
print("aoaoa")
print(file_path)
print('b')
#ファイルの確認
shuiro = file_path
print(shuiro)

murakamisan = 'source\FLAG_BLOB.png'
if getattr(sys,'frozen',False):
    im = PhotoImage(file = shuiro)
    print('a')
else:
    im = PhotoImage(file = murakamisan)
    print('b')

n_im = im.subsample(10,10)
label1 = Label(root,bg='white',image=n_im)      #背景が白だから透過される

#おはなしきのう

talk = "こんにちは" #全角半角15文字まで
label2 = Label(root,text=talk)

#メニューを表示
def Pop_menu(self):
    menu.post(self.x_root,self.y_root)      

def exit():
    root.quit()
    #root.destroy()

#移動させる
def move():
        global a
        if (a == int(1)):
            root.overrideredirect(boolean=False)
            a = int(0)
        else:
            root.overrideredirect(boolean=True)
            a = int(1)

#しなちくAPI
def shinachi():
    API_Endpoint = 'https://api.thinaticsystem.com/v1/debobigego'
    result = requests.get(API_Endpoint)
    data = str(result.json())       #取得例：{'generated': 'ジローデ'}
    data = data[15:]        #前半を消す 例：ジローデ'}
    data = data[:-2]        #後半を消す 例：ジローデ

    messagebox.showinfo(title='しなちく',message=data)


    #apiトークンの読み込み
    if getattr(sys,'frozen',False):
        script_dir = sys._MEIPASS
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir,'api.txt')

    apifile = file_path

    f = open(apifile,'r')
    datalist = f.readlines()
    sitename = datalist[0].rstrip('\n')
    api = Misskey(sitename)   
    api.token = datalist[1].rstrip('\n')
    f.close

    api.notes_create(text= '「' + data + '」\nhttps://thinaticsystem.com/\n#しなちくシステム無料ガチャ',visibility=NoteVisibility.PUBLIC)

#設定メニュー
def Option():
    #ウィンドウ設定
    op_win = Toplevel()
    op_win.title('設定')
    op_win.geometry('300x80')

    #インスタンス入力（未実装）
    frame2 = ttk.Frame(op_win)
    label2 = Label(frame2,text='インスタンス名->')
    ins_name = StringVar()
    entry2 = Entry(frame2,textvariable=ins_name)
    #API入力
    frame3 = ttk.Frame(op_win)
    label3 = Label(frame3,text='APIトークン->')
    new_api = StringVar()
    entry3 = Entry(frame3,width='35',textvariable=new_api)

    #ファイルに保存
    def save():
        if getattr(sys,'frozen',False):
            script_dir = sys._MEIPASS
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir,'api.txt')

        apifile = file_path
        print(apifile)
        print(new_api.get())
        f = open(apifile,mode='w')
        f.write(ins_name.get() + '\n' + new_api.get())
        f.close()
        messagebox.showinfo(title='保存',message='保存が完了しました')
    frame4 = ttk.Frame(op_win)
    button2 = Button(frame4,text='保存',command=save)

    #パック    
    frame2.grid(row=0,column=0)
    frame3.grid()
    frame4.grid()
    label2.pack(side=LEFT)
    entry2.pack(side=TOP)
    label3.pack(side=LEFT)
    entry3.pack(side=TOP)
    button2.pack(side=TOP)

#misskey
#公開範囲
class NoteVisibility(Enum):
    PUBLIC = 'public'
    HOME = 'home'
    FOLLOWERS = 'followers'
    SPECIFIED = 'specified'    



def misskey():
    #パス検索
    if getattr(sys,'frozen',False):
        script_dir = sys._MEIPASS
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir,'api.txt')

    apifile = file_path

    #apiトークンの読み込み
    apifile = file_path

    f = open(apifile,'r')
    datalist = f.readlines()

    sitename = datalist[0].rstrip('\n')
    api = Misskey(sitename)   
    api.token = datalist[1].rstrip('\n')
    f.close

    #ノート作成
    def note_create():
        #投稿範囲取得
        nv = notevisi_var.get()
        if nv == 'パブリック':
            visi = NoteVisibility.PUBLIC
        elif nv == 'ホーム':
            visi = NoteVisibility.HOME
        elif nv == 'フォロワー':
            visi = NoteVisibility.FOLLOWERS
        elif nv == 'ダイレクト':
            visi = NoteVisibility.SPECIFIED
        else:
            return messagebox.showinfo(message='投稿範囲を選択してね')
        
        #note
        note = str(honi.get())
        newnote = api.notes_create(text=note,visibility=visi)
        entry1.delete(0,'end')
        noteid = newnote['createdNote']['id']
        pyperclip.copy(noteid)
        return messagebox.showinfo(title='投稿完了',message='投稿が完了しました')

    #NoteWindow定義
    sub_win = Toplevel()
    sub_win.title('Misskey')
    frame1 = ttk.Frame(sub_win,padding=20)
    honi = StringVar()
    entry1 = ttk.Entry(frame1,textvariable=honi)
    #コンボボックス
    notevisi_var = StringVar()
    notevisi = ttk.Combobox(frame1,textvariable=notevisi_var)
    notevisi.bind('<<ComboboxSelected>>')
    notevisi['values'] = ('パブリック','ホーム','フォロワー','ダイレクト')
    notevisi.state(["readonly"])
    button1 = ttk.Button(sub_win,text="ノート",command=note_create)
    
    
    frame1.pack()
   
    notevisi.pack(side=TOP)
    entry1.pack(side=LEFT)
    button1.pack(side=TOP)

#メニュー
menu=Menu(root,tearoff=0)       #メニューを作る
menu.add_command(label='のーと',command=misskey)      #メニューの中身
menu.add_command(label='しなち',command=shinachi)
menu.add_command(label='いどう',command=move)
menu.add_command(label='せってい',command=Option)
menu.add_command(label='とじる',command=exit)


#右クリ
label1.bind('<ButtonPress-3>',Pop_menu)


label1.pack()
label2.pack()
print('aaa')
root.mainloop()