import os
import keyboard

CONFIGFILE = "darksaveconfig.txt"
SAVEPATH = os.path.join(os.getcwd(), r'saves')


class Config:

    def __init__(self, savepath=SAVEPATH, configfile=CONFIGFILE):
        self.savepath = savepath
        self.srcfile = ""
        self.savehotkey = "None"
        self.loadhotkey = "None"
        self.setup(configfile)

    def setup(self, filename):
        try:
            with open(filename, "x") as configfile:
                configfile.write(f"savepath={self.savepath}\nsrcfile={self.srcfile}\nsavehotkey={self.savehotkey}\nloadhotkey={self.loadhotkey}")
        except Exception:
            with open(filename, "r") as f:
                contents = f.read()
                self.savepath = contents.splitlines()[0].split("=")[1]
                self.srcfile = contents.splitlines()[1].split("=")[1]
                self.savehotkey = contents.splitlines()[2].split("=")[1]
                self.loadhotkey = contents.splitlines()[3].split("=")[1]
        return

    def updateSrcfile(self, path):
        self.srcfile = path
        with open(CONFIGFILE, "w") as f:
            f.write(f"savepath={self.savepath}\nsrcfile={self.srcfile}\nsavehotkey={self.savehotkey}\nloadhotkey={self.loadhotkey}")
        return

    def updateSavepath(self, path):
        self.savepath = path
        with open(CONFIGFILE, "w") as f:
            f.write(f"savepath={self.savepath}\nsrcfile={self.srcfile}\nsavehotkey={self.savehotkey}\nloadhotkey={self.loadhotkey}")
        return

    def updateHotkeys(self, gui, type, saveaction, loadaction):
        if type == "save":
            print("save key: " + gui.savekey.get())
            if gui.savekey.get() in ('', 'None'):
                self.savehotkey = 'None'
            else:
                self.savehotkey = gui.savekey.get()
                keyboard.add_hotkey(self.savehotkey, lambda var1=gui: saveaction(var1, self))
            if self.loadhotkey != 'None':
                keyboard.add_hotkey(self.loadhotkey, lambda var1=gui: loadaction(var1, self))
            with open(CONFIGFILE, "w") as f:
                f.write(f"savepath={self.savepath}\nsrcfile={self.srcfile}\nsavehotkey={self.savehotkey}\nloadhotkey={self.loadhotkey}")
        else:
            print("load key: " + gui.savekey.get())
            if gui.loadkey.get() in ('', 'None'):
                self.loadhotkey = 'None'
            else:
                self.loadhotkey = gui.loadkey.get()
                keyboard.add_hotkey(self.loadhotkey, lambda var1=gui: loadaction(var1, self))
            if self.savehotkey != 'None':
                keyboard.add_hotkey(self.savehotkey, lambda var1=gui: saveaction(var1, self))
            with open(CONFIGFILE, "w") as f:
                f.write(f"savepath={self.savepath}\nsrcfile={self.srcfile}\nsavehotkey={self.savehotkey}\nloadhotkey={self.loadhotkey}")
        return
