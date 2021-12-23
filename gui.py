import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox


class Gui:

    def __init__(self, windowSize, title):
        self.windowSize = windowSize
        self.title = title
        self.selectedEntry = ""
        root = Tk()
        self.root = root
        root.title(self.title)
        root.geometry(self.windowSize)
        root.resizable(False, False)
        # if "nt" == os.name:
        #     root.wm_iconbitmap(bitmap="save.ico")
        # main display
        mainframe = ttk.Frame(root, padding="10")
        mainframe.grid(column=0, row=0, sticky=N + E + S + W)
        l1 = Label(mainframe, text="source file:")
        l1.grid()
        src = StringVar()
        self.src = src
        e1 = Entry(mainframe, textvariable=src, width=20, state="readonly")
        e1.grid(row=0, column=1, columnspan=3, padx=5, sticky=E + W)
        b1 = Button(mainframe, text="Select", command=lambda: self.selectfile(src))
        b1.grid(row=0, column=4, padx=5, sticky=N + E + S + W)
        b0 = Button(mainframe, text="Reset")
        self.resetBtnfirst = b0
        b0.grid(row=0, column=5, padx=5, sticky=N + E + S + W)
        l1 = Label(mainframe, text="save path:")
        l1.grid(row=1, column=0)
        path = StringVar()
        self.path = path
        e1 = Entry(mainframe, textvariable=path, width=20, state="readonly")
        e1.grid(row=1, column=1, columnspan=3, padx=5, sticky=E + W)
        b1 = Button(mainframe, text="Select", command=lambda:self.selectdir(path))
        b1.grid(row=1, column=4, padx=5, sticky=N + E + S + W)
        b5 = Button(mainframe, text="Reset")
        self.resetBtnsecond = b5
        b5.grid(row=1, column=5, padx=5, sticky=N + E + S + W)
        pathcontents = StringVar()
        self.pathContents = pathcontents
        # text display
        lstbox = Listbox(mainframe, width=20, height=10)
        self.listbox = lstbox
        lstbox.grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky=N + E + S + W)
        # t1 = scrolledtext.ScrolledText(mainframe, wrap="none", width=20, height=10, state="disabled")
        # self.text = t1
        # t1.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky=N + E + S + W)
        # side buttons display
        sideframe = Frame(mainframe)
        sideframe.grid(row=2, column=5, pady=5, sticky=N + E + S + W)
        b1 = Button(sideframe, text="Save")
        self.saveBtn = b1
        b1.grid(row=0, column=0, pady=5, sticky=N + E + S + W)
        b2 = Button(sideframe, text="Load")
        self.loadBtn = b2
        b2.grid(row=1, column=0, pady=5, sticky=N + E + S + W)
        b3 = Button(sideframe, text="Rename")
        self.renameBtn = b3
        b3.grid(row=2, column=0, pady=5, sticky=N + E + S + W)
        b4 = Button(sideframe, text="Delete")
        self.deleteBtn = b4
        b4.grid(row=3, column=0, pady=5, sticky=N + E + S + W)
        # hotkeys display
        hotkeys = Frame(mainframe)
        hotkeys.grid(row=3, column=0, columnspan=2)
        l1 = Label(hotkeys, text="Save:")
        l1.grid(row=0, column=0)
        savehotkey = Entry(hotkeys, width=5)
        self.savekey = savehotkey

        savehotkey.grid(row=0, column=1)
        l2 = Label(hotkeys, text="Load:")
        l2.grid(row=0, column=2)
        loadhotkey = Entry(hotkeys, width=5)
        self.loadkey = loadhotkey
        loadhotkey.grid(row=0, column=3)

    def setPath(self, newPath):
        self.path = newPath

    def render(self):
        self.root.mainloop()

    def selectdir(self, field):
        if self.path.get() not in ('', "None"):
            dirname = fd.askdirectory(title='Select a directory', initial=self.path.get())
        else:
            dirname = fd.askdirectory(title='Select a directory', initial=os.getcwd())
        print(dirname)
        if dirname != '':
            field.set(os.path.normpath(dirname))
        else:
            print("Invalid directory!")

    def selectfile(self, field):
        if self.src.get() not in ('', "None"):
            filename = fd.askopenfilename(title='Select a file', initialfile=self.src.get())
        else:
            filename = fd.askopenfilename(title='Select a file', initialdir=os.getcwd())
        if filename != '':
            field.set(os.path.normpath(filename))
        else:
            print("Invalid filename!")

    def popup_box(self, title, msg, selected, config, action):
        win = Toplevel()
        win.wm_title(title)

        l = Label(win, text=msg)
        l.grid(row=0, column=0)
        e = Entry(win)
        e.grid(row=0, column=1, sticky=N+E+S+W)

        def submit(entry):
            action(selected, entry.get(), config)
            win.destroy()

        b = ttk.Button(win, text="Ok", command=lambda: submit(e))
        b.grid(row=1, column=0)
        b2 = ttk.Button(win, text="Cancel", command=win.destroy)
        b2.grid(row=1, column=1)

    def showerrormsg(self, title, msg):
        messagebox.showerror(title, msg)