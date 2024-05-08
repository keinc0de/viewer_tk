import tkinter as tk
from pathlib import Path
from PIL import ImageTk, Image, ImageOps


class ViewerTk(tk.Frame):
    """visor de imagenes basico (no gifs)
    """
    def __init__(self, parent, bg="gray"):
        super(ViewerTk, self).__init__(master=parent, bg=bg)
        self.parent = parent
        self.bg = bg
        self.IMG = None
        self.AJUSTAR = False
        self._config_viewer()
        
    def _config_viewer(self):
        self.cv = tk.Canvas(master=self.parent, bg='red', borderwidth=0, bd=0)
        self.cv.grid(row=0, column=0, sticky='wens')
        self.bind("<Configure>", self.resizer)
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)

    def asigna_imagen(self, archivo):
        img = Path(archivo).as_posix()
        img_tk = ImageTk.PhotoImage(Image.open(img))
        w = img_tk.width()
        h = img_tk.height()
        self.IMG = {
            'imagen':img,
            'w':w, 'h':h, 'ar':w//h,
            'img_tk':img_tk,
        }
        self.img_id = self.cv.create_image(0,0,image=img_tk, anchor='nw')

    def resizer(self, e):
        # if self.IMG and "imagen" in self.IMG.keys() and hasattr(self.img_id, "self"):
        if self.IMG and "imagen" in self.IMG.keys():
            medidas = (e.width, e.height)
            img = Image.open(self.IMG.get('imagen'))
            # red_img = img.resize((e.width, e.height), Image.Resampling.BILINEAR)
            if self.AJUSTAR:
                # red_img = ImageOps.fit(img, medidas, method=5, centering=(1.0, 0.0)) # anclado arriba
                red_img = ImageOps.fit(img, medidas, method=5)
            else:

                red_img = ImageOps.pad(img, medidas, method=5, color=self.bg)
            img_tk = ImageTk.PhotoImage(red_img)
            self.IMG["img_tk"] = img_tk
            self.cv.itemconfigure(self.img_id, image=img_tk)
        

if __name__=="__main__":
    app = tk.Tk()
    app.geometry("320x450")

    visor = ViewerTk(app, "black")
    visor.grid(row=0, column=0, sticky='wens')
    visor.AJUSTAR = True
    visor.asigna_imagen("otros/alic.jpg")

    
    app.mainloop()