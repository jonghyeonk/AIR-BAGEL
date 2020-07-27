import warnings
import os
warnings.filterwarnings(action='ignore')

#GUI PACKAGES
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#For Data preprocess
import numpy
import pandas as pd
import datetime

#Pages
from PageTwo_Inject_Anomaly import Inject_Anomaly
from abnormal_patterns_sys import Abnorm_sys
from PageThree import PageThree

class System_Step1(tk.Toplevel):

    def new_window(self, root2, parent, Win_class):
        global System_Step1_sub
        System_Step1_sub = tk.Toplevel(parent)
        System_Step1_sub.root2 = root2
        Win_class(System_Step1_sub, root2)
        
    def __init__(self, root , parent,*args, **kwargs):
        self.root = root
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root["bg"] = 'dark slate gray'
        self.root['padx' ] =5
        self.root['pady' ] =5
        root2 = root

        # Create main containers
        base_frame = Frame(root, bg='gray1', width=250, height=200 )
        base_frame.grid(row=0, column=0, sticky="nsew")
        base_frame.grid_rowconfigure(1, weight=1)
        base_frame.grid_columnconfigure(0, weight=1)
        center = Frame(root, bg='gray1')
        center.grid(row=1, column=0, sticky="nsew")

        # title label (top)
        base_frame_label1 = Label(base_frame, text='Parameter setting on system root', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray25' , relief="raised")
        base_frame_label1.grid(row=0, column=0, columnspan=3,sticky="nsew")


        # System info (Center-top) , to set system attribute
        system_info_frame1 = LabelFrame(base_frame, text="(A) Set system attribute", font=("Consolas", 10, 'bold'),
                                          fg="white", bg='gray1', bd=3)
        system_info_frame1.config(highlightbackground="dark orange", highlightcolor = "dark orange", highlightthickness=2)

        system_info_frame1.grid(row=1, column=0, sticky="nw", padx=10, pady=7)

        System_Step1.system_info_frame1 = system_info_frame1
        self.system_info_frame1= system_info_frame1
        self.cVar1 = IntVar()
        s = ttk.Style()
        s.configure('Red.TCheckbutton', foreground="aquamarine", background='gray1')

        sub_frame0 = Frame(system_info_frame1, bg='gray1', width=500)
        sub_frame0.grid(row=0, column=0, pady=(0,3),sticky='w')
        sub_frame0_label1 = ttk.Checkbutton(sub_frame0, text="Select a system attribute from existing dataframe: ", variable=self.cVar1, width=20,
                                  onvalue=1, style='Red.TCheckbutton')
        sub_frame0_label1.grid(row=0, column=0, sticky="w", padx=(0 ,1))
        sub_frame0_label1.config(width=50)

        system_chosen = ttk.Combobox(sub_frame0, width=15, textvariable=tk.StringVar())
        system_chosen.grid(row=0, column=1, padx=(0,10))
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

        sub_frame0_label2 = ttk.Checkbutton(sub_frame0, text='Generate an artificial system attribute ', variable=self.cVar1,
                                  onvalue=2, style='Red.TCheckbutton')
        sub_frame0_label2.grid(row=1, column=0, sticky="w", padx=(0 ,1))

        self.cVar1.set(0)

        System_Step1_sub.extracted_data = self.extracted_data   # data with key attributes
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
                Inject_Anomaly.data_with_system = extracted_data4
                systemlist = dat_system.groupby('System').agg(params).reset_index()
                systemlist.columns = ["System", "Frequency", "Activities"]
                systemlist = systemlist.sort_values(["Frequency"], ascending=False)
                cols = ["System", "Frequency", "Activities"]
                systemlist = systemlist[cols]
                systemlist = systemlist.reset_index(drop=True)
                self.systemlist = systemlist
                self.systemlist2 = systemlist

                system_info_frame1.config(text="Systems in event log")
                System_Step1.mylist1.insert(tk.CURRENT, pd.DataFrame(systemlist).to_string(
                    index=False))
                extracted_data2 = self.extracted_data
                extracted_data2["System"] = dat_system["System"]
                self.extracted_data2 = extracted_data2
                PageThree.before = extracted_data2
                system_info_frame1.config(highlightbackground="gray1", highlightcolor = "gray1", highlightthickness=2)
                base_frame_label2.config(highlightbackground="dark orange", highlightcolor = "dark orange", highlightthickness=2)



            elif self.cVar1.get() == 2:
                self.new_window(root2, parent, System_Step1_sub)


            elif self.cVar1.get() < 1:
                messagebox.showinfo("Error", "Nothing was checked")
                root.attributes('-topmost', 1)
                root.attributes('-topmost', 0)

        action1 = tk.Button(sub_frame0, text="Set", padx=25, command = set_sys_attribute)
        action1.grid(row=2, column=2, padx= (20,10 ))

        # Sys info (center-left-up)
        sys_info_frame1 = LabelFrame(center ,text="Systems in event log", font=("Consolas", 10, 'bold'),
                                     fg="white", bg='gray1', bd=3, padx=12 ,width=385 ,height=245, pady=7)
        sys_info_frame1.grid(row=0, column=0, sticky = 'nws', padx=10, pady=7)

        System_Step1.mylist1= Text(sys_info_frame1, width=75 ,height=13, wrap=NONE)
        vscroll1= Scrollbar(sys_info_frame1, orient=VERTICAL ,command=System_Step1.mylist1.yview)
        vscroll1.place(in_=System_Step1.mylist1, relx=1.0, relheight=1.0, bordermode="outside")
        System_Step1.mylist1['yscroll'] = vscroll1.set

        hscroll1= Scrollbar(sys_info_frame1, orient=HORIZONTAL ,command=System_Step1.mylist1.xview)
        hscroll1.place(in_=System_Step1.mylist1, rely=1.0, relwidth=1.0, bordermode="outside")
        System_Step1.mylist1['xscroll'] = hscroll1.set
        System_Step1.mylist1.grid(row=0, column=0, padx=(10,20), pady=(10,30))

        pd.set_option('display.width' ,1000)
        pd.options.display.max_colwidth = 200
        df1= pd.DataFrame(index=[0], columns=['System','Frequency',  'Activities'])
        System_Step1.mylist1.insert(tk.CURRENT, df1.to_string(index=False))

        # Sys info (center-left-down)
        sys_info_frame2 = LabelFrame(center ,text="Log of system malfunctioning", font=("Consolas", 10, 'bold'),
                                     fg="white", bg='gray1', bd=3, padx=12 ,width=385 ,height=262, pady=7)
        sys_info_frame2.grid(row=1, column=0, sticky = 'nws', padx=10, pady=7)

        System_Step1.mylist2= Text(sys_info_frame2, width=75 ,height=14, wrap=NONE)
        vscroll2= Scrollbar(sys_info_frame2, orient=VERTICAL ,command=System_Step1.mylist2.yview)
        vscroll2.place(in_=System_Step1.mylist2, relx=1.0, relheight=1.0, bordermode="outside")
        System_Step1.mylist2['yscroll'] = vscroll2.set

        hscroll2= Scrollbar(sys_info_frame2, orient=HORIZONTAL ,command=System_Step1.mylist2.xview)
        hscroll2.place(in_=System_Step1.mylist2, rely=1.0, relwidth=1.0, bordermode="outside")
        System_Step1.mylist2['xscroll'] = hscroll2.set
        System_Step1.mylist2.grid(row=0, column=0, padx=(10,20), pady=(10,30))

        pd.set_option('display.width' ,1000)
        pd.options.display.max_colwidth = 200
        df2= pd.DataFrame(index=[0], columns=['Event:system malfunctioning','Start_Timestamp'])
        System_Step1.mylist2.insert(tk.CURRENT, df2.to_string(index=False))

        # choose parameters (center-right)
        base_frame_label2 = LabelFrame(center ,text=" (B) Simulate Poisson Process ", font=("Consolas", 10, 'bold'),
                                       fg="white", bg='gray1', bd=3, padx=14, pady=7)
        base_frame_label2.grid(row=0, rowspan=2, column=1, sticky = 'nwse', padx=10, pady=7)
        System_Step1.base_frame_label2 = base_frame_label2

        # image for explaining poisson process (center-right)

        os.chdir(os.sep.join([str(self.org_path), "utils"]))
        image_frame= Frame(base_frame_label2, bg='gray1')
        image_frame.grid(row=5, column=0 ,columnspan=3, pady=(60 ,10))
        image1 = PhotoImage(file= "test4.GIF")      #stochastical process (poisson)
        smaller_image1 = image1.subsample(2, 2)

        panel = Label(image_frame, image = smaller_image1)
        panel.photo = smaller_image1
        panel.grid(row=0 ,column=0)

        s = ttk.Style()
        s.configure('Red.TCheckbutton', foreground="aquamarine" ,background='gray1')

        # input poisson parameter (center-right)

        # Set seed (center-right)
        seed_frame1 = Frame(base_frame_label2, bg='gray30', relief='ridge', borderwidth=2, width=15)
        seed_frame1.grid(row=0, column=0, padx=(15, 3), pady=(5, 5), stick='w')
        seed_Label = Label(seed_frame1, text="(Optional) Seed = ",
                           fg="white", bg='gray30', anchor="w")
        seed_Label.grid(row=0, column=0, sticky='w')
        seed_frame1_sub = Frame(seed_frame1, bg='gray30')
        seed_frame1_sub.grid(row=0, column=1, stick='w')
        seedBox1 = Text(seed_frame1_sub, height=1, width=4)
        seedBox1.grid(row=0, column=0, padx=(0, 5))
        seedBox1.configure(state="normal", background="white")

        fixed = Label(base_frame_label2, text="(1) Average interval of 'start_timestamp' between system malfunctioning events",
                      font=("Consolas", 10, 'bold'), fg="white", bg='gray1', anchor="w", width=80)
        fixed.grid(row=1, column=0, sticky='w', padx=(0,5))

        sub_frame1 = Frame(base_frame_label2, bg='gray1', width= 300, height= 100)
        sub_frame1.grid(row=2, column=0, stick='w', pady= (5,5))

        empty_label1 = Label(sub_frame1, text=' ', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1' ,anchor="w")
        empty_label1.grid(row=0, column=0)

        sub_frame1_label1 = Label(sub_frame1, text=' -1/\u03BB (days) = ', font=("Consolas", 10, 'bold'),
                                  fg="aquamarine", bg='gray1' ,anchor="w")
        sub_frame1_label1.grid(row=0, column=1, sticky="w", padx=(0 ,1))

        textBox1 =Text(sub_frame1, height=1, width=5)
        textBox1.grid(row=0, column=2, padx=(0,30))
        textBox1.configure(state="normal", background="white")


        fixed2 = Label(base_frame_label2, text="(2) Max/Min duration of system malfunctioning to set 'finish_timestamp'",
                      font=("Consolas", 10, 'bold'), fg="white", bg='gray1', anchor="w", width=80)
        fixed2.grid(row=3, column=0, sticky='w', padx=(0,5))

        sub_frame3 = Frame(base_frame_label2, bg='gray1', width= 300, height= 100)
        sub_frame3.grid(row=4, column=0, stick='w', pady= (5,5))

        empty_label2 = Label(sub_frame3, text=' ', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1' ,anchor="w")
        empty_label2.grid(row=0, column=0)

        sub_frame1_label2 = Label(sub_frame3, text=' -a (minimum hours) = ', font=("Consolas", 10, 'bold'),
                                  fg="aquamarine", bg='gray1' ,anchor="w")
        sub_frame1_label2.grid(row=0, column=1, sticky="w", padx=(0 ,1))

        textBox2 =Text(sub_frame3, height=1, width=5)
        textBox2.grid(row=0, column=2, padx=(0,3))
        textBox2.configure(state="normal", background="white")


        sub_frame1_label3 = Label(sub_frame3, text=', b (maximum hours) = ', font=("Consolas", 10, 'bold'),
                                  fg="aquamarine", bg='gray1' ,anchor="w")
        sub_frame1_label3.grid(row=0, column=3, sticky="w", padx=(0 ,1))

        textBox3 =Text(sub_frame3, height=1, width=5)
        textBox3.grid(row=0, column=4, padx=(0,30))
        textBox3.configure(state="normal", background="white")

        empty_label3 = Label(sub_frame3, text=' ', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1' ,anchor="w")



        empty_label3.grid(row=1, column=0, pady=(5,0))



        # Simulate Poisson Process
        def PoissonProcess():
            if seedBox1.get("1.0", "end-1c") != '':
                seed_value = int(seedBox1.get("1.0", "end-1c"))
                numpy.random.seed(seed_value)
            unixtime = self.extracted_data['unixtime']
            mintime= min(unixtime)
            maxtime= max(unixtime)
            lamb = int(textBox1.get("1.0", "end-1c"))
            Abnorm_sys.lamb = lamb
            sl = self.systemlist2['System']
            df3 = pd.DataFrame( columns=['Event:system malfunctioning', 'Start_Timestamp_Unix','Start_Timestamp',
                                         'Finish_Timestamp_Unix','Finish_Timestamp'])
            for i in sl:
                t = mintime
                cat1= pd.DataFrame()
                Start_Timestamp_Unix=[]
                while t<maxtime:
                    t = t+numpy.random.exponential(lamb, 1)*86400   #86400: To match time unit as second
                    Start_Timestamp_Unix.append(float(t))
                cat1['Event:system malfunctioning'] = list(numpy.repeat(i, len(Start_Timestamp_Unix)))
                cat1['Start_Timestamp_Unix'] = Start_Timestamp_Unix
                Start_Timestamp = cat1['Start_Timestamp_Unix'].apply(lambda x: datetime.datetime.utcfromtimestamp(x))
                cat1['Start_Timestamp'] = Start_Timestamp
                a = float(textBox2.get("1.0", "end-1c"))*3600
                b = float(textBox3.get("1.0", "end-1c"))*3600

                cat1['Finish_Timestamp_Unix'] = Start_Timestamp_Unix + numpy.random.uniform(a, b, 1)
                Finish_Timestamp = cat1['Finish_Timestamp_Unix'].apply(lambda x: datetime.datetime.utcfromtimestamp(x))
                cat1['Finish_Timestamp'] = Finish_Timestamp
                cat1 = cat1[cat1['Finish_Timestamp_Unix'] < maxtime]
                df3= df3.append(cat1, ignore_index = True)

            numpy.random.seed(0)
            df4= df3[['Event:system malfunctioning', 'Start_Timestamp','Finish_Timestamp']]
            Inject_Anomaly.system_down =df4     # malfunctioning
            PageThree.system_down =df4
            System_Step1.mylist2.delete('1.0', END)
            System_Step1.mylist2.insert(tk.CURRENT, df4[0:len(df4)].to_string(index=False))
            messagebox.showinfo("Message", "Finished Poisson Simulation")
            system_info_frame1.config(highlightbackground="gray1", highlightcolor = "gray1", highlightthickness=2)
            base_frame_label2.config(highlightbackground="gray1", highlightcolor = "gray1", highlightthickness=2)
            sys_info_frame2.config(highlightbackground="dark orange", highlightcolor = "dark orange", highlightthickness=2)

            root.attributes('-topmost', 1)
            root.attributes('-topmost', 0)

        action2 = tk.Button(base_frame_label2, text="Apply", width=10, command= PoissonProcess)
        action2.grid(row=4, column=0, sticky='e', padx=(0,10))

        def next():
            root.destroy()
        action3 = tk.Button(center, text="Close", width=10, command= next)
        action3.grid(row=2, column=1, sticky='e', pady=10, padx=(0,10))

#############################################################################################

class System_Step1_sub(tk.Toplevel):    # resource- failure rate
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
            numpy.random.seed(1234)
            k=0
            for i in activitylist['Activity']:
                k+=1
                globals()['act{}_sys'.format(k)]['values'] = systemlist
                globals()['act{}_sys'.format(k)].current(numpy.random.randint(0,len(systemlist)))
            messagebox.showinfo("Message",
                                    "{} systems have been generated".format(n), parent= root)
            system_info_frame1.config(highlightbackground="gray1", highlightcolor="gray1",
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
            System_Step1.systemlist2 = systemlist2
            System_Step1.mylist1.delete('1.0', END)
            System_Step1.mylist1.insert(tk.CURRENT, systemlist2[0:len(systemlist2)].to_string(index=False))
            Inject_Anomaly.data_with_system = extracted_data4
            messagebox.showinfo("Message", "Successfully proceeded")
            System_Step1.system_info_frame1.config(highlightbackground="gray1", highlightcolor="gray1", highlightthickness=2)
            System_Step1.base_frame_label2.config(highlightbackground="dark orange", highlightcolor="dark orange",
                                     highlightthickness=2)
            root.destroy()
            self.root2.lift()


        action_sys1 = tk.Button(base_frame, text="Apply", width=10, command= lambda: attach_sys(activitylist))
        action_sys1.grid(row=3, column=0, sticky = 'e', padx= (0,20), pady=10)