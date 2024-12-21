import tkinter as tk
from tkinter import messagebox as mb    
from tkinter import ttk
import random as rand

# CONSTANTS
root = tk.Tk()
root.title("Minesweeper")
background = "#B2BEBF"
root.configure(bg=background)
txtColor = "#262524"
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Courier New", 10), padding=10)
fStyle = ("Courier New", 25)

# GLOBALS
difficulty = "Easy"
first_click = True
cells = []
seconds = 0
H = 9
W = 9
N = 10
continueTimer = True
timer_id = None
gameWon = False

def grid_maker(h, w, frame, diff):
    global cells, H, W, difficulty, first_click, seconds, continueTimer
    stopTimer()
    continueTimer = True
    first_click = True
    cells.clear()
    H = h 
    W = w 
    seconds = 0
    
    timer_label.config(text=str(seconds))

    for widget in frame.winfo_children():
        widget.destroy()
        
    for x1 in range(h):
        a = []
        for y1 in range(w):
            if x1 % 2 == 0 and y1 % 2 == 0 or x1 % 2 != 0 and y1 % 2 != 0:
                bg_color = "#486966"
            else: 
                bg_color= "#889C9B"
            bottone = tk.Button(frame, width=2, height=1, bg= bg_color, command= lambda x=x1, y=y1: play(x,y))  
            bottone.grid(column=y1, row=x1)
            bottone.bind("<Button-3>", lambda event, x=x1, y=y1: flag(x,y))
            a.append({"btn": bottone, "adjacent": 0, "bomb": False, "revealed": False})   #tiene conto del bottone, imposta le celle agiacenti a 0 (aggiornate dopo)
        cells.append(a)

    difficulty = diff

def flag(x,y):
    global cells, N
    if not cells[x][y]["revealed"]:
        if cells[x][y]["btn"]["text"] != "🚩":
            cells[x][y]["btn"].config(text="🚩")
            N-=1
        else:
            cells[x][y]["btn"].config(text="")
            N+=1
    bombs_label.config(text=str(N))


def play(x, y):
    global first_click
    if first_click:
        calc_bombs(x, y)
        update_timer()
        first_click = False
    if cells[x][y]["bomb"]:
        cells[x][y]["btn"].config(text="🚩")
        stopTimer()
        mb.showerror("Minesweeper", "You Lost")
        root.destroy()
    else:  
        reveal(x,y)
    
    
def reveal(x, y):
    global gameWon
    if x % 2 == 0 and y % 2 == 0 or x % 2 != 0 and y % 2 != 0:
        bgColor = "#a8a8a8"
    else: 
        bgColor = "#e3e3e3"
    adjacent = count_adjacent(x, y)
    cells[x][y]["revealed"] = True
    if adjacent == 0:
        cells[x][y]["btn"].config(text="", bg=bgColor)
        for x1 in [-1, 0, 1]:
            for y1 in [-1, 0, 1]:
                if x1 == 0 and y1 == 0:
                    continue
                nx, ny = x1 + x, y1 + y
                if nx >= 0 and nx < H and ny >= 0 and ny < W and not cells[nx][ny]["revealed"]:
                    reveal(nx, ny)
    else:
        cells[x][y]["btn"].config(text=str(count_adjacent(x,y)), bg=bgColor)
        
    if checkWin() and not gameWon:
        gameWon = True
        stopTimer()
        mb.showinfo("Minesweeper", "You Won!!!")
        root.destroy()
   
        
def calc_bombs(x1, y1):
    global cells, N
    if difficulty == "Easy":
        N = 10
    elif difficulty =="Normal":
        N = 40
    else:
        N = 99
    
    print(H, W)
    bombs = 0
    notValid = []
    for x2 in [-1, 0, 1]:       #fa un controllo delle celle attorno
        nx = x1 + x2
        for y2 in [-1, 0, 1]:
            ny = y1 + y2     #aggiorna le coordinate rispettive a quelle vere
            notValid.append((nx, ny))
            
    while N != bombs:
        x = rand.randrange(H)
        y = rand.randrange(W)
        if (x, y) not in notValid and not cells[x][y]["bomb"]:
            #cells[r][c]["btn"].config(text="🚩")
            cells[x][y]["bomb"] = True
            bombs += 1
            
                
def count_adjacent(x, y):
    adjacent = 0
    for x1 in [-1, 0, 1]:       #fa un controllo delle celle attorno
        for y1 in [-1, 0, 1]:
            if x1 == 0 and y1 == 0: #se il controllo è su se stessa salta linea 31
                continue
            nx, ny = x + x1, y + y1     #aggiorna le coordinate rispettive a quelle vere
            if nx >= 0 and nx < H and ny >= 0 and ny < W:     #controlla se la cella appartiene alla griglia
                if cells[nx][ny]["bomb"] == True:                #se la cella è attiva aggiorna adiacenti      
                    adjacent += 1
    return adjacent

def update_timer():
    global seconds, timer_id, continueTimer
    seconds += 1
    timer_label.config(text=str(seconds))
    if continueTimer:
        timer_id = root.after(1000, update_timer)

def stopTimer():
    global timer_id, continueTimer
    if timer_id is not None:
        root.after_cancel(timer_id)
    continueTimer = False  
    
def checkWin():
    for x in range(H):
        for y in range(W):
            if not cells[x][y]["bomb"] and not cells[x][y]["revealed"]:
                return False    
    return True
    
timer_frame = tk.Frame(root, padx=10, pady=10, bg=background)
timer_frame.pack()
main_frame = tk.Frame(root, padx=10, pady=10, bg=background)
main_frame.pack()
tools_frame = tk.Frame(root, bg=background, padx=10, pady=10)
tools_frame.pack()

timer_label = tk.Label(timer_frame, text="00", font=fStyle, bg=background, fg=txtColor)
timer_label.pack(side="left")
space_label = tk.Label(timer_frame, text="                       ", bg=background)
space_label.pack(side="left")
bombs_label = tk.Label(timer_frame, text=str(N), font=fStyle, bg=background, fg=txtColor)
bombs_label.pack(side="left")

grid_maker(W, H, main_frame, "Easy")
btn_easy = ttk.Button(tools_frame, text="EASY", command= lambda: grid_maker(9, 9, main_frame, "Easy"))
btn_easy.pack(side="left")
btn_normal = ttk.Button(tools_frame, text="NORMAL", command= lambda: grid_maker(16, 16, main_frame, "Normal"))
btn_normal.pack(side="left")
btn_difficult = ttk.Button(tools_frame, text="DIFFICULT", command= lambda: grid_maker(16, 30, main_frame, "Hard"))
btn_difficult.pack(side="left")


root.mainloop() 