import warnings
warnings.filterwarnings(action='ignore')

#GUI PACKAGES
import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
#from typing import TYPE_CHECKING

#Pages
from abnormal_patterns import Abnorm_p
from abnormal_patterns_sys import Abnorm_sys


class Inject_Anomaly(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, bg='dark slate gray')

        # Create main containers
        top_frame = Frame(self, bg='dark slate gray',    padx=7, pady=3)
        center = Frame(self, bg='dark slate gray',   padx=7, pady=3)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        top_frame.grid(row=0, sticky="nsew")
        center.grid(row=1, sticky="nsew")
        top_frame.grid_rowconfigure(0, weight=1)
        top_frame.grid_columnconfigure(0, weight=1)
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(0, weight=1)
        Inject_Anomaly.parent = parent

        # Create main containers
        base_frame = Frame(center, bg='gray1')
        base_frame.grid(row=0, column=0, sticky="nsew")
        base_frame_label_t = LabelFrame(base_frame, text="Progress Status", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1', bd=3, padx=15, pady=15)
        Inject_Anomaly.text_progress = Text(base_frame_label_t, width=84, height=10, wrap=NONE)
        Inject_Anomaly.text_progress.grid(row=5, column=0, columnspan=2,  sticky="nsew", padx=10, pady=10)

        # Title widget
        base_frame_label1 = Label(top_frame, text='(3) Fault injection', font=("Consolas", 13, 'bold'),
                                  fg="white", bg='gray25', anchor="center", relief="raised")
        base_frame_label1.grid(row=0, column=0, sticky="nsew")
        base_frame_label1.grid_rowconfigure(1, weight=1)
        base_frame_label1.grid_columnconfigure(0, weight=1)


        # Frame setting
        base_frame_label2 = LabelFrame(base_frame, text=" Set anomaly patterns ",
                                       font=("Consolas", 10, 'bold'),
                                       fg="white", bg='gray1', bd=3, padx=14, pady=15)


        base_frame_label4 = LabelFrame(base_frame, text=" Set anomaly patterns ",
                                       font=("Consolas", 10, 'bold'),
                                       fg="white", bg='gray1', bd=3, padx=14, pady=15)
        def seedBox(seed):
            Abnorm_p.seedBox = seed
            Abnorm_sys.seedBox = seed



        def iserror(func, *args):
            try:
                func(*args)
                return False
            except Exception:
                return True

        self.ok=0
        def isok():
            self.ok=1

        def Seeresult():
            if self.ok==0:
                messagebox.showinfo("Error", "Inject anomalies firstly")
            else:
                parent.show_frame2()

        # Implement resource error
        if (self.a == 1 and self.b == 0):
            base_frame_label2.grid(row=0, column=0,columnspan=2,   padx=10, pady=10)
            base_frame_label_t.grid(row=2, column=0, columnspan=2,  padx=10, pady=10)
            but_implement = tk.Button(base_frame, text="Apply", width=10,
                                      command=lambda: [isok(),seedBox(seedBox1), Abnorm_p(self.extracted_data2).implement_resource(
                                          types=self.apply_type(parent),
                                          mag=[self.apply_w_skip(parent), self.apply_w_form(parent), self.apply_w_switch(parent),
                                               self.apply_w_insert(parent), self.apply_w_rework(parent), self.apply_w_moved(parent),
                                               self.apply_w_incomplete(parent), self.apply_w_replace(parent)],
                                          m_skip=self.apply_p_skip(parent), m_form=self.apply_p_form(parent),
                                          m_switch=self.apply_p_switch(parent), m_insert=self.apply_p_insert(parent), h_moved=self.apply_p_moved(parent),
                                          m_rework=self.apply_p_rework(parent), m_replace=self.apply_p_replace(parent))])  # extracted_data2 = event log with pass/fail(resource)
            but_implement.grid(row=1, column=0,  sticky="e", padx=10, pady=10)

            action2 = tk.Button(base_frame, text="See result", width=14,
                                command= lambda: Seeresult())
            action2.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        # Implement system error
        elif (self.a == 0 and self.b == 1):
            base_frame_label4.grid(row=0, column=0,sticky= 'w', columnspan=2,  padx=10, pady=10)
            # Set seed - system (mid-down)
            seed_frame2 = Frame(base_frame_label4, bg='gray30', relief='ridge', borderwidth=2, width=15)
            seed_frame2.grid(row=0, column=0, padx=10, pady=5, stick='nws')
            seed_Label2 = Label(seed_frame2, text="(Optional) Seed = ",
                                fg="white", bg='gray30', anchor="w")
            seed_Label2.grid(row=0, column=0, sticky='w')
            seed_frame2_sub = Frame(seed_frame2, bg='gray30')
            seed_frame2_sub.grid(row=0, column=1, stick='w')
            seedBox2 = Text(seed_frame2_sub, height=1, width=4)
            seedBox2.grid(row=0, column=0, padx=(0, 5))
            seedBox2.configure(state="normal", background="white")
            Abnorm_sys.seedBox2 = seedBox2
            # t00~ t02 : column name in table

            matrix_frame2 = Frame(base_frame_label4, bg='gray1')
            matrix_frame2.grid(row=1, column=0, padx=10, pady=5, sticky='nwes')
            t00 = Frame(matrix_frame2, width=17, bg='gray25', highlightbackground="lavender", highlightthickness=1)
            t00.grid(row=0, column=0, sticky="nwse")
            t00.grid_rowconfigure(0, weight=1)
            t00.grid_columnconfigure(0, weight=1)
            txt00 = Label(t00, text='Pattern (System)', font=("Consolas", 10, 'bold'),
                          fg="white", bg='gray25', anchor="center", width=20)
            txt00.grid(row=0, column=0, sticky="nwse", padx=2, pady=2)
            txt00.grid_rowconfigure(0, weight=1)
            txt00.grid_columnconfigure(0, weight=1)
            t01 = Frame(matrix_frame2, bg='gray25', width=10, highlightbackground="lavender", highlightthickness=1)
            t01.grid(row=0, column=10, sticky="nwse")
            t01.grid_rowconfigure(0, weight=1)
            t01.grid_columnconfigure(0, weight=1)
            txt01 = Label(t01, text='Strength', font=("Consolas", 10, 'bold'),
                          fg="white", bg='gray25', anchor="center", width=10)
            txt01.grid(row=0, column=0, sticky="nwse", padx=2, pady=2)
            txt01.grid_rowconfigure(0, weight=1)
            txt01.grid_columnconfigure(0, weight=1)

            # t10~ t12 : skip - system
            t10 = Frame(matrix_frame2, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
            t10.grid(row=10, column=0, sticky="nwse")
            t10.grid_rowconfigure(0, weight=1)
            t10.grid_columnconfigure(0, weight=1)
            parent.cVar_skip_sys = IntVar()
            parent.cVar_skip_sys.set(0)
            t11 = Frame(matrix_frame2, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
            t11.grid(row=10, column=10, sticky="nwse")
            t11.grid_rowconfigure(0, weight=1)
            t11.grid_columnconfigure(0, weight=1)
            parent.weight_skip_sys = Text(t11, height=1, width=5)
            parent.weight_skip_sys.grid(row=10, column=10, padx=(30, 31), pady=2)
            parent.weight_skip_sys.configure(state="disabled", bg="gray60")

            but_skip_sys = ttk.Checkbutton(t10, text="skip", onvalue=1, offvalue=0, variable=parent.cVar_skip_sys,
                                           style='Red.TCheckbutton', width=10,
                                           command=lambda: self.able_skip_sys(parent))
            but_skip_sys.grid(row=10, column=0, padx=2, pady=2, sticky= 'w')
            but_skip_sys.grid_rowconfigure(0, weight=1)
            but_skip_sys.grid_columnconfigure(0, weight=1)

            # t20~ t22 : form-based - system
            t20 = Frame(matrix_frame2, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
            t20.grid(row=20, column=0, sticky="nwse")
            t20.grid_rowconfigure(0, weight=1)
            t20.grid_columnconfigure(0, weight=1)
            parent.cVar_form_sys = IntVar()
            parent.cVar_form_sys.set(0)
            t21 = Frame(matrix_frame2, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
            t21.grid(row=20, column=10, sticky="nwse")
            t21.grid_rowconfigure(0, weight=1)
            t21.grid_columnconfigure(0, weight=1)
            parent.weight_form_sys = Text(t21, height=1, width=5)
            parent.weight_form_sys.grid(row=20, column=10, padx=(30, 31), pady=2)
            parent.weight_form_sys.configure(state="disabled", bg="gray60")

            but_form_sys = ttk.Checkbutton(t20, text="form based", onvalue=1, offvalue=0, variable=parent.cVar_form_sys,
                                           style='Red.TCheckbutton', width=10,
                                           command=lambda: self.able_form_sys(parent))
            but_form_sys.grid(row=20, column=0, padx=2, pady=2, sticky= 'w')
            but_form_sys.grid_rowconfigure(0, weight=1)
            but_form_sys.grid_columnconfigure(0, weight=1)

            # t30~ t32 : cut - system
            t30 = Frame(matrix_frame2, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
            t30.grid(row=30, column=0, sticky="nwse")
            t30.grid_rowconfigure(0, weight=1)
            t30.grid_columnconfigure(0, weight=1)
            parent.cVar_cut_sys = IntVar()
            parent.cVar_cut_sys.set(0)
            t31 = Frame(matrix_frame2, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
            t31.grid(row=30, column=10, sticky="nwse")
            t31.grid_rowconfigure(0, weight=1)
            t31.grid_columnconfigure(0, weight=1)
            parent.weight_cut_sys = Text(t31, height=1, width=5)
            parent.weight_cut_sys.grid(row=30, column=10, padx=(30, 31), pady=2)
            parent.weight_cut_sys.configure(state="disabled", bg="gray60")

            but_cut_sys = ttk.Checkbutton(t30, text="cut", onvalue=1, offvalue=0, variable=parent.cVar_cut_sys,
                                          style='Red.TCheckbutton', width=10, command=lambda: self.able_cut_sys(parent))
            but_cut_sys.grid(row=30, column=0, padx=2, pady=2, sticky= 'w')
            but_cut_sys.grid_rowconfigure(0, weight=1)
            but_cut_sys.grid_columnconfigure(0, weight=1)
            base_frame_label_t.grid(row=2, column=0,columnspan=2,   padx=10, pady=10)
            but_implement_sys = tk.Button(base_frame, text="Apply", width=10,
                                          command=lambda: [isok(), seedBox(seedBox2), Abnorm_sys(sys_file=self.system_down, log_file=self.data_with_system, old_file=None).implement_sys_single(df_log=None, df_sys=None,
                                              types_sys=self.apply_type_sys(parent),
                                              mag_sys=[self.apply_w_skip_sys(parent), self.apply_w_form_sys(parent), self.apply_w_cut_sys(parent)])])    # system_down = malfunctioning log, data_with_system = event log(system)
            but_implement_sys.grid(row=1, column=0, sticky="e", padx=10, pady=10)

            action2 = tk.Button(base_frame, text="See result", width=10,
                                command= lambda: Seeresult())
            action2.grid(row=1, column=1,  sticky="w", padx=10, pady=10)

        # Implement resource and system error
        elif (self.a == 1 and self.b == 1):
            base_frame_label_t.grid(row=3, column=0,columnspan=2,  padx=10, pady=10)
            base_frame_label2.grid(row=0, column=0,columnspan=2,  padx=10, pady=10)

            matrix_frame3 = Frame(base_frame_label2, bg='gray1')
            matrix_frame3.grid(row=2, column=0, padx=10, pady=5, sticky='nws')
            # t10~ t12 : skip - system
            t00 = Frame(matrix_frame3, width=17, bg='gray25', highlightbackground="lavender", highlightthickness=1)
            t00.grid(row=0, column=0, sticky="nwse")
            t00.grid_rowconfigure(0, weight=1)
            t00.grid_columnconfigure(0, weight=1)
            txt00 = Label(t00, text='Pattern (System)', font=("Consolas", 10, 'bold'),
                          fg="white", bg='gray25', anchor="center", width=20)
            txt00.grid(row=0, column=0, sticky="nwse", padx=2, pady=2)
            txt00.grid_rowconfigure(0, weight=1)
            txt00.grid_columnconfigure(0, weight=1)
            t01 = Frame(matrix_frame3, bg='gray25', width=10, highlightbackground="lavender", highlightthickness=1)
            t01.grid(row=0, column=10, sticky="nwse")
            t01.grid_rowconfigure(0, weight=1)
            t01.grid_columnconfigure(0, weight=1)
            txt01 = Label(t01, text='Strength', font=("Consolas", 10, 'bold'),
                          fg="white", bg='gray25', anchor="center", width=10)
            txt01.grid(row=0, column=0, sticky="nwse", padx=2, pady=2)
            txt01.grid_rowconfigure(0, weight=1)
            txt01.grid_columnconfigure(0, weight=1)


            t10 = Frame(matrix_frame3, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
            t10.grid(row=10, column=0, sticky="nwse")
            t10.grid_rowconfigure(0, weight=1)
            t10.grid_columnconfigure(0, weight=1)
            parent.cVar_skip_sys = IntVar()
            parent.cVar_skip_sys.set(0)
            t11 = Frame(matrix_frame3, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
            t11.grid(row=10, column=10, sticky="nwse")
            t11.grid_rowconfigure(0, weight=1)
            t11.grid_columnconfigure(0, weight=1)
            parent.weight_skip_sys = Text(t11, height=1, width=5)
            parent.weight_skip_sys.grid(row=10, column=10, padx=(30, 31), pady=2)
            parent.weight_skip_sys.configure(state="disabled", bg="gray60")

            but_skip_sys = ttk.Checkbutton(t10, text="skip", onvalue=1, offvalue=0, variable=parent.cVar_skip_sys,
                                           style='Red.TCheckbutton', width=10,
                                           command=lambda: self.able_skip_sys(parent))
            but_skip_sys.grid(row=10, column=0, padx=2, pady=2, sticky= 'w')
            but_skip_sys.grid_rowconfigure(0, weight=1)
            but_skip_sys.grid_columnconfigure(0, weight=1)

            # t20~ t22 : form-based - system
            t20 = Frame(matrix_frame3, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
            t20.grid(row=20, column=0, sticky="nwse")
            t20.grid_rowconfigure(0, weight=1)
            t20.grid_columnconfigure(0, weight=1)
            parent.cVar_form_sys = IntVar()
            parent.cVar_form_sys.set(0)
            t21 = Frame(matrix_frame3, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
            t21.grid(row=20, column=10, sticky="nwse")
            t21.grid_rowconfigure(0, weight=1)
            t21.grid_columnconfigure(0, weight=1)
            parent.weight_form_sys = Text(t21, height=1, width=5)
            parent.weight_form_sys.grid(row=20, column=10, padx=(30, 31), pady=2)
            parent.weight_form_sys.configure(state="disabled", bg="gray60")

            but_form_sys = ttk.Checkbutton(t20, text="form based", onvalue=1, offvalue=0, variable=parent.cVar_form_sys,
                                           style='Red.TCheckbutton', width=10,
                                           command=lambda: self.able_form_sys(parent))
            but_form_sys.grid(row=20, column=0, padx=2, pady=2, sticky= 'w')
            but_form_sys.grid_rowconfigure(0, weight=1)
            but_form_sys.grid_columnconfigure(0, weight=1)

            # t30~ t32 : cut - system
            t30 = Frame(matrix_frame3, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
            t30.grid(row=30, column=0, sticky="nwse")
            t30.grid_rowconfigure(0, weight=1)
            t30.grid_columnconfigure(0, weight=1)
            parent.cVar_cut_sys = IntVar()
            parent.cVar_cut_sys.set(0)
            t31 = Frame(matrix_frame3, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
            t31.grid(row=30, column=10, sticky="nwse")
            t31.grid_rowconfigure(0, weight=1)
            t31.grid_columnconfigure(0, weight=1)
            parent.weight_cut_sys = Text(t31, height=1, width=5)
            parent.weight_cut_sys.grid(row=30, column=10, padx=(30, 31), pady=2)
            parent.weight_cut_sys.configure(state="disabled", bg="gray60")

            but_cut_sys = ttk.Checkbutton(t30, text="cut", onvalue=1, offvalue=0, variable=parent.cVar_cut_sys,
                                          style='Red.TCheckbutton', width=10, command=lambda: self.able_cut_sys(parent))
            but_cut_sys.grid(row=30, column=0, padx=2, pady=2, sticky= 'w')
            but_cut_sys.grid_rowconfigure(0, weight=1)
            but_cut_sys.grid_columnconfigure(0, weight=1)

            but_implement = tk.Button(base_frame, text="Apply", width=10,
                                      command=lambda: [isok(), seedBox(seedBox1) ,Abnorm_sys(sys_file=self.system_down,
                                                                 log_file=self.data_with_system,
                                                                 old_file=self.extracted_data2).implement_bind(
                                          types_sys=self.apply_type_sys(parent), types_re=self.apply_type(parent),
                                          mag_sys=[self.apply_w_skip_sys(parent), self.apply_w_form_sys(parent),
                                                   self.apply_w_cut_sys(parent)],
                                          mag_re=[self.apply_w_skip(parent), self.apply_w_form(parent),
                                                  self.apply_w_switch(parent),
                                                  self.apply_w_insert(parent), self.apply_w_rework(parent),
                                                  self.apply_w_moved(parent),
                                                  self.apply_w_incomplete(parent),
                                                  self.apply_w_replace(parent)],
                                          m_skip=self.apply_p_skip(parent), m_form=self.apply_p_form(parent),
                                          m_switch=self.apply_p_switch(parent), h_moved=self.apply_p_moved(parent),
                                          m_rework=self.apply_p_rework(parent))])
            but_implement.grid(row=2, column=0, sticky="e", padx=10, pady=10)

            action2 = tk.Button(base_frame, text="See result", width=10,
                                command= lambda: Seeresult())
            action2.grid(row=2, column=1,  sticky="w", padx=10, pady=10)

        else:
            pass

        # Anomaly pattern widget - resource (mid)

        s = ttk.Style()
        s.configure('Red.TCheckbutton', foreground="aquamarine", background='gray40')
        s.map('Red.TCheckbutton', background=[('active', 'gray40')])

        # Set seed - resource (mid)
        seed_frame1 = Frame(base_frame_label2, bg='gray30', relief='ridge', borderwidth=2, width=15)
        seed_frame1.grid(row=0, column=0, padx=10, pady=5, stick='nws')
        seed_Label1 = Label(seed_frame1, text="(Optional) Seed = ",
                            fg="white", bg='gray30', anchor="w")
        seed_Label1.grid(row=0, column=0, sticky='w')
        seed_frame1_sub = Frame(seed_frame1, bg='gray30')
        seed_frame1_sub.grid(row=0, column=1, stick='w')
        seedBox1 = Text(seed_frame1_sub, height=1, width=4)
        seedBox1.grid(row=0, column=0, padx=(0, 5))
        seedBox1.configure(state="normal", background="white")
        # t00~ t02 : column name in table

        matrix_frame1 = Frame(base_frame_label2, bg='gray1')
        matrix_frame1.grid(row=1, column=0, padx=10,pady=5, sticky= 'nwse')

        # table00~ table02 : column name in table
        table00 = Frame(matrix_frame1,  bg='gray25', width=10,highlightbackground="lavender", highlightthickness=1)
        table00.grid(row=0, column=0,  sticky='nwse')
        table00.grid_rowconfigure(0, weight=1)
        table00.grid_columnconfigure(0, weight=1)

        text00 = Label(matrix_frame1, text='Pattern (Resource)', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray25', anchor="center", width=20)
        text00.grid(row=0, column=0,  sticky='nwse', padx=2, pady=2)
        text00.grid_rowconfigure(0, weight=1)
        text00.grid_columnconfigure(0, weight=1)

        table01 = Frame(matrix_frame1, bg='gray25', width=10, highlightbackground="lavender", highlightthickness=1)
        table01.grid(row=0, column=10, sticky='nwse')
        table01.grid_rowconfigure(0, weight=1)
        table01.grid_columnconfigure(0, weight=1)
        text01 = Label(table01, text='Strength', font=("Consolas", 10, 'bold'),
                       fg="white", bg='gray25', anchor="center", width=10)
        text01.grid(row=0, column=0, sticky="nwse", padx=2, pady=2)
        text01.grid_rowconfigure(0, weight=1)
        text01.grid_columnconfigure(0, weight=1)

        table02 = Frame(matrix_frame1, bg='gray25', width=10, highlightbackground="lavender", highlightthickness=1)
        table02.grid(row=0, column=20, sticky='nwse')
        table02.grid_rowconfigure(0, weight=1)
        table02.grid_columnconfigure(0, weight=1)
        text02 = Label(table02, text='Parameter', font=("Consolas", 10, 'bold'),
                       fg="white", bg='gray25', anchor="center")
        text02.grid(row=0, column=0, sticky="nwse", padx=2, pady=2)
        text02.grid_rowconfigure(0, weight=1)
        text02.grid_columnconfigure(0, weight=1)

        # table10~ table12 : skip
        table10 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table10.grid(row=10, column=0, sticky="nwse")
        table10.grid_rowconfigure(0, weight=1)
        table10.grid_columnconfigure(0, weight=1)
        parent.cVar_skip = IntVar()
        parent.cVar_skip.set(0)
        table11 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table11.grid(row=10, column=10, sticky="nwse")
        table11.grid_rowconfigure(0, weight=1)
        table11.grid_columnconfigure(0, weight=1)
        parent.weight_skip = Text(table11, height=1, width=5)
        parent.weight_skip.grid(row=10, column=10, padx=(30, 31), pady=2)
        parent.weight_skip.configure(state="disabled", bg="gray60")
        table12 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table12.grid(row=10, column=20, sticky="nwse")
        table12.grid_rowconfigure(0, weight=1)
        table12.grid_columnconfigure(0, weight=1)
        p_skip_text = Label(table12, text="", font=("Consolas", 10, 'bold'),
                            fg="white", bg='gray40', anchor="center", width=12)
        p_skip_text.grid(row=50, column=0,  padx=2, pady=2)

        but_skip = ttk.Checkbutton(table10, text="skip", onvalue=1, offvalue=0, variable=parent.cVar_skip,
                                   style='Red.TCheckbutton', width=10, command=lambda: self.able_skip(parent))
        but_skip.grid(row=10, column=0, padx=2, pady=2, sticky= 'w')
        but_skip.grid_rowconfigure(0, weight=1)
        but_skip.grid_columnconfigure(0, weight=1)

        # table60~ table62 : form-based
        table60 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table60.grid(row=60, column=0, sticky="nwse")
        table60.grid_rowconfigure(0, weight=1)
        table60.grid_columnconfigure(0, weight=1)
        parent.cVar_form = IntVar()
        parent.cVar_form.set(0)
        table61 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table61.grid(row=60, column=10, sticky="nwse")
        table61.grid_rowconfigure(0, weight=1)
        table61.grid_columnconfigure(0, weight=1)
        parent.weight_form = Text(table61, height=1, width=5)
        parent.weight_form.grid(row=60, column=10, padx=(30, 31), pady=2)
        parent.weight_form.configure(state="disabled", bg="gray60")
        table62 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table62.grid(row=60, column=20, sticky="nwse")
        table62.grid_rowconfigure(0, weight=1)
        table62.grid_columnconfigure(0, weight=1)
        table62_sub = Frame(table62,bg='gray40')
        table62_sub.grid(row=0, column=0)
        p_form_text = Label(table62_sub, text="Max_length = ", font=("Consolas", 10, 'bold'),
                            fg="white", bg='gray40',width=12, anchor="center")
        p_form_text.grid(row=60, column=0, padx=2, pady=2)
        parent.parameter_form = Text(table62_sub, height=1, width=5)
        parent.parameter_form.grid(row=60, column=20, sticky= 'w')
        parent.parameter_form.configure(state="disabled", bg="gray60")
        but_form = ttk.Checkbutton(table60, text="form based", onvalue=1, offvalue=0, variable=parent.cVar_form,
                                   style='Red.TCheckbutton', width=10, command=lambda: self.able_form(parent))
        but_form.grid(row=60, column=0, padx=2, pady=2, sticky= 'w')
        but_form.grid_rowconfigure(0, weight=1)
        but_form.grid_columnconfigure(0, weight=1)

        # table20~ table22 : switch
        table20 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table20.grid(row=20, column=0, sticky="nwse")
        table20.grid_rowconfigure(0, weight=1)
        table20.grid_columnconfigure(0, weight=1)
        parent.cVar_switch = IntVar()
        parent.cVar_switch.set(0)
        table21 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table21.grid(row=20, column=10, sticky="nwse")
        table21.grid_rowconfigure(0, weight=1)
        table21.grid_columnconfigure(0, weight=1)
        parent.weight_switch = Text(table21, height=1, width=5)
        parent.weight_switch.grid(row=20, column=10, padx=(30, 31), pady=2)
        parent.weight_switch.configure(state="disabled", bg="gray60")
        table22 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table22.grid(row=20, column=20, sticky="nwse")
        table22.grid_rowconfigure(0, weight=1)
        table22.grid_columnconfigure(0, weight=1)
        p_switch_text = Label(table22, text="", font=("Consolas", 10, 'bold'),
                            fg="white", bg='gray40', anchor="center", width=12)
        p_switch_text.grid(row=20, column=0, padx=2, pady=2)

        but_switch = ttk.Checkbutton(table20, text="switch", onvalue=1, offvalue=0, variable=parent.cVar_switch,
                                    style='Red.TCheckbutton', width=10, command=lambda:self.able_switch(parent))
        but_switch.grid(row=20, column=0, padx=2, pady=2, sticky= 'w')
        but_switch.grid_rowconfigure(0, weight=1)
        but_switch.grid_columnconfigure(0, weight=1)

        # table70~ table72 : insert
        table70 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table70.grid(row=70, column=0, sticky="nwse")
        table70.grid_rowconfigure(0, weight=1)
        table70.grid_columnconfigure(0, weight=1)
        parent.cVar_insert = IntVar()
        parent.cVar_insert.set(0)
        table71 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table71.grid(row=70, column=10, sticky="nwse")
        table71.grid_rowconfigure(0, weight=1)
        table71.grid_columnconfigure(0, weight=1)
        parent.weight_insert = Text(table71, height=1, width=5)
        parent.weight_insert.grid(row=70, column=10, padx=(30, 31), pady=2)
        parent.weight_insert.configure(state="disabled", bg="gray60")
        table72 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table72.grid(row=70, column=20, sticky="nwse")
        table72.grid_rowconfigure(0, weight=1)
        table72.grid_columnconfigure(0, weight=1)
        table72_sub = Frame(table72,bg='gray40')
        table72_sub.grid(row=0, column=0)
        p_insert_text = Label(table72_sub, text="Max_length = ", font=("Consolas", 10, 'bold'),
                            fg="white", bg='gray40', width=12)
        p_insert_text.grid(row=70, column=0,  padx=2, pady=2, sticky='w')
        parent.parameter_insert = Text(table72_sub, height=1, width=5)
        parent.parameter_insert.grid(row=70, column=1, sticky= 'w')
        parent.parameter_insert.configure(state="disabled", bg="gray60")
        but_insert = ttk.Checkbutton(table70, text="insert", onvalue=1, offvalue=0, variable=parent.cVar_insert,
                                     style='Red.TCheckbutton', width=10, command=lambda:self.able_insert(parent))
        but_insert.grid(row=70, column=0, padx=2, pady=2, sticky= 'w')
        but_insert.grid_rowconfigure(0, weight=1)
        but_insert.grid_columnconfigure(0, weight=1)

        # table50~ table52 : rework
        table50 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table50.grid(row=50, column=0, sticky="nwse")
        table50.grid_rowconfigure(0, weight=1)
        table50.grid_columnconfigure(0, weight=1)
        parent.cVar_rework = IntVar()
        parent.cVar_rework.set(0)
        table51 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table51.grid(row=50, column=10, sticky="nwse")
        table51.grid_rowconfigure(0, weight=1)
        table51.grid_columnconfigure(0, weight=1)
        parent.weight_rework = Text(table51, height=1, width=5)
        parent.weight_rework.grid(row=50, column=10, padx=(30, 31), pady=2)
        parent.weight_rework.configure(state="disabled", bg="gray60")
        table52 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table52.grid(row=50, column=20, sticky="nwse")
        table52.grid_rowconfigure(0, weight=1)
        table52.grid_columnconfigure(0, weight=1)
        table52_sub = Frame(table52,bg='gray40')
        table52_sub.grid(row=0, column=0)
        p_rework_text = Label(table52_sub, text="Max_length = ", font=("Consolas", 10, 'bold'),
                            fg="white", bg='gray40', anchor="center", width=12)
        p_rework_text.grid(row=50, column=0,  padx=2, pady=2)
        parent.parameter_rework = Text(table52_sub, height=1, width=5)
        parent.parameter_rework.grid(row=50, column=1,  sticky= 'w')
        parent.parameter_rework.configure(state="disabled", bg="gray60")
        but_rework = ttk.Checkbutton(table50, text="rework", onvalue=1, offvalue=0, variable=parent.cVar_rework,
                                     style='Red.TCheckbutton', width=10, command=lambda:self.able_rework(parent))
        but_rework.grid(row=50, column=0, padx=2, pady=2, sticky= 'w')
        but_rework.grid_rowconfigure(0, weight=1)
        but_rework.grid_columnconfigure(0, weight=1)

        # table80~ table82 : moved
        table80 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table80.grid(row=80, column=0, sticky="nwse")
        table80.grid_rowconfigure(0, weight=1)
        table80.grid_columnconfigure(0, weight=1)
        parent.cVar_moved = IntVar()
        parent.cVar_moved.set(0)
        table81 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table81.grid(row=80, column=10, sticky="nwse")
        table81.grid_rowconfigure(0, weight=1)
        table81.grid_columnconfigure(0, weight=1)
        parent.weight_moved = Text(table81, height=1, width=5)
        parent.weight_moved.grid(row=80, column=10, padx=(30, 31), pady=2)
        parent.weight_moved.configure(state="disabled", bg="gray60")
        table82 = Frame(matrix_frame1, bg='gray40', width=100, highlightbackground="lavender", highlightthickness=1)
        table82.grid(row=80, column=20, sticky="nwse")
        table82.grid_rowconfigure(0, weight=1)
        table82.grid_columnconfigure(0, weight=1)
        table82_sub = Frame(table82,bg='gray40')
        table82_sub.grid(row=0, column=0)
        p_moved_text = Label(table82_sub, text="Max:", font=("Consolas", 10, 'bold'),
                              fg="white", bg='gray40', anchor="e", width=5)
        p_moved_text.grid(row=80, column=0, padx=2, pady=2)
        p_moved_Y_text = Label(table82_sub, text="Y =", font=("Consolas", 10, 'bold'),
                            fg="white", bg='gray40', anchor="center", width=5)
        p_moved_Y_text.grid(row=80, column=10, padx=5.5, pady=2)
        parent.parameter_moved_Y = Text(table82_sub, height=1, width=5)
        parent.parameter_moved_Y.grid(row=80, column=30, padx=3.7)
        parent.parameter_moved_Y.configure(state="disabled", bg="gray60")
        p_moved_m_text = Label(table82_sub, text="m =", font=("Consolas", 10, 'bold'),
                                fg="white", bg='gray40', anchor="center", width=5)
        p_moved_m_text.grid(row=80, column=35, padx=4.5, pady=2)
        parent.parameter_moved_m = Text(table82_sub, height=1, width=5)
        parent.parameter_moved_m.grid(row=80, column=40, padx=5)
        parent.parameter_moved_m.configure(state="disabled", bg="gray60")
        p_moved_d_text = Label(table82_sub, text="d =", font=("Consolas", 10, 'bold'),
                                fg="white", bg='gray40', anchor="center", width=5)
        p_moved_d_text.grid(row=80, column=45, padx=4.5, pady=2)
        parent.parameter_moved_d = Text(table82_sub, height=1, width=5)
        parent.parameter_moved_d.grid(row=80, column=50, padx=5)
        parent.parameter_moved_d.configure(state="disabled", bg="gray60")
        p_moved_h_text = Label(table82_sub, text="h =", font=("Consolas", 10, 'bold'),
                                fg="white", bg='gray40', anchor="center", width=5)
        p_moved_h_text.grid(row=80, column=55, padx=4.5, pady=2)
        parent.parameter_moved_h = Text(table82_sub, height=1, width=5)
        parent.parameter_moved_h.grid(row=80, column=60, padx=5)
        parent.parameter_moved_h.configure(state="disabled", bg="gray60")
        p_moved_M_text = Label(table82_sub, text="M =", font=("Consolas", 10, 'bold'),
                                fg="white", bg='gray40', anchor="center", width=5)
        p_moved_M_text.grid(row=80, column=65, padx=4.4, pady=2)
        parent.parameter_moved_M = Text(table82_sub, height=1, width=5)
        parent.parameter_moved_M.grid(row=80, column=70, padx=4.7)
        parent.parameter_moved_M.configure(state="disabled", bg="gray60")
        but_moved = ttk.Checkbutton(table80, text="moved", onvalue=1, offvalue=0, variable=parent.cVar_moved,
                                     style='Red.TCheckbutton', width=10, command=lambda:self.able_moved(parent))
        but_moved.grid(row=80, column=0, padx=2, pady=2, sticky= 'w')
        but_moved.grid_rowconfigure(0, weight=1)
        but_moved.grid_columnconfigure(0, weight=1)

        # table40~ table42 : incomplete
        table40 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table40.grid(row=40, column=0, sticky="nwse")
        table40.grid_rowconfigure(0, weight=1)
        table40.grid_columnconfigure(0, weight=1)
        parent.cVar_incom = IntVar()
        parent.cVar_incom.set(0)
        table41 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table41.grid(row=40, column=10, sticky="nwse")
        table41.grid_rowconfigure(0, weight=1)
        table41.grid_columnconfigure(0, weight=1)
        parent.weight_incom = Text(table41, height=1, width=5)
        parent.weight_incom.grid(row=40, column=10, padx=(30, 31), pady=2)
        parent.weight_incom.configure(state="disabled", bg="gray60")
        table42 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table42.grid(row=40, column=20, sticky="nwse")
        table42.grid_rowconfigure(0, weight=1)
        table42.grid_columnconfigure(0, weight=1)
        p_incomplete_text = Label(table42, text="", font=("Consolas", 10, 'bold'),
                            fg="white", bg='gray40', anchor="center", width=12)
        p_incomplete_text.grid(row=40, column=0, padx=2, pady=2)

        but_incom = ttk.Checkbutton(table40, text="incomplete", onvalue=1, offvalue=0, variable=parent.cVar_incom,
                                    style='Red.TCheckbutton', width=10, command=lambda:self.able_incom(parent))
        but_incom.grid(row=40, column=0, padx=2, pady=2, sticky= 'w')
        but_incom.grid_rowconfigure(0, weight=1)
        but_incom.grid_columnconfigure(0, weight=1)

        # table30~ table32 : replace
        table30 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table30.grid(row=30, column=0, sticky="nwse")
        table30.grid_rowconfigure(0, weight=1)
        table30.grid_columnconfigure(0, weight=1)
        parent.cVar_replace = IntVar()
        parent.cVar_replace.set(0)
        table31 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table31.grid(row=30, column=10, sticky="nwse")
        table31.grid_rowconfigure(0, weight=1)
        table31.grid_columnconfigure(0, weight=1)
        parent.weight_replace = Text(table31, height=1, width=5)
        parent.weight_replace.grid(row=30, column=10, padx=(30, 31), pady=2)
        parent.weight_replace.configure(state="disabled", bg="gray60")
        table32 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table32.grid(row=30, column=20, sticky="nwse")
        table32.grid_rowconfigure(0, weight=1)
        table32.grid_columnconfigure(0, weight=1)
        p_replace_text = Label(table32, text="", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=12)
        p_replace_text.grid(row=30, column=0, padx=2, pady=2)

        but_replace = ttk.Checkbutton(table30, text="replace", onvalue=1, offvalue=0, variable=parent.cVar_replace,
                                    style='Red.TCheckbutton', width=10, command=lambda: self.able_replace(parent))
        but_replace.grid(row=30, column=0, padx=2, pady=2, sticky= 'w')
        but_replace.grid_rowconfigure(0, weight=1)
        but_replace.grid_columnconfigure(0, weight=1)







#####################################################################################


        s = ttk.Style()
        s.configure('Red.TCheckbutton', foreground="aquamarine", background='gray40')
        s.map('Red.TCheckbutton', background=[('active', 'gray40')])

    # "able_X" check resource error type "X" to make writing parameter & weight possible/impossible
    def able_skip(self, parent):
        if parent.cVar_skip.get() == 1:
            parent.weight_skip.configure(state="normal", bg="white")
            #parent.parameter_skip.configure(state="normal", bg="white")
        elif parent.cVar_skip.get() == 0:
            parent.weight_skip.configure(state="disabled", bg="gray60")
            #parent.parameter_skip.configure(state="disabled", bg="gray60")

    def able_form(self, parent):
        if parent.cVar_form.get() == 1:
            parent.weight_form.configure(state="normal", bg="white")
            parent.parameter_form.configure(state="normal", bg="white")
        elif parent.cVar_form.get() == 0:
            parent.weight_form.configure(state="disabled", bg="gray60")
            parent.parameter_form.configure(state="disabled", bg="gray60")

    def able_switch(self, parent):
        if parent.cVar_switch.get() == 1:
            parent.weight_switch.configure(state="normal", bg="white")
            #parent.parameter_switch.configure(state="normal", bg="white")
        elif parent.cVar_switch.get() == 0:
            parent.weight_switch.configure(state="disabled", bg="gray60")
            #parent.parameter_switch.configure(state="disabled", bg="gray60")

    def able_insert(self, parent):
        if parent.cVar_insert.get() == 1:
            parent.weight_insert.configure(state="normal", bg="white")
            parent.parameter_insert.configure(state="normal", bg="white")
        elif parent.cVar_insert.get() == 0:
            parent.weight_insert.configure(state="disabled", bg="gray60")
            parent.parameter_insert.configure(state="disabled", bg="gray60")

    def able_rework(self, parent):
        if parent.cVar_rework.get() == 1:
            parent.weight_rework.configure(state="normal", bg="white")
            parent.parameter_rework.configure(state="normal", bg="white")
        elif parent.cVar_rework.get() == 0:
            parent.weight_rework.configure(state="disabled", bg="gray60")
            parent.parameter_rework.configure(state="disabled", bg="gray60")

    def able_moved(self, parent):
        if parent.cVar_moved.get() == 1:
            parent.weight_moved.configure(state="normal", bg="white")
            parent.parameter_moved_Y.configure(state="normal", bg="white")
            parent.parameter_moved_m.configure(state="normal", bg="white")
            parent.parameter_moved_d.configure(state="normal", bg="white")
            parent.parameter_moved_h.configure(state="normal", bg="white")
            parent.parameter_moved_M.configure(state="normal", bg="white")
        elif parent.cVar_moved.get() == 0:
            parent.weight_moved.configure(state="disabled", bg="gray60")
            parent.parameter_moved_Y.configure(state="disabled", bg="gray60")
            parent.parameter_moved_m.configure(state="disabled", bg="gray60")
            parent.parameter_moved_d.configure(state="disabled", bg="gray60")
            parent.parameter_moved_h.configure(state="disabled", bg="gray60")
            parent.parameter_moved_M.configure(state="disabled", bg="gray60")

    def able_incom(self, parent):
        if parent.cVar_incom.get() == 1:
            parent.weight_incom.configure(state="normal", bg="white")
        elif parent.cVar_incom.get() == 0:
            parent.weight_incom.configure(state="disabled", bg="gray60")
        else:
            pass

    def able_replace(self, parent):
        if parent.cVar_replace.get() == 1:
            parent.weight_replace.configure(state="normal", bg="white")
            #parent.parameter_replace.configure(state="normal", bg="white")
        elif parent.cVar_replace.get() == 0:
            parent.weight_replace.configure(state="disabled", bg="gray60")
            #parent.parameter_replace.configure(state="disabled", bg="gray60")

    # Check resource error type which will be implement
    def apply_type(self, parent):
        ab_type = []
        if parent.cVar_skip.get() == 1:
            ab_type.append("skip")
        else:
            pass
        if parent.cVar_form.get() == 1:
            ab_type.append("form based")
        else:
            pass
        if parent.cVar_switch.get() == 1:
            ab_type.append("switch")
        else:
            pass
        if parent.cVar_insert.get() == 1:
            ab_type.append("insert")
        else:
            pass
        if parent.cVar_rework.get() == 1:
            ab_type.append("rework")
        else:
            pass
        if parent.cVar_moved.get() == 1:
            ab_type.append("moved")
        else:
            pass
        if parent.cVar_incom.get() == 1:
            ab_type.append("incomplete")
        else:
            pass
        if parent.cVar_replace.get() == 1:
            ab_type.append("replace")
        else:
            pass
        return ab_type

    # "apply_p_X" check parameter of resource error type "X"
    # "apply_w_X" check weight of resource error type "X"
    def apply_p_skip(self, parent):
        if parent.cVar_skip.get() == 1:
            m_skip = 1
        else:
            m_skip = 0
        return m_skip

    def apply_w_skip(self, parent):
        if parent.cVar_skip.get() == 1:
            if parent.weight_skip.get("1.0", "end-1c") == "":
                w_skip = 1
            else:
                w_skip = float(parent.weight_skip.get("1.0", "end-1c"))
        else:
            w_skip = 0
        return w_skip

    def apply_p_form(self, parent):
        if parent.cVar_form.get() == 1:
            m_form = int(parent.parameter_form.get("1.0", "end-1c"))
        else:
            m_form = 0
        return m_form

    def apply_w_form(self, parent):
        if parent.cVar_form.get() == 1:
            if parent.weight_form.get("1.0", "end-1c") == "":
                w_form = 1
            else:
                w_form = float(parent.weight_form.get("1.0", "end-1c"))
        else:
            w_form = 0
        return w_form

    def apply_p_moved(self, parent):
        if parent.cVar_moved.get() == 1:
            if parent.parameter_moved_Y.get("1.0", "end-1c") == "":
                Y = 0
            else:
                Y = int(parent.parameter_moved_Y.get("1.0", "end-1c"))
            if parent.parameter_moved_m.get("1.0", "end-1c") == "":
                m = 0
            else:
                m = int(parent.parameter_moved_m.get("1.0", "end-1c"))
            if parent.parameter_moved_d.get("1.0", "end-1c") == "":
                d = 0
            else:
                d = int(parent.parameter_moved_d.get("1.0", "end-1c"))
            if parent.parameter_moved_h.get("1.0", "end-1c") == "":
                h = 0
            else:
                h = int(parent.parameter_moved_h.get("1.0", "end-1c"))
            if parent.parameter_moved_M.get("1.0", "end-1c") == "":
                M = 0
            else:
                M = int(parent.parameter_moved_M.get("1.0", "end-1c"))
            h_moved = Y*946080000 + m*2592000 + d*86400 + h*3600 + M*60
        else:
            h_moved = 0
        return h_moved

    def apply_w_moved(self, parent):
        if parent.cVar_moved.get() == 1:
            if parent.weight_moved.get("1.0", "end-1c") == "":
                w_moved = 1
            else:
                w_moved = float(parent.weight_moved.get("1.0", "end-1c"))
        else:
            w_moved = 0
        return w_moved

    def apply_p_switch(self, parent):
        if parent.cVar_switch.get() == 1:
            m_switch = 1
        else:
            m_switch = 0
        return m_switch

    def apply_w_switch(self, parent):
        if parent.cVar_switch.get() == 1:
            if parent.weight_switch.get("1.0", "end-1c") == "":
                w_switch = 1
            else:
                w_switch = float(parent.weight_switch.get("1.0", "end-1c"))
        else:
            w_switch = 0
        return w_switch

    def apply_p_rework(self, parent):
        if parent.cVar_rework.get() == 1:
            m_rework = int(parent.parameter_rework.get("1.0", "end-1c"))
        else:
            m_rework = 0
        return m_rework

    def apply_w_rework(self, parent):
        if parent.cVar_rework.get() == 1:
            if parent.weight_rework.get("1.0", "end-1c") == "":
                w_rework = 1
            else:
                w_rework = float(parent.weight_rework.get("1.0", "end-1c"))
        else:
            w_rework = 0
        return w_rework

    def apply_p_insert(self, parent):
        if parent.cVar_insert.get() == 1:
            m_insert = int(parent.parameter_insert.get("1.0", "end-1c"))
        else:
            m_insert = 0
        return m_insert

    def apply_w_insert(self, parent):
        if parent.cVar_insert.get() == 1:
            if parent.weight_insert.get("1.0", "end-1c") == "":
                w_insert = 1
            else:
                w_insert = float(parent.weight_insert.get("1.0", "end-1c"))
        else:
            w_insert = 0
        return w_insert

    def apply_w_incomplete(self, parent):
        if parent.cVar_incom.get() == 1:
            if parent.weight_incom.get("1.0", "end-1c") == "":
                w_incom = 1
            else:
                w_incom = float(parent.weight_incom.get("1.0", "end-1c"))
        else:
            w_incom = 0
        return w_incom

    def apply_p_replace(self, parent):
        if parent.cVar_replace.get() == 1:
            m_replace = 1
        else:
            m_replace = 0
        return m_replace

    def apply_w_replace(self, parent):
        if parent.cVar_replace.get() == 1:
            if parent.weight_replace.get("1.0", "end-1c") == "":
                w_replace = 1
            else:
                w_replace = float(parent.weight_replace.get("1.0", "end-1c"))
        else:
            w_replace = 0
        return w_replace


    ##############################################################

    # Check system error type which will be implement
    def apply_type_sys(self, parent):
        ab_type = []
        if parent.cVar_skip_sys.get() == 1:
            ab_type.append("skip")
        else:
            pass
        if parent.cVar_form_sys.get() == 1:
            ab_type.append("form based")
        else:
            pass
        """if parent.cVar_lost_sys.get() == 1:
            ab_type.append("lost")
        else:
            pass"""
        if parent.cVar_cut_sys.get() == 1:
            ab_type.append("cut")
        else:
            pass
        return ab_type

    # "able_X_sys" check system error type "X" to make writing parameter & weight possible/impossible
    def able_skip_sys(self, parent):
        if parent.cVar_skip_sys.get() == 1:
            parent.weight_skip_sys.configure(state="normal", bg="white")
        elif parent.cVar_skip_sys.get() == 0:
            parent.weight_skip_sys.configure(state="disabled", bg="gray60")

    def able_form_sys(self, parent):
        if parent.cVar_form_sys.get() == 1:
            parent.weight_form_sys.configure(state="normal", bg="white")
        elif parent.cVar_form_sys.get() == 0:
            parent.weight_form_sys.configure(state="disabled", bg="gray60")


    def able_cut_sys(self, parent):
        if parent.cVar_cut_sys.get() == 1:
            parent.weight_cut_sys.configure(state="normal", bg="white")
        elif parent.cVar_cut_sys.get() == 0:
            parent.weight_cut_sys.configure(state="disabled", bg="gray60")


    # "apply_p_X_sys" check parameter of system error type "X"
    # "apply_w_X_sys" check weight of system error type "X"


    def apply_w_skip_sys(self, parent):
        if parent.cVar_skip_sys.get() == 1:
            if parent.weight_skip_sys.get("1.0", "end-1c") == "":
                w_skip_sys = 1
            else:
                w_skip_sys = float(parent.weight_skip_sys.get("1.0", "end-1c"))
        else:
            w_skip_sys = 0
        return w_skip_sys


    def apply_w_form_sys(self, parent):
        if parent.cVar_form_sys.get() == 1:
            if parent.weight_form_sys.get("1.0", "end-1c") == "":
                w_form_sys = 1
            else:
                w_form_sys = float(parent.weight_form_sys.get("1.0", "end-1c"))
        else:
            w_form_sys = 0
        return w_form_sys


    def apply_w_cut_sys(self, parent):
        if parent.cVar_cut_sys.get() == 1:
            if parent.weight_cut_sys.get("1.0", "end-1c") == "":
                w_cut_sys = 1
            else:
                w_cut_sys = float(parent.weight_cut_sys.get("1.0", "end-1c"))
        else:
            w_cut_sys = 0
        return w_cut_sys