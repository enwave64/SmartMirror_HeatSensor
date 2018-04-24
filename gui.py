from tkinter import *
from client import main, getValues
import datetime
import threading

root = Tk()
root.configure(bg="black")

def escape(root):
        root.geometry("200x200")

def fullscreen(root):
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (width, height))
        root.overrideredirect(1)

master = root
width, height = master.winfo_screenwidth(), master.winfo_screenheight()
master.geometry("%dx%d+0+0" % (width, height))
master.bind("<Escape>", lambda a :escape(master))
master.bind("<F1>", lambda b: fullscreen(master))


lab1 = Label(root)
lab2 = Label(root)
lab3 = Label(root)
lab4 = Label(root)
lab1.grid(row=1, column=1)
lab2.grid(row=1, column=0, sticky=W, padx=(120,180))    
lab3.grid(row=1, column=2, sticky=E, padx=(180,10))
lab4.grid(row=5, column=1)

thread = threading.Thread(target=main, args=())  #start client in new thread
thread.daemon = True                            # Daemonize thread
thread.start()                                              

def poll():         # update labels in GUI
    time = datetime.datetime.now().strftime("%H:%M:%S")
    quote = "\"Just because something doesn’t \ndo what you planned it to do doesn’t\n mean it’s useless.\" - Thomas Edison"
    lab1.config(text=time, fg="white", bg="black", font=("garamond", 54))
    lab4.config(text=quote, fg="white", bg="black", font =("garamond", 33))
    values = getValues()
    if len(values) >=2:
        temp = "Temperature \n"+values[0]+" °F"
        hum = "Humidity \n"+values[2]+" %"
        lab2.config(text=temp, fg="white", bg="black", font=("garamond", 44))
        lab3.config(text=hum, fg="white", bg="black", font=("garamond", 44))
    root.after(1000, poll) # start over again

# run first time
poll()
root.mainloop()
master.mainloop()
