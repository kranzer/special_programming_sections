from spyre import server
import pandas as pd
import os
class MyApp(server.App):
    title = "Daniel's APP"
    inputs = [
        {
            "type": "dropdown",
            "id": "file",
            "label": "Provience file",
            "options": [{"label": filename, "value": filename} for filename in os.listdir("data")],
            "key": 'file',
            "action_id": "update"
        },
        {
            "type": "dropdown",
            "id": "year",
            "label": "Year",
            "options": [{"label": year, "value": year} for year in range(1981, 2018)],
            "key": "year",
            "action_id": "update",
        },
        {
            "type": "dropdown",
            "id": "week1",
            "label": "Week to start",
            "options": [{"label": week1, "value": week1} for week1 in range(1, 53)],  # fix 1981 and 2017
            "key": "week1",
            "action_id": "update",
        },
        {
            "type": "dropdown",
            "id": "week2",
            "label": "Finishing week",
            "options": [{"label": week2, "value": week2} for week2 in range(1, 53)],
            "key": "week2",
            "action_id": "update",
        },
        {
            "type": "dropdown",
            "id": "type",
            "label": "Researchable index",
            "options": [
                {"label": "VHI", "value": "VHI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VCI", "value": "VCI"},
                {"label": "SMT", "value": "SMT"},
                {"label": "SMN", "value": "SMN"},
            ],
            "key": "type",
            "action_id": "update",
        }
    ]
    outputs = [
        {
            "type": "table",
            "id": "table_year",
            "control_id": "update",
            "tab": "Table"
        },
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update",
            "tab": "Plot",
        }
    ]
    controls = [
        {
            "type": "hidden",
            "id": "update",
        }
    ]
    tabs = [
        "Table",
        "Plot",
    ]

    def getData(self, params):
        filename = params["file"]
        year = int(params["year"])
        sweek = int(params["week1"])
        fweek = int(params["week2"])
        df = pd.read_csv("data/" + filename, index_col=False, engine='python', header=0)
        df = df.ix[df.year == year]
        return df[(df.week >= sweek) & (df.week <= fweek)]

    def getPlot(self, params):
        df = self.getData(params).set_index('week')
        type_index = params["type"]
        df = df[[type_index]]
        plt_obj = df.plot()
        plt_obj.set_ylabel(type_index)
        plt_obj.set_title(type_index + " for week range you chose")
        plt_obj.grid()
        return plt_obj.get_figure()
app = MyApp()
app.launch()