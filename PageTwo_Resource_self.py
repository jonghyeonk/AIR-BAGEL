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
from abnormal_patterns_sys import Abnorm_sys
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
        self.root.geometry("715x450")
        self.root.resizable(False, False)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root["bg"] = 'dark slate gray'
        self.root['padx'] = 5
        self.root['pady'] = 5
        root2 = root
        Resource_step1_self.root= root
        # Create main containers
        base_frame = Frame(root, bg='gray1', width=250, height=200)
        base_frame.grid(row=0, column=0, pady=(0, 7), sticky="nsew")

        # title label (top)
        base_frame_label1 = Label(base_frame, text='Connection between Resource & Activity',
                                  font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray25', anchor="center", relief="raised")
        base_frame_label1.grid(row=0, column=0, sticky="w")
        base_frame_label1.config(width=100)

        # Resource info (center-top)

        # Reference to represent the number of activity  (center-top)
        global activitylist
        params = {
            'Case': 'count'
        }
        activitylist = self.extracted_data.groupby('Activity').agg(params).reset_index()
        resource_info_frame1 = LabelFrame(base_frame, text="The number of activities ={}".format(len(activitylist)),
                                        font=("Consolas", 10, 'bold'),
                                        fg="white", bg='gray1', bd=3, padx=12, width=700, height=310, pady=7)
        resource_info_frame1.place(x=10, y=30)

        # Select resource attribute (center-top)
        self.cVar1 = IntVar()
        s = ttk.Style()
        s.configure('Red.TCheckbutton', foreground="aquamarine", background='gray1')
        sub_frame0 = Frame(resource_info_frame1, bg='gray1', width=600)
        sub_frame0.grid(row=0, column=0, sticky='w')
        sub_frame0_label1 = ttk.Checkbutton(sub_frame0, text="Select a resource attribute from existing dataframe: ",
                                            variable=self.cVar1, width=8,
                                            onvalue=1, style='Red.TCheckbutton')
        sub_frame0_label1.grid(row=0, column=0, sticky="w", padx=(0, 1))
        sub_frame0_label1.config(width=55)

        resource_chosen = ttk.Combobox(sub_frame0, width=15, textvariable=tk.StringVar())
        resource_chosen.grid(row=0, column=1)
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
        sub_frame1 = Frame(resource_info_frame1, bg='gray1', width=700)
        sub_frame1.grid(row=1, column=0, sticky='w')

        sub_frame1_label1 = ttk.Checkbutton(sub_frame1, text='Generate an artificial resource attribute-', variable=self.cVar1,
                                            onvalue=2, style='Red.TCheckbutton')
        sub_frame1_label1.grid(row=0, column=0, pady=(3, 0), sticky="w")

        sub_frame2_label1_1 = Label(sub_frame1, text='the number of groups =', font=("Consolas", 10, 'bold'),
                                    fg="white", bg='gray1', anchor="w")
        sub_frame2_label1_1.grid(row=0, column=1, pady=(3, 0), sticky="w")

        textBox1 = Text(sub_frame1, height=1, width=4)
        textBox1.grid(row=0, column=2, pady=(3, 0), sticky="w")
        textBox1.configure(state="normal", background="white")


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
                resource_info_frame1.config(text="Resource list (n={})".format(len(self.resourcelist)))
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
                    globals()['res{}'.format(k)].config(width=25)
                    globals()['res{}_rate'.format(k)] = Text(Resource_step1_self.frame_buttons1, height=1, width=5)
                    globals()['res{}_rate'.format(k)].grid(row=k - 1, column=1)
                    globals()['res{}_rate'.format(k)].configure(state="normal", background="white")
                    globals()['res{}_rate'.format(k)].insert(END, "0.03")

                Resource_step1_self.frame_buttons1.update_idletasks()
                Resource_step1_self.canvas_failure.config(scrollregion=Resource_step1_self.canvas_failure.bbox("all"))
                Resource_step1_self.root.update()

            elif self.cVar1.get() == 2:
                Resource_self_sub.ngroup = textBox1.get("1.0", "end-1c")
                self.new_window(root2, parent, Resource_self_sub)
            elif self.cVar1.get() < 1:
                messagebox.showinfo("Button Clicked", "Nothing was checked")
                root.attributes('-topmost', 1)
                root.attributes('-topmost', 0)

        action1 = tk.Button(sub_frame1, text="Set", padx=20, command = set_res_attribute)
        action1.grid(row=0, column=3, padx=(50,0), pady=(10,0))


        # Res info (left)
        res_info_frame2 = LabelFrame(base_frame ,text="Resource list", font=("Consolas", 10, 'bold'),
                                     fg="white", bg='gray1', bd=3, padx=12 ,width=385 ,height=252, pady=7)
        res_info_frame2.place(x=10 ,y=130)
        Resource_step1_self.res_info_frame2 = res_info_frame2

        mylist1= Text(res_info_frame2, width=45 ,height=13, wrap=NONE)
        vscroll1= Scrollbar(res_info_frame2, orient=VERTICAL ,command=mylist1.yview)
        vscroll1.place(in_=mylist1, relx=1.0, relheight=1.0, bordermode="outside")
        mylist1['yscroll'] = vscroll1.set

        hscroll1= Scrollbar(res_info_frame2, orient=HORIZONTAL ,command=mylist1.xview)
        hscroll1.place(in_=mylist1, rely=1.0, relwidth=1.0, bordermode="outside")
        mylist1['xscroll'] = hscroll1.set
        mylist1.place(x=10 ,y=10)
        Resource_step1_self.mylist1 = mylist1

        pd.set_option('display.width' ,1000)
        pd.options.display.max_colwidth = 200

        # Resource failure rate (right)
        base_frame_label1 = LabelFrame(base_frame, text="Set failure rate for each resource",
                                       font=("Consolas", 10, 'bold'),
                                       fg="white", bg='gray1', bd=3, padx=14, pady=7, width=385 ,height=245)
        base_frame_label1.place(x=410, y=130)
        sub_frame2 = Frame(base_frame_label1, bg='gray1')
        sub_frame2.grid(row=0, column=0, sticky='w')

        sub_frame2.rowconfigure(0, weight=1)
        sub_frame2.columnconfigure(0, weight=1)
        sub_frame2.grid_propagate(False)

        canvas_failure = Canvas(sub_frame2, bd=0, bg='gray1', highlightthickness=0)
        canvas_failure.grid(row=0, column=0, sticky="news")
        Resource_step1_self.frame_buttons1 = Frame(canvas_failure, bg='gray1')
        sub_frame2.config(width=250, height=220)
        vsb1 = tk.Scrollbar(sub_frame2, orient="vertical", command=canvas_failure.yview)
        vsb1.grid(row=0, column=1, sticky='ns')
        Resource_step1_self.canvas_failure = canvas_failure
        canvas_failure.configure(yscrollcommand=vsb1.set)
        canvas_failure.create_window((0, 0), window=Resource_step1_self.frame_buttons1, anchor='nw')

        # Set seed
        seed_frame1 = Frame(base_frame, bg='gray30', relief = 'ridge', borderwidth = 2, width=15)
        seed_frame1.place(x=440, y=395)
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
            messagebox.showinfo("Button Clicked2", "Completed: parameters on resource root have been defined")
            root.destroy()

        action3 = tk.Button(base_frame, text="Apply", padx=20, command=passfail)
        action3.place(x=600, y=395)







#############################################################################################

class Resource_self_sub(tk.Toplevel):    # resource- failure rate
    def __init__(self, root, root2  ,*args, **kwargs):
        self.root2= root2
        self.root = root
        self.root.geometry("721x396")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root["bg"] = 'dark slate gray'
        self.root['padx' ] =5
        self.root['pady' ] =5

        # Create main containers
        base_frame = Frame(root, bg='gray1')
        base_frame.grid(row=0, column=0, pady=(0, 7), sticky="nsew")

        # title label (top)
        base_frame_label1 = Label(base_frame, text='Connection between Resource group & Activity', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray25' ,anchor="center", relief="raised")
        base_frame_label1.grid(row=0, column=0, columnspan =2 , pady= (0,14), sticky="w")
        base_frame_label1.config(width=100)

        # System info (center-top)

        # Reference to represent the number of activity  (center-top)
        global activitylist
        params = {
            'Case': 'count'
        }
        activitylist = self.extracted_data.groupby('Activity').agg(params).reset_index()
        resource_info_frame1 = LabelFrame(base_frame, text="The number of groups ={}".format(self.ngroup), font=("Consolas", 10, 'bold'),
                                          fg="white", bg='gray1', bd=3, padx=12 , pady=7)
        resource_info_frame1.grid(row=1, column=0)

        #
        sub_frame2 = Frame(resource_info_frame1, bg='gray1')
        sub_frame2.grid(row=0, column=0, sticky='w')

        sub_frame2.rowconfigure(0, weight=1)
        sub_frame2.columnconfigure(0, weight=1)
        sub_frame2.grid_propagate(False)

        canvas1 = Canvas(sub_frame2, bd=0, bg='gray1', highlightthickness=0)
        canvas1.grid(row=0, column=0, sticky="news")
        vsb = tk.Scrollbar(sub_frame2, orient="vertical", command=canvas1.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas1.configure(yscrollcommand=vsb.set)

        frame_buttons1 = Frame(canvas1, bg='gray1')
        canvas1.create_window((0, 0), window=frame_buttons1, anchor='nw')

        k=0
        for i in range(0, int(self.ngroup)):
            k += 1
            globals()['grp{}'.format(k)] = Label(frame_buttons1, text='Size: Resource_Group{} = '.format(i), font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1' ,anchor="w")
            globals()['grp{}'.format(k)].grid(row= k-1, column= 0)
            globals()['grp{}'.format(k)].config(width=26)
            globals()['grp{}_size'.format(k)] = Text(frame_buttons1, height=1, width=5)
            globals()['grp{}_size'.format(k)].grid(row= k-1, column= 1)
            globals()['grp{}_size'.format(k)].configure(state="normal", background="white")
            globals()['grp{}_size'.format(k)].insert(END,"3")
        sub_frame2.config(width=270, height=270)
        canvas1.config(scrollregion=canvas1.bbox("all"))
        frame_buttons1.update_idletasks()


        # Resource group - activity connection (Right)
        base_frame_label2 = LabelFrame(base_frame, text="Allocate resource groups on each activity", font=("Consolas", 10, 'bold'),
                                       fg="white", bg='gray1', bd=3, padx=14, pady=7)
        base_frame_label2.grid(row=1, column=1)

        sub_frame3 =Frame(base_frame_label2, bg='gray1')
        sub_frame3.grid(row=0, column=0, sticky='w')

        sub_frame3.rowconfigure(0, weight=1)
        sub_frame3.columnconfigure(0, weight=1)
        sub_frame3.grid_propagate(False)

        canvas = Canvas(sub_frame3, bd=0, bg='gray1', highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="news")
        vsb = tk.Scrollbar(sub_frame3, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        frame_buttons2 = Frame(canvas, bg='gray1')
        canvas.create_window((0, 0), window=frame_buttons2, anchor='nw')

        k=0
        for i in activitylist['Activity']:
            k += 1
            globals()['act{}'.format(k)] = Label(frame_buttons2, text='{} = '.format(i), font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1' ,anchor="w")
            globals()['act{}'.format(k)].grid(row= k-1, column= 0)
            globals()['act{}'.format(k)].config(width=30)
            globals()['dist2{}'.format(k)] = tk.StringVar()
            globals()['act{}_grp'.format(k)] = ttk.Combobox(frame_buttons2, width=14, textvariable=['dist2{}'.format(k)])
            globals()['act{}_grp'.format(k)].grid(row= k-1, column= 1)
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
                globals()['res{}'.format(k)].config(width=25)
                globals()['res{}_rate'.format(k)] = Text(Resource_step1_self.frame_buttons1, height=1, width=5)
                globals()['res{}_rate'.format(k)].grid(row= k-1, column= 1)
                globals()['res{}_rate'.format(k)].configure(state="normal", background="white")
                globals()['res{}_rate'.format(k)].insert(END,"0.03")

            Resource_step1_self.frame_buttons1.update_idletasks()
            Resource_step1_self.res_info_frame2.update_idletasks()
            Resource_step1_self.canvas_failure.config(scrollregion=Resource_step1_self.canvas_failure.bbox("all"))

            Resource_step1_self.root.update()
            Inject_Anomaly.data_with_resource = extracted_data4
            messagebox.showinfo("Successfully proceeded", "Successfully proceeded")
            root.destroy()
            self.root2.lift()

        action_res1 = tk.Button(base_frame, text="Apply", padx=25, command= lambda: attach_res(activitylist))
        action_res1.place(x=600, y=344)
