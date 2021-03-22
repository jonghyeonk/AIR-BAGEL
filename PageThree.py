import warnings
import os
warnings.filterwarnings(action='ignore')

#GUI PACKAGES
import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox

#For Data preprocess
from PIL import ImageTk, Image
import numpy as np
import pandas as pd

#For PM4PY

# import pm4py

# from pm4py.objects.conversion.log import factory as conversion_factory
# from pm4py.objects.log.adapters.pandas import csv_import_adapter
# from pm4py.algo.discovery.inductive import factory as inductive_miner
# from pm4py.visualization.process_tree import factory as pt_vis_factory
# from pm4py.visualization.petrinet import factory as vis_factory
# from pm4py.visualization.petrinet import factory as pn_vis_factory
#
# from pm4py.objects.conversion.log import factory as conversion_factory
# from pm4py.objects.log.adapters.pandas import csv_import_adapter
# from pm4py.algo.discovery.inductive import factory as inductive_miner
# from pm4py.visualization.process_tree import factory as pt_vis_factory
# from pm4py.visualization.petrinet import factory as vis_factory
# from pm4py.visualization.petrinet import factory as pn_vis_factory

import pm4py
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.petrinet import visualizer as pn_visualizer


class PageThree(tk.Frame):

    def show_frame1(self):
        frame = self
        frame.tkraise()

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='dark slate gray')

        top_frame = Frame(self, bg='dark slate gray', width=300, height=50, padx= 5, pady=3)
        center = Frame(self, bg='dark slate gray', width=50, height=40, padx= 5, pady=3)

        os.chdir(os.sep.join([str(self.org_path), "output"]))

        # layout all of the main containers
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top_frame.grid(row=0, sticky="nsew")
        center.grid(row=1, sticky="nsew")

        # create the widgets for the top frame

        top_frame.grid_rowconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)

        top_mid = Frame(top_frame, bg='gray25', height=48, highlightbackground="gray15",
                        highlightthickness=1)
        top_mid.grid(row=0, column=1, pady=(2, 0), sticky="nsew")
        top_mid.grid_rowconfigure(1, weight=1)
        top_mid.grid_columnconfigure(0, weight=1)

        top_mid_label1 = Label(top_mid, text='(4) Output evaluation', font=("Consolas", 13, 'bold'),
                               fg="white", bg='gray25', anchor="center", relief = "raised")
        top_mid_label1.grid(row=0, column=0, sticky="nsew")
        top_mid_label1.grid_rowconfigure(1, weight=1)
        top_mid_label1.grid_columnconfigure(0, weight=1)

        # create the center widgets
        ctr_mid = Frame(center, bg='gray1', width=900, height=425)
        ctr_mid.grid(row=0, column=1, pady=(0, 7), sticky="nsew")

        # center-left : statistics
        ctr_mid_label1 = LabelFrame(ctr_mid, text=" Anomaly frequency ", font=("Consolas", 10, 'bold'),
                                    fg="white", bg='gray1', bd=3, padx=14, pady=7)
        ctr_mid_label1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctr_mid_subframe1 = Frame(ctr_mid_label1, bg='gray1', width=505, height=48, padx=3, pady=0,
                                  highlightbackground="gray15",
                                  highlightthickness=1)
        ctr_mid_subframe1.grid(row=1, column=1)


        table1_00 = Frame(ctr_mid_subframe1, width=25, bg='gray25', highlightbackground="lavender",
                          highlightthickness=2)
        table1_00.grid(row=0, column=0)

        # resource

        # jh

        treeview = tk.ttk.Treeview(table1_00, columns=["one", "two"], displaycolumns=["two", "one"])
        treeview.column("#0", stretch=False, anchor= 'center', width=130)
        treeview.heading("#0", text="Type")

        treeview.column("one",  stretch=False, anchor= 'center', width=100)
        treeview.heading("one", text="Ratio")

        treeview.column("two",  stretch=False, anchor= 'center', width=140)
        treeview.heading("two", text="Case frequency")

        if self.a == 1 and self.b==0 :
            ab_dict = {"type": [0, 0, 0, 0, 0, 0,0]}
            ab_count = pd.DataFrame(ab_dict,
                                    index=[["skip", "form based", "switch" , "moved", "rework", "insert",
                                            "incomplete"]])

            ab = self.data_with_parameter_res[["type", "Case"]].drop_duplicates()
            abc = ab.groupby("type").size().reset_index(name='parameter')
            abc = abc[["type", "parameter"]]

            for i in range(len(abc.index)):
                if abc.loc[i,'type'] == "skip":
                    ab_count.loc["skip"] = abc.loc[i,"parameter"]
                elif abc.loc[i, 'type'] == "form based":
                    ab_count.loc["form based"] = abc.loc[i,"parameter"]
                elif abc.loc[i, 'type'] == "switch":
                    ab_count.loc["switch"] = abc.loc[i,"parameter"]
                elif abc.loc[i, 'type'] == "moved":
                    ab_count.loc["moved"] = abc.loc[i,"parameter"]
                elif abc.loc[i, 'type'] == "rework":
                    ab_count.loc["rework"] = abc.loc[i,"parameter"]
                elif abc.loc[i, 'type'] == "insert":
                    ab_count.loc["insert"] = abc.loc[i,"parameter"]
                elif abc.loc[i, 'type'] == "incomplete":
                    ab_count.loc["incomplete"] = abc.loc[i,"parameter"]
                elif abc.loc[i, 'type'] == "replace":
                    ab_count.loc["incomplete"] = abc.loc[i, "parameter"]
                else:
                    pass


            def cc1(self):
                treeview.tag_configure("tag2", background="red")

            treelist = ab_count[ab_count['type'] > 0]
            total = len(self.data_with_parameter_res["Case"].unique())
            na = sum(treelist["type"])
            treelist["ratio"] = treelist["type"] / total

            nn = total - na

            treeview.insert('', 'end', text="Normal", values=[round(nn / total, 5), int(nn)], iid="Normal")
            top = treeview.insert('', 'end', text="Anomaly (res)", values=[round(na / total, 5), int(na)],
                                  iid="Anomaly1", tags="tag1")

            for i in range(len(treelist)):
                globals()['top_mid{}'] = treeview.insert(top, 'end', text=treelist.index[i],
                                                         values=[round(treelist.loc[treelist.index[i]]["ratio"], 5),
                                                                 int(treelist.loc[treelist.index[i]]["type"])], iid=i)

            # center-right

            # center-left : statistics

            ctr_mid_label3 = LabelFrame(ctr_mid, text=" Root information ", font=("Consolas", 10, 'bold'),
                                        fg="white", bg='gray1', bd=3, padx=14, pady=7)
            ctr_mid_label3.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

            ctr_mid_subframe3 = Frame(ctr_mid_label3, bg='gray1', width=505, height=48, padx=3, pady=0,
                                      highlightbackground="gray15",
                                      highlightthickness=1)
            ctr_mid_subframe3.grid(row=1, column=1)

            table3_00 = Frame(ctr_mid_subframe3, width=25, bg='gray25', highlightbackground="lavender",
                              highlightthickness=2)
            table3_00.grid(row=0, column=0)

            def cc2(self):
                treeview2.tag_configure("tag2", background="red")

            treeview2 = tk.ttk.Treeview(table3_00, columns=["one"], displaycolumns=["one"])

            treeview2.column("#0", stretch=False, anchor='center', width=230)
            treeview2.heading("#0", text="Type")

            treeview2.column("one", stretch=False, anchor='center', width=120)
            treeview2.heading("one", text="Values")

            sum_res = self.data_with_parameter_res.groupby(["Resource"], as_index=False).count()
            fail_res = self.data_with_parameter_res.groupby(["Resource"], as_index=False)["Resource_Anomaly/Normal"].sum()
            rate_res = pd.merge(sum_res, fail_res, on="Resource", how="outer")

            rate_res["rate"] = rate_res["Resource_Anomaly/Normal_y"] / rate_res["Resource_Anomaly/Normal_x"]
            res_mean = round(np.mean(rate_res["rate"]), 6)
            res_max = round(np.max(rate_res["rate"]), 6)
            res_min = round(np.min(rate_res["rate"]), 6)
            res_top5 = rate_res.sort_values(by=['rate'], ascending=False).head(5)
            res_top5.reset_index(drop=True, inplace=True)


            if "Resource" in list(self.data_with_parameter_res.columns):
                res_val = len(self.data_with_parameter_res["Resource"].unique())
            else:
                res_val = 0


            res = treeview2.insert('', 'end', text="# of resources",
                                   values=res_val, iid="Resource", tags="tag3")

            res_top = treeview2.insert(res, 'end', text='Failure probability',
                                       iid=1, tags="tag4")
            res_top_mean = treeview2.insert(res_top, 'end', text='Average',
                                            values=res_mean, iid=2)
            res_top_max = treeview2.insert(res_top, 'end', text='Max',
                                           values=res_max, iid=3)
            res_top_max = treeview2.insert(res_top, 'end', text='Min',
                                           values=res_min, iid=4)

            res_bot = treeview2.insert(res, 'end', text='Top 5 resources with Failure.Prob',
                                       iid=5, tags="tag4")

            for i in range(len(res_top5.index)):
                rb1 = str(res_top5.loc[res_top5.index[i], 'Resource'])
                rb2 = round(float(res_top5.loc[res_top5.index[i], 'rate']), 6)
                globals()['res_bot{}'] = treeview2.insert(res_bot, 'end', text=rb1,
                                                          values=rb2, iid=6 + i)

            treeview.tag_configure('tag1', background='lightgrey')
            treeview.tag_bind("tag1", sequence="<<TreeviewSelect>>", callback=cc1)

            treeview.grid(row=0, column=0)
            self.update()

            treeview2.tag_configure('tag3', background='lightgrey')
            treeview2.tag_bind("tag3", sequence="<<TreeviewSelect>>", callback=cc2)

            treeview2.grid(row=0, column=0)
            self.update()
        else:
            pass


        if self.a == 0 and self.b==1 :
            ab2 = self.data_with_parameter_sys[["type", "Case"]].drop_duplicates()
            abc2 = ab2.groupby("type").size().reset_index(name='parameter')
            abc2 = abc2[["type", "parameter"]]

            ab2_dict = {"type": [0, 0, 0]}
            ab2_count = pd.DataFrame(ab2_dict,
                                    index=[["skip", "form based", "cut"]])

            for i in range(len(abc2.index)):
                if abc2.loc[i,'type'] == "skip":
                    ab2_count.loc["skip"] = abc2.loc[i,'parameter']
                elif abc2.loc[i,'type'] == "form based":
                    ab2_count.loc["form based"] = abc2.loc[i,'parameter']
                elif abc2.loc[i,'type'] == "cut":
                    ab2_count.loc["cut"] = abc2.loc[i,'parameter']
                else:
                    pass

            def cc1(self):
                treeview.tag_configure("tag2", background="red")

            total = len(self.data_with_parameter_sys["Case"].unique())

            treelist2 = ab2_count[ab2_count['type'] > 0]

            na2 = sum(treelist2["type"])
            nn = total - na2
            treelist2["ratio"] = treelist2["type"] / total

            treeview.insert('', 'end', text="Normal", values=[round(nn / total, 5), int(nn)], iid="Normal")

            bot = treeview.insert('', 'end', text="Anomaly (sys)", values=[round(na2 / total, 5), int(na2)],
                                  iid="Anomaly2", tags="tag1")
            for i in range(len(treelist2)):
                globals()['bot_mid{}'] = treeview.insert(bot, 'end', text=treelist2.index[i],
                                                         values=[round(treelist2.loc[treelist2.index[i]]["ratio"], 5),
                                                                 int(treelist2.loc[treelist2.index[i]]["type"])], iid=10+i)

            # center-right

            # center-left : statistics

            ctr_mid_label3 = LabelFrame(ctr_mid, text=" Root information ", font=("Consolas", 10, 'bold'),
                                        fg="white", bg='gray1', bd=3, padx=14, pady=7)
            ctr_mid_label3.place(x=460, y=10)

            ctr_mid_subframe3 = Frame(ctr_mid_label3, bg='gray1', width=505, height=48, padx=3, pady=0,
                                      highlightbackground="gray15",
                                      highlightthickness=1)
            ctr_mid_subframe3.grid(row=1, column=1)

            table3_00 = Frame(ctr_mid_subframe3, width=25, bg='gray25', highlightbackground="lavender",
                              highlightthickness=2)
            table3_00.grid(row=0, column=0)

            def cc2(self):
                treeview2.tag_configure("tag2", background="red")

            treeview2 = tk.ttk.Treeview(table3_00, columns=["one"], displaycolumns=["one"])

            treeview2.column("#0", stretch=False, anchor='center', width=230)
            treeview2.heading("#0", text="Type")

            treeview2.column("one", stretch=False, anchor='center', width=120)
            treeview2.heading("one", text="Values")


            sys_top5 = self.df_sys.sort_values(by=['down_duration'], ascending=False).head(5)
            sys_top5.reset_index(drop=True, inplace=True)


            if "System" in list(self.data_with_parameter_sys.columns):
                sys_val = len(self.data_with_parameter_sys["System"].unique())
            else:
                sys_val = 0

            sys = treeview2.insert('', 'end', text="# of systems",
                                   values=sys_val, iid="System", tags="tag3")

            sys_top = treeview2.insert(sys, 'end', text='system malfunctioning time',
                                       iid=11, tags="tag4")
            sys_top_n = treeview2.insert(sys_top, 'end', text='# of system malfunctioning',
                                         values=[len(self.df_sys.index)], iid=12)
            sys_top_mean = treeview2.insert(sys_top, 'end', text='Average',
                                            values=[np.mean(self.df_sys["down_duration"])], iid=13)
            sys_top_max = treeview2.insert(sys_top, 'end', text='Max',
                                           values=[np.max(self.df_sys["down_duration"])], iid=14)
            sys_top_max = treeview2.insert(sys_top, 'end', text='Min',
                                           values=[np.min(self.df_sys["down_duration"])], iid=15)

            sys_bot = treeview2.insert(sys, 'end', text='Top 5 systems with down time',
                                       iid=16, tags="tag4")

            for i in range(len(sys_top5.index)):
                sb1 = str(sys_top5.loc[sys_top5.index[i], 'Event:system malfunctioning'])
                sb2 = str(sys_top5.loc[sys_top5.index[i]]['down_duration'])
                globals()['sys_bot{}'] = treeview2.insert(sys_bot, 'end', text=sb1,
                                                          values=[sb2], iid=17 + i)

            treeview.tag_configure('tag1', background='lightgrey')
            treeview.tag_bind("tag1", sequence="<<TreeviewSelect>>", callback=cc1)

            treeview.grid(row=0, column=0)
            self.update()

            treeview2.tag_configure('tag3', background='lightgrey')
            treeview2.tag_bind("tag3", sequence="<<TreeviewSelect>>", callback=cc2)

            treeview2.grid(row=0, column=0)
            self.update()


        else:
            pass

        if self.a == 1 and self.b==1 :
            ab_dict = {"type": [0, 0, 0, 0, 0, 0,0]}
            ab_count = pd.DataFrame(ab_dict,
                                    index=[["skip", "form based", "switch","moved", "rework", "insert",
                                            "incomplete"]])


            ab = self.data_with_parameter_res[["type", "Case"]].drop_duplicates()
            abc = ab.groupby("type").size().reset_index(name='parameter')
            abc = abc[["type", "parameter"]]

            ab2 = self.data_with_parameter_sys[["type", "Case"]].drop_duplicates()
            abc2 = ab2.groupby("type").size().reset_index(name='parameter')
            abc2 = abc2[["type", "parameter"]]

            for i in range(len(abc.index)):
                if abc.loc[i,'type'] == "skip":
                    ab_count.loc["skip"] = abc.loc[i,"parameter"]
                elif abc.loc[i, 'type'] == "form based":
                    ab_count.loc["form based"] = abc.loc[i,"parameter"]
                elif abc.loc[i, 'type'] == "switch":
                    ab_count.loc["switch"] = abc.loc[i,"parameter"]
                elif abc.loc[i, 'type'] == "moved":
                    ab_count.loc["moved"] = abc.loc[i,"parameter"]
                elif abc.loc[i, 'type'] == "rework":
                    ab_count.loc["rework"] = abc.loc[i,"parameter"]
                elif abc.loc[i, 'type'] == "insert":
                    ab_count.loc["insert"] = abc.loc[i,"parameter"]
                elif abc.loc[i, 'type'] == "incomplete":
                    ab_count.loc["incomplete"] = abc.loc[i,"parameter"]
                elif abc.loc[i, 'type'] == "replace":
                    ab_count.loc["incomplete"] = abc.loc[i, "parameter"]
                else:
                    pass


            ab2_dict = {"type": [0, 0, 0]}
            ab2_count = pd.DataFrame(ab2_dict,
                                    index=[["skip", "form based", "cut"]])

            for i in range(len(abc2.index)):
                if abc2.loc[i,'type'] == "skip":
                    ab2_count.loc["skip"] = abc2.loc[i,'parameter']
                elif abc2.loc[i,'type'] == "form based":
                    ab2_count.loc["form based"] = abc2.loc[i,'parameter']
                elif abc2.loc[i,'type'] == "cut":
                    ab2_count.loc["cut"] = abc2.loc[i,'parameter']
                else:
                    pass

            def cc1(self):
                treeview.tag_configure("tag2", background="red")

            treelist = ab_count[ab_count['type'] > 0]
            total = len(self.data_with_parameter_res["Case"].unique())
            na = sum(treelist["type"])
            treelist["ratio"] = treelist["type"] / total

            treelist2 = ab2_count[ab2_count['type'] > 0]

            na2 = sum(treelist2["type"])
            nn = total - na - na2
            treelist2["ratio"] = treelist2["type"] / total

            treeview.insert('', 'end', text="Normal", values=[round(nn / total, 5), int(nn)], iid="Normal")
            top = treeview.insert('', 'end', text="Anomaly (res)", values=[round(na / total, 5), int(na)],
                                  iid="Anomaly1", tags="tag1")
            for i in range(len(treelist)):
                globals()['top_mid{}'] = treeview.insert(top, 'end', text=treelist.index[i],
                                                         values=[round(treelist.loc[treelist.index[i]]["ratio"], 5),
                                                                 int(treelist.loc[treelist.index[i]]["type"])], iid=i)

            bot = treeview.insert('', 'end', text="Anomaly (sys)", values=[round(na2 / total, 5), int(na2)],
                                  iid="Anomaly2", tags="tag1")
            for i in range(len(treelist2)):
                globals()['bot_mid{}'] = treeview.insert(bot, 'end', text=treelist2.index[i],
                                                         values=[round(treelist2.loc[treelist2.index[i]]["ratio"], 5),
                                                                 int(treelist2.loc[treelist2.index[i]]["type"])], iid=10+i)

            # center-right

            # center-left : statistics

            ctr_mid_label3 = LabelFrame(ctr_mid, text=" Root information ", font=("Consolas", 10, 'bold'),
                                        fg="white", bg='gray1', bd=3, padx=14, pady=7)
            ctr_mid_label3.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

            ctr_mid_subframe3 = Frame(ctr_mid_label3, bg='gray1', width=505, height=48, padx=3, pady=0,
                                      highlightbackground="gray15",
                                      highlightthickness=1)
            ctr_mid_subframe3.grid(row=1, column=1)

            table3_00 = Frame(ctr_mid_subframe3, width=25, bg='gray25', highlightbackground="lavender",
                              highlightthickness=2)
            table3_00.grid(row=0, column=0)

            def cc2(self):
                treeview2.tag_configure("tag2", background="red")

            treeview2 = tk.ttk.Treeview(table3_00, columns=["one"], displaycolumns=["one"])

            treeview2.column("#0", stretch=False, anchor='center', width=230)
            treeview2.heading("#0", text="Type")

            treeview2.column("one", stretch=False, anchor='center', width=120)
            treeview2.heading("one", text="Values")

            sum_res = self.data_with_parameter_res.groupby(["Resource"], as_index=False).count()
            fail_res = self.data_with_parameter_res.groupby(["Resource"], as_index=False)["Resource_Anomaly/Normal"].sum()
            rate_res = pd.merge(sum_res, fail_res, on="Resource", how="outer")

            rate_res["rate"] = rate_res["Resource_Anomaly/Normal_y"] / rate_res["Resource_Anomaly/Normal_x"]
            res_mean = round(np.mean(rate_res["rate"]), 6)
            res_max = round(np.max(rate_res["rate"]), 6)
            res_min = round(np.min(rate_res["rate"]), 6)
            res_top5 = rate_res.sort_values(by=['rate'], ascending=False).head(5)
            res_top5.reset_index(drop=True, inplace=True)

            sys_top5 = self.df_sys.sort_values(by=['down_duration'], ascending=False).head(5)
            sys_top5.reset_index(drop=True, inplace=True)
            if "Resource" in list(self.data_with_parameter_res.columns):
                res_val = len(self.data_with_parameter_res["Resource"].unique())
            else:
                res_val = 0

            if "System" in list(self.data_with_parameter_sys.columns):
                sys_val = len(self.data_with_parameter_sys["System"].unique())
            else:
                sys_val = 0

            res = treeview2.insert('', 'end', text="# of resources",
                                   values=res_val, iid="Resource", tags="tag3")
            sys = treeview2.insert('', 'end', text="# of systems",
                                   values=sys_val, iid="System", tags="tag3")

            res_top = treeview2.insert(res, 'end', text='Failure probability',
                                       iid=1, tags="tag4")
            res_top_mean = treeview2.insert(res_top, 'end', text='Average',
                                            values=res_mean, iid=2)
            res_top_max = treeview2.insert(res_top, 'end', text='Max',
                                           values=res_max, iid=3)
            res_top_max = treeview2.insert(res_top, 'end', text='Min',
                                           values=res_min, iid=4)

            res_bot = treeview2.insert(res, 'end', text='Top 5 resources with Failure.Prob',
                                       iid=5, tags="tag4")

            for i in range(len(res_top5.index)):
                rb1 = str(res_top5.loc[res_top5.index[i], 'Resource'])
                rb2 = round(float(res_top5.loc[res_top5.index[i], 'rate']), 6)
                globals()['res_bot{}'] = treeview2.insert(res_bot, 'end', text=rb1,
                                                          values=rb2, iid=6 + i)

            sys_top = treeview2.insert(sys, 'end', text='system malfunctioning time',
                                       iid=11, tags="tag4")
            sys_top_n = treeview2.insert(sys_top, 'end', text='# of system malfunctioning',
                                         values=[len(self.df_sys.index)], iid=12)
            sys_top_mean = treeview2.insert(sys_top, 'end', text='Average',
                                            values=[np.mean(self.df_sys["down_duration"])], iid=13)
            sys_top_max = treeview2.insert(sys_top, 'end', text='Max',
                                           values=[np.max(self.df_sys["down_duration"])], iid=14)
            sys_top_max = treeview2.insert(sys_top, 'end', text='Min',
                                           values=[np.min(self.df_sys["down_duration"])], iid=15)

            sys_bot = treeview2.insert(sys, 'end', text='Top 5 systems with down time',
                                       iid=16, tags="tag4")

            for i in range(len(sys_top5.index)):
                sb1 = str(sys_top5.loc[sys_top5.index[i], 'Event:system malfunctioning'])
                sb2 = str(sys_top5.loc[sys_top5.index[i]]['down_duration'])
                globals()['sys_bot{}'] = treeview2.insert(sys_bot, 'end', text=sb1,
                                                          values=[sb2], iid=17 + i)

            treeview.tag_configure('tag1', background='lightgrey')
            treeview.tag_bind("tag1", sequence="<<TreeviewSelect>>", callback=cc1)

            treeview.grid(row=0, column=0)
            self.update()

            treeview2.tag_configure('tag3', background='lightgrey')
            treeview2.tag_bind("tag3", sequence="<<TreeviewSelect>>", callback=cc2)

            treeview2.grid(row=0, column=0)
            self.update()


        else:
            pass






        # process map (inductive miner)


        ctr_mid_label2 = LabelFrame(ctr_mid, text=" Process model (Inductive Miner) ", font=("Consolas", 10, 'bold'),
                                    fg="white", bg='gray1', bd=3, padx=14, pady=7)
        ctr_mid_label2.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        ctr_mid_subframe2 = Frame(ctr_mid_label2, bg='gray1', width=950, height=48, padx=3, pady=0,
                                  highlightbackground="gray15",
                                  highlightthickness=1)
        ctr_mid_subframe2.grid(row=1, column=1)


        # before
        before_c = Label(ctr_mid_subframe2, text=" (A) Petri-net before injecting anomalies",
                                   width=34,foreground="aquamarine", background='gray1', anchor="w")
        before_c.grid(row=0, column=0, sticky='w',padx=(0,15))

        # after
        after_c = Label(ctr_mid_subframe2, text=" (B) Petri-net after injecting anomalies",  width=34,
                                   foreground="aquamarine", background='gray1',anchor="w")
        after_c.grid(row=1, column=0, sticky='w', padx=(0,15))
        global b_click
        b_click = 0
        global a_click
        a_click = 0

        def function_before_see(b_click) :
            if b_click == 1 :
                before_gviz.view()
            else:
                before = self.before

                if self.a == 1:
                    before = before[['Case', 'Activity', "Timestamp", "Resource"]]
                    before.rename(columns={"Case": "case:concept:name", "Activity": "concept:name",
                                           "Timestamp": "time:timestamp", "Resource": "Resource"})
                    before.columns = ['case:concept:name', 'concept:name', "time:timestamp", "Resource"]
                elif self.a == 0 and self.b == 1:
                    before = before[['Case', 'Activity', "Timestamp", "System"]]
                    before.rename(columns={"Case": "case:concept:name", "Activity": "concept:name",
                                           "Timestamp": "time:timestamp", "System": "Resource"})

                    before.columns = ['case:concept:name', 'concept:name', "time:timestamp", "Resource"]

                before_log = log_converter.apply(before)
                b_net, b_initial_marking, b_final_marking = inductive_miner.apply(before_log)
                before_gviz = pn_visualizer.apply(b_net, b_initial_marking, b_final_marking)
                b_click = 1
                before_gviz.view()

            return b_click

        def function_after_see(a_click):
            if a_click == 1:
                after_gviz.view()
            else:
                after = self.after

                if self.a == 1:
                    after = after[['Case', 'Activity', "Timestamp", "Resource"]]
                    after.rename(columns={"Case": "case:concept:name", "Activity": "concept:name",
                                           "Timestamp": "time:timestamp", "Resource": "Resource"})
                    after.columns = ['case:concept:name', 'concept:name', "time:timestamp", "Resource"]
                elif self.a == 0 and self.b == 1:
                    after = after[['Case', 'Activity', "Timestamp", "System"]]
                    after.rename(columns={"Case": "case:concept:name", "Activity": "concept:name",
                                           "Timestamp": "time:timestamp", "System": "Resource"})

                    after.columns = ['case:concept:name', 'concept:name', "time:timestamp", "Resource"]

                after_log = log_converter.apply(after)
                a_net, a_initial_marking, a_final_marking = inductive_miner.apply(after_log)
                after_gviz = pn_visualizer.apply(a_net, a_initial_marking, a_final_marking)
                a_click = 1
                after_gviz.view()

            return a_click

        def function_before_get(b_click):
            if b_click ==1 :
                pn_visualizer.save(before_gviz, "clean_process.png")
                messagebox.showinfo("Message", "Downloaded in 'output' folder")

            else:
                before = self.before

                if self.a == 1:
                    before = before[['Case', 'Activity', "Timestamp", "Resource"]]
                    before.rename(columns={"Case": "case:concept:name", "Activity": "concept:name",
                                           "Timestamp": "time:timestamp", "Resource": "Resource"})
                    before.columns = ['case:concept:name', 'concept:name', "time:timestamp", "Resource"]
                elif self.a == 0 and self.b == 1:
                    before = before[['Case', 'Activity', "Timestamp", "System"]]
                    before.rename(columns={"Case": "case:concept:name", "Activity": "concept:name",
                                           "Timestamp": "time:timestamp", "System": "Resource"})

                    before.columns = ['case:concept:name', 'concept:name', "time:timestamp", "Resource"]

                before_log = log_converter.apply(before)
                b_net, b_initial_marking, b_final_marking = inductive_miner.apply(before_log)
                before_gviz = pn_visualizer.apply(b_net, b_initial_marking, b_final_marking)
                b_click = 1
                pn_visualizer.save(before_gviz, "{}_clean_process.png".format(self.dat_name))
                messagebox.showinfo("Message", "Downloaded in 'output' folder")

                
            return b_click


        def function_after_get(a_click):
            if a_click == 1:
                pn_visualizer.save(after_gviz, "anomaly_process.png")
                messagebox.showinfo("Message", "Downloaded in 'output' folder")

            else:
                after = self.after

                if self.a == 1:
                    after = after[['Case', 'Activity', "Timestamp", "Resource"]]
                    after.rename(columns={"Case": "case:concept:name", "Activity": "concept:name",
                                           "Timestamp": "time:timestamp", "Resource": "Resource"})
                    after.columns = ['case:concept:name', 'concept:name', "time:timestamp", "Resource"]
                elif self.a == 0 and self.b == 1:
                    after = after[['Case', 'Activity', "Timestamp", "System"]]
                    after.rename(columns={"Case": "case:concept:name", "Activity": "concept:name",
                                           "Timestamp": "time:timestamp", "System": "Resource"})

                    after.columns = ['case:concept:name', 'concept:name', "time:timestamp", "Resource"]

                after_log = log_converter.apply(after)
                a_net, a_initial_marking, a_final_marking = inductive_miner.apply(after_log)
                after_gviz = pn_visualizer.apply(a_net, a_initial_marking, a_final_marking)
                a_click = 1
                pn_visualizer.save(after_gviz, "{}_anomaly_process.png".format(self.dat_name))
                messagebox.showinfo("Message", "Downloaded in 'output' folder")

            return a_click

        button_before = tk.Button(ctr_mid_subframe2, text="See", width=6,  command= lambda: function_before_see(b_click))
        button_before.grid(row=0, column=1, padx= (0,4), sticky='w')

        button_after = tk.Button(ctr_mid_subframe2, text="See",width=6, command= lambda: function_after_see(a_click))
        button_after.grid(row=1, column=1, padx= (0,4), sticky='w')

        button_before_c = tk.Button(ctr_mid_subframe2, text="Download", width=10,  command= lambda: function_before_get(b_click))
        button_before_c.grid(row=0, column=2, sticky='w')

        button_after_c = tk.Button(ctr_mid_subframe2, text="Download",width=10, command= lambda: function_after_get(a_click))
        button_after_c.grid(row=1, column=2, sticky='w')



        ## data export

        ctr_mid_label4 = LabelFrame(ctr_mid, text=" Export csv file ", font=("Consolas", 10, 'bold'),
                                    fg="white", bg='gray1', bd=3, padx=14, pady=7)
        ctr_mid_label4.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        ctr_mid_subframe4 = Frame(ctr_mid_label4, bg='gray1', width=950, height=48, pady=0,
                                  highlightbackground="gray15",
                                  highlightthickness=1)
        ctr_mid_subframe4.grid(row=1, column=1)

        # before
        # before_a = Label(ctr_mid_subframe4, text=" (A) Parameters before injecting anomalies",
        #                            width=33,foreground="aquamarine", background='gray1', anchor="w")
        # before_a.grid(row=0, column=0, sticky='w',padx=(0,20))

        # after
        after_a = Label(ctr_mid_subframe4, text=" Event log after injecting anomalies",  width=33,
                                   foreground="aquamarine", background='gray1',anchor="w")
        after_a.grid(row=0, column=0, sticky='w', padx=(0,20))


        # button_before_a = tk.Button(ctr_mid_subframe4, text="Download", width=10,  command= lambda: before_gviz.view())
        # button_before_a.grid(row=0, column=1, padx=(25,0), sticky='w')

        button_after_a = tk.Button(ctr_mid_subframe4, text="Download",width=10, command= lambda: [self.after.to_csv("{}_with_anomalies.csv".format(self.dat_name), mode='w', index=False),
                                                                                                  messagebox.showinfo("Message","Downloaded in 'output' folder")])
        button_after_a.grid(row=0, column=1, padx=(25,0), sticky='w')


        def close():
            parent.destroy()
        button1 = tk.Button(ctr_mid, text="Close", padx=25,
                            command=close)
        button1.grid(row=2, column=1, sticky="e", padx=10, pady=10)
        self.update()
