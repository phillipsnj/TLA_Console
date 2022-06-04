import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import serial
import time
import solo_uart
import solo_widgets
import json

print("Running 0.2")

class soloBasic(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open('config.json') as f:
            self.data = json.load(f)
        print(f"Config {str(self.data['port'])}")
        self.UART = solo_uart.soloUART(self.data['port'], self.processInput, self.processOutput)
        self.UART.start()
        self.tlas = {}
        self.outText = tk.StringVar()
        self.title("SOLO Test Screen")
        self.geometry("950x680")
        self.resizable(width=False, height=False)
        self.nodeFrame = ttk.LabelFrame(self, text=" SOLO UART Test ")
        self.nodeFrame.grid(row=0, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.infoFrame = ttk.LabelFrame(self, text=" Incoming Messages ")
        self.infoFrame.grid(row=0, column=8, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        solo_widgets.display_button(self.UART,self.infoFrame,0,0, "INF", "INF")
        # self.imf_button = tk.Button(self.infoFrame, text="INF", command = self.sendINF)
        # self.imf_button.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        self.clear_button = tk.Button(self.infoFrame, text="Clear", command=self.clearInfo)
        self.clear_button.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        self.reset_button = tk.Button(self.infoFrame, text="Reset", command=self.resetAll)
        self.reset_button.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        self.in_text = tk.scrolledtext.ScrolledText(self.infoFrame, height=15, width=30)
        self.in_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        #self.in_text.insert(tk.INSERT,"Starting.....\r")
        self.out_text = tk.scrolledtext.ScrolledText(self.infoFrame, height=15, width=30)
        self.out_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        # self.sendText = tk.Text(self.infoFrame, height=1, width=10, command=self.send_TLA)
        # self.sendText.grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        self.sendText = tk.Entry(self.infoFrame)
        self.sendText.bind('<Return>',self.send_TLA)
        self.sendText.grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        # self.send_button = tk.Button(self.infoFrame, text="Send", command=self.send_TLA)
        # self.send_button.grid(row=3, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        # self.in_text. = "Starting.....\r"
        # self.out_box = tk.scrolledtext.ScrolledText(self.infoFrame, height=5, width=30)
        # self.out_box.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        # self.out_box.insert(tk.INSERT, "Starting.....\r")
        self.UART.send("INF\r")

    def sendINF(self):
        self.UART.send("INF\r")
        #self.out_text.insert(tk.END, "INF\n")
        #self.out_text.yview(tk.END)

    def send_TLA(self, name):
        print(f"NAME = {name}")
        text_output = self.sendText.get()
        self.UART.send(text_output+"\r")
        #self.processOutput(text_output+"\r")

    def processOutput(self,msg):
        self.out_text.insert(tk.END, str(msg)+"\n")
        self.out_text.yview(tk.END)

    def clearInfo(self):
        #self.tlas = {}
        self.display_grid()
        self.in_text.delete(1.0, tk.END)
        self.in_text.yview(tk.END)
        self.out_text.delete(1.0, tk.END)
        self.out_text.yview(tk.END)

    def resetAll(self):
        for widget in self.nodeFrame.winfo_children():
            widget.destroy()
        self.tlas = {}
        self.display_grid()
        self.in_text.delete(1.0, tk.END)
        self.in_text.yview(tk.END)
        self.out_text.delete(1.0, tk.END)
        self.out_text.yview(tk.END)

    def processInput(self, msg):
        print("msg : "+str(msg))
        self.in_text.insert(tk.END, str(msg)+"\n")
        self.in_text.yview(tk.END)
        # self.out_box.insert(tk.END, str(msg) + "\n")
        # self.out_box.yview(tk.END)
        tla = msg[:3]
        if len(msg) > 3:
            operator = msg[3]
            value = msg[4:].replace(',\r', '')
        else:
            operator = ""
            value = ""
        print("tla :"+tla+" : Operator :"+operator+" : Value:"+str(value))

        if operator == ':':
            action_operator = value[:3]
            action_value = value[4:]
            if action_operator == "CNM":
                self.tlas[tla]["name"].set(action_value)
            elif action_operator == "INC":
                self.tlas[tla]["increment"]=action_value
            elif action_operator == "OPT":
                if action_value not in self.tlas[tla]["options"]:
                    self.tlas[tla]["options"].append(action_value)
        elif tla in self.tlas:
            self.tlas[tla]["value"].set(value)
        elif len(tla) < 3:
            print("Command Ignored")
        else:
            self.tlas[tla] = {}
            self.tlas[tla]["name"] = tk.StringVar()
            self.tlas[tla]["value"] = tk.StringVar()
            self.tlas[tla]["name"].set(tla)
            self.tlas[tla]["options"] = []
            if operator == '=':
                self.tlas[tla]["value"].set(value)
                self.tlas[tla]["type"] = "variable"
            elif operator == '~':
                self.tlas[tla]["value"].set(value)
                self.tlas[tla]["type"] = "literal"
            elif operator == '%':
                self.tlas[tla]["value"].set(value)
                self.tlas[tla]["type"] = "option"
            else:
                self.tlas[tla]["value"].set("")
                self.tlas[tla]["type"] = "command"

        self.display_grid()

    def display_grid(self):
        i=1
        for key, value in self.tlas.items():
            print("Display : "+key+" -> "+value["type"]+" --> "+value["value"].get())
            solo_widgets.display_tla(self.nodeFrame,key , value, i, self.UART)
            i = i+1

    def ButtonPress(self,msg):
        #data = "1,1"
        self.UART.send(msg)
        print("Button Pressed : "+str(msg))
        self.out_text.insert(tk.END, str(msg) + "\n")
        self.out_text.yview(tk.END)
        #self.UART.send("TYP\n")

    def sliderMoved(self, Pos):
        print("Slider : "+Pos)


if __name__ == '__main__':
    app = soloBasic()
    app.mainloop()
