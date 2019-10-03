import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import gui_support

from bindings import *

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = CurveExtWindow (root)
    gui_support.init(root, top)
    root.mainloop()

w = None
def create_CurveExtWindow(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = CurveExtWindow (w)
    gui_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_CurveExtWindow():
    global w
    w.destroy()
    w = None

class CurveExtWindow:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font9 = "-family {Arial Black} -size 12 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"

        top.geometry("1266x777+120+85")
        top.title("Curve Extractor")
        top.configure(background="#191919")
        
        self.root = top

        self.image_canvas = tk.Canvas(self.root)
        self.image_canvas.place(relx=0.221, rely=0.013, relheight=0.969
                , relwidth=0.769)
        self.image_canvas.configure(background="#2d2d2d")
        self.image_canvas.configure(highlightbackground="#000000")
        self.image_canvas.configure(insertbackground="black")
        self.image_canvas.configure(relief="ridge")
        self.image_canvas.configure(selectbackground="#c4c4c4")
        self.image_canvas.configure(selectforeground="black")

        self.open_file_button = tk.Button(self.root)
        self.open_file_button.place(relx=0.008, rely=0.013, height=43, width=136)

        self.open_file_button.configure(activebackground="#ececec")
        self.open_file_button.configure(activeforeground="#000000")
        self.open_file_button.configure(background="#606060")
        self.open_file_button.configure(disabledforeground="#9e0000")
        self.open_file_button.configure(font=font9)
        self.open_file_button.configure(foreground="#000000")
        self.open_file_button.configure(highlightbackground="#d9d9d9")
        self.open_file_button.configure(highlightcolor="black")
        self.open_file_button.configure(pady="0")
        self.open_file_button.configure(relief="flat")
        self.open_file_button.configure(text='''Import''')

        self.export_button = tk.Button(self.root)
        self.export_button.place(relx=0.008, rely=0.077, height=43, width=136)
        self.export_button.configure(activebackground="#ececec")
        self.export_button.configure(activeforeground="#009e00")
        self.export_button.configure(background="#606060")
        self.export_button.configure(disabledforeground="#9e0000")
        self.export_button.configure(font="-family {Arial Black} -size 12 -weight bold")
        self.export_button.configure(foreground="#000000")
        self.export_button.configure(highlightbackground="#d9d9d9")
        self.export_button.configure(highlightcolor="black")
        self.export_button.configure(pady="0")
        self.export_button.configure(relief="flat")
        self.export_button.configure(text='''Export''')

        self.x1_button = tk.Button(self.root)
        self.x1_button.place(relx=0.008, rely=0.193, height=43, width=66)
        self.x1_button.configure(activebackground="#ececec")
        self.x1_button.configure(activeforeground="#000000")
        self.x1_button.configure(background="#606060")
        self.x1_button.configure(disabledforeground="#9e0000")
        self.x1_button.configure(font=font9)
        self.x1_button.configure(foreground="#000000")
        self.x1_button.configure(highlightbackground="#d9d9d9")
        self.x1_button.configure(highlightcolor="black")
        self.x1_button.configure(pady="0")
        self.x1_button.configure(relief="flat")
        self.x1_button.configure(text='''X1''')

        self.x2_button = tk.Button(self.root)
        self.x2_button.place(relx=0.008, rely=0.257, height=43, width=66)
        self.x2_button.configure(activebackground="#ececec")
        self.x2_button.configure(activeforeground="#000000")
        self.x2_button.configure(background="#606060")
        self.x2_button.configure(disabledforeground="#9e0000")
        self.x2_button.configure(font="-family {Arial Black} -size 12 -weight bold")
        self.x2_button.configure(foreground="#000000")
        self.x2_button.configure(highlightbackground="#d9d9d9")
        self.x2_button.configure(highlightcolor="black")
        self.x2_button.configure(pady="0")
        self.x2_button.configure(relief="flat")
        self.x2_button.configure(text='''X2''')

        self.y1_button = tk.Button(self.root)
        self.y1_button.place(relx=0.008, rely=0.322, height=43, width=66)
        self.y1_button.configure(activebackground="#ececec")
        self.y1_button.configure(activeforeground="#000000")
        self.y1_button.configure(background="#606060")
        self.y1_button.configure(disabledforeground="#9e0000")
        self.y1_button.configure(font="-family {Arial Black} -size 12 -weight bold")
        self.y1_button.configure(foreground="#000000")
        self.y1_button.configure(highlightbackground="#d9d9d9")
        self.y1_button.configure(highlightcolor="black")
        self.y1_button.configure(pady="0")
        self.y1_button.configure(relief="flat")
        self.y1_button.configure(text='''Y1''')

        self.y2_button = tk.Button(self.root)
        self.y2_button.place(relx=0.008, rely=0.386, height=43, width=66)
        self.y2_button.configure(activebackground="#ececec")
        self.y2_button.configure(activeforeground="#000000")
        self.y2_button.configure(background="#606060")
        self.y2_button.configure(disabledforeground="#9e0000")
        self.y2_button.configure(font="-family {Arial Black} -size 12 -weight bold")
        self.y2_button.configure(foreground="#000000")
        self.y2_button.configure(highlightbackground="#d9d9d9")
        self.y2_button.configure(highlightcolor="black")
        self.y2_button.configure(pady="0")
        self.y2_button.configure(relief="flat")
        self.y2_button.configure(text='''Y2''')

        self.x1_entry = tk.Entry(self.root)
        self.x1_entry.place(relx=0.095, rely=0.193,height=44, relwidth=0.098)
        self.x1_entry.configure(background="#c6c6c6")
        self.x1_entry.configure(disabledforeground="#a3a3a3")
        self.x1_entry.configure(font=font9)
        self.x1_entry.configure(foreground="#000000")
        self.x1_entry.configure(insertbackground="black")
        self.x1_entry.configure(justify='center')
        self.x1_entry.configure(relief="flat")
        self.x1_entry.configure(selectbackground="#56a06f")
        self.x1_entry.configure(selectforeground="#000000")

        self.x2_entry = tk.Entry(self.root)
        self.x2_entry.place(relx=0.095, rely=0.257,height=44, relwidth=0.098)
        self.x2_entry.configure(background="#c6c6c6")
        self.x2_entry.configure(disabledforeground="#a3a3a3")
        self.x2_entry.configure(font="-family {Arial Black} -size 12 -weight bold")
        self.x2_entry.configure(foreground="#000000")
        self.x2_entry.configure(highlightbackground="#d9d9d9")
        self.x2_entry.configure(highlightcolor="black")
        self.x2_entry.configure(insertbackground="black")
        self.x2_entry.configure(justify='center')
        self.x2_entry.configure(relief="flat")
        self.x2_entry.configure(selectbackground="#56a06f")
        self.x2_entry.configure(selectforeground="#000000")

        self.y1_entry = tk.Entry(self.root)
        self.y1_entry.place(relx=0.095, rely=0.322,height=44, relwidth=0.098)
        self.y1_entry.configure(background="#c6c6c6")
        self.y1_entry.configure(disabledforeground="#a3a3a3")
        self.y1_entry.configure(font="-family {Arial Black} -size 12 -weight bold")
        self.y1_entry.configure(foreground="#000000")
        self.y1_entry.configure(highlightbackground="#d9d9d9")
        self.y1_entry.configure(highlightcolor="black")
        self.y1_entry.configure(insertbackground="black")
        self.y1_entry.configure(justify='center')
        self.y1_entry.configure(relief="flat")
        self.y1_entry.configure(selectbackground="#56a06f")
        self.y1_entry.configure(selectforeground="#000000")

        self.y2_entry = tk.Entry(self.root)
        self.y2_entry.place(relx=0.095, rely=0.386,height=44, relwidth=0.098)
        self.y2_entry.configure(background="#c6c6c6")
        self.y2_entry.configure(disabledforeground="#a3a3a3")
        self.y2_entry.configure(font="-family {Arial Black} -size 12 -weight bold")
        self.y2_entry.configure(foreground="#000000")
        self.y2_entry.configure(highlightbackground="#d9d9d9")
        self.y2_entry.configure(highlightcolor="black")
        self.y2_entry.configure(insertbackground="black")
        self.y2_entry.configure(justify='center')
        self.y2_entry.configure(relief="flat")
        self.y2_entry.configure(selectbackground="#56a06f")
        self.y2_entry.configure(selectforeground="#000000")

        self.num_points_entry = tk.Entry(self.root)
        self.num_points_entry.place(relx=0.095, rely=0.566, height=44, relwidth=0.098)
        self.num_points_entry.configure(background="#c6c6c6")
        self.num_points_entry.configure(disabledforeground="#a3a3a3")
        self.num_points_entry.configure(font="-family {Arial Black} -size 12 -weight bold")
        self.num_points_entry.configure(foreground="#000000")
        self.num_points_entry.configure(highlightbackground="#d9d9d9")
        self.num_points_entry.configure(highlightcolor="black")
        self.num_points_entry.configure(insertbackground="black")
        self.num_points_entry.configure(justify='center')
        self.num_points_entry.configure(relief="flat")
        self.num_points_entry.configure(selectbackground="#56a06f")
        self.num_points_entry.configure(selectforeground="#000000")

        self.Label1 = tk.Label(self.root)
        self.Label1.place(relx=0.008, rely=0.566, height=46, width=102)
        self.Label1.configure(activebackground="#191919")
        self.Label1.configure(activeforeground="white")
        self.Label1.configure(activeforeground="#c6c6c6")
        self.Label1.configure(background="#191919")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font9)
        self.Label1.configure(foreground="#c6c6c6")
        self.Label1.configure(text='''# Points''')
        
        self.bindings = Bindings(self)
        

if __name__ == '__main__':
    vp_start_gui()





