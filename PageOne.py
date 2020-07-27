import os
import warnings
warnings.filterwarnings(action='ignore')


#GUI PACKAGES
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import webbrowser

#For Data preprocess
import pandas as pd
import time
from datetime import datetime as dt
import datetime
import numpy

#Pages
from PageTwo import PageTwo

from PageTwo_Resource import Resource_Step1
from PageTwo_System import System_Step1
from PageThree import PageThree
from PageTwo_Inject_Anomaly import Inject_Anomaly

class GridTest(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("AIR-BAGEL")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # global container
        # container = tk.Frame(self)
        # container.grid(row=0, column=0, columnspan=10, rowspan=10, sticky="nsew")
        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = PageOne(self)
        self._frame = frame
        frame.grid(row=0, column=0, sticky="nesw")

        self.show_frame(frame)

    def show_frame(self, cont):
        frame = cont
        frame.tkraise()

    def show_frame1(self):

        new_frame = PageTwo(self)
        new_frame.grid(row=0, column=0, sticky="nesw")

        self._frame.destroy()
        self._frame = new_frame
        new_frame.tkraise()


    def show_frame1_2(self):

        new_frame = Inject_Anomaly(self)
        new_frame.grid(row=0, column=0, sticky="nesw")

        self._frame.destroy()
        self._frame = new_frame
        new_frame.tkraise()


    def show_frame2(self):

        new_frame = PageThree(self)
        new_frame.grid(row=0, column=0, sticky="nesw")

        self._frame.destroy()
        self._frame = new_frame
        new_frame.tkraise()



class PageOne(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='dark slate gray')


        # Create main containers
        top_frame = Frame(self, bg='dark slate gray', width=50, height=50, padx=7, pady=3)
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
        top_mid_label1 = Label(top_frame, text='(1) Data import and preprocessing', font=("Consolas", 13, 'bold'),
                               fg="white", bg='gray25', relief = "raised")

        top_mid_label1.grid(row=0, column=1, sticky="nsew")

        # Create sub frame (center frame)
        ctr_left = Frame(center, bg='gray1', width=150, height=190, highlightthickness=1, highlightbackground="gray15")
        ctr_right = Frame(center, bg='gray1', height=190, highlightthickness=1, highlightbackground="gray15")
        ctr_left.grid(row=0, column=0, padx=(0, 7), pady=(0, 3), sticky="ns")
        ctr_right.grid(row=0, column=1, pady=(0, 3), sticky="nsew")
        ctr_right.grid_rowconfigure(1, weight=1)
        ctr_right.grid_columnconfigure(0, weight=1)

        # File list in directory folder (center-left)
        global path
        org_path = os.getcwd()
        Resource_Step1.org_path = org_path
        System_Step1.org_path = org_path
        PageThree.org_path =org_path
        os.chdir(os.sep.join([str(org_path), "input"]))
        input_path = os.getcwd()

        ctr_left_label1 = Label(ctr_left, text='Files', font=("Consolas", 10, 'bold'),
                                fg="white", bg='gray25', anchor="center", relief="raised")
        ctr_left_label1.grid(row=0, column=0, sticky="we")
        # ctr_left_label1.config(width=25)

        dir_scroll = ScrolledText(ctr_left, width=24, height=2, wrap=tk.WORD)
        dir_scroll.grid(row=1, column=0, rowspan=4)
        dir_scroll.insert(tk.INSERT, 'Directory : "{}"'.format(input_path))
        dir_scroll.configure(background='snow', font=("ms sans Serif", 6))

        file_list = os.listdir(input_path)
        csv_list = [s for s in file_list if '.csv' in s]

        def selectdata():
            global event_log
            alert_value = 0
            alert_message1 = ''
            if self.cVar1.get() > 0:
                event_log = pd.read_csv(csv_list[int(self.cVar1.get()) - 1])
                dat_name = str(csv_list[int(self.cVar1.get()) - 1])
                dat_name = str(dat_name.split('.')[0])
                PageThree.dat_name=dat_name
                alert_value += 1
                alert_message1 = 'Completely loaded: {}'.format(csv_list[int(self.cVar1.get()) - 1])
                PageTwo.event_log = event_log       #orginal data without preprocessing
                datainfo(event_log)
                autodetection()
                messagebox.showinfo("Message", alert_message1)
                ctr_left_label2.config(highlightbackground="gray1", highlightcolor = "gray1", highlightthickness=2)
                ctr_right_label2.config(highlightbackground="dark orange", highlightcolor = "dark orange", highlightthickness=2)

            if alert_value == 0:
                alert_message1 = "Nothing was checked"
                messagebox.showinfo("Error", alert_message1)

        # autodetection: automatically set key attributes (center-right)
        def autodetection():
            # Caseid
            case_candidate = [list(event_log).index(i) for i in list(event_log)
                              if "case" in i or "Case" in i or "CASE" in i]
            if len(case_candidate) == 0:
                pass
            if len(case_candidate) == 1:
                caseid_value_chosen.current(case_candidate)
            if len(case_candidate) > 1:
                att_list = [list(event_log)[i] for i in case_candidate]
                case_candidate2 = [att_list.index(i) for i in att_list if "id" in i or "ID" in i]
                if len(case_candidate2) == 1:
                    caseid_value_chosen.current(case_candidate2)
                else:
                    caseid_value_chosen.current(case_candidate[0])

            # Eventid
            cand = ["-- no attribute --"] + list(event_log)
            event_candidate = [cand.index(i) for i in cand
                              if "event" in i or "Event" in i or "EVENT" in i]
            if len(event_candidate) == 0:
                pass
            if len(event_candidate) == 1:
                eventid_value_chosen.current(event_candidate)
            if len(event_candidate) > 1:
                att_list = [cand[i] for i in event_candidate]
                event_candidate2 = [att_list.index(i) for i in att_list if "id" in i or "ID" in i]
                if len(event_candidate2) == 1:
                    eventid_value_chosen.current(event_candidate2)
                else:
                    eventid_value_chosen.current(event_candidate[0])

            # Activity
            activity_candidate = [list(event_log).index(i) for i in list(event_log)
                               if "activity" in i or "Activity" in i or "ACTIVITY" in i]
            if len(activity_candidate) == 0:
                activity_candidate = [list(event_log).index(i) for i in list(event_log)
                               if "name" in i or "Name" in i or "NAME" in i]
                if len(activity_candidate) == 0:
                    pass
                if len(activity_candidate) == 1:
                    activity_value_chosen.current(activity_candidate)
                if len(activity_candidate) > 1:
                    activity_value_chosen.current(activity_candidate[0])
            if len(activity_candidate) == 1:
                activity_value_chosen.current(activity_candidate)
            if len(activity_candidate) > 1:
                activity_value_chosen.current(activity_candidate[0])

            # timestamp
            time_candidate = [list(event_log).index(i) for i in list(event_log)
                               if "time" in i or "Time" in i or "TIME" in i]
            if len(time_candidate) == 0:
                time_candidate = [list(event_log).index(i) for i in list(event_log)
                                      if "date" in i or "Date" in i or "DATE" in i]
                if len(time_candidate) == 0:
                    pass
                if len(time_candidate) == 1:
                    timestamp_value_chosen.current(time_candidate)
                if len(time_candidate) > 1:
                    timestamp_value_chosen.current(time_candidate[0])
            if len(time_candidate) == 1:
                timestamp_value_chosen.current(time_candidate)
            if len(time_candidate) > 1:
                att_list = [list(event_log)[i] for i in time_candidate]
                time_candidate2 = [att_list.index(i) for i in att_list
                                   if "complete" in i or "Complete" in i or "COMPLETE" in i]
                if len(time_candidate2) == 1:
                    timestamp_value_chosen.current(time_candidate2)
                else:
                    timestamp_value_chosen.current(time_candidate[0])

        # datainfo: display maximum 20 rows of data (center-right)
        def datainfo(event_log):
            l=list(event_log)
            caseid_value_chosen['values'] = list(event_log)
            caseid_value_chosen.current(0)
            eventid_value_chosen['values'] = ["-- no attribute --"] +l
            eventid_value_chosen.current(0)
            activity_value_chosen['values'] = list(event_log)
            activity_value_chosen.current(0)
            timestamp_value_chosen['values'] = list(event_log)
            timestamp_value_chosen.current(0)
            pd.set_option('display.width', 1000)
            mylist.delete('1.0', END)
            mylist.insert(tk.CURRENT, event_log[1:20].to_string(index=False))

        ctr_left_label2 = LabelFrame(ctr_left, text="csv_list (max=10)", font=("Consolas", 10, 'bold'),
                                     fg="white", bg='gray1', bd=3, height=248)
        ctr_left_label2.config(highlightbackground="dark orange", highlightcolor = "dark orange", highlightthickness=2)
        ctr_left_label2.grid(row=12, sticky="we", padx=5, pady=(7, 0), ipadx=0, ipady=0)
        ctr_left_label2.grid_propagate(False)
        style1 = ttk.Style()
        style1.configure("Red.TCheckbutton", foreground="aquamarine", background='gray1')
        i = 0
        self.cVar1 = IntVar()
        self.cVar1.set(0)
        for values in csv_list[0:10]:
            globals()['c{}'.format(i)] = ttk.Checkbutton(ctr_left_label2, text=csv_list[i], onvalue=i + 1, offvalue=0,
                                                         variable=self.cVar1)
            globals()['c{}'.format(i)].grid(column=0, row=i + 10, sticky='w')
            globals()['c{}'.format(i)].configure(style="Red.TCheckbutton")
            i = i + 1
        action = tk.Button(ctr_left, text="Load",  width = 10, command=selectdata)
        action.grid(row=13,  sticky="we" , padx =60 ,pady= (7,10))



        os.chdir(os.sep.join([str(org_path), "utils"]))
        image1 = PhotoImage(file= "IEL lab logo5.png")
        # smaller_image1 = image1.subsample(2, 2)
        smaller_image1 = image1

        image_frame = Frame(ctr_left, bg='gray1')
        image_frame.grid(row=15, pady=(20,0))

        panel1 = Label(image_frame, image = smaller_image1, bg ='gray1',borderwidth=0, highlightthickness=0)
        panel1.photo = smaller_image1
        panel1.grid(row=0, column=0)

        def callback(url):
            webbrowser.open_new(url)

        link1 = Label(image_frame, text=" Intelligent Enterprise Lab.", bg = 'gray1', fg="cyan2", cursor="hand2")
        link1.bind("<Button-1>", lambda e: callback("http://iel.unist.ac.kr/?page=introduction"))
        link1.grid(row=0, column=1, sticky='w')



        image2 = PhotoImage(file= "GitHub-Mark-Light-32px.png")
        # smaller_image2 = image2.subsample(1, 1)
        smaller_image2=image2


        panel2 = Label(image_frame, image = smaller_image2, bg ='gray1',borderwidth=0, highlightthickness=0)
        panel2.photo = smaller_image2
        panel2.grid(row=1, column=0, pady=5)

        link2 = Label(image_frame, text=" Github repository", bg = 'gray1', fg="cyan2", cursor="hand2")
        link2.bind("<Button-1>", lambda e: callback("https://github.com/jonghyeonk/AIR-BAGEL"))
        link2.grid(row=1, column=1, pady=5, sticky='w')

        os.chdir(os.sep.join([str(org_path), "input"]))


        # Select key attribute (center-right)
        ctr_right_label1 = Label(ctr_right, text='Environment', font=("Consolas", 10, 'bold'),
                                 fg="white", bg='gray25',  relief="raised")
        ctr_right_label1.grid(row=0, column=0, sticky="nsew")
        # ctr_right_label1.config(width=45)

        ctr_right_sub = Frame(ctr_right, bg='gray1', height=190, highlightthickness=1, highlightbackground="gray15")
        ctr_right_sub.grid(row=1, column=0, sticky="nsew")


        ctr_right_label2 = LabelFrame(ctr_right_sub, text="Set key attributes", font=("Consolas", 10, 'bold'),
                                      fg="white", bg='gray1', bd=3, padx=14, pady=7)

        ctr_right_label2.grid(row=1, sticky="w", padx=14, pady=(7, 0))

        Caseid_Label = Label(ctr_right_label2, text=" 1. Case_ID", font=("Consolas", 10, 'bold'),
                             fg="white", bg='gray10', anchor="w", width=14)
        Caseid_Label.grid(column=0, row=4)
        Eventid_Label = Label(ctr_right_label2, text=" 2. Event_ID", font=("Consolas", 10, 'bold'),
                             fg="white", bg='gray10', anchor="w", width=14)
        Eventid_Label.grid(column=0, row=5)
        Activity_Label = Label(ctr_right_label2, text=" 3. Activity", font=("Consolas", 10, 'bold'),
                             fg="white", bg='gray10', anchor="w", width=14)
        Activity_Label.grid(column=0, row=6)
        Timestamp_Label = Label(ctr_right_label2, text=" 4. Timestamp", font=("Consolas", 10, 'bold'),
                             fg="white", bg='gray10', anchor="w", width=14)
        Timestamp_Label.grid(column=0, row=7)
        Timeform_Label = Label(ctr_right_label2, text="    - format", font=("Consolas", 10),
                             fg="white", bg='gray10', anchor="w", width=14)
        Timeform_Label.grid(column=0, row=8)

        caseid_value = tk.StringVar()
        caseid_value_chosen = ttk.Combobox(ctr_right_label2, width=26, textvariable=caseid_value)
        caseid_value_chosen.grid(column=1, row=4)

        eventid_value = tk.StringVar()
        eventid_value_chosen = ttk.Combobox(ctr_right_label2, width=26, textvariable=eventid_value)
        eventid_value_chosen.grid(column=1, row=5)

        activity_value = tk.StringVar()
        activity_value_chosen = ttk.Combobox(ctr_right_label2, width=26, textvariable=activity_value)
        activity_value_chosen.grid(column=1, row=6)

        timestamp_value = tk.StringVar()
        timestamp_value_chosen = ttk.Combobox(ctr_right_label2, width=26, textvariable=timestamp_value)
        timestamp_value_chosen.grid(column=1, row=7)

        timeform_value = tk.StringVar()
        timeform_value_chosen = ttk.Combobox(ctr_right_label2, width=26, textvariable=timeform_value)
        timeform_value_chosen.grid(column=1, row=8)
        timeform_value_chosen['values'] = ["","2020-01-02 03:04:05.006" , "2020-01-02 03:04:05",
                                           "2020-01-02 03:04:05.006 PM", "2020-01-02 03:04:05 PM",
                                           "20-01-02 03:04:05.006", "20-01-02 03:04:05",
                                           "20-01-02 03:04:05.006 PM", "20-01-02 03:04:05 PM",
                                           "2020/01/02 03:04:05.006", "2020/01/02 03:04:05",
                                           "2020/01/02 03:04:05.006 PM", "2020/01/02 03:04:05 PM",
                                           "20/01/02 03:04:05.006", "20/01/02 03:04:05",
                                           "20/01/02 03:04:05.006 PM", "20/01/02 03:04:05 PM",
                                           "Self-configuration"]
        timeform_value_chosen.current(0)

        def TextBoxUpdate(event=None):
            if event.widget.get() == "Self-configuration":
                timeform_value_chosen.current(0)

        timeform_value_chosen.bind("<<ComboboxSelected>>", TextBoxUpdate)

        # Scrollbar to represent dataframe (center-left)
        ctr_right_label3 = LabelFrame(ctr_right_sub, text="Data preview (maximum 20 rows)", font=("Consolas", 10, 'bold'),
                                      fg="white", bg='gray1', bd=3, padx=12, width=400, height=135, pady=7)

        ctr_right_label3.grid(row=3, sticky="w", padx=14, pady=(14, 0))

        mylist = Text(ctr_right_label3, width=50, height=6, wrap=NONE)
        vscroll = Scrollbar(ctr_right_label3, orient=VERTICAL, command=mylist.yview)
        vscroll.place(in_=mylist, relx=1.0, relheight=1.0, bordermode="outside")
        mylist['yscroll'] = vscroll.set
        hscroll = Scrollbar(ctr_right_label3, orient=HORIZONTAL, command=mylist.xview)
        hscroll.place(in_=mylist, rely=1.0, relwidth=1.0, bordermode="outside")
        mylist['xscroll'] = hscroll.set
        mylist.grid(row=0, column=0, padx=(0,20), pady=(0,30))
        global n
        n = 0

        def iserror(func, *args, **kw):
            try:
                func(*args, **kw)
                return False
            except Exception:
                return True

        def save_key_attributes():
            if len(event_log) > 0:
                selected_caseid = caseid_value_chosen.get()
                selected_eventid = eventid_value_chosen.get()
                selected_activity = activity_value_chosen.get()
                selected_timestamp = timestamp_value_chosen.get()

                global extracted_data  #event_log only with key attributes
                if selected_eventid=="-- no attribute --" :
                    extracted_data = event_log[
                        [selected_caseid, selected_activity, selected_timestamp]]
                    extracted_data["Event"] = list(range(0,len(event_log.index)))
                    cols = extracted_data.columns.tolist()
                    cols = cols[:1]+ cols[-1:] + cols[1:3]
                    extracted_data = extracted_data[cols]

                if selected_eventid!="-- no attribute --" :
                    extracted_data = event_log[[selected_caseid, selected_eventid, selected_activity, selected_timestamp]]
                extracted_data.columns = \
                    ["Case", "Event", "Activity", "Timestamp"]
                PageTwo.firstpreprocess = extracted_data
                extracted_data = extracted_data.sort_values(["Case", "Timestamp"],
                                                            ascending=[True, True])

                form_dict = {"2020-01-02 03:04:05.006":"%Y-%m-%d %H:%M:%S.%f",
                             "2020-01-02 03:04:05":"%Y-%m-%d %H:%M:%S",
                            "2020-01-02 03:04:05.006 PM":"%Y-%m-%d %I:%M:%S.%f %p",
                            "2020-01-02 03:04:05 PM":"%Y-%m-%d %I:%M:%S %p",
                            "20-01-02 03:04:05.006":"%y-%m-%d %H:%M:%S.%f",
                            "20-01-02 03:04:05":"%y-%m-%d %H:%M:%S",
                            "20-01-02 03:04:05.006 PM":"%y-%m-%d %I:%M:%S.%f %p",
                            "20-01-02 03:04:05 PM":"%y-%m-%d %I:%M:%S %p",
                             "2020/01/02 03:04:05.006": "%Y/%m/%d %H:%M:%S.%f",
                             "2020/01/02 03:04:05": "%Y/%m/%d %H:%M:%S",
                             "2020/01/02 03:04:05.006 PM": "%Y/%m/%d %I:%M:%S.%f %p",
                             "2020/01/02 03:04:05 PM": "%Y/%m/%d %I:%M:%S %p",
                             "20/01/02 03:04:05.006": "%y/%m/%d %H:%M:%S.%f",
                             "20/01/02 03:04:05": "%y/%m/%d %H:%M:%S",
                             "20/01/02 03:04:05.006 PM": "%y/%m/%d %I:%M:%S.%f %p",
                             "20/01/02 03:04:05 PM": "%y/%m/%d %I:%M:%S %p"
                             }

                if timeform_value_chosen.get() not in form_dict.keys() :
                    form = timeform_value_chosen.get()
                    if iserror(dt.strptime, extracted_data['Timestamp'][0], form):
                        if "\"" in form or "\'" in form:
                            words = ["Type timestamp format without", "\'", "or", "\""]
                            words = " ".join(words)
                            messagebox.showinfo("Error", words)
                        else: messagebox.showinfo("Error", "Wrong input for timestamp format: use format in 'datetime' packages. (ex: %Y-%m-%d %H:%M:%S)")
                    else:
                        time = extracted_data['Timestamp'].apply(lambda x: dt.strptime(x, form))
                        unixtime = time.apply(lambda x: (x - dt(1970, 1, 1)).total_seconds())
                        extracted_data['Timestamp'] = time
                        extracted_data['unixtime'] = unixtime
                        PageTwo.extracted_data = extracted_data
                        messagebox.showinfo("Message", "Loaded")
                        tk.Frame.grid_forget()
                        parent.show_frame1()


                if timeform_value_chosen.get() in form_dict.keys():
                    form = form_dict[timeform_value_chosen.get()]
                    if iserror(dt.strptime, extracted_data['Timestamp'][0], form):
                        messagebox.showinfo("Error",
                                            "{0} is not matched with {1}".format(extracted_data['Timestamp'][0], form))
                    else:
                        time = extracted_data['Timestamp'].apply(lambda x: dt.strptime(x, form))
                        unixtime = time.apply(lambda x: (x - dt(1970, 1, 1)).total_seconds())
                        extracted_data['Timestamp'] = time
                        extracted_data['unixtime'] = unixtime
                        PageTwo.extracted_data = extracted_data
                        messagebox.showinfo("Message", "Loaded")
                        parent.show_frame1()

            else:
                messagebox.showinfo("Error", "Error")

        button1 = tk.Button(ctr_right_sub, text="Next", width=10,
                            command= save_key_attributes)
        button1.grid(row=4, padx=(0,20), pady=(7,10), sticky = 'e')


app = GridTest()
app.mainloop()
