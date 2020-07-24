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

#Pages
from PageTwo_Inject_Anomaly import Inject_Anomaly
from PageThree import PageThree

class Resource_Step1(tk.Toplevel):    # resource- failure rate
    def new_window(self, root2, parent, Win_class):
        global Resource_Step1_sub
        Resource_Step1_sub = tk.Toplevel(parent)
        Resource_Step1_sub.root2 = root2
        Win_class(Resource_Step1_sub, root2)

    def __init__(self, root , parent, *args, **kwargs):
        self.root = root

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root["bg"] = 'dark slate gray'
        self.root['padx' ] =5
        self.root['pady' ] =5
        root2 = root
        Resource_Step1.root = root
        # Create main containers
        base_frame = Frame(root, bg='gray1' )
        base_frame.grid(row=0, column=0,  sticky="nsew")
        base_frame.grid_rowconfigure(1, weight=1)
        base_frame.grid_columnconfigure(0, weight=1)

        center = Frame(root, bg='gray1')
        center.grid(row=1, column=0, sticky="nsew")

        # title label (top)
        base_frame_label1 = Label(base_frame, text='Parameter setting on resource root', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray25' ,anchor="center", relief="raised")
        base_frame_label1.grid(row=0, column=0, sticky="nsew")


        # Set resource attribute (Center-top)
        system_info_frame1 = LabelFrame(base_frame, text="(A) Set resource attribute", font=("Consolas", 10, 'bold'),
                                          fg="white", bg='gray1', bd=3)
        system_info_frame1.config(highlightbackground="dark orange", highlightcolor = "dark orange", highlightthickness=2)

        system_info_frame1.grid(row=1, column=0, sticky="w", padx=5, pady=7)
        Resource_Step1.system_info_frame1=system_info_frame1
        self.cVar1 = IntVar()
        s = ttk.Style()
        s.configure('Red.TCheckbutton', foreground="aquamarine", background='gray1')

        sub_frame0 = Frame(system_info_frame1, bg='gray1', width=400)
        sub_frame0.grid(row=0, column=0, pady=(0,3), sticky='w')
        sub_frame0_label1 = ttk.Checkbutton(sub_frame0, text="Select a resource attribute from existing dataframe: ", variable=self.cVar1,
                                  onvalue=1, style='Red.TCheckbutton')
        sub_frame0_label1.grid(row=0, column=0, sticky="w", padx=(0 ,1))

        resource_chosen = ttk.Combobox(sub_frame0, width=15, textvariable=tk.StringVar())
        resource_chosen.grid(row=0, column=1)
        resource_chosen['values'] = list(self.event_log)  # original data without any preprocessing

        # Auto detection of Resource
        resource_candidate = [list(self.event_log).index(i) for i in list(self.event_log)
                          if "resource" in i or "Resource" in i or "RESOURCE" in i]
        if len(resource_candidate) == 0:
            pass
        if len(resource_candidate) == 1:
            resource_chosen.current(resource_candidate)
        if len(resource_candidate) > 1:
            resource_chosen.current(resource_candidate[0])

        sub_frame0_2 = Frame(system_info_frame1, bg='gray1', width=400)
        sub_frame0_2.grid(row=1, column=0, sticky='w')

        sub_frame0_label1 = ttk.Checkbutton(sub_frame0_2, text='Generate an artificial resource attribute ', variable=self.cVar1,
                                  onvalue=2, style='Red.TCheckbutton')
        sub_frame0_label1.grid(row=0, column=0, pady=(3, 0), sticky="w")

        sub_frame2_label2_1 = Label(sub_frame0_2, text='- the number of resource groups =', font=("Consolas", 10, 'bold'),
                                    fg="white", bg='gray1', anchor="w")
        sub_frame2_label2_1.grid(row=0, column=1, pady=(4, 0), padx=2)

        textBox0 = Text(sub_frame0_2, height=1, width=4)
        textBox0.grid(row=0, column=2, padx=(0,10) ,pady=(4,0))
        textBox0.configure(state="normal", background="white")

        self.cVar1.set(0)
        def iserror(func, *args):
            try:
                func(*args)
                return False
            except Exception:
                return True

        def set_res_attribute(extracted_data):
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
                cols = ["Resource", "Frequency", "Resource_failure_rate", "Activities"]
                resourcelist = resourcelist[cols]
                resourcelist = resourcelist.reset_index(drop=True)
                self.resourcelist= resourcelist
                resource_info_frame1.config(text="Resources in event log")
                mylist2.insert(tk.CURRENT, pd.DataFrame(resourcelist).to_string(index=False))    # Data with Resource ID - Workload - Failure rate
                extracted_data2 = extracted_data
                extracted_data2["Resource"] = dat_resource["Resource"]
                self.extracted_data2= extracted_data2
                PageThree.before = extracted_data2
                system_info_frame1.config(highlightbackground="gray1", highlightcolor = "gray1", highlightthickness=2)
                base_frame_label2.config(highlightbackground="dark orange", highlightcolor = "dark orange", highlightthickness=2)


            elif self.cVar1.get() == 2:
                if iserror(int, textBox0.get("1.0", "end-1c")):
                    messagebox.showinfo("Error", "Input integer in number of resource groups!")
                elif int(textBox0.get("1.0", "end-1c"))>0:
                    Resource_Step1_sub.ngroup = textBox0.get("1.0", "end-1c")
                    self.new_window(root2, parent, Resource_Step1_sub)

                else:
                    messagebox.showinfo("Error", "Input number of resource groups over than 0!")
            elif self.cVar1.get() < 1:
                messagebox.showinfo("Error", "Nothing was checked")
                root.attributes('-topmost', 1)
                root.attributes('-topmost', 0)

        action1 = tk.Button(system_info_frame1, text="Set", width=8, command = lambda: set_res_attribute(self.extracted_data))
        action1.grid(row=2, column=0, padx=(0,10), pady=8, sticky='e')


        # resource info (left)
        # resource_info_frame1 = LabelFrame(base_frame ,text="Resource list (n={})".format(len(self.resourcelist)), font=("Consolas", 10, 'bold'),
        #                                   fg="white", bg='gray1', bd=3, padx=12 ,width=385 ,height=340, pady=7)
        # resource_info_frame1.place(x=10 ,y=140)
        resource_info_frame1 = LabelFrame(center ,text="Resources in event log", font=("Consolas", 10, 'bold'),
                                          fg="white", bg='gray1', bd=3, padx=12 ,width=385 ,height=340, pady=7)
        resource_info_frame1.grid(row=0, column=0, sticky = 'nws', padx=5, pady=7)


        mylist2= Text(resource_info_frame1, width=45 ,height=22, wrap=NONE)
        vscroll2= Scrollbar(resource_info_frame1, orient=VERTICAL ,command=mylist2.yview)
        vscroll2.place(in_=mylist2, relx=1.0, relheight=1.0, bordermode="outside")
        mylist2['yscroll'] = vscroll2.set

        hscroll2= Scrollbar(resource_info_frame1, orient=HORIZONTAL ,command=mylist2.xview)
        hscroll2.place(in_=mylist2, rely=1.0, relwidth=1.0, bordermode="outside")
        mylist2['xscroll'] = hscroll2.set
        mylist2.grid(row=0, column=0, padx=(0,20), pady=(0,30))
        Resource_Step1.mylist2 = mylist2
        pd.set_option('display.width', 1000)
        pd.options.display.max_colwidth = 200

        # choose parameters (right)
        base_frame_label2 = LabelFrame(center ,text="(B) Sampling failure rate from chosen distribution ", font=("Consolas", 10, 'bold'),
                                       fg="white", bg='gray1', bd=3, padx=14, pady=7)
        base_frame_label2.grid(row=0, column=1, sticky= 'nw',padx=5, pady=7)
        Resource_Step1.base_frame_label2= base_frame_label2
        # Set seed
        seed_frame1 = Frame(base_frame_label2, bg='gray30', relief = 'ridge', borderwidth = 2, width=15)
        seed_frame1.grid(row=0, column=0, padx=(0,3), pady=(0,5),stick='w')
        seed_Label = Label(seed_frame1, text="(Optional) Seed = ",
                                fg="white", bg='gray30', anchor="w")
        seed_Label.grid(row=0, column=0, sticky='w')
        seed_frame1_sub = Frame(seed_frame1, bg='gray30')
        seed_frame1_sub.grid(row=0, column=1, stick='w')
        seedBox1 =Text(seed_frame1_sub, height=1, width=4)
        seedBox1.grid(row= 0, column=0,padx=(0,5))
        seedBox1.configure(state="normal", background="white")

        # images of statistical distributions (right)
        os.chdir(os.sep.join([str(self.org_path), "utils"]))

        image_frame= Frame(base_frame_label2, bg='gray1')
        image_frame.grid(row=5, column=0 ,columnspan=3, pady=(50 ,10))
        root.cVar2 = IntVar()
        root.cVar2.set(1)
        image1 = PhotoImage(file= "test1.gif")  #exponential pdf
        smaller_image1 = image1.subsample(2, 2)
        image2 = PhotoImage(file= "test2.gif")  #normal pdf
        smaller_image2 = image2.subsample(2, 2)
        image3 = PhotoImage(file= "test3.gif")  #uniform pdf
        smaller_image3 = image3.subsample(2, 2)

        def display_image(img):
            global panel
            panel = Label(image_frame, image = img)
            panel.photo = img
            panel.grid(row=0 ,column=0)

        def onoff():
            chnum =root.cVar2.get()
            panel.grid_remove()
            if chnum ==1:
                panel2.grid_remove()
                panel3.grid_remove()
                textBox1.configure(state="normal", background="white")
                panel1.grid(row=0 ,column=0)
                textBox2.configure(state="disabled", background="gray60")
                textBox3.configure(state="disabled", background="gray60")
                textBox4.configure(state="disabled", background="gray60")
                textBox5.configure(state="disabled", background="gray60")
            elif chnum == 11 :
                textBox1.configure(state="disabled", background="gray60")
                textBox2.configure(state="disabled", background="gray60")
                textBox3.configure(state="disabled", background="gray60")
                textBox4.configure(state="disabled", background="gray60")
                textBox5.configure(state="disabled", background="gray60")
            elif chnum==2:
                panel1.grid_remove()
                panel3.grid_remove()
                textBox2.configure(state="normal", background="white")
                textBox3.configure(state="normal", background="white")
                panel2.grid(row=0 ,column=0)
                textBox1.configure(state="disabled", background="gray60")
                textBox4.configure(state="disabled", background="gray60")
                textBox5.configure(state="disabled", background="gray60")
            elif chnum == 22 :
                textBox1.configure(state="disabled", background="gray60")
                textBox2.configure(state="disabled", background="gray60")
                textBox3.configure(state="disabled", background="gray60")
                textBox4.configure(state="disabled", background="gray60")
                textBox5.configure(state="disabled", background="gray60")
            elif chnum ==3:
                panel1.grid_remove()
                panel2.grid_remove()
                textBox4.configure(state="normal", background="white")
                textBox5.configure(state="normal", background="white")
                panel3.grid(row=0 ,column=0)
                textBox1.configure(state="disabled", background="gray60")
                textBox2.configure(state="disabled", background="gray60")
                textBox3.configure(state="disabled", background="gray60")
            elif chnum == 33 :
                textBox1.configure(state="disabled", background="gray60")
                textBox2.configure(state="disabled", background="gray60")
                textBox3.configure(state="disabled", background="gray60")
                textBox4.configure(state="disabled", background="gray60")
                textBox5.configure(state="disabled", background="gray60")

        panel1 = Label(image_frame, image = smaller_image1)
        panel1.photo = smaller_image1
        panel2 = Label(image_frame, image = smaller_image2)
        panel2.photo = smaller_image2
        panel3 = Label(image_frame, image = smaller_image3)
        panel3.photo = smaller_image3

        s = ttk.Style()
        s.configure('Red.TCheckbutton', foreground="aquamarine" ,background='gray1')

        # exponentital dist. parameter (right)
        bace_c1 = ttk.Checkbutton(base_frame_label2, text="Exponetial dist. (\u03BB)", variable = root.cVar2, width=20,
                                  onvalue=1, offvalue=11 ,style='Red.TCheckbutton', command=lambda:  onoff())
        bace_c1.grid(row=2, column=0, sticky='w')

        display_image(smaller_image1)
        sub_frame1 = Frame(base_frame_label2, bg='gray1')
        sub_frame1.grid(row=3, column=0, stick='w')
        sub_frame1_label1 = Label(sub_frame1, text='\u03BB = ', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1' ,anchor="w")
        sub_frame1_label1.grid(row=0, column=0, sticky="w", padx=(0 ,1))
        sub_frame1_label1.config(width=3)

        textBox1 =Text(sub_frame1, height=1, width=4)
        textBox1.grid(row=0, column=1)
        textBox1.configure(state="normal", background="white")

        # normal dist. parameter (right)
        bace_c2 = ttk.Checkbutton(base_frame_label2, text="Normal dist.(\u03BC, \u03C3)", variable = root.cVar2, width=20,
                                  onvalue=2 ,offvalue=22, style='Red.TCheckbutton', command= lambda:  onoff()  )
        bace_c2.grid(row=2, column=1, sticky='w')

        sub_frame2 = Frame(base_frame_label2, bg='gray1')
        sub_frame2.grid(row=3, column=1, stick='w')
        sub_frame2_label1 = Label(sub_frame2, text='\u03BC = ', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1' ,anchor="w")
        sub_frame2_label1.grid(row=0, column=0, sticky="w", padx=(0 ,1))
        sub_frame2_label1.config(width=3)

        textBox2 =Text(sub_frame2, height=1, width=4)
        textBox2.grid(row=0, column=1)
        textBox2.configure(state="disabled", background="gray60")

        sub_frame2_label2 = Label(sub_frame2, text='\u03C3 = ', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1' ,anchor="w")
        sub_frame2_label2.grid(row=0, column=2, sticky="w", padx=(3 ,1))
        sub_frame2_label2.config(width=3)

        textBox3 =Text(sub_frame2, height=1, width=4)
        textBox3.grid(row=0, column=3)
        textBox3.configure(state="disabled", background="gray60")

        # uniform dist. parameter (right)
        bace_c3 = ttk.Checkbutton(base_frame_label2, text="Uniform dist. (a, b)", variable = root.cVar2, width=20,
                                  onvalue=3 ,offvalue=33 ,style='Red.TCheckbutton', command=lambda: onoff())
        bace_c3.grid(row=2, column=2, sticky='w')

        sub_frame3 = Frame(base_frame_label2, bg='gray1')
        sub_frame3.grid(row=3, column=2, stick='w')
        sub_frame3_label1 = Label(sub_frame3, text='a = ', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1', anchor="w")
        sub_frame3_label1.grid(row=0, column=0, sticky="w", padx=(0, 1))
        sub_frame3_label1.config(width=3)

        textBox4 = Text(sub_frame3, height=1, width=4)
        textBox4.grid(row=0, column=1)
        textBox4.configure(state="disabled", background="gray60")

        sub_frame3_label2 = Label(sub_frame3, text='b = ', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1', anchor="w")
        sub_frame3_label2.grid(row=0, column=2, sticky="w", padx=(3, 1))
        sub_frame3_label2.config(width=3)

        textBox5 = Text(sub_frame3, height=1, width=4)
        textBox5.grid(row=0, column=3)
        textBox5.configure(state="disabled", background="gray60")

        # update failure rate (left)
        def sampling():
            a = root.cVar2.get()
            global resourcelist2
            if a == 1:
                if seedBox1.get("1.0", "end-1c") != '':
                    seed_value = int(seedBox1.get("1.0", "end-1c"))
                    numpy.random.seed(seed_value)
                lamb = float(textBox1.get("1.0", "end-1c"))
                resourcelist2 = self.resourcelist
                resourcelist2["Resource_failure_rate"] = numpy.random.exponential(lamb, len(self.resourcelist))
                numpy.random.seed(0)
                mylist2.delete('1.0', END)
                mylist2.insert(tk.CURRENT, resourcelist2[0:len(self.resourcelist)].to_string(index=False))
                messagebox.showinfo("Message", "'Sampling from exp dist' applied. Check updated resources in event log.")
                system_info_frame1.config(highlightbackground="gray1", highlightcolor = "gray1", highlightthickness=2)
                base_frame_label2.config(highlightbackground="gray1", highlightcolor = "gray1", highlightthickness=2)
                resource_info_frame1.config(highlightbackground="dark orange", highlightcolor = "dark orange", highlightthickness=2)

            elif a == 2:
                if seedBox1.get("1.0", "end-1c") != '':
                    seed_value = int(seedBox1.get("1.0", "end-1c"))
                    numpy.random.seed(seed_value)
                mean = float(textBox2.get("1.0", "end-1c"))
                sd = float(textBox3.get("1.0", "end-1c"))
                resourcelist2 = self.resourcelist
                resourcelist2["Resource_failure_rate"] = numpy.random.normal(mean, sd, len(self.resourcelist))
                numpy.random.seed(0)
                mylist2.delete('1.0', END)
                mylist2.insert(tk.CURRENT, resourcelist2[0:len(self.resourcelist)].to_string(index=False))
                messagebox.showinfo("Message",
                                    "'Sampling from normal dist' applied. Check updated resources in event log.")
                system_info_frame1.config(highlightbackground="gray1", highlightcolor = "gray1", highlightthickness=2)
                base_frame_label2.config(highlightbackground="gray1", highlightcolor = "gray1", highlightthickness=2)
                resource_info_frame1.config(highlightbackground="dark orange", highlightcolor = "dark orange", highlightthickness=2)

            elif a == 3:
                if seedBox1.get("1.0", "end-1c") != '':
                    seed_value = int(seedBox1.get("1.0", "end-1c"))
                    numpy.random.seed(seed_value)
                a = float(textBox4.get("1.0", "end-1c"))
                b = float(textBox5.get("1.0", "end-1c"))
                resourcelist2 = self.resourcelist
                resourcelist2["Resource_failure_rate"] = numpy.random.uniform(a, b, len(self.resourcelist))
                resourcelist2 = resourcelist2[['Resource', 'Frequency','Resource_failure_rate', 'Activities']]
                numpy.random.seed(0)
                mylist2.delete('1.0', END)
                mylist2.insert(tk.CURRENT, resourcelist2[0:len(self.resourcelist)].to_string(index=False))
                messagebox.showinfo("Message",
                                    "'Sampling from uniform dist' applied. Check updated resources in event log.")
                system_info_frame1.config(highlightbackground="gray1", highlightcolor = "gray1", highlightthickness=2)
                base_frame_label2.config(highlightbackground="gray1", highlightcolor = "gray1", highlightthickness=2)
                resource_info_frame1.config(highlightbackground="dark orange", highlightcolor = "dark orange", highlightthickness=2)

            root.attributes('-topmost', 1)
            root.attributes('-topmost', 0)

        action2 = tk.Button(base_frame_label2, text="Apply", width=10, command=sampling)
        action2.grid(row=4, column=2, stick='e', padx=(0,5), pady= (5,0))

        # apply pass/fail (right)
        def passfail():
            extracted_data2 = self.extracted_data2
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

        action3 = tk.Button(center, text="Close",width= 10,  command=passfail)
        action3.grid(row=1, column=1,sticky="e",  padx=(0,20), pady=(0,10))




#############################################################################################

class Resource_Step1_sub(tk.Toplevel):    # resource- failure rate
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
                                  fg="white", bg='gray25', relief="raised")
        base_frame_label1.grid(row=0, column=0 , columnspan =3, sticky="nsew")
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
                                          fg="white", bg='gray1', bd=3, padx=12 , pady=14)
        resource_info_frame1.grid(row=1, column=0, padx=10, sticky='nsw')

        #
        sub_frame4 = Frame(resource_info_frame1, bg='gray1')
        sub_frame4.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        sub_frame4.rowconfigure(0, weight=1)
        sub_frame4.columnconfigure(0, weight=1)
        sub_frame4.grid_propagate(False)

        canvas1 = Canvas(sub_frame4, bd=0, bg='gray1', highlightthickness=0)
        canvas1.grid(row=0, column=0, sticky="news")
        vsb = tk.Scrollbar(sub_frame4, orient="vertical", command=canvas1.yview)
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

        frame_buttons1.update_idletasks()

        sub_frame4.config(width=270, height=270)
        canvas1.config(scrollregion=canvas1.bbox("all"))


        # Resource group - activity connection (Right)
        base_frame_label2 = LabelFrame(base_frame, text="Allocate resource groups on each activity", font=("Consolas", 10, 'bold'),
                                       fg="white", bg='gray1', bd=3)
        base_frame_label2.grid(row=1, column=1,sticky='nwse', padx=10)

        sub_frame3 =Frame(base_frame_label2, bg='gray1')
        sub_frame3.grid(row=0, column=0, sticky='nwse', padx=10,pady=10)

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
            globals()['dist1{}'.format(k)] = tk.StringVar()
            globals()['act{}_grp'.format(k)] = ttk.Combobox(frame_buttons2, width=14, textvariable=['dist1{}'.format(k)])
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

            Resource_Step1.extracted_data2 = extracted_data4
            PageThree.before = extracted_data4

            resourcelist2 = extracted_data4.groupby('Resource').agg(params).reset_index()
            resourcelist2.columns = ["Resource", "Frequency", "Activities"]
            resourcelist2 = resourcelist2.sort_values(["Frequency"], ascending=False)
            cols = ["Resource", "Frequency",  "Activities"]
            resourcelist2 = resourcelist2[cols]

            Resource_Step1.resourcelist = resourcelist2
            Resource_Step1.mylist2.delete('1.0', END)
            Resource_Step1.mylist2.insert(tk.CURRENT, resourcelist2[0:len(resourcelist2)].to_string(index=False))
            Inject_Anomaly.data_with_resource = extracted_data4
            Resource_Step1.root.update()
            messagebox.showinfo("Message", "Successfully proceeded")
            Resource_Step1.system_info_frame1.config(highlightbackground="gray1", highlightcolor="gray1", highlightthickness=2)
            Resource_Step1.base_frame_label2.config(highlightbackground="dark orange", highlightcolor="dark orange",
                                     highlightthickness=2)
            root.destroy()
            self.root2.lift()

        action_res1 = tk.Button(base_frame, text="Apply", width=10, command= lambda: attach_res(activitylist))
        action_res1.grid(row=2, column=1, sticky = 'e', padx= (0,20), pady=10)