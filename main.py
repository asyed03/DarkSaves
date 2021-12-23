from gui import *
from config import *
import shutil
import keyboard
import sys


def getPathContents(path):
    files = []
    try:
        for entry in os.listdir(path):
            if os.path.isfile(os.path.join(path, entry)):
                files.append(entry)
    except Exception:
        return []
    return files


def updateEntries(gui, config):
    config.savepath = gui.path.get()
    if os.path.exists(gui.path.get()):
        config.updateSavepath(gui.path.get())
    else:
        print("Path does not exist!")
    files = getPathContents(gui.path.get())
    print(files)
    gui.listbox.delete(0, END)
    # gui.pathContents.set(files)
    for i in range(len(files)):
        gui.listbox.insert(i, files[i])


def findLatestFile(path):
    curr_index = -1
    for file in os.listdir(path):
        if file.startswith("unnamed_save_file_") and int(file.split("_")[-1]) > curr_index:
            curr_index = int(file.split("_")[-1])
    return curr_index + 1


def rename(selectedFile, newname, config):
    os.rename(selectedFile, os.path.join(config.savepath, newname))
    updateEntries(gui, conf)


def saveEntry(gui, config):
    dest = config.srcfile
    if dest in ('', "None"):
        gui.showerrormsg("Error", "Choose a source file!")
        return
    savepath = conf.savepath
    if savepath in ('', "None"):
        gui.showerrormsg("Error", "Choose a save path!")
        return
    os.makedirs(config.savepath, exist_ok=True)
    latest_index = findLatestFile(config.savepath)
    shutil.copyfile(dest, os.path.join(config.savepath, f"unnamed_save_file_{latest_index}"))
    updateEntries(gui, config)


def loadEntry(gui, conf):
    dest = conf.srcfile
    if dest != '':
        gui.showerrormsg("Error", "Choose a source file!")
        return
    savepath = conf.savepath
    if savepath != '':
        gui.showerrormsg("Error", "Choose a save path!")
        return
    src = gui.listbox.get(ANCHOR)
    if gui.listbox.get(ANCHOR) == '':
        src = gui.listbox.get(END)
    selectedFile = os.path.join(conf.savepath, src)
    shutil.copy(selectedFile, dest)
    print(f"{src} file loaded!")


def deleteEntry(gui, config):
    selectedFile = os.path.join(config.savepath, gui.listbox.get(ANCHOR))
    print(selectedFile)
    if os.path.exists(selectedFile) and gui.listbox.get(ANCHOR) != '':
        response = messagebox.askokcancel("Confirm deletion", f"Delete {gui.listbox.get(ANCHOR)}?")
        if response:
            os.remove(selectedFile)
    else:
        print("File does not exist!")
    gui.listbox.delete(ANCHOR)


def renameEntry(gui, config):
    selectedFile = os.path.join(config.savepath, gui.listbox.get(ANCHOR))
    print(selectedFile)
    if os.path.exists(selectedFile) and gui.listbox.get(ANCHOR) != '':
        gui.popup_box("Rename", "Enter a name:", selectedFile, config, rename)
    else:
        print("File does not exist!")


def on_close():
    gui.root.destroy()
    sys.exit()


def removehotkey(event):
    keyboard.remove_all_hotkeys()


def hotkey(event, config):
    whitelist = ('BackSpace', 'space', 'Return', 'Escape', 'w', 'a', 's', 'd', 'g', 'q', 'r', 'f', 'Shift_L', 'Shift_R', config.loadhotkey, config.savehotkey)
    if event.keysym in whitelist:
        event.widget.delete(0, 'end')
        event.widget.insert(0, "None")
    else:
        event.widget.delete(0, 'end')
        event.widget.insert(0, event.keysym)
    event.widget.master.focus_set()


def refreshSrc(gui, conf):
    gui.src.set('')


def refreshPath(gui, conf):
    gui.path.set('')


if __name__ == '__main__':
    gui = Gui("320x280", "Dark Saves")
    conf = Config()
    gui.src.trace("w", lambda name, index, mode: conf.updateSrcfile(gui.src.get()))
    gui.path.trace("w", lambda name, index, mode: updateEntries(gui, conf))
    # default values
    gui.src.set(conf.srcfile)
    gui.path.set(conf.savepath)
    # super long and complicated hotkey setup
    gui.savekey.insert(0, conf.savehotkey)
    gui.loadkey.insert(0, conf.loadhotkey)
    if conf.savehotkey != 'None':
        keyboard.add_hotkey(conf.savehotkey, lambda: saveEntry(gui, conf))
    if conf.loadhotkey != 'None':
        keyboard.add_hotkey(conf.loadhotkey, lambda: loadEntry(gui, conf))
    gui.savekey.bind('<KeyRelease>', lambda event: hotkey(event, conf))
    gui.loadkey.bind('<KeyRelease>', lambda event: hotkey(event, conf))
    gui.savekey.bind('<FocusIn>', removehotkey)
    gui.loadkey.bind('<FocusIn>', removehotkey)
    gui.savekey.bind('<FocusOut>', lambda var=gui: conf.updateHotkeys(gui, "save", saveEntry, loadEntry))
    gui.loadkey.bind('<FocusOut>', lambda var=gui: conf.updateHotkeys(gui, "load", saveEntry, loadEntry))
    # again, the above is way too long and complicated

    # make buttons do stuff
    gui.saveBtn.config(command=lambda: saveEntry(gui, conf))
    gui.loadBtn.config(command=lambda: loadEntry(gui, conf))
    gui.renameBtn.config(command=lambda: renameEntry(gui, conf))
    gui.deleteBtn.config(command=lambda: deleteEntry(gui, conf))
    gui.resetBtnfirst.config(command=lambda: refreshSrc(gui, conf))
    gui.resetBtnsecond.config(command=lambda: refreshPath(gui, conf))

    # make sure to stop program
    gui.root.protocol("WM_DELETE_WINDOW", on_close)

    # display program
    gui.render()


