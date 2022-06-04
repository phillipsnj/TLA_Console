import tkinter as tk
from tkinter import ttk


# class DoubleButton(tk.Frame):
#     def __init__(self, parent, column, row, UART, onMessage, offMessage, on_text, off_text, **kwargs):
#         super().__init__(parent, **kwargs)
#         tk.Frame.__init__(self, parent)
#         # self.Frame = ttk.Frame(self,parent)
#         self.UART = UART
#         self.buttonOn = ttk.Button(parent, text=on_text, command=lambda: self.ButtonPress(onMessage))
#         self.buttonOn.grid(row=row, column=column, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
#         self.buttonOff = ttk.Button(parent, text=off_text, command=lambda: self.ButtonPress(offMessage))
#         self.buttonOff.grid(row=row, column=column+1, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
#
#     def ButtonPress(self,msg):
#         #data = "1,1"
#         self.UART.send(msg)
#         print("Button Pressed : "+str(msg))
#         #self.UART.send("TYP,\n")

def display_button(uart, parent, row, column, name, text):
    print("Button")
    output = str(text + "\r")
    ttk.Button(parent, text=name, command=lambda text=output: ButtonPress(uart, text)) \
        .grid(row=row, column=column, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

def display_label(uart, parent, row, column, name):
    print("Label")
    ttk.Label(parent, textvariable=name) \
        .grid(row=row, column=column, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)


def display_tla(parent, key, data, row, uart):
    print("display_tla")
    display_label(uart, parent, row, 1, data['name'])
    display_label(uart, parent, row, 2, data['value'])
    # ttk.Label(parent, textvariable=data['name'])\
    #     .grid(row=row, column=1, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
    # ttk.Label(parent, textvariable=data['value'])\
    #     .grid(row=row, column=2, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
    if data['type'] == "variable":
        if 'increment' in data.keys():
            display_button(uart, parent, row, 3, "+5", key + "+5")
            display_button(uart, parent, row, 4, "+", key + "+1")
            display_button(uart, parent, row, 3, "-", key + "-1")
            display_button(uart, parent, row, 4, "-5", key + "-5")
            # ttk.Button(parent, text="-5", command=lambda: ButtonPress(uart, key + "-5\r")) \
            #     .grid(row=row, column=3, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
            # ttk.Button(parent, text="-", command=lambda: ButtonPress(uart, key + "-1\r")) \
            #     .grid(row=row, column=4, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
            # ttk.Button(parent, text="+", command=lambda: ButtonPress(uart, key + "+1\r")) \
            #     .grid(row=row, column=5, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
            # ttk.Button(parent, text="+5", command=lambda: ButtonPress(uart, key + "+5\r")) \
            #     .grid(row=row, column=6, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        else:
            display_button(uart, parent, row, 3, "-", key+"-1")
            display_button(uart, parent, row, 4, "+", key + "+1")
            # ttk.Button(parent, text="-", command=lambda: ButtonPress(uart, key + "-1\r")) \
            #    .grid(row=row, column=3, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
            # ttk.Button(parent, text="+", command=lambda: ButtonPress(uart, key + "+1\r")) \
            #    .grid(row=row, column=4, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
    elif data['type'] == "option":
        if len(data['options']) > 0:
            # ttk.Button(parent, text="-", command=lambda: ButtonPress(uart, key + "=Normal\r")) \
            #     .grid(row=row, column=3, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
            # ttk.Button(parent, text="+", command=lambda: ButtonPress(uart, key + "=Reverse\r")) \
            #     .grid(row=row, column=4, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
            colCount = 3
            #for option in data['options']:
            for x in range(len(data['options'])):
                output = str(key + "="+data['options'][x]+"\r")
                ttk.Button(parent, text=data['options'][x], command=lambda text = output: ButtonPress(uart, text))\
                .grid(row=row, column=colCount, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
                colCount += 1
                print("Options Set : "+output)
            print('HAS OPTIONS')
    elif data['type'] == "command":
        #ttk.Button(parent, textvariable=data['name'], command=lambda: ButtonPress(uart, key+"\r")) \
        #    .grid(row=row, column=3, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        display_button(uart, parent,row,3, data['name'].get(), key )



def ButtonPress(UART, msg):
    #data = "1,1"
    UART.send(msg)
    print("Button Pressed : "+str(msg))
    #self.UART.send("TYP,\n")

