import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
from datetime import datetime as dt
import tkinter as tk
from tkinter import messagebox
import time
import random

#Pages
from PageThree import PageThree

class Abnorm_sys():

    def __init__(self, sys_file, log_file, old_file):

        self.sys_file = sys_file
        self.log_file = log_file
        self.old_file = old_file

    # Data about which system make error
    def dataframe_sys(self):

        df = pd.read_csv(self.sys_file)
        return df

    # Event logs
    def dataframe_log(self):

        df = pd.read_csv(self.log_file)
        return df

    # Preprocess: to make new attribute 'type' and 'parameter' value in system error data
    def setting1_sys(self, df, mag, types, h_skip, h_form, h_cut):

        mag_c = []
        df["type"] = np.nan
        df["parameter"] = np.nan
        df["down_start"] = np.nan
        df["down_start"] = df["Start_Timestamp"]
        df.drop(columns="Start_Timestamp")
        df["down_finish"] = np.nan
        df["unixtime"] = np.nan
        for i in range(len(mag)):
            if mag[i] != 0:
                mag_c.append(mag[i])
            else:
                pass
        types_a = np.array(types)
        if sum(mag) == 1:
            num_fail = len(df)
            applied_patterns = np.repeat(random.choice(types), num_fail)
            df["type"] = applied_patterns
        else:
            applied_patterns = np.repeat(types_a, mag_c)
            df["type"] = df["type"].apply(lambda x: random.choice(applied_patterns))
        df_new = pd.DataFrame.copy(df)
        df_new["unixtime"] = df_new["down_start"].apply(lambda x: (x - dt(1970, 1, 1)).total_seconds())
        if "skip" in df_new["type"].unique():
            df_new.loc[(df_new["type"] == "skip"), "parameter"] = df_new["parameter"].apply(lambda x: random.randint(0, h_skip))
        else:
            pass
        if "form based" in df_new["type"].unique():
            df_new.loc[(df_new["type"] == "form based"), "parameter"] = df_new["parameter"].apply(lambda x: random.randint(0, h_form))
        else:
            pass
        if "cut" in df_new["type"].unique():
            df_new.loc[(df_new["type"] == "cut"), "parameter"] = df_new["parameter"].apply(lambda x: random.randint(0, h_cut))
        else:
            pass
        df_new["down_finish"] = df_new.apply(lambda x: x["unixtime"] + x["parameter"], axis=1)
        df_new["down_finish"] = df_new["down_finish"].apply(lambda x: datetime.datetime.utcfromtimestamp(x))
        df_new.reset_index(drop=True, inplace=True)
        print("end setting1_sys")
        return df_new

    # Preprocess: to make new attribute 'type' and 'parameter' value in event logs(system)
    def setting2_sys(self, df_log, df_sys):
        pd.set_option('display.max_columns', 30)
        pd.set_option('display.width', 500)
        df_log["type"] = np.nan
        df_log["down_start"] = np.nan
        df_log["down_finish"] = np.nan
        df_log["down_duration"] = np.nan
        df_log = df_log.sort_values(by=["Case", "Timestamp"], ascending=[True, True])
        for i in range(len(df_sys)):
            df_log["type"] = np.where((df_log["System"] == df_sys.loc[i, "Event:system down"]) & (df_sys.loc[i, "down_start"] <= df_log["Timestamp"]) & (df_log["Timestamp"] < df_sys.loc[i, "down_finish"]), df_sys.loc[i, "type"], df_log["type"])
            df_log["down_start"] = np.where((df_log["System"] == df_sys.loc[i, "Event:system down"]) & (df_sys.loc[i, "down_start"] <= df_log["Timestamp"]) & (df_log["Timestamp"] < df_sys.loc[i, "down_finish"]), df_sys.loc[i, "down_start"], df_log["down_start"])
            df_log["down_finish"] = np.where((df_log["System"] == df_sys.loc[i, "Event:system down"]) & (df_sys.loc[i, "down_start"] <= df_log["Timestamp"]) & (df_log["Timestamp"] < df_sys.loc[i, "down_finish"]), df_sys.loc[i, "down_finish"], df_log["down_finish"])
            df_log["down_start"] = df_log["down_start"].apply(lambda x: datetime.datetime.utcfromtimestamp(x//1000000000) if isinstance(x, int) is True else x)
            df_log["down_finish"] = df_log["down_finish"].apply(lambda x: datetime.datetime.utcfromtimestamp(x // 1000000000) if isinstance(x, int) is True else x)
        df_log["down_duration"] = df_log.apply(lambda x: x["down_finish"] - x["down_start"], axis=1)
        df_log.reset_index(drop=True, inplace=True)
        df_new = pd.DataFrame.copy(df_log)
        df_log["length"] = 1
        df_log["check"] = 0
        df_log["check"] = np.where(df_log["type"] != "nan", 1, 0)
        df_new["cusum"] = df_log.groupby(["Case"])["check"].cumsum()
        df_new["order"] = df_log.groupby(["Case"])["length"].cumsum()
        df_new["max"] = df_new.groupby(["Case"])["order"].transform("max")
        df_ct = df_new.loc[(df_new["cusum"] == 1) & (df_new["type"].isin(["skip", "form based", "cut"]))]
        df_ct["sys_anomaly_type"] = df_ct["type"]
        df_ct["sys_parameter"] = df_ct.apply(lambda x: "sysID = {0}, start = {1}, end = {2}, duration = {3}".format(x["System"], x["down_start"], x["down_finish"], x["down_duration"]), axis=1)
        df_ct = df_ct[["Case", "sys_anomaly_type", "sys_parameter"]]
        df_new = pd.merge(df_new, df_ct, on="Case", how="outer")
        df_new.loc[df_new["sys_anomaly_type"].isna(), "sys_anomaly_type"] = "normal"
        df_new.reset_index(drop=True, inplace=True)
        global data_with_parameter_sys
        data_with_parameter_sys = df_new
        PageThree.data_with_parameter_sys = data_with_parameter_sys
        # df_new.to_csv("data_with_parameter2.csv", mode='w', index=False)
        print("end setting2_sys")
        return df_new

    # Events are not recorded
    def skip_sys(self, df):

        df_new = pd.DataFrame.copy(df)
        list_skip = list(df_new.index[(df_new["type"] == "skip")])
        df_new = df_new.drop(list_skip)
        df_new.reset_index(drop=True, inplace=True)
        return df_new

    # Events have same timestamp (Get timestamp when error finished)
    def form_based_sys(self, df):

        df_new = pd.DataFrame.copy(df)
        list_form = list(df_new.index[(df_new["type"] == "form based")])
        df_new.loc[list_form, "Timestamp"] = df_new.loc[list_form, "down_finish"]
        df_new.reset_index(drop=True, inplace=True)
        return df_new

    # Last events in a case are recorded as different case
    def cut(self, df):

        df_new = pd.DataFrame.copy(df)
        df_new["sys_anomaly_type"] = np.where(df_new["sys_anomaly_type"] == "cut", "cut_from", df_new["sys_anomaly_type"])
        list_cut_i = list(df_new.index[(df_new["type"] == "cut")])
        list_cut_p = list(df_new.loc[list_cut_i, "order"])
        list_cut_m = list(df_new.loc[list_cut_i, "max"])
        dic_cut = {"index": list_cut_i, "order": list_cut_p, "max": list_cut_m}
        list_cut = pd.DataFrame(dic_cut)
        list_cut = list_cut.apply(lambda row: np.arange(row["index"], row["index"] + row["max"] - row["order"] + 1, 1), axis=1)
        if len(list_cut)>0 :
            list_cut = list(set(np.concatenate(list_cut)))
            df_new.loc[list_cut, "sys_anomaly_type"] = "cut_to"
            df_new.loc[list_cut, "sys_parameter"] = df_new.apply(lambda x: "caseID = {0}".format(x["Case"]), axis=1)
            df_new.loc[list_cut, "Case"] = df_new.apply(lambda x: "{0}_1".format(x["Case"]), axis=1)
            df_new.reset_index(drop=True, inplace=True)
        else:
            pass
        return df_new

    # Implement functions and save result
    def implement_sys(self, mag_sys, types_sys, h_skip, h_form, h_cut, df_log, df_sys): #df_log = event logs, df_sys = system error data
        if df_log is None:
            df_log = self.log_file
        else:
            pass
        if df_sys is None:
            df_sys = self.sys_file
        else:
            pass

        if self.seedBox.get("1.0", "end-1c") != '':
            seed_value = int(self.seedBox.get("1.0", "end-1c"))
            np.random.seed(seed_value)

        from PageTwo_Inject_Anomaly import Inject_Anomaly
        Inject_Anomaly.text_progress.insert(tk.END, "<System> Started preprocessing to set the input of anomaly patterns\n")
        Inject_Anomaly.text_progress.see(tk.END)
        time.sleep(1)
        Inject_Anomaly.root.update()
        start_parameter = datetime.datetime.now()
        df_sys = self.setting1_sys(df_sys, mag_sys, types_sys, h_skip, h_form, h_cut)
        df_new = self.setting2_sys(df_log, df_sys)

        df_sys["down_duration"] = df_sys.apply(lambda x: x["down_finish"] - x["down_start"], axis=1)
        PageThree.df_sys = df_sys

        end_parameter = datetime.datetime.now()
        Inject_Anomaly.text_progress.insert(tk.END, "<System> Finished preprocessing (running time={0})\n".format(end_parameter - start_parameter))
        Inject_Anomaly.text_progress.see(tk.END)
        Inject_Anomaly.root.update()
        time.sleep(1)
        Inject_Anomaly.text_progress.insert(tk.END, "<System> Started to inject anomaly patterns\n")
        Inject_Anomaly.text_progress.see(tk.END)
        Inject_Anomaly.root.update()
        time.sleep(1)
        print("Started to inject anomaly patterns")
        start_inject = datetime.datetime.now()
        for i in range(len(types_sys)):
            if types_sys[i] == "skip":
                df_new = self.skip_sys(df_new)
                Inject_Anomaly.text_progress.insert(tk.END, "<System> Finished skip ({0}/{1})\n".format(i + 1, len(types_sys)))
                Inject_Anomaly.text_progress.see(tk.END)
                Inject_Anomaly.root.update()
                time.sleep(1)
            elif types_sys[i] == "form based":
                df_new = self.form_based_sys(df_new)
                Inject_Anomaly.text_progress.insert(tk.END, "<System> Finished form based ({0}/{1})\n".format(i + 1, len(types_sys)))
                Inject_Anomaly.text_progress.see(tk.END)
                Inject_Anomaly.root.update()
                time.sleep(1)
            elif types_sys[i] == "cut":
                df_new = self.cut(df_new)
                Inject_Anomaly.text_progress.insert(tk.END, "<System> Finished cut ({0}/{1})\n".format(i + 1, len(types_sys)))
                Inject_Anomaly.text_progress.see(tk.END)
                Inject_Anomaly.root.update()
                time.sleep(1)
            else:
                pass
        df_new["Timestamp"] = df_new["Timestamp"].apply(lambda x: datetime.datetime.utcfromtimestamp(x // 1000000000) if isinstance(x, int) is True else x)
        df_new = df_new.sort_values(by=["Case", "Timestamp"], ascending=[True, True])
        df_new["order_b"] = df_new["order"]
        df_new["trace_temp"] = np.nan
        df_new["trace_change_system"] = np.nan
        df2 = pd.DataFrame.copy(df_new)
        df2["length"] = 1
        df2["check"] = 0
        df2["check"] = np.where(df2["type"] != "nan", 1, 0)
        df_new["cusum"] = df2.groupby(["Case"])["check"].cumsum()
        df_new["order"] = df2.groupby(["Case"])["length"].cumsum()
        df_new["max"] = df_new.groupby(["Case"])["order"].transform("max")
        df_new["trace_temp"] = np.where(df_new["order"] != df_new["order_b"], 1, 0)
        df_new["trace_change_system"] = df_new.groupby(["Case"])["trace_temp"].transform("max")
        df_new["trace_change_system"] = np.where((df_new["sys_anomaly_type"] == "cut_from") | (df_new["sys_anomaly_type"] == "skip"), 1, df_new["trace_change_system"])
        df_new = df_new.drop(["type", "down_finish", "down_start", "cusum", "max", "order_b", "trace_temp"], axis=1)
        end_inject = datetime.datetime.now()
        Inject_Anomaly.text_progress.insert(tk.END, "<System> Finished to inject anomaly patterns (running time={0})\n".format(end_inject - start_inject))
        Inject_Anomaly.text_progress.see(tk.END)
        Inject_Anomaly.root.update()
        time.sleep(1)
        print("end implement")
        global data_with_anomalies
        data_with_anomalies = df_new
        PageThree.after = df_new
        # df_new.to_csv("data_with_anomalies.csv", mode="w", index=False)

        return df_new

    def implement_sys_single(self, mag_sys, types_sys, h_skip, h_form, h_cut, df_log, df_sys):
        df = self.implement_sys(mag_sys, types_sys, h_skip, h_form, h_cut, df_log, df_sys)
        # df.to_csv("data_with_anomalies_sys.csv", mode="w", index=False)
        messagebox.showinfo("Successfully Applied", "Successfully Applied")

    def implement_bind(self, types_sys, types_re, mag_sys, mag_re=[], m_skip=1, m_form=2, h_moved=1, m_switch=1, m_rework=1, m_replace=1, h_skip=0, h_form=0, h_cut=0):

        df_old = self.old_file
        from abnormal_patterns import Abnorm_p
        df_res = Abnorm_p(df_old)
        df_re = df_res.implement(types_re, mag_re, m_skip, m_form, h_moved, m_switch, m_rework, m_replace, df_res=df_old)
        df_re = pd.merge(df_re, self.dat, on="Activity")
        df_sys = Abnorm_sys(sys_file=self.sys_file, log_file=df_re, old_file=df_old)
        df_new = df_sys.implement_sys(mag_sys, types_sys, h_skip, h_form, h_cut, df_log=df_re, df_sys=None)
        df_new["anomaly_type"] = np.nan
        df_new["anomaly_type"] = df_new.apply(lambda x:
                                              "{0}(res)".format(x["resource_anomaly_type"])
                                              if (x["resource_anomaly_type"] != "normal") &(x["sys_anomaly_type"] == "normal")
                                              else "{0}(sys)".format(x["sys_anomaly_type"])
                                              if (x["resource_anomaly_type"] == "normal") & (x["sys_anomaly_type"] != "normal")
                                              else "{0}(res), {1}(sys)".format(x["resource_anomaly_type"], x["sys_anomaly_type"])
                                              if (x["resource_anomaly_type"] != "normal") & (x["sys_anomaly_type"] != "normal")
                                              else "normal", axis=1)

        # df_new = df_new.drop(["sys_anomaly_type", "resource_anomaly_type"], axis=1)
        PageThree.after = df_new
        # df_new.to_csv("data_with_anomalies.csv", mode="w", index=False)
        messagebox.showinfo("Successfully Applied", "Completed to inject anomalies")
        return df_new






