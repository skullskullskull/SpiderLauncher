#! /usr/bin/env python3

import sqlite3
import tkinter as tk
from tkinter import ttk
import subprocess

root = tk.Tk()
root.title("Spider Launch")
#root.minsize(500, 200)
#root.geometry("370x300") #frame will fit to elements (like ttk.Notebook's size) otherwise. 

style = ttk.Style()
style.configure('TNotebook', tabposition='wn') #'wn' as in compass directions
style.configure('TNotebook.Tab', width=10)# default is to fit tab width to string length. 
box = ttk.Notebook(root, width=400, height=450)

dynamic_buttons = []
listSys = []

db = sqlite3.connect('.Spiderdb.db')
c = db.cursor()
c.execute('''select DISTINCT TAGS from SL ORDER BY LOWER(TAGS)''')

for it in c:
    listSys.append(it[0])

for num in listSys:
	tab = tk.Frame(root)
	box.add(tab, text=num)
	dynamic_buttons.append(tab)

box.enable_traversal() #Control-Tab will select the tab after the one currently selected. 
box.pack(side=tk.TOP)

def launchGame(launcher,game):
	# launcher='mednafen'
	# game="MP.zip"
	# subprocess.call([program, parameter])
	program=launcher.rstrip().split(" ") #deals with whitespace in launcher string (eg 'PCSX2 --nogui')
	program.append(game)
	subprocess.Popen(program)
	
for sys in range(0,len(listSys)): #sys is TAGS in database
	text = tk.Text(dynamic_buttons[sys], wrap="none")
	vsb = tk.Scrollbar(dynamic_buttons[sys], orient="vertical", command=text.yview)
	text.configure(yscrollcommand=vsb.set)
	vsb.pack(side="right", fill="y")
	text.pack(fill="both", expand=True)

	c.execute('''select * from SL where TAGS=? ORDER BY LOWER(NAME)''', (listSys[sys],))
	for it in c:
		#b is the handle for the button. using b for the 'next' button overwrites the command, unless we pass it as opt1 & opt2. 
		b = tk.Button(root, text="%s" % it[0], command=lambda opt1=it[1],opt2=it[2]: launchGame(opt1,opt2), width=41)
		text.window_create("end",padx=10, window=b)
		text.insert("end", "\n")

	text.configure(state="disabled") # to disable cursor in button text box

c.close()
root.mainloop()
