import tkinter as tk
from pathlib import Path
from PIL import ImageTk, Image, ImageOps
from mi_checkbox import MiCheckbox


class ViewerTk(tk.Frame):
    """visor de imagenes basico (no gifs)
    Viewer().AJUSTAR: (por defecto False)
        True: mostrar imagen centrada
        False: mostrar imagen manteniendo escala
    """
    def __init__(self, parent, bg="gray", **kw):
        super(ViewerTk, self).__init__(master=parent, bg=bg, **kw)
        self.parent = parent
        self.bg = bg
        self.IMG = None
        self.AJUSTAR = False
        self._config_viewertk()
        
    def _config_viewertk(self):
        self.cv = tk.Canvas(master=self.parent, bg=self.bg, highlightthickness=0)
        self.cv.grid(row=0, column=0, sticky='wens')
        self.bind("<Configure>", self._resizer)
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)
        self.parent.bind("<space>", self.cambia)

    def asigna_imagen(self, archivo):
        """archivo: ruta de la imagen"""
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

    def _resizer(self, e=None):
        if self.IMG and "imagen" in self.IMG.keys():
            # medidas = (e.width, e.height)
            self.parent.update()
            medidas = (self.parent.winfo_width(), self.parent.winfo_height())
            img = Image.open(self.IMG.get('imagen'))

            d = {'size':medidas, 'method':5, 'image':img}
            rimg = ImageOps.fit(**d) if self.AJUSTAR else ImageOps.pad(color=self.bg, **d)
            img_tk = ImageTk.PhotoImage(rimg)
            self.IMG["img_tk"] = img_tk
            self.cv.itemconfigure(self.img_id, image=img_tk)

    def cambia(self, e=None):
        self.AJUSTAR = False if self.AJUSTAR else True
        self._resizer()

    def __str__(self):
        s = """ViewerTk
        METODOS:
            asigna_imagen(archivo)
        """
        return s
    

if __name__=="__main__":
    app = tk.Tk()
    app.geometry("320x450")

    visor = ViewerTk(app, "black")
    visor.grid(row=0, column=0, sticky='wens')
    # visor.AJUSTAR = True
    visor.asigna_imagen("otros/alic.jpg")
    # print(visor.__doc__)
    # help(visor)
    print(visor)
    
    app.mainloop()