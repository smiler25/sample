import os
import re
import sys
import lastfmfavs
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory

PATH_SEP = os.path.sep

def function(path):
    print(path)

class MainWindow:

    def __init__(self, parent):
        self.parent = parent

        self.csvpath = StringVar()
        self.logpath = StringVar()
        self.message = StringVar()
        self.message.set('Выберите входной файл и папку для логов')

        frame = Frame(self.parent)
        file_path_label = Label(frame, text="Файл с данными:", underline=0)
        file_path_label.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        file_path_entry = Entry(frame, width=50, textvariable=self.csvpath)
        file_path_entry.grid(row=0, column=1, columnspan=2, padx=2, pady=2, sticky=EW)
        file_path_button = Button(frame, text="Выбрать", command=self.choose_file, width=10)
        file_path_button.grid(row=0, column=3, sticky=W)

        log_dir_label = Label(frame, text="Папка для логов", underline=0)
        log_dir_label.grid(row=1, column=0, padx=2, pady=2, sticky=W)
        log_dir_entry = Entry(frame, width=50, textvariable=self.logpath)
        log_dir_entry.grid(row=1, column=1, columnspan=2, padx=2, pady=2, sticky=EW)
        log_dir_button = Button(frame, text="Выбрать", command=self.choose_dir, width=10)
        log_dir_button.grid(row=1, column=3, sticky=W)

        start_button = Button(frame, text="Начать", command=self.start)
        start_button.grid(row=3, column=0, columnspan=4, padx=2, pady=2, sticky=EW)

        self.message_label = Label(frame, relief=GROOVE,
                                          anchor=W, bg="white",
                                          textvariable=self.message)
        self.message_label.grid(row=14, column=0, columnspan=4, padx=2,
                               pady=2, sticky=EW)

        frame.grid(row=0, column=0, sticky=NSEW)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=999)
        frame.columnconfigure(2, weight=999)

        window = self.parent.winfo_toplevel()
        window.columnconfigure(0, weight=1)

        file_path_entry.focus_set()
        parent.bind("<Control-q>", self.quit)
        parent.bind("<Escape>", self.quit)
        parent.title("Title")


    def start(self, *ignore):
        if not self.csvpath.get() or not self.logpath.get():
            self.message.set('Нужно выбрать входной файл с данными и папку для сохранения логов')
            self.message_label.config({'fg': 'white', 'bg': 'red'})
        else:
            self.message.set('Можно начинать')
            self.message_label.config({'fg': 'black', 'bg': 'white'})
            # main()

    def choose_file(self):
        fname = askopenfilename(filetypes=(("Файлы csv", "*.csv"),
                                           # ("All files", "*.*")
                                ))
        if fname:
            self.csvpath.set(fname)
            if self.logpath.get():
                self.message.set('Можно начинать')
            function(fname)

    def choose_dir(self):
        dirname = askdirectory()
        if dirname:
            self.logpath.set(dirname)
            if self.csvpath.get():
                self.message.set('Можно начинать')
            function(dirname)

    def quit(self, event=None):
        self.parent.destroy()




application = Tk()
window = MainWindow(application)
application.protocol("WM_DELETE_WINDOW", window.quit)
application.mainloop()

