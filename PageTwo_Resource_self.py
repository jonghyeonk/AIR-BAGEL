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

# Pages
from PageTwo_Inject_Anomaly import Inject_Anomaly
from PageThree import PageThree


class Resource_step1_self(tk.Toplevel):

    def new_window(self, root2, parent, Win_class):
        global Resource_self_sub
        Resource_self_sub.extracted_data = self.extracted_data
        Resource_self_sub = tk.Toplevel(parent)
        Resource_self_sub.root2 = root2
        Win_class(Resource_self_sub, root2)


    def __init__(self, root, parent, *args, **kwargs):
        self.root = root
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root["bg"] = 'dark slate gray'
        self.root['padx'] = 5
        self.root['pady'] = 5
        root2 = root
        Resource_step1_self.root= root
        # Create main containers
        base_frame = Frame(root, bg='gray1')
        base_frame.grid(row=0, column=0,  sticky="nsew")
        base_frame.grid_rowconfigure(1, weight=1)
        base_frame.grid_columnconfigure(0, weight=1)

        center = Frame(root, bg='gray1')
        center.grid(row=1, column=0, sticky="nsew")

        # title label (top)
        base_frame_label1 = Label(base_frame, text='Connection between Resource & Activity',
                                  font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray25', anchor="center", relief="raised")
        base_frame_label1.grid(row=0, column=0, columnspan=3,sticky="nsew")


        # Resource info (center-top)

        # Reference to represent the number of activity  (center-top)
        global activitylist
        params = {
            'Case': 'count'
        }
        activitylist = self.extracted_data.groupby('Activity').agg(params).reset_index()
        resource_info_frame1 = LabelFrame(base_frame, text="(A) Set resource attribute",
                                        font=("Consolas", 10, 'bold'),
                                        fg="white", bg='gray1', bd=3)
        resource_info_frame1.config(highlightbackground="dark orange", highlightcolor = "dark orange", highlightthickness=2)

        resource_info_frame1.grid(row=1, column=0, sticky="nw", padx=10, pady=7)
        Resource_step1_self.resource_info_frame1 = resource_info_frame1
        # Select resource attribute (center-top)
        self.cVar1 = IntVar()
        s = ttk.Style()
        s.configure('Red.TCheckbutton', foreground="aquamarine", background='gray1')
        s.map('Red.TCheckbutton', background=[('active', 'gray1')])

        sub_frame0 = Frame(resource_info_frame1, bg='gray1')
        sub_frame0.grid(row=0, column=0, pady=(0,3), sticky='w')
        sub_frame0_label1 = ttk.Checkbutton(sub_frame0, text="Select a resource attribute from existing dataframe: ",
                                            variable=self.cVar1,
                                            onvalue=1, style='Red.TCheckbutton')
        sub_frame0_label1.grid(row=0, column=0, sticky="w", padx=(0, 1))

        resource_chosen = ttk.Combobox(sub_frame0, width=16, textvariable=tk.StringVar())
        resource_chosen.grid(row=0, column=1, padx=(0,10))
        resource_chosen['values'] = list(self.event_log)  # original data without any preprocessing

        # Auto detection of resource
        resource_candidate = [list(self.event_log).index(i) for i in list(self.event_log)
                              if "resource" in i or "Resource" in i or "RESOURCE" in i]
        if len(resource_candidate) == 0:
            pass
        if len(resource_candidate) == 1:
            resource_chosen.current(resource_candidate)
        if len(resource_candidate) > 1:
            resource_chosen.current(resource_candidate[0])

        # Input the number of resources  (center-top)
        # sub_frame1 = Frame(resource_info_frame1, bg='gray1', width=700)
        sub_frame1 = Frame(resource_info_frame1, bg='gray1')
        sub_frame1.grid(row=1, column=0, sticky='w')

        sub_frame1_label1 = ttk.Checkbutton(sub_frame1, text='Generate an artificial resource attribute-', variable=self.cVar1,
                                            onvalue=2, style='Red.TCheckbutton')
        sub_frame1_label1.grid(row=0, column=0, pady=(3, 0), sticky="w")

        sub_frame2_label1_1 = Label(sub_frame1, text='the number of groups =', font=("Consolas", 10, 'bold'),
                                    fg="white", bg='gray1', anchor="w")
        sub_frame2_label1_1.grid(row=0, column=1, pady=(4, 0), padx=2)

        textBox1 = Text(sub_frame1, height=1, width=4)
        textBox1.grid(row=0, column=2, padx=(0,10) ,pady=(4,0))
        textBox1.configure(state="normal", background="white")

        def iserror(func, *args):
            try:
                func(*args)
                return False
            except Exception:
                return True

        def set_res_attribute():
            if self.cVar1.get() == 1:
                selected_resource = resource_chosen.get()
                dat_resource = self.firstpreprocess
                dat_resource["Resource"] = self.event_log[selected_resource]
                dat_resource = dat_resource.sort_values(["Case", "Timestamp"],
                                                            ascending=[True, True])
                params = {
                    'Case': 'count',
                    'Activity': lambda x: ','.join(sorted(pd.Series.unique(x)))
                }
                resourcelist = dat_resource.groupby('Resource').agg(params).reset_index()
                resourcelist.columns = ["Resource", "Frequency", "Activities"]
                resourcelist['Resource_failure_rate'] = 0
                resourcelist = resourcelist.sort_values(["Frequency"], ascending=False)
                cols = ["Resource", "Frequency", "Activities"]
                resourcelist = resourcelist[cols]
                resourcelist = resourcelist.reset_index(drop=True)
                self.resourcelist= resourcelist
                resource_info_frame1.config(text="(A) Set resource attribute")
                mylist1.insert(tk.CURRENT, pd.DataFrame(resourcelist).to_string(index=False))    # Data with Resource ID - Workload - Failure rate
                extracted_data2 = self.extracted_data
                extracted_data2["Resource"] = dat_resource["Resource"]
                self.extracted_data2= extracted_data2
                PageThree.before = extracted_data2

                k = 0
                for i in resourcelist["Resource"]:
                    k += 1
                    globals()['res{}'.format(k)] = Label(Resource_step1_self.frame_buttons1, text='{} = '.format(i),
                                                         font=("Consolas", 10, 'bold'),
                                                         fg="white", bg='gray1', anchor="w")
                    globals()['res{}'.format(k)].grid(row=k - 1, column=0)
                    globals()['res{}_rate'.format(k)] = Text(Resource_step1_self.frame_buttons1, height=1, width=7)
                    globals()['res{}_rate'.format(k)].grid(row=k - 1, column=1, padx=(0,3))
                    globals()['res{}_rate'.format(k)].configure(state="normal", background="white")
                    globals()['res{}_rate'.format(k)].insert(END, "0.03")

                Resource_step1_self.frame_buttons1.update_idletasks()
                Resource_step1_self.canvas_failure.config(scrollregion=Resource_step1_self.canvas_failure.bbox("all"))
                Resource_step1_self.root.update()
                resource_info_frame1.config(highlightbackground="gray1", highlightcolor = "gray1", highlightthickness=2)
                base_frame_label1.config(highlightbackground="dark orange", highlightcolor = "dark orange", highlightthickness=2)

            elif self.cVar1.get() == 2:
                if iserror(int, textBox1.get("1.0", "end-1c")):
                    messagebox.showinfo("Error", "Input integer in number of resource groups!")
                elif int(textBox1.get("1.0", "end-1c"))>0:
                    Resource_self_sub.ngroup = textBox1.get("1.0", "end-1c")
                    self.new_window(root2, parent, Resource_self_sub)

                else:
                    messagebox.showinfo("Error", "Input number of resource groups over than 0!")
            elif self.cVar1.get() < 1:
                messagebox.showinfo("Error", "Nothing was checked")
                root.attributes('-topmost', 1)
                root.attributes('-topmost', 0)

        action1 = tk.Button(resource_info_frame1, text="Set", width=8, command = set_res_attribute)
        action1.grid(row=2, column=0, padx=(0,10), pady=8, sticky='e')


        # Res info (left)
        res_info_frame2 = LabelFrame(center ,text="Resources in event log", font=("Consolas", 10, 'bold'),
                                     fg="white", bg='gray1', bd=3)
        res_info_frame2.grid(row=0, column=0, sticky = 'nws', padx=10, pady=7)
        Resource_step1_self.res_info_frame2 = res_info_frame2

        mylist1= Text(res_info_frame2, width=45 ,height=14, wrap=NONE)
        vscroll1= Scrollbar(res_info_frame2, orient=VERTICAL ,command=mylist1.yview)
        vscroll1.place(in_=mylist1, relx=1.0, relheight=1.0, bordermode="outside")
        mylist1['yscroll'] = vscroll1.set

        hscroll1= Scrollbar(res_info_frame2, orient=HORIZONTAL ,command=mylist1.xview)
        hscroll1.place(in_=mylist1, rely=1.0, relwidth=1.0, bordermode="outside")
        mylist1['xscroll'] = hscroll1.set
        mylist1.grid(row=0, column=0, padx=(10,20), pady=(10,30))
        Resource_step1_self.mylist1 = mylist1

        pd.set_option('display.width' ,1000)
        pd.options.display.max_colwidth = 200

        # Resource failure rate (right)
        base_frame_label1 = LabelFrame(center, text="(B) Set failure rate",
                                       font=("Consolas", 10, 'bold'),
                                       fg="white", bg='gray1', bd=3)
        base_frame_label1.grid(row=0, column=1, sticky= 'nws',padx=10, pady=7)
        Resource_step1_self.base_frame_label1 = base_frame_label1

        sub_frame2 = Frame(base_frame_label1, bg='gray1')
        sub_frame2.grid(row=0, column=0, padx=10, stick='nswe' )

        sub_frame2.rowconfigure(0, weight=1)
        sub_frame2.columnconfigure(0, weight=1)
        sub_frame2.grid_propagate(False)
        sub_frame2.config(width=250, height=270)

        canvas_failure = Canvas(sub_frame2, bd=0, bg='gray1', highlightthickness=0)
        canvas_failure.grid(row=0, column=0, sticky="ns")
        Resource_step1_self.frame_buttons1 = Frame(canvas_failure, bg='gray1')
        vsb1 = tk.Scrollbar(sub_frame2, orient="vertical", command=canvas_failure.yview)
        vsb1.grid(row=0, column=1, padx=(2,0), sticky='ns')
        Resource_step1_self.canvas_failure = canvas_failure

        canvas_failure.configure(yscrollcommand=vsb1.set)
        canvas_failure.create_window((0, 0), window=Resource_step1_self.frame_buttons1, anchor='nw')

        # Set seed
        seed_frame1 = Frame(center, bg='gray30', relief = 'ridge', borderwidth = 2, width=15)
        seed_frame1.grid(row=1, column=1, sticky='e', padx=(0,10))
        seed_Label = Label(seed_frame1, text="(Optional) Seed = ",
                                fg="white", bg='gray30', anchor="w")
        seed_Label.grid(row=0, column=0, sticky='w')
        seed_frame1_sub = Frame(seed_frame1, bg='gray30')
        seed_frame1_sub.grid(row=0, column=1, stick='w')
        seedBox1 =Text(seed_frame1_sub, height=1, width=4)
        seedBox1.grid(row= 0, column=0,padx=(0,5))
        seedBox1.configure(state="normal", background="white")

        # apply pass/fail (right)
        def passfail():
            extracted_data2 = self.extracted_data2
            resourcelist2 = self.resourcelist
            ratelist= list()
            k=0
            for i in resourcelist2["Resource"]:
                k+=1
                ratelist.append(float(globals()['res{}_rate'.format(k)].get("1.0", "end-1c")))

            resourcelist2["Resource_failure_rate"] = ratelist
            resourcelist3 = resourcelist2[["Resource", "Resource_failure_rate"]]
            extracted_data2 = pd.merge(extracted_data2, resourcelist3, on="Resource")
            if seedBox1.get("1.0", "end-1c") != '':
                seed_value = int(seedBox1.get("1.0", "end-1c"))
                numpy.random.seed(seed_value)
            PF = numpy.random.binomial(numpy.repeat(1, len(extracted_data2)), extracted_data2["Resource_failure_rate"])
            numpy.random.seed(0)
            extracted_data2['Resource_Pass/Fail'] = PF
            extracted_data3 = extracted_data2
            Inject_Anomaly.extracted_data2 = extracted_data3    # Dataset with resource anomaly
            messagebox.showinfo("Message", "Completed: parameters on resource root have been defined")
            root.destroy()

        action3 = tk.Button(center, text="Apply", width=10, command=passfail)
        action3.grid(row=2, column=1, sticky='e', padx=(0,10), pady=10)







#############################################################################################

class Resource_self_sub(tk.Toplevel):    # resource- failure rate
    def __init__(self, root, root2  ,*args, **kwargs):
        self.root2= root2
        self.root = root
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root["bg"] = 'dark slate gray'
        self.root['padx' ] =5
        self.root['pady' ] =5

        # Create main containers
        base_frame = Frame(root, bg='gray1')
        base_frame.grid(row=0, column=0, sticky="nsew")
        base_frame.grid_rowconfigure(1, weight=1)
        base_frame.grid_columnconfigure(0, weight=1)
        # title label (top)
        base_frame_label1 = Label(base_frame, text='Connection between Resource group & Activity', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray25' ,relief="raised")
        base_frame_label1.grid(row=0, column=0 , columnspan =2, sticky="nsew")
        base_frame_label1.grid_rowconfigure(1, weight=1)
        base_frame_label1.grid_columnconfigure(0, weight=1)

        # System info (center-top)

        # Reference to represent the number of activity  (center-top)
        global activitylist
        params = {
            'Case': 'count'
        }
        activitylist = self.extracted_data.groupby('Activity').agg(params).reset_index()
        resource_info_frame1 = LabelFrame(base_frame, text="The number of groups ={}".format(self.ngroup), font=("Consolas", 10, 'bold'),
                                          fg="white", bg='gray1', bd=3)
        resource_info_frame1.grid(row=1, column=0, sticky='nsw', padx=(10,0))

        #
        sub_frame2 = Frame(resource_info_frame1, bg='gray1')
        sub_frame2.grid(row=0, column=0, sticky='nsw', padx=10,pady=10)

        sub_frame2.rowconfigure(0, weight=1)
        sub_frame2.columnconfigure(0, weight=1)
        sub_frame2.grid_propagate(False)

        canvas1 = Canvas(sub_frame2, bd=0, bg='gray1', highlightthickness=0)
        canvas1.grid(row=0, column=0, sticky="news")
        vsb = tk.Scrollbar(sub_frame2, orient="vertical", command=canvas1.yview)
        vsb.grid(row=0, column=1, sticky='nse')
        canvas1.configure(yscrollcommand=vsb.set)

        frame_buttons1 = Frame(canvas1, bg='gray1')
        canvas1.create_window((0, 0), window=frame_buttons1, anchor='nw')

        k=0
        for i in range(0, int(self.ngroup)):
            k += 1
            globals()['grp{}'.format(k)] = Label(frame_buttons1, text='Size: Resource_Group{} = '.format(i), font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1' ,anchor="w")
            globals()['grp{}'.format(k)].grid(row= k-1, column= 0)
            globals()['grp{}_size'.format(k)] = Text(frame_buttons1, height=1, width=5)
            globals()['grp{}_size'.format(k)].grid(row= k-1, column= 1)
            globals()['grp{}_size'.format(k)].configure(state="normal", background="white")
            globals()['grp{}_size'.format(k)].insert(END,"3")
        canvas1.config(scrollregion=canvas1.bbox("all"))
        sub_frame2.config(width=250, height=270)

        frame_buttons1.update_idletasks()


        # Resource group - activity connection (Right)
        base_frame_label2 = LabelFrame(base_frame, text="Allocate resource groups on each activity", font=("Consolas", 10, 'bold'),
                                       fg="white", bg='gray1', bd=3)
        base_frame_label2.grid(row=1, column=1, sticky='nwse',padx=10)

        sub_frame3 =Frame(base_frame_label2, bg='gray1')
        sub_frame3.grid(row=0, column=0, sticky='nws', padx=10,pady=10)

        sub_frame3.rowconfigure(0, weight=1)
        sub_frame3.columnconfigure(0, weight=1)
        sub_frame3.grid_propagate(False)

        canvas = Canvas(sub_frame3, bd=0, bg='gray1', highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="news")
        vsb = tk.Scrollbar(sub_frame3, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, padx=(2,0), sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        frame_buttons2 = Frame(canvas, bg='gray1')
        canvas.create_window((0, 0), window=frame_buttons2, anchor='nw')

        k=0
        for i in activitylist['Activity']:
            k += 1
            globals()['act{}'.format(k)] = Label(frame_buttons2, text='{} = '.format(i), font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1' ,anchor="w")
            globals()['act{}'.format(k)].grid(row= k-1, column= 0, sticky='w')
            globals()['dist2{}'.format(k)] = tk.StringVar()
            globals()['act{}_grp'.format(k)] = ttk.Combobox(frame_buttons2, width=16, textvariable=['dist2{}'.format(k)])
            globals()['act{}_grp'.format(k)].grid(row= k-1, column= 1, padx=(0,3))
            globals()['act{}_grp'.format(k)]['values']= list(["Resource_Group" + str(i) for i in range(0,int(self.ngroup))])
            globals()['act{}_grp'.format(k)].current(numpy.random.randint(0, int(self.ngroup) ) )

        frame_buttons2.update_idletasks()
        sub_frame3.config(width=360, height=270)
        canvas.config(scrollregion=canvas.bbox("all"))

        def attach_res(dat):
            k = 0
            rl=list(numpy.repeat("act",len(dat)))
            for i in dat['Activity']:
                k += 1
                rl[k-1] = globals()['act{}_grp'.format(k)].get()
            dat['Resource_Group'] = pd.DataFrame(rl)
            dat = dat[['Activity' , 'Resource_Group']]

            global extracted_data4
            extracted_data4 = pd.merge(self.extracted_data, dat, on="Activity")
            d = {'Resource_Group': ["Resource_Group" + str(i) for i in range(0, 10)],
                 'Resource_Group_Size': range(0, 10)}
            group_size = pd.DataFrame(data=d)
            extracted_data4 = pd.merge(extracted_data4, group_size , on="Resource_Group")
            attach = ["res_" + str(numpy.random.randint(0,int(i)+1)) for i in extracted_data4["Resource_Group_Size"]]
            extracted_data4["attach"] = attach
            extracted_data4["Resource"] = extracted_data4[['Resource_Group', 'attach']].apply(lambda x: "_".join(x) ,axis=1)
            params = {
                'Case': 'count',
                'Activity': lambda x: ','.join(sorted(pd.Series.unique(x)))
            }

            Resource_step1_self.extracted_data2 = extracted_data4
            PageThree.before = extracted_data4

            resourcelist2 = extracted_data4.groupby('Resource').agg(params).reset_index()
            resourcelist2.columns = ["Resource", "Frequency", "Activities"]
            resourcelist2 = resourcelist2.sort_values(["Frequency"], ascending=False)
            cols = ["Resource", "Frequency",  "Activities"]
            resourcelist2 = resourcelist2[cols]

            Resource_step1_self.resourcelist = resourcelist2
            Resource_step1_self.mylist1.delete('1.0', END)
            Resource_step1_self.mylist1.insert(tk.CURRENT, pd.DataFrame(resourcelist2[0:len(resourcelist2)]).to_string(index=False))

            k=0
            for i in resourcelist2["Resource"]:
                k+=1
                globals()['res{}'.format(k)] = Label(Resource_step1_self.frame_buttons1, text='{} = '.format(i), font=("Consolas", 10, 'bold'),
                                      fg="white", bg='gray1' ,anchor="w")
                globals()['res{}'.format(k)].grid(row= k-1, column= 0)
                globals()['res{}_rate'.format(k)] = Text(Resource_step1_self.frame_buttons1, height=1, width=7)
                globals()['res{}_rate'.format(k)].grid(row= k-1, column= 1, padx=(0,3))
                globals()['res{}_rate'.format(k)].configure(state="normal", background="white")
                globals()['res{}_rate'.format(k)].insert(END,"0.03")

            Resource_step1_self.frame_buttons1.update_idletasks()
            Resource_step1_self.res_info_frame2.update_idletasks()
            Resource_step1_self.canvas_failure.config(scrollregion=Resource_step1_self.canvas_failure.bbox("all"))

            Resource_step1_self.root.update()
            Inject_Anomaly.data_with_resource = extracted_data4
            messagebox.showinfo("Message", "Successfully proceeded")
            Resource_step1_self.resource_info_frame1.config(highlightbackground="gray1", highlightcolor="gray1",
                                        highlightthickness=2)
            Resource_step1_self.base_frame_label1.config(highlightbackground="dark orange", highlightcolor="dark orange",
                                     highlightthickness=2)
            root.destroy()
            self.root2.lift()

        action_res1 = tk.Button(base_frame, text="Apply", width=10, command= lambda: attach_res(activitylist))
        action_res1.grid(row=2, column=1, sticky = 'e', padx= (0,20), pady=10)