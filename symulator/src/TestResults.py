import pandas as pd
import matplotlib.pyplot as plt

from src.Algorithms import *


class Test:
    def __init__(self, filename, cv, wl, interval_number, alg_type, avg_late, avg_latency, done_in_time_percent):
        self.filename = filename
        self.cv = cv
        self.wl = wl
        self.interval_number = interval_number
        self.alg_type = alg_type
        self.avg_late = avg_late
        self.avg_latency = avg_latency
        self.done_in_time_percent = done_in_time_percent

    def to_string(self):
        return format(', '.join("%s: %s" % item for item in vars(self).items()))


class TestsResults(object):
    test_list: List[Test]
    df: pd.DataFrame

    def __init__(self):
        self.test_list = []
        self.df = None

    def append(self, test_result):
        self.test_list.append(test_result)

    def print_all(self):
        for test in self.test_list:
            print(test.to_string())

    def read_from_file(self, filename):
        df = pd.read_csv(filename)
        self.df = df.groupby(["filename", "alg_type"]).mean().reset_index()

    def to_latex_table(self):
        pass

    def to_file(self, filename="output.txt", path=""):
        if self.df is None:
            self.to_data_frame()

        self.df.to_csv(path + filename, index=False)

    def to_data_frame(self):
        variables = ['filename', 'cv', 'wl', 'interval_number', 'alg_type', 'avg_late', 'avg_latency', 'done_in_time_percent']
        self.df = pd.DataFrame([[getattr(i, j) for j in variables] for i in self.test_list], columns=variables)
        self.df = self.df.groupby(["filename", "alg_type"]).mean().reset_index()

        return self.df

    def do_plot(self, df, variables, type=0, to_file=True, show=False, const_param="cv", const_param_values=[1], x_var="wl", output_path=""):
        variables = ['avg_late', 'avg_latency', 'done_in_time_percent']
        titles = ['Średni czas opóźnienia', 'Średni czas odpowiedzi', 'Zadania obsłużone w czasie [%]']
        const_param_values_len = len(const_param_values)
        fig, big_axes = plt.subplots(figsize=(15.0, const_param_values_len * 5.0), nrows=const_param_values_len,
                                     ncols=1, sharey=True)

        for row, big_ax in enumerate(big_axes, start=1):
            if x_var is "wl":
                big_ax.set_title("Współczynnik zmienności: " + str(const_param_values[row - 1]) + "\n", fontsize=16)
            else:
                big_ax.set_title("Obciążenie: " + str(const_param_values[row - 1]) + "\n", fontsize=16)
            big_ax.tick_params(labelcolor=(1., 1., 1., 0.0), top='off', bottom='off', left='off', right='off')
            big_ax._frameon = False
        if x_var is "wl":
            plot_kind = "scatter"
        else:
            plot_kind = "line"
        pos = 1
        for cpv in const_param_values:
            for i in range(3):
                title = titles[i]
                var = variables[i]
                ax = fig.add_subplot(const_param_values_len, 3, pos)
                ax.set_title(title)
                df[(df["alg_type"] == 0) & (df[const_param] == cpv)].plot(kind='line', x=x_var, y=var, color='red', ax=ax,
                                                                   label="Algorytm podstawowy")
                df[(df["alg_type"] == 1) & (df[const_param] == cpv)].plot(kind='line', x=x_var, y=var, color='blue', ax=ax,
                                                                   label="Algorytm ulepszony")
                df[(df["alg_type"] == 2) & (df[const_param] == cpv)].plot(kind='line', x=x_var, y=var, color='green', ax=ax,
                                                                   label="Algorytm podstawowy, const dt_max")
                df[(df["alg_type"] == 3) & (df[const_param] == cpv)].plot(kind='line', x=x_var, y=var, color='pink', ax=ax,
                                                                   label="Algorytm ulepszony, const dt_max")

                pos += 1

        fig.set_facecolor('w')
        plt.tight_layout()

        if to_file:
            if type == 0:
                output_filename = name = f'{output_path}{const_param}-{const_param_values[0]}-{const_param_values[-1]}.png'
            else:
                output_filename = name = f'{output_path}diff-{const_param}-{const_param_values[0]}-{const_param_values[-1]}.png'
            plt.savefig(output_filename)
        if show:
            plt.show()

    def plot_differences(self, to_file=True, show=False, const_param="cv", const_param_value=1, x_var="wl", output_path=""):
        if self.df is None:
            self.to_data_frame()
        df2 = self.df.loc[:, ["cv", "wl", "interval_number"]].drop_duplicates().reset_index()
        df1 = self.df.groupby("filename").diff().dropna().drop(["alg_type", "cv", "wl", "interval_number"], axis=1).rename(
            columns={"avg_late": "avg_late 1-0", "avg_latency": "avg_latency 1-0",
                     "done_in_time_percent": "done_in_time_percent 1-0"}).reset_index()
        df = pd.concat([df1, df2], axis=1)
        variables = ['avg_late 1-0', 'avg_latency 1-0', 'done_in_time_percent 1-0']
        self.do_plot(df, variables, 1, to_file, show, const_param, const_param_value, x_var, output_path)

    def plot_results(self, to_file=True, show=False, const_param="cv", const_param_values=[1], x_var="wl", output_path=""):
        if self.df is None:
            self.to_data_frame()
        df = self.df.sort_values(x_var)
        variables = ['avg_late', 'avg_latency', 'done_in_time_percent']

        self.do_plot(df, variables, 0, to_file, show, const_param, const_param_values, x_var, output_path)