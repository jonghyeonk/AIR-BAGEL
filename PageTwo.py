import warnings
warnings.filterwarnings(action='ignore')

#GUI PACKAGES
import tkinter as tk
from tkinter import *
from tkinter import ttk

#Pages
from PageTwo_Resource import Resource_Step1
from PageTwo_Resource import Resource_Step1_sub
from PageTwo_Inject_Anomaly import Inject_Anomaly
from PageTwo_System import System_Step1
from PageThree import PageThree
from PageTwo_System_self import System_step1_self
from PageTwo_Resource_self import Resource_step1_self


class PageTwo(tk.Frame):
    def new_window1(self, parent, extracted_data):
        if self.type1.get() == 'Random':
            Win_class = Resource_Step1
        if self.type1.get() == 'Self-configuration':
            Win_class = Resource_step1_self
        global win2
        Resource_Step1.extracted_data = extracted_data
        Resource_Step1_sub.extracted_data = extracted_data
        win2 = tk.Toplevel(self)
        Win_class(win2, parent)

        Win_class(win2, parent)

    def new_window2(self, Win_class):
        Inject_Anomaly.a = self.cVar1.get()
        Inject_Anomaly.b = self.cVar2.get()
        PageThree.a = self.cVar1.get()
        PageThree.b = self.cVar2.get()
        global win2
        win2 = tk.Toplevel(self)
        Win_class(win2)

    def new_window3(self, parent):
        if self.type2.get() == 'Random':
            Win_class = System_Step1
        if self.type2.get() == 'Self-configuration' :
            Win_class = System_step1_self
        global win2
        win2 = tk.Toplevel(self)
        Win_class(win2, parent)


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='dark slate gray')

        # Create main containers
        top_frame = Frame(self, bg='dark slate gray', width=300, height=50, padx=7, pady=3)
        center = Frame(self, bg='dark slate gray', width=50, height=40, padx=7, pady=3)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        top_frame.grid(row=0, sticky="nsew")
        center.grid(row=1, sticky="nsew")
        top_frame.grid_rowconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)

        # Title widget (top frame)
        top_mid = Frame(top_frame, bg='gray25', width=300, height=48,
                        highlightthickness=1, highlightbackground="gray15")
        top_mid.grid(row=0, column=1, pady=(2, 0), sticky="nsew")
        top_mid_label1 = Label(top_mid, text='(2) Anomaly Generation', font=("Consolas", 13, 'bold'),
                               fg="white", bg='gray25', anchor="center", relief = "raised", width=63)
        top_mid_label1.grid(row=0, column=0, sticky="w")

        # Create sub frame (center frame)
        ctr_mid = Frame(center, bg='gray1', width=500, height=190, highlightthickness=1, highlightbackground="gray15")
        ctr_mid.grid(row=0, column=1, pady=(0, 7), sticky="nsew")
        ctr_mid_label1 = Label(ctr_mid, text='Root design (Resource/System)', font=("Consolas", 10, 'bold'),
                               fg="white", bg='gray25', anchor="center", relief="raised")
        ctr_mid_label1.grid(row=0, column=0, sticky="w")
        ctr_mid_label1.config(width=81)

        # Page explanation (center-top)
        ctr_mid_label2b = LabelFrame(ctr_mid, text=" Explanation ", font=("Consolas", 10, 'bold'),
                                     fg="white", bg='gray1', bd=1, padx=14, pady=3)
        ctr_mid_label2b.place(x=20, y=30)

        Guide_container1 = Frame(ctr_mid_label2b, bg='gray0', width=505, height=30, highlightbackground="gray1",
                                 highlightthickness=0)
        Guide_container1.grid(row=0, column=0)
        Guide_Label1 = Text(Guide_container1, width=45, height=6, wrap=tk.WORD, fg="aquamarine", bg='gray1', bd=0)
        Guide_Label1.insert(tk.CURRENT,
                            "In step 1, select one or more roots among resource/system being a cause of anomalous event, then set parameters on selected root causes. In step 2, select anomaly types and weights to be applied on anomalous events.")
        Guide_Label1.grid(row=0, column=0)

        # Set failure rate (center-mid)
        ctr_mid_label2 = LabelFrame(ctr_mid, text=" Step 1. Set parameters on root causes ", font=("Consolas", 10, 'bold'),
                                    fg="white", bg='gray1', bd=3, padx=14, pady=7)
        ctr_mid_label2.place(x=20, y=150)

        # For failure rate of resource (center-mid)
        ctr_mid_subframe1 = Frame(ctr_mid_label2, bg='gray1', width=505, height=48, padx=3, pady=0,
                                  highlightbackground="gray1",
                                  highlightthickness=1)
        ctr_mid_subframe1.grid(row=1, column=1)

        self.cVar1 = IntVar() #resource button
        Resource_Step1.event_log = self.event_log         #orginal data without preprocessing
        Resource_step1_self.event_log = self.event_log
        Resource_Step1.firstpreprocess = self.firstpreprocess         #orginal data without preprocessing
        Resource_step1_self.firstpreprocess = self.firstpreprocess
        Resource_step1_self.extracted_data = self.extracted_data

        s = ttk.Style()
        s.configure('Red.TCheckbutton', foreground="white", background='gray1', font=("Consolas", 10, 'bold'))
        Resource_Label1 = ttk.Checkbutton(ctr_mid_subframe1, text=" Failure rate of Resource: ", variable=self.cVar1, width=27,
                                  onvalue=1, offvalue=0, style='Red.TCheckbutton')
        Resource_Label1.place(x=10, y=10)

        self.cVar1.set(1)
        dist_chosen1 = ttk.Combobox(ctr_mid_subframe1, width=17, textvariable=tk.StringVar())
        dist_chosen1.place(x=230, y=10)
        dist_chosen1['values'] = ['Random', 'Self-configuration']
        dist_chosen1.current(0)

        self.type1 = dist_chosen1
        ctr_button1 = tk.Button(ctr_mid_subframe1, text="Set", padx=25,
                                command=lambda: self.new_window1(parent, self.extracted_data ))
        ctr_button1.place(x=380, y=10)

        # For failure rate of system (center-mid)
        self.cVar2 = IntVar()  # system button
        System_Step1.event_log = self.event_log         #orginal data without preprocessing
        System_step1_self.event_log = self.event_log
        ctr_mid_subframe2 = Frame(ctr_mid_label2, bg='gray1', width=505, height=48, padx=3, pady=0,
                                  highlightbackground="gray1",
                                  highlightthickness=1)
        ctr_mid_subframe2.grid(row=2, column=1)
        System_Label1 = ttk.Checkbutton(ctr_mid_subframe2, text=" System down interval: ", variable=self.cVar2, width=25,
                                  onvalue=1, offvalue=0, style='Red.TCheckbutton')
        System_Label1.place(x=10, y=10)

        self.cVar2.set(0)
        dist_chosen2 = ttk.Combobox(ctr_mid_subframe2, width=17, textvariable=tk.StringVar())
        dist_chosen2['values'] = list(['Random', 'Self-configuration'])
        dist_chosen2.current(0)
        dist_chosen2.place(x=230, y=10)

        System_Step1.extracted_data = self.extracted_data   #data with key attributes
        System_step1_self.extracted_data = self.extracted_data

        self.type2 = dist_chosen2
        ctr_button3 = tk.Button(ctr_mid_subframe2, text="Set", padx=25,
                                command=lambda: self.new_window3(parent))
        ctr_button3.place(x=380, y=9)

        # Inject Anomaly patterns (center-bot)
        ctr_mid_label3 = LabelFrame(ctr_mid, text=" Step 2. Inject anomaly patterns", font=("Consolas", 10, 'bold'),
                                    fg="white", bg='gray1', bd=3, padx=14, pady=7)
        ctr_mid_label3.place(x=20, y=290)
        ctr_mid_subframe3 = Frame(ctr_mid_label3, bg='gray1', width=505, height=48, padx=3, pady=0,
                                  highlightbackground="gray1",
                                  highlightthickness=1)
        ctr_mid_subframe3.grid(row=1, column=1)

        Anomaly_Label = Label(ctr_mid_subframe3, text="- Set anomaly patterns ", font=("Consolas", 10, 'bold'),
                                fg="white", bg='gray1', anchor="w", width=25)
        Anomaly_Label.place(x=10, y=10)

        ctr_button2 = tk.Button(ctr_mid_subframe3, text="Set", padx=25,
                                command=lambda: self.new_window2(Inject_Anomaly))
        ctr_button2.place(x=380, y=9)
        PageThree.PageTwo = PageTwo

        def save_parameters():
            controller.show_frame2(PageThree)
        button2 = tk.Button(ctr_mid, text="Next", padx=25,
                            command=save_parameters)
        button2.place(x=475, y=380)

        parent.update()




