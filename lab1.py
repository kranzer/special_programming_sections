import requests, os
import pandas as pd
from time import strftime, gmtime
from bs4 import BeautifulSoup

if not os.path.isdir("data"):
    os.makedirs("data")


def get_file(index):
    vhi_url = requests.get('https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID={}&year1=1981&year2=2017&type=Mean'.format(index))
    soup = BeautifulSoup(vhi_url.text)
    text = soup.body.tt.pre.getText().replace('year,week,, provinceID, SMN,SMT,VCI,TCI,VHI', 'year,week,SMN,SMT,VCI,TCI,VHI').replace(',', ' ').replace('   ', ' ').replace('  ', ' ').replace(' ',',')
    filename = 'data/provience-{0}-{1}.csv'.format(index, strftime('_%Y-%m-%d_%H:%M', gmtime()))
    output = open(filename, 'w')
    output.write(text)
    output.close()


def change_names(filedir):
    names_dict = {"1": "24", "2": "25", "3": "5", "4": "6", "5": "27", "6": "23", "7": "26",
                  "8": "7", "9": "11", "10": "13", "11": "14", "12": "15", "13": "16", "14": "17",
                  "15": "18", "16": "19", "17": "21", "18": "22", "19": "8", "20": "9", "21": "10",
                  "22": "1", "23": "3", "24": "2", "25": "4"}
    for filename in os.listdir(filedir):
        for k, v in names_dict.items():
            if v == filename.split("-")[1]:
                filename1 = filename
                filename1 = "data/renamed_"+filename1.replace('-{}-'.format(v), '-{}-'.format(k))
                os.rename("data/"+filename, filename1)


def create_data_frame(filedir):
    frame_dict = {}
    for filename in os.listdir(filedir):
        if filename.endswith('.csv') and "renamed" in filename:
            frame_dict[filename] = pd.read_csv(filedir+"/"+filename, index_col=False, header=0)
    return frame_dict


def count_data_per_year(data_frame, year):
    data_dict = {}
    data_frame = data_frame[data_frame['year'] == year].set_index("year")
    data_dict['year'] = year
    data_dict['VHI_of_year'] = data_frame['VHI'].tolist()
    data_dict['min_VHI'] = data_frame['VHI'].min()
    data_dict['max_VHI'] = data_frame['VHI'].max()
    return data_dict


def extreme_conditions(percent):
    vhi_url = requests.get('https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID=19&year1=1981&year2=2017&type=VHI_Parea')
    soup = BeautifulSoup(vhi_url.text)
    text = soup.body.tt.pre.getText().replace('year,week,, provinceID, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95,100',
                                              'year,week, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95,100').replace(',', ' ').replace('   ',' ').replace('  ', ' ').replace(' ', ',')
    filename = 'temp.csv'
    output = open(filename, 'w')
    output.write(text)
    output.close()
    vhi_frame = pd.read_csv('temp.csv', index_col=False, header=0)
    dict_of_years = {}
    list_of_years = []
    for year in range(1981, 2018):
        short_frame = vhi_frame[vhi_frame.year == year][['0', '5', '10', '15']]
        list_sum = 0
        for i in list(short_frame.columns.values):
            list_sum += short_frame[i].mean()
        dict_of_years["{}".format(year)] = list_sum
    series_year = pd.Series(dict_of_years)
    print(series_year.items)

    for key in series_year.keys():
        if series_year[key] > percent:
            list_of_years.append(key)
    print(list_of_years)
    return list_of_years


def neutral_conditions(percent):
    vhi_url = requests.get('https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID=19&year1=1981&year2=2017&type=VHI_Parea')
    soup = BeautifulSoup(vhi_url.text)
    text = soup.body.tt.pre.getText().replace('year,week,, provinceID, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95,100',
                                              'year,week, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95,100').replace(',', ' ').replace('   ',' ').replace('  ', ' ').replace(' ', ',')
    filename = 'temp.csv'
    output = open(filename, 'w')
    output.write(text)
    output.close()
    vhi_frame = pd.read_csv('temp.csv', index_col=False, header=0)
    dict_of_years = {}
    list_of_years = []
    for year in range(1981, 2018):
        short_frame = vhi_frame[vhi_frame.year == year][['20', '25', '30', '35']]
        list_sum = 0
        for i in list(short_frame.columns.values):
            list_sum += short_frame[i].mean()
        dict_of_years["{}".format(year)] = list_sum
    series_year = pd.Series(dict_of_years)
    print(series_year.items)

    for key in series_year.keys():
        if series_year[key] > percent:
            list_of_years.append(key)
    print(list_of_years)
    return list_of_years

def main():
    #for index in range(1, 28):
    #    get_file(index)
    #change_names("data")

    dfs = create_data_frame("data")
    df1 = dfs['renamed_provience-16-_2017-02-26_12:49.csv']
    print(count_data_per_year(df1, 1990))
    extreme_conditions(5)
    neutral_conditions(25)


if __name__ == "__main__":
    main()
