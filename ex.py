import tkinter as tk

class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.pack()
        self.build()
        self.create_widgets()

    def buildApp(self):
        self.master.title("Weable Computing Toolkit")
        self.master.config(background = "white") 
        self.master.minsize(800, 500)

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")


if __name__ == '__main__':
    root = tk.Tk()
    app = GUI(master=root)
    app.mainloop()