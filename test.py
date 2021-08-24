import tkinter as tk     # python 3

from PIL import Image,ImageEnhance,ImageTk
import io

root = tk.Tk()
root.title('select screen area')
img2 = ImageTk.PhotoImage(Image.open('test.png'))
w,h = img2.width(),img2.height()
# create a canvas
cv = tk.Canvas(root ,width=w, height=h, background="bisque")
cv.create_image(0,0,image=img2)
cv.pack()
root.mainloop()