import multiprocessing as mp
import threading
import time
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory


def worker(count, progress_callback=None):
    if progress_callback is None:
        progress_callback = lambda x: None
    for i in range(1, count + 1):
        time.sleep(1)
        progress_callback('done [{}/{}]'.format(i, count))


class Worker(mp.Process):
    SENTINEL = 'STOPPED'

    def __init__(self, count):
        super().__init__(target=worker)
        self.count = count
        self.msg_queue = mp.Queue()

    def run(self):
        worker(self.count, self.msg_callback)
        self.msg_queue.put(self.SENTINEL)

    def msg_callback(self, text):
        self.msg_queue.put(text)


class Starter(threading.Thread):
    def __init__(self, count, progress_callback, done_callback):
        super().__init__()
        self.worker = Worker(count)
        self.progress_callback = progress_callback
        self.done_callback = done_callback
        self.stopped = False

    def run(self):
        self.worker.start()
        for msg in iter(self.worker.msg_queue.get, self.worker.SENTINEL):
            self.progress_callback(msg)
        if not self.stopped:
            self.done_callback()

    def stop(self):
        self.stopped = True
        self.worker.msg_queue.put(self.worker.SENTINEL)
        self.worker.terminate()


class MainWindow:
    def __init__(self, parent):
        self.worker = None
        self.parent = parent

        self.csvpath = tk.StringVar()
        self.logpath = tk.StringVar()
        self.message = tk.StringVar()
        self.message.set('Select file and folder')

        row = 0
        frame = tk.Frame(self.parent)
        file_path_label = tk.Label(frame, text='Choose file:', underline=0)
        file_path_label.grid(row=row, column=0, padx=2, pady=2, sticky=tk.W)
        file_path_entry = tk.Entry(frame, width=50, textvariable=self.csvpath)
        file_path_entry.grid(row=row, column=1, columnspan=2, padx=2, pady=2, sticky=tk.EW)
        file_path_button = tk.Button(frame, text='Open', command=self.choose_file, width=10)
        file_path_button.grid(row=row, column=3, sticky=tk.W)

        row += 1
        log_dir_label = tk.Label(frame, text='Choose folder', underline=0)
        log_dir_label.grid(row=row, column=0, padx=2, pady=2, sticky=tk.W)
        log_dir_entry = tk.Entry(frame, width=50, textvariable=self.logpath)
        log_dir_entry.grid(row=row, column=1, columnspan=2, padx=2, pady=2, sticky=tk.EW)
        log_dir_button = tk.Button(frame, text='Open', command=self.choose_dir, width=10)
        log_dir_button.grid(row=row, column=3, sticky=tk.W)

        row += 1
        self.start_button = tk.Button(frame, text='Start', command=self.start)
        self.start_button.grid(row=row, column=0, columnspan=4, padx=2, pady=2, sticky=tk.EW)

        row += 1
        self.message_label = tk.Label(frame, relief=tk.GROOVE, anchor=tk.W, bg='white',
                                      textvariable=self.message)
        self.message_label.grid(row=row, column=0, columnspan=4, padx=2, pady=2, sticky=tk.EW)

        frame.grid(row=0, column=0, sticky=tk.NSEW)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=999)
        frame.columnconfigure(2, weight=999)

        window = self.parent.winfo_toplevel()
        window.columnconfigure(0, weight=1)

        file_path_entry.focus_set()
        parent.bind('<Control-q>', self.quit)
        parent.bind('<Escape>', self.quit)
        parent.title('Title')

    def choose_file(self):
        # ("All files", "*.*")))
        fname = askopenfilename(filetypes=(('CSV', '*.csv'),))
        if fname:
            self.csvpath.set(fname)
            if self.logpath.get():
                self.message.set('Ready')
            worker(fname)

    def choose_dir(self):
        dirname = askdirectory()
        if dirname:
            self.logpath.set(dirname)
            if self.csvpath.get():
                self.message.set('Ready')
            worker(dirname)

    def start(self):
        if not self.csvpath.get() or not self.logpath.get():
            self.set_message_error('Choose file and folder')
            return

        self.set_message_info('Running')
        self.start_button.config(state=tk.DISABLED)
        self.worker = Starter(10, self.set_message_info, self.stop)
        self.worker.start()

    def stop(self):
        self.start_button.config(state=tk.NORMAL)
        self.set_message_success()

    def set_message_error(self, text):
        self.message.set(text)
        self.message_label.config({'fg': 'black', 'bg': 'red'})

    def set_message_success(self, text='Done!'):
        self.message.set(text)
        self.message_label.config({'fg': 'black', 'bg': 'green'})

    def set_message_info(self, text):
        self.message.set(text)
        self.message_label.config({'fg': 'black', 'bg': 'white'})

    def quit(self, *args):
        if self.worker is not None:
            try:
                self.worker.stop()
            except:
                pass
        self.parent.destroy()


if __name__ == '__main__':
    application = tk.Tk()
    window = MainWindow(application)
    application.protocol("WM_DELETE_WINDOW", window.quit)
    application.mainloop()
