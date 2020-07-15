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


class Inject_Anomaly:  # Jongyup page
    def __init__(self, root, *args, **kwargs):
        self.root = root
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root["bg"] = 'dark slate gray'
        self.root['padx'] = 7
        self.root['pady'] = 5
        Inject_Anomaly.root = root

        # Create main containers
        base_frame = Frame(root, bg='gray1', width=269, height=300)
        base_frame.grid(row=0, column=0, pady=(0, 7), sticky="nsew")
        base_frame_label_t = LabelFrame(base_frame, text="Progress Status", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray1', bd=3, padx=15, pady=15)
        Inject_Anomaly.text_progress = Text(base_frame_label_t, width=84, height=10, wrap=NONE)
        Inject_Anomaly.text_progress.grid(row=0, column=0, sticky="w")

        # Title widget
        base_frame_label1 = Label(base_frame, text='Anomaly generation', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray25', anchor="center", relief="raised")
        base_frame_label1.grid(row=0, column=0, sticky="w")
        base_frame_label1.config(width=92)  # 가로 길이


        # Frame setting
        base_frame_label2 = LabelFrame(base_frame, text=" Anomaly patterns for resource root ",
                                       font=("Consolas", 10, 'bold'),
                                       fg="white", bg='gray1', bd=3, padx=14, pady=15)
        base_frame_label4 = LabelFrame(base_frame, text=" Anomaly patterns for system root ",
                                       font=("Consolas", 10, 'bold'),
                                       fg="white", bg='gray1', bd=3, padx=14, pady=15)
        def seedBox(seed):
            Abnorm_p.seedBox = seed
            Abnorm_sys.seedBox = seed


        def seedBox_two(seed1, seed2):
            Abnorm_p.seedBox = seed1
            Abnorm_sys.seedBox = seed2

        # Implement resource error
        if (self.a == 1 and self.b == 0):
            self.root.geometry("663x570")
            base_frame_label2.place(x=10, y=35)
            base_frame_label_t.place(x=10, y=360)
            but_implement = tk.Button(base_frame, text="Apply", padx=25,
                                      command=lambda: [seedBox(seedBox1), Abnorm_p(self.extracted_data2).implement_resource(
                                          types=self.apply_type(root),
                                          mag=[self.apply_w_skip(root), self.apply_w_form(root), self.apply_w_switch(root),
                                               self.apply_w_insert(root), self.apply_w_rework(root), self.apply_w_moved(root),
                                               self.apply_w_incomplete(root), self.apply_w_replace(root)],
                                          m_skip=self.apply_p_skip(root), m_form=self.apply_p_form(root),
                                          m_switch=self.apply_p_switch(root), m_insert=self.apply_p_insert(root), h_moved=self.apply_p_moved(root),
                                          m_rework=self.apply_p_rework(root), m_replace=self.apply_p_replace(root))])  # extracted_data2 = event log with pass/fail(resource)
            but_implement.place(x=460, y=330)

            action2 = tk.Button(base_frame, text="Close", padx=20,
                                command= lambda: [s.configure('Red.TCheckbutton', foreground="white", background='gray1', font=("Consolas", 10, 'bold'))
                                    ,root.destroy()])
            action2.place(x=560, y=330)

        # Implement system error
        elif (self.a == 0 and self.b == 1):
            self.root.geometry("663x450")
            base_frame_label4.place(x=10, y=35)
            base_frame_label_t.place(x=10, y=240)
            but_implement_sys = tk.Button(base_frame, text="Apply", padx=25,
                                          command=lambda: [seedBox(seedBox2), Abnorm_sys(sys_file=self.system_down, log_file=self.data_with_system, old_file=None).implement_sys_single(df_log=None, df_sys=None,
                                              types_sys=self.apply_type_sys(root),
                                              mag_sys=[self.apply_w_skip_sys(root), self.apply_w_form_sys(root), self.apply_w_cut_sys(root)],
                                              h_skip=self.apply_p_skip_sys(root), h_form=self.apply_p_form_sys(root),
                                              h_cut=self.apply_p_cut_sys(root))])    # system_down = system down log, data_with_system = event log(system)
            but_implement_sys.place(x=460, y=210)

            action2 = tk.Button(base_frame, text="Close", padx=20,
                                command= lambda: [s.configure('Red.TCheckbutton', foreground="white", background='gray1', font=("Consolas", 10, 'bold')),
                                    root.destroy()])
            action2.place(x=560, y=210)

        # Implement resource and system error
        elif (self.a == 1 and self.b == 1):
            self.root.geometry("663x760")
            base_frame_label_t.place(x=10, y=550)
            base_frame_label2.place(x=10, y=35)
            base_frame_label4.place(x=10, y=330)
            but_implement = tk.Button(base_frame, text="Apply", padx=25,
                                      command=lambda: [seedBox_two(seedBox1,seedBox2) ,Abnorm_sys(sys_file=self.system_down,
                                                                 log_file=self.data_with_system,
                                                                 old_file=self.extracted_data2).implement_bind(
                                          types_sys=self.apply_type_sys(root), types_re=self.apply_type(root),
                                          mag_sys=[self.apply_w_skip_sys(root), self.apply_w_form_sys(root),
                                                   self.apply_w_cut_sys(root)],
                                          mag_re=[self.apply_w_skip(root), self.apply_w_form(root),
                                                  self.apply_w_switch(root),
                                                  self.apply_w_insert(root), self.apply_w_rework(root),
                                                  self.apply_w_moved(root),
                                                  self.apply_w_incomplete(root),
                                                  self.apply_w_replace(root)],
                                          m_skip=self.apply_p_skip(root), m_form=self.apply_p_form(root),
                                          m_switch=self.apply_p_switch(root), h_moved=self.apply_p_moved(root),
                                          m_rework=self.apply_p_rework(root), h_skip=self.apply_p_skip_sys(root),
                                          h_form=self.apply_p_form_sys(root),
                                          h_cut=self.apply_p_cut_sys(root))])
            but_implement.place(x=460, y=510)

            action2 = tk.Button(base_frame, text="Close", padx=20,
                                command= lambda: [s.configure('Red.TCheckbutton', foreground="white", background='gray1', font=("Consolas", 10, 'bold')),
                                    root.destroy()])
            action2.place(x=560, y=510)

        else:
            pass

        # Anomaly pattern widget - resource (mid)

        s = ttk.Style()
        s.configure('Red.TCheckbutton', foreground="aquamarine", background='gray40')


        # Set seed - resource (mid)
        seed_frame1 = Frame(base_frame_label2, bg='gray30', relief='ridge', borderwidth=2, width=15)
        seed_frame1.grid(row=0, column=0, padx=(0, 3), pady=(0, 5), stick='w')
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
        matrix_frame1.grid(row=1, column=0)

        # table00~ table02 : column name in table
        table00 = Frame(matrix_frame1, width=17, bg='gray25', highlightbackground="lavender", highlightthickness=1)
        table00.grid(row=0, column=0)
        text00 = Label(table00, text='Name', font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray25', anchor="center", width=12)
        text00.grid(row=0, column=0,  sticky="w", padx=6)
        table01 = Frame(matrix_frame1, bg='gray25', width=10, highlightbackground="lavender", highlightthickness=1)
        table01.grid(row=0, column=10)
        text01 = Label(table01, text='Weight', font=("Consolas", 10, 'bold'),
                       fg="white", bg='gray25', anchor="center", width=10)
        text01.grid(row=0, column=10, sticky="w", padx=5)
        table02 = Frame(matrix_frame1, bg='gray25', width=10, highlightbackground="lavender", highlightthickness=1)
        table02.grid(row=0, column=20)
        text02 = Label(table02, text='Parameter', font=("Consolas", 10, 'bold'),
                       fg="white", bg='gray25', anchor="center")
        text02.grid(row=0, column=20, sticky="w", padx=165)

        # table10~ table12 : skip
        table10 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table10.grid(row=10, column=0)
        root.cVar_skip = IntVar()
        root.cVar_skip.set(0)
        table11 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table11.grid(row=10, column=10)
        root.weight_skip = Text(table11, height=1, width=3)
        root.weight_skip.grid(row=10, column=10, padx=(30, 31), pady=2)
        root.weight_skip.configure(state="disabled", bg="gray60")
        table12 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table12.grid(row=10, column=20)
        p_skip_text = Label(table12, text="", font=("Consolas", 10, 'bold'),
                            fg="white", bg='gray40', anchor="center", width=12)
        p_skip_text.grid(row=50, column=0, padx=(145, 164))
        """root.parameter_skip = Text(table12, height=1, width=3)
        root.parameter_skip.grid(row=10, column=20, padx=(0, 150))
        root.parameter_skip.configure(state="disabled", bg="gray60")"""
        but_skip = ttk.Checkbutton(table10, text="skip", onvalue=1, offvalue=0, variable=root.cVar_skip,
                                   style='Red.TCheckbutton', width=10, command=lambda: self.able_skip(root))
        but_skip.grid(row=10, column=0, padx=(5, 4))

        # table60~ table62 : form-based
        table60 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table60.grid(row=60, column=0)
        root.cVar_form = IntVar()
        root.cVar_form.set(0)
        table61 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table61.grid(row=60, column=10)
        root.weight_form = Text(table61, height=1, width=3)
        root.weight_form.grid(row=60, column=10, padx=(30, 31), pady=2)
        root.weight_form.configure(state="disabled", bg="gray60")
        table62 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table62.grid(row=60, column=20)
        p_form_text = Label(table62, text="Max_length = ", font=("Consolas", 10, 'bold'),
                            fg="white", bg='gray40', anchor="center", width=12)
        p_form_text.grid(row=60, column=0, padx=(130, 0))
        root.parameter_form = Text(table62, height=1, width=3)
        root.parameter_form.grid(row=60, column=20, padx=(3, 151))
        root.parameter_form.configure(state="disabled", bg="gray60")
        but_form = ttk.Checkbutton(table60, text="form based", onvalue=1, offvalue=0, variable=root.cVar_form,
                                   style='Red.TCheckbutton', width=10, command=lambda: self.able_form(root))
        but_form.grid(row=60, column=0, padx=(5, 4))

        # table20~ table22 : switch
        table20 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table20.grid(row=20, column=0)
        root.cVar_switch = IntVar()
        root.cVar_switch.set(0)
        table21 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table21.grid(row=20, column=10)
        root.weight_switch = Text(table21, height=1, width=3)
        root.weight_switch.grid(row=20, column=10, padx=(30, 31), pady=2)
        root.weight_switch.configure(state="disabled", bg="gray60")
        table22 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table22.grid(row=20, column=20)
        p_switch_text = Label(table22, text="", font=("Consolas", 10, 'bold'),
                            fg="white", bg='gray40', anchor="center", width=12)
        p_switch_text.grid(row=20, column=0, padx=(145, 164))
        """root.parameter_switch = Text(table32, height=1, width=3)
        root.parameter_switch.grid(row=30, column=20, padx=(0, 150))
        root.parameter_switch.configure(state="disabled", bg="gray60")"""
        but_switch = ttk.Checkbutton(table20, text="switch", onvalue=1, offvalue=0, variable=root.cVar_switch,
                                    style='Red.TCheckbutton', width=10, command=lambda:self.able_switch(root))
        but_switch.grid(row=20, column=0, padx=(5, 4))

        # table70~ table72 : insert
        table70 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table70.grid(row=70, column=0)
        root.cVar_insert = IntVar()
        root.cVar_insert.set(0)
        table71 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table71.grid(row=70, column=10)
        root.weight_insert = Text(table71, height=1, width=3)
        root.weight_insert.grid(row=70, column=10, padx=(30, 31), pady=2)
        root.weight_insert.configure(state="disabled", bg="gray60")
        table72 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table72.grid(row=70, column=20)
        p_insert_text = Label(table72, text="Max_length = ", font=("Consolas", 10, 'bold'),
                            fg="white", bg='gray40', anchor="center", width=12)
        p_insert_text.grid(row=70, column=0, padx=(130, 0))
        root.parameter_insert = Text(table72, height=1, width=3)
        root.parameter_insert.grid(row=70, column=20, padx=(3, 151))
        root.parameter_insert.configure(state="disabled", bg="gray60")
        but_insert = ttk.Checkbutton(table70, text="insert", onvalue=1, offvalue=0, variable=root.cVar_insert,
                                     style='Red.TCheckbutton', width=10, command=lambda:self.able_insert(root))
        but_insert.grid(row=70, column=0, padx=(5, 4))

        # table50~ table52 : rework
        table50 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table50.grid(row=50, column=0)
        root.cVar_rework = IntVar()
        root.cVar_rework.set(0)
        table51 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table51.grid(row=50, column=10)
        root.weight_rework = Text(table51, height=1, width=3)
        root.weight_rework.grid(row=50, column=10, padx=(30, 31), pady=2)
        root.weight_rework.configure(state="disabled", bg="gray60")
        table52 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table52.grid(row=50, column=20)
        p_rework_text = Label(table52, text="Max_length = ", font=("Consolas", 10, 'bold'),
                            fg="white", bg='gray40', anchor="center", width=12)
        p_rework_text.grid(row=50, column=0, padx=(130, 0))
        root.parameter_rework = Text(table52, height=1, width=3)
        root.parameter_rework.grid(row=50, column=20, padx=(3, 151))
        root.parameter_rework.configure(state="disabled", bg="gray60")
        but_rework = ttk.Checkbutton(table50, text="rework", onvalue=1, offvalue=0, variable=root.cVar_rework,
                                     style='Red.TCheckbutton', width=10, command=lambda:self.able_rework(root))
        but_rework.grid(row=50, column=0, padx=(5, 4))

        # table80~ table82 : moved
        table80 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table80.grid(row=80, column=0)
        root.cVar_moved = IntVar()
        root.cVar_moved.set(0)
        table81 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table81.grid(row=80, column=10)
        root.weight_moved = Text(table81, height=1, width=3)
        root.weight_moved.grid(row=80, column=10, padx=(30, 31), pady=2)
        root.weight_moved.configure(state="disabled", bg="gray60")
        table82 = Frame(matrix_frame1, bg='gray40', width=100, highlightbackground="lavender", highlightthickness=1)
        table82.grid(row=80, column=20)
        p_moved_text = Label(table82, text="Max:", font=("Consolas", 10, 'bold'),
                              fg="white", bg='gray40', anchor="e", width=5)
        p_moved_text.grid(row=80, column=0)
        p_moved_Y_text = Label(table82, text="Y =", font=("Consolas", 10, 'bold'),
                            fg="white", bg='gray40', anchor="center", width=3)
        p_moved_Y_text.grid(row=80, column=10, padx=5.5)
        root.parameter_moved_Y = Text(table82, height=1, width=3)
        root.parameter_moved_Y.grid(row=80, column=30, padx=3.7)
        root.parameter_moved_Y.configure(state="disabled", bg="gray60")
        p_moved_m_text = Label(table82, text="m =", font=("Consolas", 10, 'bold'),
                                fg="white", bg='gray40', anchor="center", width=3)
        p_moved_m_text.grid(row=80, column=35, padx=4.5)
        root.parameter_moved_m = Text(table82, height=1, width=3)
        root.parameter_moved_m.grid(row=80, column=40, padx=5)
        root.parameter_moved_m.configure(state="disabled", bg="gray60")
        p_moved_d_text = Label(table82, text="d =", font=("Consolas", 10, 'bold'),
                                fg="white", bg='gray40', anchor="center", width=3)
        p_moved_d_text.grid(row=80, column=45, padx=4.5)
        root.parameter_moved_d = Text(table82, height=1, width=3)
        root.parameter_moved_d.grid(row=80, column=50, padx=5)
        root.parameter_moved_d.configure(state="disabled", bg="gray60")
        p_moved_h_text = Label(table82, text="h =", font=("Consolas", 10, 'bold'),
                                fg="white", bg='gray40', anchor="center", width=3)
        p_moved_h_text.grid(row=80, column=55, padx=4.5)
        root.parameter_moved_h = Text(table82, height=1, width=3)
        root.parameter_moved_h.grid(row=80, column=60, padx=5)
        root.parameter_moved_h.configure(state="disabled", bg="gray60")
        p_moved_M_text = Label(table82, text="M =", font=("Consolas", 10, 'bold'),
                                fg="white", bg='gray40', anchor="center", width=3)
        p_moved_M_text.grid(row=80, column=65, padx=4.4)
        root.parameter_moved_M = Text(table82, height=1, width=3)
        root.parameter_moved_M.grid(row=80, column=70, padx=4.7)
        root.parameter_moved_M.configure(state="disabled", bg="gray60")
        but_moved = ttk.Checkbutton(table80, text="moved", onvalue=1, offvalue=0, variable=root.cVar_moved,
                                     style='Red.TCheckbutton', width=10, command=lambda:self.able_moved(root))
        but_moved.grid(row=80, column=0, padx=(5, 4))

        # table40~ table42 : incomplete
        table40 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table40.grid(row=40, column=0)
        root.cVar_incom = IntVar()
        root.cVar_incom.set(0)
        table41 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table41.grid(row=40, column=10)
        root.weight_incom = Text(table41, height=1, width=3)
        root.weight_incom.grid(row=40, column=10, padx=(30, 31), pady=2)
        root.weight_incom.configure(state="disabled", bg="gray60")
        table42 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table42.grid(row=40, column=20)
        p_incomplete_text = Label(table42, text="", font=("Consolas", 10, 'bold'),
                            fg="white", bg='gray40', anchor="center", width=12)
        p_incomplete_text.grid(row=40, column=0, padx=(145, 164))

        but_incom = ttk.Checkbutton(table40, text="incomplete", onvalue=1, offvalue=0, variable=root.cVar_incom,
                                    style='Red.TCheckbutton', width=10, command=lambda:self.able_incom(root))
        but_incom.grid(row=40, column=0, padx=(5, 4))

        # table30~ table32 : replace
        table30 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table30.grid(row=30, column=0)
        root.cVar_replace = IntVar()
        root.cVar_replace.set(0)
        table31 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table31.grid(row=30, column=10)
        root.weight_replace = Text(table31, height=1, width=3)
        root.weight_replace.grid(row=30, column=10, padx=(30, 31), pady=2)
        root.weight_replace.configure(state="disabled", bg="gray60")
        table32 = Frame(matrix_frame1, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        table32.grid(row=30, column=20)
        p_replace_text = Label(table32, text="", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=12)
        p_replace_text.grid(row=30, column=0, padx=(145, 164))
        """root.parameter_replace = Text(table32, height=1, width=3)
        root.parameter_replace.grid(row=30, column=20, padx=(0, 150))
        root.parameter_replace.configure(state="disabled", bg="gray60")"""
        but_replace = ttk.Checkbutton(table30, text="replace", onvalue=1, offvalue=0, variable=root.cVar_replace,
                                    style='Red.TCheckbutton', width=10, command=lambda: self.able_replace(root))
        but_replace.grid(row=30, column=0, padx=(5, 4))


#####################################################################################

        # Anomaly pattern widget - system (mid-down)

        s = ttk.Style()
        s.configure('Red.TCheckbutton', foreground="aquamarine", background='gray40')

        # Set seed - system (mid-down)
        seed_frame2 = Frame(base_frame_label4, bg='gray30', relief='ridge', borderwidth=2, width=15)
        seed_frame2.grid(row=0, column=0, padx=(0, 3), pady=(0, 5), stick='w')
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
        matrix_frame2.grid(row=1, column=0)
        t00 = Frame(matrix_frame2, width=17, bg='gray25', highlightbackground="lavender", highlightthickness=1)
        t00.grid(row=0, column=0)
        txt00 = Label(t00, text='Name', font=("Consolas", 10, 'bold'),
                      fg="white", bg='gray25', anchor="center", width=12)
        txt00.grid(row=0, column=0, sticky="w", padx=6)
        t01 = Frame(matrix_frame2, bg='gray25', width=10, highlightbackground="lavender", highlightthickness=1)
        t01.grid(row=0, column=10)
        txt01 = Label(t01, text='Weight', font=("Consolas", 10, 'bold'),
                      fg="white", bg='gray25', anchor="center", width=10)
        txt01.grid(row=0, column=10, sticky="w", padx=5)
        t02 = Frame(matrix_frame2, bg='gray25', width=10, highlightbackground="lavender", highlightthickness=1)
        t02.grid(row=0, column=20)
        txt02 = Label(t02, text='Parameter', font=("Consolas", 10, 'bold'),
                      fg="white", bg='gray25', anchor="center")
        txt02.grid(row=0, column=20, sticky="w", padx=165)

        # t10~ t12 : skip - system
        t10 = Frame(matrix_frame2, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        t10.grid(row=10, column=0)
        root.cVar_skip_sys = IntVar()
        root.cVar_skip_sys.set(0)
        t11 = Frame(matrix_frame2, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        t11.grid(row=10, column=10)
        root.weight_skip_sys = Text(t11, height=1, width=3)
        root.weight_skip_sys.grid(row=10, column=10, padx=(30, 31), pady=2)
        root.weight_skip_sys.configure(state="disabled", bg="gray60")
        t12 = Frame(matrix_frame2, bg='gray40', width=100, highlightbackground="lavender", highlightthickness=1)
        t12.grid(row=10, column=20)
        p_skip_text_sys = Label(t12, text="Max:", font=("Consolas", 10, 'bold'),
                                fg="white", bg='gray40', anchor="e", width=5)
        p_skip_text_sys.grid(row=10, column=0)
        p_skip_Y_text_sys = Label(t12, text="Y =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_skip_Y_text_sys.grid(row=10, column=10, padx=(4.5, 4))
        root.parameter_skip_Y_sys = Text(t12, height=1, width=3)
        root.parameter_skip_Y_sys.grid(row=10, column=30, padx=5)
        root.parameter_skip_Y_sys.configure(state="disabled", bg="gray60")
        p_skip_m_text_sys = Label(t12, text="m =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_skip_m_text_sys.grid(row=10, column=35, padx=5)
        root.parameter_skip_m_sys = Text(t12, height=1, width=3)
        root.parameter_skip_m_sys.grid(row=10, column=40, padx=5)
        root.parameter_skip_m_sys.configure(state="disabled", bg="gray60")
        p_skip_d_text_sys = Label(t12, text="d =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_skip_d_text_sys.grid(row=10, column=45, padx=5)
        root.parameter_skip_d_sys = Text(t12, height=1, width=3)
        root.parameter_skip_d_sys.grid(row=10, column=50, padx=5)
        root.parameter_skip_d_sys.configure(state="disabled", bg="gray60")
        p_skip_h_text_sys = Label(t12, text="h =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_skip_h_text_sys.grid(row=10, column=55, padx=5)
        root.parameter_skip_h_sys = Text(t12, height=1, width=3)
        root.parameter_skip_h_sys.grid(row=10, column=60, padx=5)
        root.parameter_skip_h_sys.configure(state="disabled", bg="gray60")
        p_skip_M_text_sys = Label(t12, text="M =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_skip_M_text_sys.grid(row=10, column=65, padx=(5, 5.5))
        root.parameter_skip_M_sys = Text(t12, height=1, width=3)
        root.parameter_skip_M_sys.grid(row=10, column=70, padx=4)
        root.parameter_skip_M_sys.configure(state="disabled", bg="gray60")
        but_skip_sys = ttk.Checkbutton(t10, text="skip", onvalue=1, offvalue=0, variable=root.cVar_skip_sys,
                                       style='Red.TCheckbutton', width=10, command=lambda: self.able_skip_sys(root))
        but_skip_sys.grid(row=10, column=0, padx=(5,4))

        # t20~ t22 : form-based - system
        t20 = Frame(matrix_frame2, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        t20.grid(row=20, column=0)
        root.cVar_form_sys = IntVar()
        root.cVar_form_sys.set(0)
        t21 = Frame(matrix_frame2, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        t21.grid(row=20, column=10)
        root.weight_form_sys = Text(t21, height=1, width=3)
        root.weight_form_sys.grid(row=20, column=10, padx=(30, 31), pady=2)
        root.weight_form_sys.configure(state="disabled", bg="gray60")
        t22 = Frame(matrix_frame2, bg='gray40', width=100, highlightbackground="lavender", highlightthickness=1)
        t22.grid(row=20, column=20)
        p_form_text_sys = Label(t22, text="Max:", font=("Consolas", 10, 'bold'),
                                fg="white", bg='gray40', anchor="e", width=5)
        p_form_text_sys.grid(row=20, column=0)
        p_form_Y_text_sys = Label(t22, text="Y =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_form_Y_text_sys.grid(row=20, column=10, padx=(4.5, 4))
        root.parameter_form_Y_sys = Text(t22, height=1, width=3)
        root.parameter_form_Y_sys.grid(row=20, column=30, padx=5)
        root.parameter_form_Y_sys.configure(state="disabled", bg="gray60")
        p_form_m_text_sys = Label(t22, text="m =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_form_m_text_sys.grid(row=20, column=35, padx=5)
        root.parameter_form_m_sys = Text(t22, height=1, width=3)
        root.parameter_form_m_sys.grid(row=20, column=40, padx=5)
        root.parameter_form_m_sys.configure(state="disabled", bg="gray60")
        p_form_d_text_sys = Label(t22, text="d =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_form_d_text_sys.grid(row=20, column=45, padx=5)
        root.parameter_form_d_sys = Text(t22, height=1, width=3)
        root.parameter_form_d_sys.grid(row=20, column=50, padx=5)
        root.parameter_form_d_sys.configure(state="disabled", bg="gray60")
        p_form_h_text_sys = Label(t22, text="h =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_form_h_text_sys.grid(row=20, column=55, padx=5)
        root.parameter_form_h_sys = Text(t22, height=1, width=3)
        root.parameter_form_h_sys.grid(row=20, column=60, padx=5)
        root.parameter_form_h_sys.configure(state="disabled", bg="gray60")
        p_form_M_text_sys = Label(t22, text="M =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_form_M_text_sys.grid(row=20, column=65, padx=(5, 5.5))
        root.parameter_form_M_sys = Text(t22, height=1, width=3)
        root.parameter_form_M_sys.grid(row=20, column=70, padx=4)
        root.parameter_form_M_sys.configure(state="disabled", bg="gray60")
        but_form_sys = ttk.Checkbutton(t20, text="form based", onvalue=1, offvalue=0, variable=root.cVar_form_sys,
                                       style='Red.TCheckbutton', width=10, command=lambda: self.able_form_sys(root))
        but_form_sys.grid(row=20, column=0, padx=(5, 4))

        # t30~ t32 : cut - system
        t30 = Frame(matrix_frame2, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        t30.grid(row=30, column=0)
        root.cVar_cut_sys = IntVar()
        root.cVar_cut_sys.set(0)
        t31 = Frame(matrix_frame2, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        t31.grid(row=30, column=10)
        root.weight_cut_sys = Text(t31, height=1, width=3)
        root.weight_cut_sys.grid(row=30, column=10, padx=(30, 31), pady=2)
        root.weight_cut_sys.configure(state="disabled", bg="gray60")
        t32 = Frame(matrix_frame2, bg='gray40', width=100, highlightbackground="lavender", highlightthickness=1)
        t32.grid(row=30, column=20)
        p_cut_text_sys = Label(t32, text="Max:", font=("Consolas", 10, 'bold'),
                               fg="white", bg='gray40', anchor="e", width=5)
        p_cut_text_sys.grid(row=30, column=0)
        p_cut_Y_text_sys = Label(t32, text="Y =", font=("Consolas", 10, 'bold'),
                                 fg="white", bg='gray40', anchor="center", width=3)
        p_cut_Y_text_sys.grid(row=30, column=10, padx=(4.5, 4))
        root.parameter_cut_Y_sys = Text(t32, height=1, width=3)
        root.parameter_cut_Y_sys.grid(row=30, column=30, padx=5)
        root.parameter_cut_Y_sys.configure(state="disabled", bg="gray60")
        p_cut_m_text_sys = Label(t32, text="m =", font=("Consolas", 10, 'bold'),
                                 fg="white", bg='gray40', anchor="center", width=3)
        p_cut_m_text_sys.grid(row=30, column=35, padx=5)
        root.parameter_cut_m_sys = Text(t32, height=1, width=3)
        root.parameter_cut_m_sys.grid(row=30, column=40, padx=5)
        root.parameter_cut_m_sys.configure(state="disabled", bg="gray60")
        p_cut_d_text_sys = Label(t32, text="d =", font=("Consolas", 10, 'bold'),
                                 fg="white", bg='gray40', anchor="center", width=3)
        p_cut_d_text_sys.grid(row=30, column=45, padx=5)
        root.parameter_cut_d_sys = Text(t32, height=1, width=3)
        root.parameter_cut_d_sys.grid(row=30, column=50, padx=5)
        root.parameter_cut_d_sys.configure(state="disabled", bg="gray60")
        p_cut_h_text_sys = Label(t32, text="h =", font=("Consolas", 10, 'bold'),
                                 fg="white", bg='gray40', anchor="center", width=3)
        p_cut_h_text_sys.grid(row=30, column=55, padx=5)
        root.parameter_cut_h_sys = Text(t32, height=1, width=3)
        root.parameter_cut_h_sys.grid(row=30, column=60, padx=5)
        root.parameter_cut_h_sys.configure(state="disabled", bg="gray60")
        p_cut_M_text_sys = Label(t32, text="M =", font=("Consolas", 10, 'bold'),
                                 fg="white", bg='gray40', anchor="center", width=3)
        p_cut_M_text_sys.grid(row=30, column=65, padx=(5, 5.5))
        root.parameter_cut_M_sys = Text(t32, height=1, width=3)
        root.parameter_cut_M_sys.grid(row=30, column=70, padx=4)
        root.parameter_cut_M_sys.configure(state="disabled", bg="gray60")
        but_cut_sys = ttk.Checkbutton(t30, text="cut", onvalue=1, offvalue=0, variable=root.cVar_cut_sys,
                                      style='Red.TCheckbutton', width=10, command=lambda: self.able_cut_sys(root))
        but_cut_sys.grid(row=30, column=0, padx=(5, 4))

        """# t40~ t42 : lost - system
        t40 = Frame(matrix_frame2, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        t40.grid(row=40, column=0)
        root.cVar_lost_sys = IntVar()
        root.cVar_lost_sys.set(0)
        t41 = Frame(matrix_frame2, bg='gray40', width=10, highlightbackground="lavender", highlightthickness=1)
        t41.grid(row=40, column=10)
        root.weight_lost_sys = Text(t41, height=1, width=3)
        root.weight_lost_sys.grid(row=40, column=10, padx=25, pady=2)
        root.weight_lost_sys.configure(state="disabled", bg="gray60")
        t42 = Frame(matrix_frame2, bg='gray40', width=100, highlightbackground="lavender", highlightthickness=1)
        t42.grid(row=40, column=20)
        p_lost_text_sys = Label(t42, text="Max:", font=("Consolas", 10, 'bold'),
                                fg="white", bg='gray40', anchor="e", width=5)
        p_lost_text_sys.grid(row=40, column=0)
        p_lost_Y_text_sys = Label(t42, text="Y =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_lost_Y_text_sys.grid(row=40, column=10, padx=5)
        root.parameter_lost_Y_sys = Text(t42, height=1, width=3)
        root.parameter_lost_Y_sys.grid(row=40, column=30, padx=5)
        root.parameter_lost_Y_sys.configure(state="disabled", bg="gray60")
        p_lost_m_text_sys = Label(t42, text="m =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_lost_m_text_sys.grid(row=40, column=35, padx=5)
        root.parameter_lost_m_sys = Text(t42, height=1, width=3)
        root.parameter_lost_m_sys.grid(row=40, column=40, padx=5)
        root.parameter_lost_m_sys.configure(state="disabled", bg="gray60")
        p_lost_d_text_sys = Label(t42, text="d =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_lost_d_text_sys.grid(row=40, column=45, padx=5)
        root.parameter_lost_d_sys = Text(t42, height=1, width=3)
        root.parameter_lost_d_sys.grid(row=40, column=50, padx=5)
        root.parameter_lost_d_sys.configure(state="disabled", bg="gray60")
        p_lost_h_text_sys = Label(t42, text="h =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_lost_h_text_sys.grid(row=40, column=55, padx=5)
        root.parameter_lost_h_sys = Text(t42, height=1, width=3)
        root.parameter_lost_h_sys.grid(row=40, column=60, padx=5)
        root.parameter_lost_h_sys.configure(state="disabled", bg="gray60")
        p_lost_M_text_sys = Label(t42, text="M =", font=("Consolas", 10, 'bold'),
                                  fg="white", bg='gray40', anchor="center", width=3)
        p_lost_M_text_sys.grid(row=40, column=65, padx=5)
        root.parameter_lost_M_sys = Text(t42, height=1, width=3)
        root.parameter_lost_M_sys.grid(row=40, column=70, padx=5)
        root.parameter_lost_M_sys.configure(state="disabled", bg="gray60")
        but_lost_sys = ttk.Checkbutton(t40, text="lost", onvalue=1, offvalue=0, variable=root.cVar_lost_sys,
                                       style='Red.TCheckbutton', width=10, command=lambda: self.able_lost_sys(root))
        but_lost_sys.grid(row=40, column=0)"""

    #####################################################################################

    # "able_X" check resource error type "X" to make writing parameter & weight possible/impossible
    def able_skip(self, root):
        if root.cVar_skip.get() == 1:
            root.weight_skip.configure(state="normal", bg="white")
            #root.parameter_skip.configure(state="normal", bg="white")
        elif root.cVar_skip.get() == 0:
            root.weight_skip.configure(state="disabled", bg="gray60")
            #root.parameter_skip.configure(state="disabled", bg="gray60")

    def able_form(self, root):
        if root.cVar_form.get() == 1:
            root.weight_form.configure(state="normal", bg="white")
            root.parameter_form.configure(state="normal", bg="white")
        elif root.cVar_form.get() == 0:
            root.weight_form.configure(state="disabled", bg="gray60")
            root.parameter_form.configure(state="disabled", bg="gray60")

    def able_switch(self, root):
        if root.cVar_switch.get() == 1:
            root.weight_switch.configure(state="normal", bg="white")
            #root.parameter_switch.configure(state="normal", bg="white")
        elif root.cVar_switch.get() == 0:
            root.weight_switch.configure(state="disabled", bg="gray60")
            #root.parameter_switch.configure(state="disabled", bg="gray60")

    def able_insert(self, root):
        if root.cVar_insert.get() == 1:
            root.weight_insert.configure(state="normal", bg="white")
            root.parameter_insert.configure(state="normal", bg="white")
        elif root.cVar_insert.get() == 0:
            root.weight_insert.configure(state="disabled", bg="gray60")
            root.parameter_insert.configure(state="disabled", bg="gray60")

    def able_rework(self, root):
        if root.cVar_rework.get() == 1:
            root.weight_rework.configure(state="normal", bg="white")
            root.parameter_rework.configure(state="normal", bg="white")
        elif root.cVar_rework.get() == 0:
            root.weight_rework.configure(state="disabled", bg="gray60")
            root.parameter_rework.configure(state="disabled", bg="gray60")

    def able_moved(self, root):
        if root.cVar_moved.get() == 1:
            root.weight_moved.configure(state="normal", bg="white")
            root.parameter_moved_Y.configure(state="normal", bg="white")
            root.parameter_moved_m.configure(state="normal", bg="white")
            root.parameter_moved_d.configure(state="normal", bg="white")
            root.parameter_moved_h.configure(state="normal", bg="white")
            root.parameter_moved_M.configure(state="normal", bg="white")
        elif root.cVar_moved.get() == 0:
            root.weight_moved.configure(state="disabled", bg="gray60")
            root.parameter_moved_Y.configure(state="disabled", bg="gray60")
            root.parameter_moved_m.configure(state="disabled", bg="gray60")
            root.parameter_moved_d.configure(state="disabled", bg="gray60")
            root.parameter_moved_h.configure(state="disabled", bg="gray60")
            root.parameter_moved_M.configure(state="disabled", bg="gray60")

    def able_incom(self, root):
        if root.cVar_incom.get() == 1:
            root.weight_incom.configure(state="normal", bg="white")
        elif root.cVar_incom.get() == 0:
            root.weight_incom.configure(state="disabled", bg="gray60")
        else:
            pass

    def able_replace(self, root):
        if root.cVar_replace.get() == 1:
            root.weight_replace.configure(state="normal", bg="white")
            #root.parameter_replace.configure(state="normal", bg="white")
        elif root.cVar_replace.get() == 0:
            root.weight_replace.configure(state="disabled", bg="gray60")
            #root.parameter_replace.configure(state="disabled", bg="gray60")

    # Check resource error type which will be implement
    def apply_type(self, root):
        ab_type = []
        if root.cVar_skip.get() == 1:
            ab_type.append("skip")
        else:
            pass
        if root.cVar_form.get() == 1:
            ab_type.append("form based")
        else:
            pass
        if root.cVar_switch.get() == 1:
            ab_type.append("switch")
        else:
            pass
        if root.cVar_insert.get() == 1:
            ab_type.append("insert")
        else:
            pass
        if root.cVar_rework.get() == 1:
            ab_type.append("rework")
        else:
            pass
        if root.cVar_moved.get() == 1:
            ab_type.append("moved")
        else:
            pass
        if root.cVar_incom.get() == 1:
            ab_type.append("incomplete")
        else:
            pass
        if root.cVar_replace.get() == 1:
            ab_type.append("replace")
        else:
            pass
        return ab_type

    # "apply_p_X" check parameter of resource error type "X"
    # "apply_w_X" check weight of resource error type "X"
    def apply_p_skip(self, root):
        if root.cVar_skip.get() == 1:
            m_skip = 1
        else:
            m_skip = 0
        return m_skip

    def apply_w_skip(self, root):
        if root.cVar_skip.get() == 1:
            if root.weight_skip.get("1.0", "end-1c") == "":
                w_skip = 1
            else:
                w_skip = float(root.weight_skip.get("1.0", "end-1c"))
        else:
            w_skip = 0
        return w_skip

    def apply_p_form(self, root):
        if root.cVar_form.get() == 1:
            m_form = int(root.parameter_form.get("1.0", "end-1c"))
        else:
            m_form = 0
        return m_form

    def apply_w_form(self, root):
        if root.cVar_form.get() == 1:
            if root.weight_form.get("1.0", "end-1c") == "":
                w_form = 1
            else:
                w_form = float(root.weight_form.get("1.0", "end-1c"))
        else:
            w_form = 0
        return w_form

    def apply_p_moved(self, root):
        if root.cVar_moved.get() == 1:
            if root.parameter_moved_Y.get("1.0", "end-1c") == "":
                Y = 0
            else:
                Y = int(root.parameter_moved_Y.get("1.0", "end-1c"))
            if root.parameter_moved_m.get("1.0", "end-1c") == "":
                m = 0
            else:
                m = int(root.parameter_moved_m.get("1.0", "end-1c"))
            if root.parameter_moved_d.get("1.0", "end-1c") == "":
                d = 0
            else:
                d = int(root.parameter_moved_d.get("1.0", "end-1c"))
            if root.parameter_moved_h.get("1.0", "end-1c") == "":
                h = 0
            else:
                h = int(root.parameter_moved_h.get("1.0", "end-1c"))
            if root.parameter_moved_M.get("1.0", "end-1c") == "":
                M = 0
            else:
                M = int(root.parameter_moved_M.get("1.0", "end-1c"))
            h_moved = Y*946080000 + m*2592000 + d*86400 + h*3600 + M*60
        else:
            h_moved = 0
        return h_moved

    def apply_w_moved(self, root):
        if root.cVar_moved.get() == 1:
            if root.weight_moved.get("1.0", "end-1c") == "":
                w_moved = 1
            else:
                w_moved = float(root.weight_moved.get("1.0", "end-1c"))
        else:
            w_moved = 0
        return w_moved

    def apply_p_switch(self, root):
        if root.cVar_switch.get() == 1:
            m_switch = 1
        else:
            m_switch = 0
        return m_switch

    def apply_w_switch(self, root):
        if root.cVar_switch.get() == 1:
            if root.weight_switch.get("1.0", "end-1c") == "":
                w_switch = 1
            else:
                w_switch = float(root.weight_switch.get("1.0", "end-1c"))
        else:
            w_switch = 0
        return w_switch

    def apply_p_rework(self, root):
        if root.cVar_rework.get() == 1:
            m_rework = int(root.parameter_rework.get("1.0", "end-1c"))
        else:
            m_rework = 0
        return m_rework

    def apply_w_rework(self, root):
        if root.cVar_rework.get() == 1:
            if root.weight_rework.get("1.0", "end-1c") == "":
                w_rework = 1
            else:
                w_rework = float(root.weight_rework.get("1.0", "end-1c"))
        else:
            w_rework = 0
        return w_rework

    def apply_p_insert(self, root):
        if root.cVar_insert.get() == 1:
            m_insert = int(root.parameter_insert.get("1.0", "end-1c"))
        else:
            m_insert = 0
        return m_insert

    def apply_w_insert(self, root):
        if root.cVar_insert.get() == 1:
            if root.weight_insert.get("1.0", "end-1c") == "":
                w_insert = 1
            else:
                w_insert = float(root.weight_insert.get("1.0", "end-1c"))
        else:
            w_insert = 0
        return w_insert

    def apply_w_incomplete(self, root):
        if root.cVar_incom.get() == 1:
            if root.weight_incom.get("1.0", "end-1c") == "":
                w_incom = 1
            else:
                w_incom = float(root.weight_incom.get("1.0", "end-1c"))
        else:
            w_incom = 0
        return w_incom

    def apply_p_replace(self, root):
        if root.cVar_replace.get() == 1:
            m_replace = 1
        else:
            m_replace = 0
        return m_replace

    def apply_w_replace(self, root):
        if root.cVar_replace.get() == 1:
            if root.weight_replace.get("1.0", "end-1c") == "":
                w_replace = 1
            else:
                w_replace = float(root.weight_replace.get("1.0", "end-1c"))
        else:
            w_replace = 0
        return w_replace


    ##############################################################

    # Check system error type which will be implement
    def apply_type_sys(self, root):
        ab_type = []
        if root.cVar_skip_sys.get() == 1:
            ab_type.append("skip")
        else:
            pass
        if root.cVar_form_sys.get() == 1:
            ab_type.append("form based")
        else:
            pass
        """if root.cVar_lost_sys.get() == 1:
            ab_type.append("lost")
        else:
            pass"""
        if root.cVar_cut_sys.get() == 1:
            ab_type.append("cut")
        else:
            pass
        return ab_type

    # "able_X_sys" check system error type "X" to make writing parameter & weight possible/impossible
    def able_skip_sys(self, root):
        if root.cVar_skip_sys.get() == 1:
            root.weight_skip_sys.configure(state="normal", bg="white")
            root.parameter_skip_Y_sys.configure(state="normal", bg="white")
            root.parameter_skip_m_sys.configure(state="normal", bg="white")
            root.parameter_skip_d_sys.configure(state="normal", bg="white")
            root.parameter_skip_h_sys.configure(state="normal", bg="white")
            root.parameter_skip_M_sys.configure(state="normal", bg="white")
        elif root.cVar_skip_sys.get() == 0:
            root.weight_skip_sys.configure(state="disabled", bg="gray60")
            root.parameter_skip_Y_sys.configure(state="disabled", bg="gray60")
            root.parameter_skip_m_sys.configure(state="disabled", bg="gray60")
            root.parameter_skip_d_sys.configure(state="disabled", bg="gray60")
            root.parameter_skip_h_sys.configure(state="disabled", bg="gray60")
            root.parameter_skip_M_sys.configure(state="disabled", bg="gray60")

    def able_form_sys(self, root):
        if root.cVar_form_sys.get() == 1:
            root.weight_form_sys.configure(state="normal", bg="white")
            root.parameter_form_Y_sys.configure(state="normal", bg="white")
            root.parameter_form_m_sys.configure(state="normal", bg="white")
            root.parameter_form_d_sys.configure(state="normal", bg="white")
            root.parameter_form_h_sys.configure(state="normal", bg="white")
            root.parameter_form_M_sys.configure(state="normal", bg="white")
        elif root.cVar_form_sys.get() == 0:
            root.weight_form_sys.configure(state="disabled", bg="gray60")
            root.parameter_form_Y_sys.configure(state="disabled", bg="gray60")
            root.parameter_form_m_sys.configure(state="disabled", bg="gray60")
            root.parameter_form_d_sys.configure(state="disabled", bg="gray60")
            root.parameter_form_h_sys.configure(state="disabled", bg="gray60")
            root.parameter_form_M_sys.configure(state="disabled", bg="gray60")

    """def able_lost_sys(self, root):
        if root.cVar_lost_sys.get() == 1:
            root.weight_lost_sys.configure(state="normal", bg="white")
            root.parameter_lost_Y_sys.configure(state="normal", bg="white")
            root.parameter_lost_m_sys.configure(state="normal", bg="white")
            root.parameter_lost_d_sys.configure(state="normal", bg="white")
            root.parameter_lost_h_sys.configure(state="normal", bg="white")
            root.parameter_lost_M_sys.configure(state="normal", bg="white")
        elif root.cVar_lost_sys.get() == 0:
            root.weight_lost_sys.configure(state="disabled", bg="gray60")
            root.parameter_lost_Y_sys.configure(state="disabled", bg="gray60")
            root.parameter_lost_m_sys.configure(state="disabled", bg="gray60")
            root.parameter_lost_d_sys.configure(state="disabled", bg="gray60")
            root.parameter_lost_h_sys.configure(state="disabled", bg="gray60")
            root.parameter_lost_M_sys.configure(state="disabled", bg="gray60")"""

    def able_cut_sys(self, root):
        if root.cVar_cut_sys.get() == 1:
            root.weight_cut_sys.configure(state="normal", bg="white")
            root.parameter_cut_Y_sys.configure(state="normal", bg="white")
            root.parameter_cut_m_sys.configure(state="normal", bg="white")
            root.parameter_cut_d_sys.configure(state="normal", bg="white")
            root.parameter_cut_h_sys.configure(state="normal", bg="white")
            root.parameter_cut_M_sys.configure(state="normal", bg="white")
        elif root.cVar_cut_sys.get() == 0:
            root.weight_cut_sys.configure(state="disabled", bg="gray60")
            root.parameter_cut_Y_sys.configure(state="disabled", bg="gray60")
            root.parameter_cut_m_sys.configure(state="disabled", bg="gray60")
            root.parameter_cut_d_sys.configure(state="disabled", bg="gray60")
            root.parameter_cut_h_sys.configure(state="disabled", bg="gray60")
            root.parameter_cut_M_sys.configure(state="disabled", bg="gray60")

    # "apply_p_X_sys" check parameter of system error type "X"
    # "apply_w_X_sys" check weight of system error type "X"
    def apply_p_skip_sys(self, root):
        if root.cVar_skip_sys.get() == 1:
            if root.parameter_skip_Y_sys.get("1.0", "end-1c") == "":
                Y = 0
            else:
                Y = int(root.parameter_skip_Y_sys.get("1.0", "end-1c"))
            if root.parameter_skip_m_sys.get("1.0", "end-1c") == "":
                m = 0
            else:
                m = int(root.parameter_skip_m_sys.get("1.0", "end-1c"))
            if root.parameter_skip_d_sys.get("1.0", "end-1c") == "":
                d = 0
            else:
                d = int(root.parameter_skip_d_sys.get("1.0", "end-1c"))
            if root.parameter_skip_h_sys.get("1.0", "end-1c") == "":
                h = 0
            else:
                h = int(root.parameter_skip_h_sys.get("1.0", "end-1c"))
            if root.parameter_skip_M_sys.get("1.0", "end-1c") == "":
                M = 0
            else:
                M = int(root.parameter_skip_M_sys.get("1.0", "end-1c"))
            h_skip = Y*946080000 + m*2592000 + d*86400 + h*3600 + M*60
        else:
            h_skip = 0
        return h_skip

    def apply_w_skip_sys(self, root):
        if root.cVar_skip_sys.get() == 1:
            if root.weight_skip_sys.get("1.0", "end-1c") == "":
                w_skip_sys = 1
            else:
                w_skip_sys = float(root.weight_skip_sys.get("1.0", "end-1c"))
        else:
            w_skip_sys = 0
        return w_skip_sys

    def apply_p_form_sys(self, root):
        if root.cVar_form_sys.get() == 1:
            if root.parameter_form_Y_sys.get("1.0", "end-1c") == "":
                Y = 0
            else:
                Y = int(root.parameter_form_Y_sys.get("1.0", "end-1c"))
            if root.parameter_form_m_sys.get("1.0", "end-1c") == "":
                m = 0
            else:
                m = int(root.parameter_form_m_sys.get("1.0", "end-1c"))
            if root.parameter_form_d_sys.get("1.0", "end-1c") == "":
                d = 0
            else:
                d = int(root.parameter_form_d_sys.get("1.0", "end-1c"))
            if root.parameter_form_h_sys.get("1.0", "end-1c") == "":
                h = 0
            else:
                h = int(root.parameter_form_h_sys.get("1.0", "end-1c"))
            if root.parameter_form_M_sys.get("1.0", "end-1c") == "":
                M = 0
            else:
                M = int(root.parameter_form_M_sys.get("1.0", "end-1c"))
            h_form = Y*946080000 + m*2592000 + d*86400 + h*3600 + M*60
        else:
            h_form = 0
        return h_form

    def apply_w_form_sys(self, root):
        if root.cVar_form_sys.get() == 1:
            if root.weight_form_sys.get("1.0", "end-1c") == "":
                w_form_sys = 1
            else:
                w_form_sys = float(root.weight_form_sys.get("1.0", "end-1c"))
        else:
            w_form_sys = 0
        return w_form_sys

    """def apply_p_lost_sys(self, root):
        if root.cVar_lost_sys.get() == 1:
            if root.parameter_lost_Y_sys.get("1.0", "end-1c") == "":
                Y = 0
            else:
                Y = int(root.parameter_lost_Y_sys.get("1.0", "end-1c"))
            if root.parameter_lost_m_sys.get("1.0", "end-1c") == "":
                m = 0
            else:
                m = int(root.parameter_lost_m_sys.get("1.0", "end-1c"))
            if root.parameter_lost_d_sys.get("1.0", "end-1c") == "":
                d = 0
            else:
                d = int(root.parameter_lost_d_sys.get("1.0", "end-1c"))
            if root.parameter_lost_h_sys.get("1.0", "end-1c") == "":
                h = 0
            else:
                h = int(root.parameter_lost_h_sys.get("1.0", "end-1c"))
            if root.parameter_lost_M_sys.get("1.0", "end-1c") == "":
                M = 0
            else:
                M = int(root.parameter_lost_M_sys.get("1.0", "end-1c"))
            h_lost = Y*946080000 + m*2592000 + d*86400 + h*3600 + M*60
        else:
            h_lost = 0
        return h_lost"""

    """def apply_w_lost_sys(self, root):
        if root.cVar_lost_sys.get() == 1:
            if root.weight_lost_sys.get("1.0", "end-1c") == "":
                w_lost_sys = 1
            else:
                w_lost_sys = int(root.weight_lost_sys.get("1.0", "end-1c"))
        else:
            w_lost_sys = 0
        return w_lost_sys"""

    def apply_p_cut_sys(self, root):
        if root.cVar_cut_sys.get() == 1:
            if root.parameter_cut_Y_sys.get("1.0", "end-1c") == "":
                Y = 0
            else:
                Y = int(root.parameter_cut_Y_sys.get("1.0", "end-1c"))
            if root.parameter_cut_m_sys.get("1.0", "end-1c") == "":
                m = 0
            else:
                m = int(root.parameter_cut_m_sys.get("1.0", "end-1c"))
            if root.parameter_cut_d_sys.get("1.0", "end-1c") == "":
                d = 0
            else:
                d = int(root.parameter_cut_d_sys.get("1.0", "end-1c"))
            if root.parameter_cut_h_sys.get("1.0", "end-1c") == "":
                h = 0
            else:
                h = int(root.parameter_cut_h_sys.get("1.0", "end-1c"))
            if root.parameter_cut_M_sys.get("1.0", "end-1c") == "":
                M = 0
            else:
                M = int(root.parameter_cut_M_sys.get("1.0", "end-1c"))
            h_cut = Y*946080000 + m*2592000 + d*86400 + h*3600 + M*60
        else:
            h_cut = 0
        return h_cut

    def apply_w_cut_sys(self, root):
        if root.cVar_cut_sys.get() == 1:
            if root.weight_cut_sys.get("1.0", "end-1c") == "":
                w_cut_sys = 1
            else:
                w_cut_sys = float(root.weight_cut_sys.get("1.0", "end-1c"))
        else:
            w_cut_sys = 0
        return w_cut_sys