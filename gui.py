from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog as fd
import traductor
from traductor import traducir, contarCiclos, traducir2

window = Tk()

window.title("MIPS Assembly to binary translator")
window.geometry('950x500')
window.resizable(False, False)

#Functions
def clearInp(event):
    txt.delete(1.0,END)

def open_text_file():
    txt.delete(1.0,END)
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    
    f = fd.askopenfile(filetypes=filetypes)
    for i in f.readlines():
        txt.insert(END, i)

open_button = Button(
    window,
    text='Open a File',
    command=open_text_file
)

def translate():
    lbl.config(text = '')
    out.delete(1.0,END)
    ret = traducir2(txt.get("1.0", END))
    print(ret)
    for i in ret:
        out.insert(END, i)
        out.insert(END,'\n')
    contarCiclos()

def freq():
    f = int(entry.get())
    lbl.config(text = "Numero de ciclos: " + str(traductor.numCiclos[0]) + " + " + str(traductor.numCiclos[1]) + "X \n"
    + "Tiempo: " + str(traductor.numCiclos[0] / f) + " + " + str(traductor.numCiclos[1] / f) + "X" + " ns")
    #print("Numero de ciclos: " + str(traductor.numCiclos[0]) + " + " + str(traductor.numCiclos[1]) + "X")
    #print("Tiempo: " + str(traductor.numCiclos[0] / f) + " + " + str(traductor.numCiclos[1] / f) + "X" + " ns")

#elements
txt = scrolledtext.ScrolledText(window,width=50,height=25)
txt.insert(INSERT,'Escribe aqui el codigo en Assembly')
txt.grid(column=0,row=0)
txt.bind("<FocusIn>", clearInp)

btn = Button(window, text="Cargar archivo", command=open_text_file)
btn.grid(column=0, row=1)

trs = Button(window, text="Traducir", command=translate)
trs.grid(column=1, row=0, rowspan=2, padx=10)

out = scrolledtext.ScrolledText(window,width=50,height=25)
out.insert(INSERT,'Traduccion')
out.grid(column=3,row=0)

Label(window, text="Frecuencia en GHz: ").grid(row=2, column = 0)
entry = Entry(window, width = 5)
entry.grid(row=2, column=1)

cc = Button(window, text="Calcular", command=freq)
cc.grid(column=2, row=2)

lbl = Label(window, text= '', padx=5, pady=5)
lbl.grid(column = 0, row = 3, columnspan = 4)

window.mainloop()