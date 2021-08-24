import tkinter as tk     # python 3

from PIL import Image,ImageEnhance,ImageTk
import io
import numpy as np
import requests
# import tkinter as tk
baseURL = 'HTTP://192.168.0.17:5001'
def createImgTk(scale):
    img = requests.get(baseURL+'/image')
    im = Image.open(io.BytesIO(img.content))
    # im.show()
    
    # im = Image.open('test.png')
    w,h = im.size
    enhancer = ImageEnhance.Brightness(im)
    enhanced_im = enhancer.enhance(4)
    # enhanced_im.show()

    # window = tk.Tk()
    # window.title('select screen area')
    imgTk = ImageTk.PhotoImage(enhanced_im)
    imgTk = imgTk._PhotoImage__photo.subsample(scale)
    return imgTk

pos = []

class Example(tk.Frame):
    """Illustrate how to drag items on a Tkinter canvas"""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.scale = 2
        self.img2 = createImgTk(self.scale)
        w,h = self.img2.width(),self.img2.height()
        
        # create a canvas
        self.canvas = tk.Canvas(parent ,width=w, height=h, background="bisque")
        self.canvas.create_image(w//2,h//2,image=self.img2,tags=("no",))
        
        self.canvas.pack(fill="both", expand=True)
        
        # this data is used to keep track of an
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # create a couple of movable objects
        # 左下、右下、右上、左上
        try:
            p = np.load('p.npy')/self.scale
            print(p)
            if len(p)==0:
                p =[[w//3, h*2//3],[w*2//3, h*2//3],[w*2//3, h//3],[w//3, h//3]] 
        except:
            p = [[w//3, h*2//3],[w*2//3, h*2//3],[w*2//3, h//3],[w//3, h//3]]
        colors = ["red","yellow","green","blue"]
        for i in range(4):
            self.create_token(p[i][0], p[i][1], colors[i],("abcd")[i])
        
        
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.drag_stop)
        self.canvas.tag_bind("token", "<B1-Motion>", self.drag)
        for i in "abcd":
            self.canvas.tag_bind("r"+i, "<ButtonPress-1>", self.drag_start(i))
            self.canvas.tag_bind("r"+i, "<Enter>", self.onE(i))
            self.canvas.tag_bind("r"+i, "<Leave>", self.onL(i))
        
        def kill(event):
            for i in "abcd":
                id = self.canvas.find_withtag(i)[0]
                itm = self.canvas.coords(id)
                pos.append([(itm[0]+itm[2])*self.scale/2,(itm[1]+itm[3])*self.scale/2])
            parent.destroy()
        parent.bind('<Return>',kill)
    


    def onE(self,index):
        def on_enter(event):
            itm = self.canvas.find_withtag(str(index))[0]
            self.canvas.itemconfig(itm,stipple="gray12")
        return on_enter

    def onL(self, index):
        def on_leave(event):
            itm = self.canvas.find_withtag(str(index))[0]
            self.canvas.itemconfig(itm,stipple="gray50")
        return on_leave

    def create_token(self, x, y, color,tag):
        """Create a token at the given coordinate in the given color"""
        siz = 25
        self.canvas.create_rectangle(
            x - siz,
            y - siz,
            x + siz,
            y + siz,
            outline="black",
            fill=color,
            tags=("token",tag,"r"+tag),
            stipple="gray50")
        di = {"a":"左下","b":"右下","c":"右上","d":"左上"}
        self.canvas.create_text(x,y-siz//2,text=di[tag],tags=("token","r"+tag))
        self.canvas.create_text(x,y,text='+',tags=("token","r"+tag))

    def drag_start(self, tag):
        """Begining drag of an object"""
        # record the item and its location
        def startE(event):
            self._drag_data["item"] = "r"+tag
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y
        return startE

    def drag_stop(self, event):
        """End drag of an object"""
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def drag(self, event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

if __name__ == "__main__":
    root = tk.Tk()
    root.title('select screen area')
    Example(root).pack(fill="both", expand=True)
    root.mainloop()
    print(pos)
    np.save('p.npy',pos)