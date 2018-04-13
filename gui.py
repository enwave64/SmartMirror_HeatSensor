from tkinter import *
import datetime
from data_fetch2.py import getValues

root = Tk()


frame = Frame(root)

# somehow loop the updates of the values.
temp = value[1]
humidity = value[3]
date = datetime.date.today().isoformat()
Label(frame, text=temp).pack()

Label(frame, text=humidity).pack()
Label(frame, text=date).pack()


frame.pack()

root.mainloop()

