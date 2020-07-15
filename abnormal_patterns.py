import warnings
warnings.filterwarnings(action='ignore')

#GUI PACKAGES
import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox

#For Data preprocess
import psycopg2
import numpy as np
import pandas as pd
from datetime import datetime as dt
import time
import random
import datetime
from datetime import timedelta

#Pages
from PageThree import PageThree


class Abnorm_p():

    def __init__(self, input_file):

        self.input_file = input_file

    # Preprocess: to make new attribute 'type' for parameter value in dataframe
    def setting1(self, df, types, mag):   # types= anomaly patterns, mag= weights
        mag_c = []
        for i in range(len(mag)):
            if mag[i] != 0:
                mag_c.append(mag[i])
            else:
                pass
        types_a = np.array(types)
        df = df.sort_values(by=["Case", "Timestamp"], ascending=[True, True])
        df["cusum"] = df.groupby(["Case"])["Resource_Pass/Fail"].cumsum()
        df["type"] = np.nan
        if sum(mag) == 1:
            num_fail = df["Resource_Pass/Fail"].sum()
            applied_patterns = np.repeat(random.choice(types), num_fail)
            fail_df = df[df["Resource_Pass/Fail"] == 1]
            clean_df = df[df["Resource_Pass/Fail"] == 0]
            fail_df["type"] = applied_patterns
            df = pd.concat([clean_df, fail_df], ignore_index=True)
        else:
            applied_patterns = np.repeat(types_a, mag_c)
            fail_df = df[(df["Resource_Pass/Fail"] == 1) & (df["cusum"] == 1)]
            clean_df1 = df[df["Resource_Pass/Fail"] == 0]
            clean_df2 = df[(df["Resource_Pass/Fail"] == 1) & (df["cusum"] > 1)]
            fail_df["type"] = fail_df["type"].apply(lambda x: random.choice(applied_patterns))
            df = pd.concat([clean_df1, clean_df2, fail_df], ignore_index=True)
        return df

    # Preprocess: To add 'parameter' attribute in df
    def setting2(self, df, m_skip, m_form, h_moved, m_switch, m_insert, m_rework, m_replace):
        df = df.sort_values(by=["Case", "Timestamp"], ascending=[True, True])
        df_new = pd.DataFrame.copy(df)
        df["check"] = 1
        df_new["order"] = df.groupby(["Case"])["check"].cumsum()            #length = event position in a case
        df_new["max"] = df_new.groupby(["Case"])["order"].transform("max")  #max = trace length
        df_new["parameter_l"] = np.nan
        df_new["parameter_r"] = np.nan
        df_new["parameter"] = np.nan
        df_c = df_new.shift(-1, axis=0)
        df_new["duration"] = df_c["Timestamp"] - df_new["Timestamp"]  #duration = time interval between events
        df_new.loc[(df_new["order"] == df_new["max"]), "duration"] = datetime.timedelta()
        df_new["duration"] = df_new.apply(lambda x: x["duration"].seconds, axis=1)
        df_ct = df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] is not np.nan)]
        df_ct["resource_anomaly_type"] = df_ct["type"]
        df_ct = df_ct[["Case", "resource_anomaly_type"]]
        df_new = pd.merge(df_new, df_ct, on="Case", how="outer")
        df_new.loc[df_new["resource_anomaly_type"].isna(), "resource_anomaly_type"] = "normal"
        if "skip" in df_new["type"].unique():
            df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] == "skip"), "parameter_l"] = 1
            df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] == "skip"), "parameter_r"] = 1
        else:
            pass
        if "form based" in df_new["type"].unique():
            if m_form < 2:
                m_form = 2
            df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] == "form based"), "parameter_l"] = df_new["max"] - df_new["order"] + 1
            df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] == "form based"), "parameter_r"] = df_new["parameter_r"].apply(lambda x:random.randint(2, m_form))
        else:
            pass
        if "rework" in df_new["type"].unique():
            df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] == "rework"), "parameter_l"] = df_new["max"] - df_new["order"] + 1
            df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] == "rework"), "parameter_r"] = df_new["parameter_r"].apply(lambda x:random.randint(1, m_rework))
        else:
            pass
        if "switch" in df_new["type"].unique():
            df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] == "switch"), "parameter_l"] = 1
            df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] == "switch"), "parameter_r"] = df_new["parameter_r"].apply(lambda x:random.randint(1, m_switch))
        else:
            pass
        if "replace" in df_new["type"].unique():
            df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] == "replace"), "parameter_l"] = 1
            df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] == "replace"), "parameter_r"] = df_new["parameter_r"].apply(lambda x:random.randint(1, m_replace))
        else:
            pass
        if df_new["parameter_r"].all() != np.nan:
            df_new.loc[df_new["parameter_l"] >= df_new["parameter_r"], "parameter"] = df_new["parameter_r"]
            df_new.loc[df_new["parameter_l"] < df_new["parameter_r"], "parameter"] = df_new["parameter_l"]
        else:
            pass
        if "moved" in df_new["type"].unique():
            df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["type"] == "moved"), "parameter"] = df_new["parameter_r"].apply(lambda x:random.randint(-h_moved, h_moved))
        else:
            pass
        if "insert" in df_new["type"].unique():
            df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] == "insert"), "parameter"] = 1 #df_new["parameter"].apply(lambda x: random.randint(1, m_insert))
        else:
            pass
        if "incomplete" in df_new["type"].unique():
            df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] == "incomplete"), "parameter"] = df_new["max"] - df_new["order"] + 1
        else:
            pass
        if "switch" in list(df_new["type"]):
            c_list = df_new[(df_new["cusum"] == 1) & (df_new["type"] == "switch")]
            c_list = c_list.groupby(["cusum"])["Case"].unique()
            m_case = df_new[(df_new["resource_anomaly_type"] == "switch")]
            n_case = df_new[df_new["resource_anomaly_type"] == "normal"]
            a_case = df_new[(df_new["resource_anomaly_type"] != "switch") & (df_new["resource_anomaly_type"] != "normal")]
            m_case_list = m_case["Case"].unique()
            n_case_list = n_case["Case"].unique()
            n_case_list = list(np.random.choice(n_case_list, len(m_case_list), replace=False))
            n_case_f = n_case[n_case["Case"].isin(n_case_list)]
            n_case_f = list(n_case_f.groupby(["Case"]))
            n_case_f = list(map(lambda x: x[1].sample(n=1), n_case_f))
            n_case_f = list(map(lambda x: int(x.index.values), n_case_f))
            n_case.loc[n_case_f, "parameter_r"] = c_list[1]
            df_new = pd.concat([m_case, n_case, a_case])
        else:
            pass
        df_p = df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] is not np.nan)]
        df_p["resource_parameter"] = df_p.apply(lambda x: "loc = {0}, len = {1}".format(x["order"], x["parameter"]), axis=1)
        df_p = df_p[["Case", "resource_parameter"]]
        df_new = pd.merge(df_new, df_p, on="Case", how="outer")
        df_new.reset_index(drop=True, inplace=True)
        global data_with_parameter_res
        data_with_parameter_res = df_new
        # df_new.to_csv("data_with_parameter1.csv", mode='w', index=False)
        PageThree.data_with_parameter_res = data_with_parameter_res
        return df_new

    # Events are not recorded
    def skip(self, df):

        df_new = pd.DataFrame.copy(df)
        list_skip_i = list(df_new.index[(df_new["type"] == "skip") & (df_new["cusum"] == 1) & (df_new["order"] != 1)])
        list_skip_p = list(df_new.loc[list_skip_i, "parameter"])
        dic_skip = {"index": list_skip_i, "parameter": list_skip_p}
        list_skip = pd.DataFrame(dic_skip)
        list_skip = list_skip.apply(lambda row: np.arange(row["index"], int(row["index"] + row["parameter"]), 1), axis=1)
        list_skip = np.concatenate(list_skip)
        df_new = df.drop(list_skip)
        df_new = df_new.sort_values(by=["Case", "order"], ascending=[True, True])
        df_new.reset_index(drop=True, inplace=True)
        return df_new

    # Events have same timestamp
    def form_based(self, df):

        df_new = pd.DataFrame.copy(df)
        df_new["resource_check2"] = np.nan
        df_ct = df_new.loc[(df_new["Resource_Pass/Fail"] == 1) & (df_new["cusum"] == 1) & (df_new["type"] == "form based")]
        df_ct["resource_check1"] = df_ct["Resource"]
        df_ct = df_ct[["Case", "resource_check1"]]
        df_new = pd.merge(df_new, df_ct, on="Case", how="outer")
        df_new["resource_check2"] = df_new.apply(lambda x: 1 if x["Resource"] == x["resource_check1"] else 0, axis=1)
        list_form_i = list(df_new.index[(df_new["type"] == "form based") & (df_new["cusum"] == 1)])
        list_form_p = list(df_new.loc[list_form_i, "parameter"])
        list_form_ts = list(df_new.loc[list_form_i, "Timestamp"])
        dic_form = {"index": list_form_i, "parameter": list_form_p, "Timestamp": list_form_ts}
        list_form = pd.DataFrame(dic_form)
        list_form_1 = list_form.apply(lambda row: np.arange(row["index"], int(row["index"] + row["parameter"]), 1), axis=1)
        list_form_1 = np.concatenate(list_form_1)
        list_form_2 = list_form.apply(lambda row: np.repeat(a=row["Timestamp"], repeats=row["parameter"]), axis=1)
        list_form_2 = np.concatenate(list_form_2)
        df_new["Timestamp_temp"] = np.nan
        df_new["Timestamp_chg"] = np.nan
        df_new.loc[list_form_1, "Timestamp_temp"] = list_form_2
        df_new.loc[list_form_1, "Timestamp_chg"] = 1
        df_new["Timestamp"] = df_new.apply(lambda x: x["Timestamp_temp"] if (x["resource_check2"] == 1) & (x["Timestamp_chg"] == 1) else x["Timestamp"], axis=1)
        """for i in range(len(list_form_1)):
            if df_new.loc[list_form_1[i], "resource_check2"] == 1:
                df_new.loc[list_form_1[i], "Timestamp"] = list_form_2[i]
            else:
                pass"""
        df_new.drop(columns=["resource_check1", "resource_check2", "Timestamp_temp", "Timestamp_chg"])
        df_new = df_new.sort_values(by=["Case", "order"], ascending=[True, True])
        df_new.reset_index(drop=True, inplace=True)
        return df_new


    # Last events in case are not recorded
    def incomplete(self, df):

        df_new = pd.DataFrame.copy(df)
        list_incom_i = list(df_new.index[(df_new["type"] == "incomplete") & (df_new["cusum"] == 1) & (df_new["order"] != 1)])
        list_incom_p = list(df_new.loc[list_incom_i, "parameter"])
        dic_incom = {"index": list_incom_i, "parameter": list_incom_p}
        list_incom = pd.DataFrame(dic_incom)
        list_incom = list_incom.apply(lambda row: np.arange(row["index"], int(row["index"] + row["parameter"]), 1), axis=1)
        list_incom = np.concatenate(list_incom)
        df_new = df.drop(list_incom)
        df_new = df_new.sort_values(by=["Case", "order"], ascending=[True, True])
        df_new.reset_index(inplace=True, drop=True)
        return df_new

    # Wrong timestamp are recorded
    def moved(self, df):

        df_new = pd.DataFrame.copy(df)
        df_new["resource_parameter"] = np.where(df_new["type"] == "moved", df_new.apply(lambda x: "eventID = {0}, duration = {1}".format(x["Event"], x["parameter"]), axis=1), np.nan)
        moved_c = df_new[df_new["Resource_Pass/Fail"] == 0]
        moved_f = df_new[(df_new["Resource_Pass/Fail"] == 1) & (df_new["type"] == "moved")]
        moved_a = df_new[(df_new["Resource_Pass/Fail"] == 1) & (df_new["type"] != "moved")]
        moved_c.reset_index(drop=True, inplace=True)
        moved_f.reset_index(drop=True, inplace=True)
        moved_a.reset_index(drop=True, inplace=True)
        unixtime = df["unixtime"]
        list_moved_i = list(df_new.index[(df_new["type"] == "moved")])
        list_moved_p = list(df_new.loc[list_moved_i, "parameter"])
        unixtime = list(unixtime.loc[list_moved_i])
        dic_moved = {"index": list_moved_i, "parameter": list_moved_p, "Timestamp": unixtime}
        list_moved = pd.DataFrame(dic_moved)
        list_moved_1 = list_moved["index"]
        list_moved_2 = list_moved.apply(lambda row: row["Timestamp"] + row["parameter"], axis=1)
        list_moved_2 = list_moved_2.apply(lambda row: datetime.datetime.utcfromtimestamp(row))
        moved_f["Timestamp"] = list_moved_2
        df_new = pd.concat([moved_f, moved_c, moved_a])
        df_new = df_new.sort_values(by=["Case", "order"], ascending=[True, True])
        df_new.reset_index(drop=True, inplace=True)
        return df_new

    # Same events are recorded more than one time
    def rework(self, df):

        df_new = pd.DataFrame.copy(df)
        col = list(df_new.columns)
        list_rework_i = list(df_new.index[(df_new["type"] == "rework") & (df_new["cusum"] == 1)])
        list_rework_c = df_new.loc[list_rework_i]
        list_rework = np.repeat(a=list_rework_c.values, repeats=list_rework_c["parameter"].astype("int"), axis=0)
        list_rework = pd.DataFrame(list_rework, columns=col)
        df_new = pd.concat([df_new, list_rework])
        df_new = df_new.sort_values(by=["Case", "order"], ascending=[True, True])
        df_new.reset_index(inplace=True, drop=True)
        return df_new

    # Unrelated event is recorded in a case
    def insert(self, df):

        df_new = pd.DataFrame.copy(df)
        act_a = list(df["Activity"].unique())
        act_c = df_new.groupby(["Case"])["Activity"].unique()
        act_r = df_new.groupby(["Activity"])["Resource"].unique()
        act_c = act_c.apply(lambda x: list(set(act_a) - set(x)))
        list_insert_i = list(df_new.index[(df_new["type"] == "insert") & (df_new["cusum"] == 1)])
        list_insert_c = df_new.loc[list_insert_i]

        list_insert_c["duration"] = list_insert_c.apply(lambda x: random.randrange(0, x["duration"] + 1), axis=1)
        list_insert_c["Activity"] = list_insert_c.apply(
            lambda x: random.choice(act_c[x["Case"]]), axis=1)
        list_insert_c["Resource"] = list_insert_c.apply(lambda x: random.choice(act_r[x["Activity"]]),
                                                        axis=1)
        list_insert_c["Timestamp"] = list_insert_c.apply(
            lambda x: x["Timestamp"] + timedelta(seconds=x["duration"]), axis=1)
        df_new = pd.concat([df_new, list_insert_c])
        df_new = df_new.sort_values(by=["Case", "order"], ascending=[True, True])
        df_new.reset_index(inplace=True, drop=True)
        return df_new

    # Events are recorded in wrong case
    def switch(self, df):

        df_new = pd.DataFrame.copy(df)
        df_new["resource_anomaly_type"] = np.where(df_new["resource_anomaly_type"] == "switch", "switch_from", df_new["resource_anomaly_type"])
        c_list = df_new[(df_new["cusum"] == 1) & (df_new["type"] == "switch") & (df_new["order"] != 1)]
        c_list = c_list.groupby(["cusum"])["Case"].unique()
        c_list = list(c_list[1])
        list_n_i = list(df_new.index[(df_new["cusum"] == 0) & (df_new["parameter_r"].isin(c_list))])
        list_n_c = list(df_new.loc[list_n_i, "Case"])
        list_n_ts = list(df_new.loc[list_n_i, "Timestamp"])
        list_n_d = list(df_new.loc[list_n_i, "duration"])
        list_switch_i = list(df_new.index[(df_new["type"] == "switch") & (df_new["cusum"] == 1) & (df_new["order"] != 1)])
        list_switch_c = list(df_new.loc[list_switch_i, "Case"])
        list_switch_p = list(df_new.loc[list_switch_i, "parameter"])
        list_switch_ts = list(df_new.loc[list_switch_i, "Timestamp"])
        dic_switch = {"index": list_switch_i, "Case": list_switch_c, "parameter": list_switch_p,
                     "parameter_c": list_n_c,
                     "Timestamp": list_switch_ts, "Timestamp_c": list_n_ts, "duration": list_n_d}
        list_switch = pd.DataFrame(dic_switch)
        list_switch_1 = list_switch.apply(lambda row: np.arange(row["index"], int(row["index"] + row["parameter"]), 1),
                                        axis=1)
        list_switch_1 = np.concatenate(list_switch_1)
        list_switch_2 = list_switch.apply(lambda row: np.repeat(a=row["parameter_c"], repeats=row["parameter"]),
                                        axis=1)
        list_switch_2 = np.concatenate(list_switch_2)
        list_switch_3 = list_switch.apply(lambda row: np.repeat(a=row["Timestamp_c"], repeats=row["parameter"]), axis=1)
        list_switch_3 = np.concatenate(list_switch_3)
        list_switch_4 = list_switch.apply(lambda row: np.repeat(a=row["duration"] / (row["parameter"] + 1), repeats=row["parameter"]), axis=1)
        list_switch_4 = list(map(lambda x: x.cumsum(), list_switch_4))
        list_switch_4 = np.concatenate(list_switch_4)
        list_switch_5 = pd.DataFrame(list(map(lambda x, y: x + timedelta(seconds=y), list_switch_3, list_switch_4)), columns=["Timestamp"])
        list_switch_i2 = set(list_switch_1)
        list_clean = [x for x in list(df_new.index) if x not in list_switch_i2]
        switch_c = df_new.loc[list_clean]
        switch_f = df_new.loc[list_switch_1]
        switch_c.reset_index(inplace=True, drop=True)
        switch_f.reset_index(inplace=True, drop=True)
        switch_f["resource_parameter"] = switch_f.apply(lambda x: "caseID = {0}".format(x["Case"]), axis=1)
        switch_f["Case"] = list_switch_2
        switch_f["Timestamp"] = list_switch_5
        df_new = pd.concat([switch_c, switch_f])
        df_new.loc[df_new["Case"].isin(list_n_c), "resource_anomaly_type"] = "switch_to"
        df_new = df_new.sort_values(by=["Case", "order"], ascending=[True, True])
        df_new.reset_index(inplace=True, drop=True)
        return df_new

    def choice_act(self, act, x):

        act_new = []
        for i in range(len(act)):
            act_new.append(act[i])
        act_new.remove(x)
        activity = random.choice(act_new)
        return activity
    def replace(self, df):

        df_new = pd.DataFrame.copy(df)
        act = list(df["Activity"].unique())
        list_replace_i = list(df_new.index[(df_new["type"] == "replace") & (df_new["cusum"] == 1)])
        list_replace_p = list(df_new.loc[list_replace_i, "parameter"])
        dic_replace = {"index": list_replace_i, "parameter": list_replace_p}
        list_replace = pd.DataFrame(dic_replace)
        list_replace_1 = list_replace.apply(lambda row: np.arange(row["index"], int(row["index"] + row["parameter"]), 1), axis=1)
        list_replace_1 = np.concatenate(list_replace_1)
        list_replace_act = list(df_new.loc[list_replace_1, "Activity"])
        list_replace_act = list(map(lambda x: self.choice_act(act, x), list_replace_act))
        df_new.loc[list_replace_1, "Activity"] = list_replace_act
        df_new = df_new.sort_values(by=["Case", "order"], ascending=[True, True])
        df_new.reset_index(inplace=True, drop=True)
        return df_new

    # Implement functions and save result
    def implement(self, types, mag=[], m_skip=1, m_form=2, h_moved=1, m_switch=1, m_insert=1, m_rework=1, m_replace=1, df_res=None):

        if df_res is None:
            df_res = self.input_file    #event logs with "Pass/Fail"
        else:
            pass
        from PageTwo_Inject_Anomaly import Inject_Anomaly
        if self.seedBox.get("1.0", "end-1c") != '':
            seed_value = int(self.seedBox.get("1.0", "end-1c"))
            np.random.seed(seed_value)

        Inject_Anomaly.text_progress.insert(tk.END, "<Resource> Started preprocessing to set the input of anomaly patterns\n")
        Inject_Anomaly.root.update()
        time.sleep(1)
        print("Started preprocessing to set the input of anomaly patterns")
        start_parameter = datetime.datetime.now()
        df_1 = self.setting1(df_res, types, mag)
        df_new = self.setting2(df_1, m_skip, m_form, h_moved, m_switch, m_insert, m_rework, m_replace)
        end_parameter = datetime.datetime.now()
        Inject_Anomaly.text_progress.insert(tk.END, "<Resource> Finished preprocessing (running time={0})\n".format(end_parameter-start_parameter))
        Inject_Anomaly.root.update()
        time.sleep(1)
        print("Finished preprocessing (running time={0})".format(end_parameter-start_parameter))
        types2 = df_new['type'].unique()
        types2 = [x for x in types2 if str(x) != 'nan']
        if "incomplete" in types2:
            types2.remove("incomplete")
            types2.append("incomplete")
        else:
            pass
        Inject_Anomaly.text_progress.insert(tk.END, "<Resource> Started to inject anomaly patterns: {0}\n".format(types2))
        Inject_Anomaly.root.update()
        time.sleep(1)
        print("Started to inject anomaly patterns")
        start_inject = datetime.datetime.now()
        for i in range(len(types2)):
            if types2[i] == "skip":
                df_new = self.skip(df_new)
                Inject_Anomaly.text_progress.insert(tk.END, "<Resource> Finished skip ({0}/{1})\n".format(i + 1, len(types2)))
                Inject_Anomaly.text_progress.see(tk.END)
                Inject_Anomaly.root.update()
                time.sleep(1)
            elif types2[i] == "incomplete":
                df_new = self.incomplete(df_new)
                Inject_Anomaly.text_progress.insert(tk.END, "<Resource> Finished incomplete ({0}/{1})\n".format(i + 1, len(types2)))
                Inject_Anomaly.text_progress.see(tk.END)
                Inject_Anomaly.root.update()
                time.sleep(1)
            elif types2[i] == "switch":
                df_new = self.switch(df_new)
                Inject_Anomaly.text_progress.insert(tk.END, "<Resource> Finished switch ({0}/{1})\n".format(i + 1, len(types2)))
                Inject_Anomaly.text_progress.see(tk.END)
                Inject_Anomaly.root.update()
                time.sleep(1)
            elif types2[i] == "form based":
                df_new = self.form_based(df_new)
                Inject_Anomaly.text_progress.insert(tk.END, "<Resource> Finished form based ({0}/{1})\n".format(i + 1, len(types2)))
                Inject_Anomaly.text_progress.see(tk.END)
                Inject_Anomaly.root.update()
                time.sleep(1)
            elif types2[i] == "rework":
                df_new = self.rework(df_new)
                Inject_Anomaly.text_progress.insert(tk.END, "<Resource> Finished rework ({0}/{1})\n".format(i + 1, len(types2)))
                Inject_Anomaly.text_progress.see(tk.END)
                Inject_Anomaly.root.update()
                time.sleep(1)
            elif types2[i] == "moved":
                df_new = self.moved(df_new)
                Inject_Anomaly.text_progress.insert(tk.END, "<Resource> Finished moved({0}/{1})\n".format(i + 1, len(types2)))
                Inject_Anomaly.text_progress.see(tk.END)
                Inject_Anomaly.root.update()
                time.sleep(1)
            elif types2[i] == "insert":
                df_new = self.insert(df_new)
                Inject_Anomaly.text_progress.insert(tk.END, "<Resource> Finished insert ({0}/{1})\n".format(i + 1, len(types2)))
                Inject_Anomaly.text_progress.see(tk.END)
                Inject_Anomaly.root.update()
                time.sleep(1)
            elif types2[i] == "replace":
                df_new = self.replace(df_new)
                Inject_Anomaly.text_progress.insert(tk.END, "<Resource> Finished replace ({0}/{1})\n".format(i + 1, len(types2)))
                Inject_Anomaly.text_progress.see(tk.END)
                Inject_Anomaly.root.update()
                time.sleep(1)
            else:
                pass

        df_new["order_b"] = df_new["order"]
        df_new["trace_temp"] = np.nan
        df_new["trace_change_resource"] = np.nan
        df_new = df_new.sort_values(by=["Case", "Timestamp"], ascending=[True, True])
        df_new["Resource_Pass/Fail"] = pd.to_numeric(df_new["Resource_Pass/Fail"])
        df_new["cusum"] = df_new.groupby(["Case"])["Resource_Pass/Fail"].cumsum()
        df_2 = pd.DataFrame.copy(df_new)
        df_2["check"] = 1
        df_new["order"] = df_2.groupby(["Case"])["check"].cumsum()
        df_new["max"] = df_new.groupby(["Case"])["order"].transform("max")
        df_3 = df_new.shift(-1, axis=0)
        df_new["duration"] = df_3["Timestamp"] - df_new["Timestamp"]
        df_new.loc[(df_new["order"] == df_new["max"]), "duration"] = datetime.timedelta()
        df_new["duration"] = df_new.apply(lambda x: x["duration"].seconds, axis=1)
        df_new["trace_temp"] = np.where(df_new["order"] != df_new["order_b"], 1, 0)
        df_new["trace_change_resource"] = df_new.groupby(["Case"])["trace_temp"].transform("max")
        df_new["trace_change_resource"] = np.where((df_new["resource_anomaly_type"] == "skip") | (df_new["resource_anomaly_type"] == "switch_from") | (df_new["resource_anomaly_type"] == "switch_to") | (df_new["resource_anomaly_type"] == "incomplete"), 1, df_new["trace_change_resource"])
        df_new = df_new[["Case", "Event", "Activity", "Timestamp", "unixtime", "Resource", "Resource_failure_rate", "Resource_Pass/Fail", "order", "resource_anomaly_type", "resource_parameter", "trace_change_resource"]]
        end_inject = datetime.datetime.now()
        Inject_Anomaly.text_progress.insert(tk.END, "<Resource> Finished to inject anomaly patterns (running time={0})\n".format(end_inject-start_inject))
        Inject_Anomaly.root.update()
        time.sleep(1)
        np.random.seed(0)
        df_cal = df_new.sort_values(by=["Case", "Timestamp"], ascending=[True, True])
        df_cal_a = list(df_cal.groupby(["Case"])["Activity"])
        df_cal_b = []
        for i in range(len(df_cal_a)):
            df_cal_b.append(tuple(df_cal_a[i][1].reset_index(drop=True)))
        df_cal_c = list(set(df_cal_b))
        df_cal_d = {}
        for i in range(len(df_cal_c)):
            df_cal_d[df_cal_c[i]] = "var_{0}".format(i)
        df_cal_e = {}
        for i in range(len(df_cal_a)):
            df_cal_e[df_cal_a[i][0]] = df_cal_d[tuple(df_cal_a[i][1].reset_index(drop=True))]
        df_new2 = pd.DataFrame.copy(df_new)
        df_new2["variant_num"] = np.nan
        df_new2["variant_num"] = df_new2.apply(lambda x: df_cal_e[x["Case"]], axis=1)
        print("Finished to inject anomaly patterns (running time={0})".format(end_inject-start_inject))
        # global data_with_anomalies
        # data_with_anomalies = df_new
        # data_with_anomalies.to_csv("data_with_anomalies_res.csv", mode='w', index=False)
        PageThree.after = df_new
        return df_new2

    def implement_resource(self, types, mag=[], m_skip=1, m_form=2, h_moved=1, m_switch=1, m_insert=1, m_rework=1, m_replace=1, df_res=None):

        df_r = self.implement(types, mag, m_skip, m_form, h_moved, m_switch, m_insert, m_rework, m_replace, df_res)
        df_p = data_with_parameter_res
        df_p = df_p.drop(["parameter_l", "parameter_r", "parameter"], axis=1)
        # df_r.to_csv("data_with_anomalies_res.csv", mode='w', index=False)
        messagebox.showinfo("Successfully Applied", "Successfully Applied")
        return df_r
