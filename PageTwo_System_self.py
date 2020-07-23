import warnings

warnings.filterwarnings(action='ignore')

# GUI PACKAGES
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# For Data preprocess
import numpy
import pandas as pd
import datetime
from datetime import datetime as dt

# Pages
from PageTwo_Inject_Anomaly import Inject_Anomaly
from abnormal_patterns_sys import Abnorm_sys
from PageThree import PageThree


class System_step1_self(tk.Toplevel):

    def new_window(self, root2, parent, Win_class):
        global System_step1_self_sub
        System_step1_self_sub = tk.Toplevel(parent)
        System_step1_self_sub.root2 = root2
        Win_class(System_step1_self_sub, root2)

    def __init__(self, root, parent, *args, **kwargs):
        self.root = root
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root["bg"] = 'dark slate gray'
        self.root['padx'] = 5
        self.root['pady'] = 5
        root2 = root


        # Create main containers
        base_frame = Frame(root, bg='gray1', width=250, height=200)
        base_frame.grid(row=0, column=0,  sticky="nsew")
        base_frame.grid_rowconfigure(1, weight=1)
        base_frame.grid_columnconfigure(0, weight=1)

        center = Frame(root, bg='gray1')
        center.grid(row=1, column=0, sticky="nsew")

        # title label (top)
        base_frame_label1 = Label(base_frame, text='Connection between System & Activity',
                                  font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray25',  relief="raised")
        base_frame_label1.grid(row=0, column=0, columnspan=3,sticky="nsew")

        # System info (center-top)

        # Reference to represent the number of activity  (center-top)
        global activitylist
        params = {
            'Case': 'count'
        }
        activitylist = self.extracted_data.groupby('Activity').agg(params).reset_index()
        system_info_frame1 = LabelFrame(center, text="(A) Set system attribute".format(len(activitylist)),
                                        font=("Consolas", 10, 'bold'),
                                        fg="white", bg='gray1', bd=3)
        system_info_frame1.config(highlightbackground="dark orange", highlightcolor = "dark orange", highlightthickness=2)
        system_info_frame1.grid(row=0, column=0, sticky="nwse", padx=10, pady=7)
        System_step1_self.system_info_frame1 = system_info_frame1
        # Select system attribute (center-top)
        self.cVar1 = IntVar()
        s = ttk.Style()
        s.configure('Red.TCheckbutton', foreground="aquamarine", background='gray1')
        sub_frame0 = Frame(system_info_frame1, bg='gray1', width=500)
        sub_frame0.grid(row=0, column=0, sticky='w', pady=(0,3))
        sub_frame0_label1 = ttk.Checkbutton(sub_frame0, text="Select a system attribute from existing dataframe: ", variable=self.cVar1, width=8,
                                  onvalue=1, style='Red.TCheckbutton')
        sub_frame0_label1.grid(row=0, column=0, sticky="w", padx=(0 ,1))
        sub_frame0_label1.config(width=50)

        system_chosen = ttk.Combobox(sub_frame0, width=15, textvariable=tk.StringVar())
        system_chosen.grid(row=0, column=1)
        system_chosen['values'] = list(self.event_log)  # original data without any preprocessing

        # Auto detection of System
        system_candidate = [list(self.event_log).index(i) for i in list(self.event_log)
                          if "system" in i or "System" in i or "SYSTEM" in i]
        if len(system_candidate) == 0:
            pass
        if len(system_candidate) == 1:
            system_chosen.current(system_candidate)
        if len(system_candidate) > 1:
            system_chosen.current(system_candidate[0])


        # Input the number of systems  (center-top)

        sub_frame1_label1 = ttk.Checkbutton(sub_frame0, text='Generate an artificial system attribute:', variable=self.cVar1,
                                  onvalue=2, style='Red.TCheckbutton')
        sub_frame1_label1.grid(row=1, column=0, sticky="w", padx=(0 ,1))


        self.cVar1.set(0)

        System_step1_self_sub.extracted_data = self.extracted_data   # data with key attributes
        def set_sys_attribute():
            if self.cVar1.get() == 1:
                selected_system = system_chosen.get()
                dat_system = self.firstpreprocess
                dat_system["System"] = self.event_log[selected_system]
                dat_system = dat_system.sort_values(["Case", "Timestamp"],
                                                        ascending=[True, True])
                params = {
                    'Case': 'count',
                    'Activity': lambda x: ','.join(sorted(pd.Series.unique(x)))
                }

                dat = dat_system[['Activity', 'System']]
                dat = dat.drop_duplicates()
                Abnorm_sys.dat = dat

                global extracted_data4
                extracted_data4 = pd.merge(self.extracted_data, dat, on="Activity")

                Inject_Anomaly.data_with_system= extracted_data4
                systemlist = dat_system.groupby('System').agg(params).reset_index()
                systemlist.columns = ["System", "Frequency", "Activities"]
                systemlist = systemlist.sort_values(["Frequency"], ascending=False)
                cols = ["System", "Frequency", "Activities"]
                systemlist = systemlist[cols]
                systemlist = systemlist.reset_index(drop=True)
                self.systemlist = systemlist
                self.systemlist2 = systemlist
                extracted_data2 = self.extracted_data
                extracted_data2["System"] = dat_system["System"]
                self.extracted_data2 = extracted_data2
                PageThree.before = extracted_data2
                system_info_frame1.config(highlightbackground="gray1", highlightcolor = "gray1", highlightthickness=2)
                base_frame_label1.config(highlightbackground="dark orange", highlightcolor = "dark orange", highlightthickness=2)

            elif self.cVar1.get() == 2:
                self.new_window(root2, parent, System_step1_self_sub)

            elif self.cVar1.get() < 1:
                messagebox.showinfo("Error", "Nothing was checked")
                root.attributes('-topmost', 1)
                root.attributes('-topmost', 0)

        action1 = tk.Button(sub_frame0, text="Set", padx=25, command = set_sys_attribute)
        action1.grid(row=2, column=2, padx= (20,10 ))

        # System down
        base_frame_label1 = LabelFrame(center, text="(B) Set system downtime event",
                                       font=("Consolas", 10, 'bold'),
                                       fg="white", bg='gray1', bd=3)
        base_frame_label1.grid(row=1, column=0, pady=10)
        System_step1_self.base_frame_label1 = base_frame_label1

        sub_frame2 = Frame(base_frame_label1, bg='gray1')
        sub_frame2.grid(row=0, column=0, sticky='w',padx=10)

        sub_frame2.rowconfigure(0, weight=1)
        sub_frame2.columnconfigure(0, weight=1)
        sub_frame2.grid_propagate(False)

        canvas_failure = Canvas(sub_frame2, bd=0, bg='gray1', highlightthickness=0)
        canvas_failure.grid(row=0, column=0, sticky="news")
        frame_buttons1 = Frame(canvas_failure, bg='gray1')
        frame_buttons1.config(width=500)
        sub_frame2.config(width=500, height=240)
        self.en = 0
        def add_downtime():
            self.en = self.en+1
            unixtime = self.extracted_data['unixtime']
            mintime= min(unixtime)
            initial = str(datetime.datetime.utcfromtimestamp(mintime))
            globals()['down_dist{}'.format(self.en)] = tk.StringVar()
            globals()['down_0_{}'.format(self.en)] = ttk.Combobox(frame_buttons1, width=6 ,textvariable=['down_dist{}'.format(self.en)])
            globals()['down_0_{}'.format(self.en)]['values'] = list(self.systemlist['System'])
            globals()['down_0_{}'.format(self.en)].grid(row=self.en-1, column=0)
            globals()['down_0_{}'.format(self.en)].current(0)

            globals()['down_1_{}'.format(self.en)] = Label(frame_buttons1, text=' : ', font=("Consolas", 10, 'bold'),
                                                 fg="white", bg='gray1', anchor="w")
            globals()['down_1_{}'.format(self.en)].grid(row=self.en-1, column=1)

            globals()['down_2_{}'.format(self.en)] = Text(frame_buttons1, height=1, width=24)
            globals()['down_2_{}'.format(self.en)].grid(row=self.en-1, column=2)
            globals()['down_2_{}'.format(self.en)].insert(tk.CURRENT, initial)
            globals()['down_3_{}'.format(self.en)] = Label(frame_buttons1, text=' ~ ', font=("Consolas", 10, 'bold'),
                                                 fg="white", bg='gray1', anchor="w")
            globals()['down_3_{}'.format(self.en)].grid(row=self.en-1, column=3)

            globals()['down_4_{}'.format(self.en)] = Text(frame_buttons1, height=1, width=24)
            globals()['down_4_{}'.format(self.en)].grid(row=self.en-1, column=4)
            globals()['down_4_{}'.format(self.en)].insert(tk.CURRENT, initial)

            downtime.grid(row=self.en, column=0, columnspan=5, padx=(2,0), pady =(3,0) ,sticky="nsew")
            canvas_failure.configure(yscrollcommand=vsb1.set, xscrollcommand=hsb1.set)
            canvas_failure.create_window((0, 0), window=frame_buttons1, anchor='nw')
            frame_buttons1.update_idletasks()
            canvas_failure.config(scrollregion=canvas_failure.bbox("all"))

        downtime = tk.Button(frame_buttons1, text="+", height=1, width= 60 , command=lambda: add_downtime())
        downtime.grid(row=0, column=0, columnspan=5, pady=(2, 0), sticky="nsew")

        vsb1 = tk.Scrollbar(sub_frame2, orient="vertical", command=canvas_failure.yview)
        vsb1.grid(row=0, column=1, sticky='ns')
        hsb1 = tk.Scrollbar(sub_frame2, orient="horizontal", command=canvas_failure.xview)
        hsb1.grid(row=1, column=0, sticky='we')
        canvas_failure.configure(yscrollcommand=vsb1.set, xscrollcommand = hsb1.set)
        canvas_failure.create_window((0, 0), window=frame_buttons1, anchor='nw')
        frame_buttons1.update_idletasks()
        canvas_failure.config(scrollregion=canvas_failure.bbox("all"))


        # Activity - System connection (Center-mid)

        def attach_sys():

            df3 = pd.DataFrame(columns=['Event:system down',  'Start_Timestamp', 'Finish_Timestamp'])

            sys_down = list(numpy.repeat("sys", self.en))
            start = list(numpy.repeat("st", self.en))
            finish = list(numpy.repeat("ft", self.en))


            for i in range(1, self.en+1):
                sys_down[i - 1] = globals()['down_0_{}'.format(i)].get()
                start[i - 1] = globals()['down_2_{}'.format(i)].get("1.0", "end-1c")
                finish[i - 1] = globals()['down_4_{}'.format(i)].get("1.0", "end-1c")

            form= "%Y-%m-%d %H:%M:%S.%f"
            df3['Event:system down'] =  sys_down
            df3['Start_Timestamp'] = start
            df3['Start_Timestamp'] = df3['Start_Timestamp'].apply(lambda x: dt.strptime(x, form))
            df3['Finish_Timestamp'] = finish
            df3['Finish_Timestamp'] = df3['Finish_Timestamp'].apply(lambda x: dt.strptime(x, form))

            df4= df3[['Event:system down', 'Start_Timestamp', 'Finish_Timestamp']]
            Inject_Anomaly.system_down =df4     # System down
            PageThree.system_down =df4

            messagebox.showinfo("Message", "Successfully proceeded")
            root.destroy()

        action_sys1 = tk.Button(center, text="Apply", width=10, command=lambda: attach_sys())
        action_sys1.grid(row=2, column=0, sticky = 'e', padx= (0,20), pady=(20,10))



#############################################################################################

class System_step1_self_sub(tk.Toplevel):    # resource- failure rate
    def __init__(self, root, root2  ,*args, **kwargs):
        self.root2= root2
        self.root = root
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root["bg"] = 'gray1'
        self.root['padx' ] =5
        self.root['pady' ] =5

        # Create main containers
        base_frame = Frame(root, bg='gray1', width=250, height=200 )
        base_frame.grid(row=0, column=0, pady=(0, 7), sticky="nsew")
        base_frame.grid_rowconfigure(1, weight=1)
        base_frame.grid_columnconfigure(0, weight=1)

        # title label (top)
        base_frame_label1 = Label(base_frame, text='Connection between System & Activity', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray25' , relief="raised")
        base_frame_label1.grid(row=0, column=0, columnspan =3, sticky="nsew")
        base_frame_label1.grid_rowconfigure(1, weight=1)
        base_frame_label1.grid_columnconfigure(0, weight=1)
        # System info (center-top)

        # Reference to represent the number of activity  (center-top)
        global activitylist
        params = {
            'Case': 'count'
        }
        activitylist = self.extracted_data.groupby('Activity').agg(params).reset_index()
        system_info_frame1 = LabelFrame(base_frame, text="The number of activities ={}".format(len(activitylist)), font=("Consolas", 10, 'bold'),
                                          fg="white", bg='gray1', bd=3)
        system_info_frame1.grid(row=1, column=0 ,  padx=10, pady=7 , sticky = 'nwse')
        system_info_frame1.config(highlightbackground="dark orange",highlightcolor = "dark orange", highlightthickness=2)

        # Input the number of systems  (center-top)
        sub_frame2 = Frame(system_info_frame1, bg='gray1')
        sub_frame2.grid(row=0, column=0, sticky='w', pady=10)
        # sub_frame2.rowconfigure(0, weight=1)
        # sub_frame2.columnconfigure(0, weight=1)
        # sub_frame2.grid_propagate(False)

        sub_frame2_label1 = Label(sub_frame2, text='Set the number of system: ', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1' ,anchor="w")

        sub_frame2_label1.grid(row=0, column=0, sticky="w", padx=(10 ,1))
        sub_frame2_label1.config(width=25)

        textBox1 =Text(sub_frame2, height=1, width=4)
        textBox1.grid(row=0, column=1)
        textBox1.configure(state="normal", background="white")

        global systemlist
        def set():
            n = int(textBox1.get("1.0", "end-1c"))
            systemlist=list(numpy.repeat("sys", n))
            for i in range(0,n):
                systemlist[i] = "Sys_{}".format(i)
            System_step1_self.systemlist= systemlist
            numpy.random.seed(1234)
            k=0
            for i in activitylist['Activity']:
                k+=1
                globals()['act{}_sys'.format(k)]['values'] = systemlist
                globals()['act{}_sys'.format(k)].current(numpy.random.randint(0,len(systemlist)))
            messagebox.showinfo("Message",
                                    "{} systems have been generated".format(n), parent= root)
            sub_frame2_label1.config(highlightbackground="gray1", highlightcolor="gray1",
                                      highlightthickness=2)

            base_frame_label2.config(highlightbackground="dark orange", highlightcolor="dark orange",
                                     highlightthickness=2)

            numpy.random.seed(0)
            root.attributes('-topmost', 1)
            root.attributes('-topmost', 0)

        action1 = tk.Button(sub_frame2, text="Set", padx=25, command= set)
        action1.grid(row=0, column=2, padx= (20,10 ))

        # Activity - System connection (Center-mid)
        base_frame_label2 = LabelFrame(base_frame, text="Allocate systems on each activity", font=("Consolas", 10, 'bold'),
                                       fg="white", bg='gray1', bd=3, padx=14, pady=7)
        base_frame_label2.grid(row=2, column=0, padx=10)

        sub_frame2 =Frame(base_frame_label2, bg='gray1')
        sub_frame2.grid(row=0, column=0, sticky='nwse')

        sub_frame2.rowconfigure(0, weight=1)
        sub_frame2.columnconfigure(0, weight=1)
        sub_frame2.grid_propagate(False)

        canvas = Canvas(sub_frame2, bd=0, bg='gray1', highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="news")
        vsb = tk.Scrollbar(sub_frame2, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        frame_buttons = Frame(canvas, bg='gray1')
        canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

        k=0
        for i in activitylist['Activity']:
            k += 1
            globals()['act{}'.format(k)] = Label(frame_buttons, text='{} = '.format(i), font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1' ,anchor="w")
            globals()['act{}'.format(k)].grid(row= k-1, column= 0)
            globals()['act{}'.format(k)].config(width=30)
            globals()['dist3{}'.format(k)] = tk.StringVar()
            globals()['act{}_sys'.format(k)] = ttk.Combobox(frame_buttons, width=10, textvariable=['dist3{}'.format(k)])
            globals()['act{}_sys'.format(k)].grid(row= k-1, column= 1)

        frame_buttons.update_idletasks()
        sub_frame2.config(width=350, height=240)
        canvas.config(scrollregion=canvas.bbox("all"))

        def attach_sys(dat):
            k = 0
            sl=list(numpy.repeat("act",len(dat)))
            for i in dat['Activity']:
                k += 1
                sl[k-1] = globals()['act{}_sys'.format(k)].get()
            dat['System'] = pd.DataFrame(sl)
            dat = dat[['Activity' , 'System']]
            Abnorm_sys.dat = dat

            global extracted_data4
            extracted_data4 = pd.merge(self.extracted_data, dat, on="Activity")
            params = {
                'Case': 'count',
                'Activity': lambda x: ','.join(sorted(pd.Series.unique(x)))
            }
            PageThree.before = extracted_data4
            systemlist2 = extracted_data4.groupby('System').agg(params).reset_index()
            systemlist2.columns = ["System", "Frequency", "Activities"]
            systemlist2 = systemlist2.sort_values(["Frequency"], ascending=False)
            cols = ["System", "Frequency",  "Activities"]
            systemlist2 = systemlist2[cols]
            System_step1_self.systemlist2 = systemlist2
            Inject_Anomaly.data_with_system = extracted_data4
            messagebox.showinfo("Message", "Successfully proceeded")
            System_step1_self.system_info_frame1.config(highlightbackground="gray1", highlightcolor="gray1", highlightthickness=2)
            System_step1_self.base_frame_label1.config(highlightbackground="dark orange", highlightcolor="dark orange",
                                     highlightthickness=2)
            root.destroy()
            self.root2.lift()

        action_sys1 = tk.Button(base_frame, text="Apply", width=10, command= lambda: attach_sys(activitylist))
        action_sys1.grid(row=3, column=0, sticky = 'e', padx= (0,20), pady=10)