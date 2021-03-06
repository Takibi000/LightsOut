import tkinter
import random
import os
import copy

# マウスの使用で使う変数
mouse_x = 0
mouse_y = 0
mouse_c = 0

# パネルの管理用のリスト
p_val = [31, 31, 31, 31, 14]

# 初期パネル用リスト
o_val = copy.deepcopy(p_val)

# 画像の中心位置のｘ，ｙ
imgx = 500
imgy = 350

# パネルの開始位置の調整用の変数
sx = 500 - (imgx/2)
sy = 350 - (imgx/2)

# 画像リスト
img_list = []
path = "img/illustration"
# 対象のフォルダに含まれる画像情報を取得
for i in os.listdir(path):
    img_list.append(os.path.join(path, i))
#img_list = ["Img/Img01.png"]

# タイマー用の変数
tmr = 0
tmr_count = 0
end_flg = 0

# ライフ用変数（残りリセット回数）
life_count = 3

b_color = "skyblue"

# マウスカーソルの位置の取得関数
def mouse_move(e):
    global mouse_x, mouse_y
    mouse_x = e.x
    mouse_y = e.y

# マウスのクリックの検出関数
def mouse_press(e):
    global mouse_c
    mouse_c = 1

# メインプログラム
def game_main():
    global mouse_c, tmr, tmr_count, life_count, b_color
    b_color = "skyblue"
    if end_flg == 0:
        tmr_count += 1
        # タイマーラベルに現在時刻を入れる処理
        time_label["text"] = "{}:{}:{}".format('%02d' %int(tmr/360),'%02d' % (int(tmr/60)%60),'%02d' %(tmr%60))
    # メインプログラムが５回で１秒なので５回目に秒数追加の処理
    if tmr_count == 5:
        # カウンターリセット
        tmr_count = 0
        tmr += 1
    # クリック位置が有効かの判定
    if mouse_c == 1 and sx <= mouse_x and mouse_x < 5*100+sx and sy <= mouse_y and mouse_y < 5*100+sy:
        # クリックされたフラグのリセット
        mouse_c = 0
        # マウスの座標からパネルの番号の算出
        select_x = int((mouse_x-sx)/100)
        select_y = int((mouse_y-sy)/100) 
        # X座標の番号からリスト変更用のマスクの作成       
        px = 2 ** (4 - select_x)
        for n, i in enumerate(p_val):
            # Y座標が一致している場合にpxと左右に１を立てたマスクでXOR
            if n == select_y:
                p_val[n] ^= (px + (px//2) + ((px*2)%32))
            # Y座標が一致した場合にpxでXOR
            elif n == (select_y - 1) or n == (select_y + 1):
                p_val[n] ^= px
            # 上記以外は何もしない
            else:
                continue
    elif mouse_x >= (imgx + 300) and mouse_x <= (imgx + 450) and mouse_y >= (imgy + 40) and mouse_y <= (imgy + 120):
        b_color = "powderblue"
        if mouse_c == 1:
            if life_count > 0:
                p_create()
                life_count -= 1
                draw_life()
            mouse_c = 0
    # 範囲外でクリックされた場合の処理
    else: mouse_c = 0
    # draw関数の呼び出し
    draw_p()
    reset_btn_draw()
    # 指定した時間の後に関数の再実行
    root.after(200, game_main)

# 画像の描画
def draw_img():
    canvas.create_image(imgx, imgy, image = imgphoto, tag="main_img")

# パネルの描画
def draw_p():
    global end_flg
    p_count = 0
    # tileタグの図形の削除
    canvas.delete("tile")
    for y, i in enumerate(p_val):
        # リストの数字を５桁の２進数に変換
        w = bin(i).replace('0b', '')
        w = ((5-len(w))*'0')+w
        for x, j in enumerate(w):
            if int(j) == 1:
                canvas.create_rectangle(x*100+sx, y*100+sy, x*100+100 +sx, y*100+100+sy, fill="lightgray", width=0, tag="tile")
                p_count += 1
    # 描画するパネルが無い場合クリアなので終了フラグを立てる
    if p_count == 0:
        end_flg = 1

# ライフの描画
def draw_life():
    canvas.delete("life")
    canvas.create_text(imgx + 375, imgy - 80, text="LIFE", tag="life", font=("times New Roman", 24), fill="white")
    for n in range(life_count):
        x1 = imgx + 320 + (n * 45)
        y1 = imgy - 35
        x2 = x1 + 20
        y2 = y1
        x3 = x1 + 10
        y3 = y1 + 50
        canvas.create_polygon(x1+5, y1-10, x2-5, y2-10, x3, y3-50, fill="green", tag="life")
        canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill="orange", tag="life")

# パネルのリセット
def p_create():
    global p_val
    p_val = copy.deepcopy(o_val)
    draw_p()

def reset_btn_draw():
    canvas.delete("BTN")
    # リセットボタンの描画
    canvas.create_oval(imgx + 300, imgy + 40, imgx + 450, imgy + 120, fill=b_color, outline="white", width=5, tag="BTN")
    canvas.create_text(imgx + 375, imgy + 80, text="RESET", font=("times New Roman", 20), fill="white", tag="BTN")

root = tkinter.Tk()
# ウィンドウのタイトル指定
root.title("Lights Out")
# ウィンドウの表示位置
root.geometry("1000x700+200+0")
# ウィンドウのサイズと背景色の指定
canvas = tkinter.Canvas(root, width=1000, height=700, bg="black")
# ウィンドウサイズを変更不可にする
root.resizable(False, False)
# マウスのクリックに関数を付加
root.bind("<ButtonPress>", mouse_press)
# マウスの移動に関数を付加
root.bind("<Motion>", mouse_move)
# 画像のファイル指定
imgphoto = tkinter.PhotoImage(file=random.choice(img_list))
# 背景画像のファイル指定
backimg = tkinter.PhotoImage(file="img/backImg.png")
# メッセージボードの画像ファイルを指定
#msgimg = tkinter.PhotoImage(file="Img.png")
canvas.pack()
# 背景画像の描画
canvas.create_image(imgx, imgy, image = backimg, tag="main_img")
#canvas.create_image(imgx + 375, imgy - 50, image = msgimg, tag="main_img")
canvas.create_text(imgx + 375, imgy - 200, text="TIME", tag="time", font=("times New Roman", 24), fill="white")
# タイマー用ラベルの設定
time_label = tkinter.Label( font=("times New Roman", 24), bg='orange', fg="white")
time_label.place(x=imgx + 320, y=imgy - 170)
reset_btn_draw()
p_create()
draw_img()
draw_p()
draw_life()
game_main()
root.mainloop()