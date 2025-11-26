import pandas as pd

df = pd.read_csv('Solar data cal poly csv.csv')
def str_to_float(s:str):
    try:
        fl = float(s)
        return fl
    except ValueError:
        return 0


class Energy:
    def __init__(self, year, month, day, goldtree, housing):
        self.year = year
        self.month = month
        self.day = day
        self.goldtree = goldtree
        self.housing = housing
    def __repr__(self):
        return 'Energy Data({}, {}, {}, {}, {})'.format(
        self.year,
        self.month,
        self.day,
        self.goldtree,
        self.housing)


def get_data():
    with open('Solar data cal poly csv.csv') as f:
        data = []
        for line in f:
            li = line.split(",")
            date = li[0].split(" ")
            dale = date[0].split("-")
            if len(dale) == 3:
                year1 = int(dale[0])
                month1 = int(dale[1])
                day1 = int(dale[2])
            if len(li) == 5:
                goldtree1 = str_to_float(li[3])
                housing1 = str_to_float(li[4])
            if len(li) == 5 and len(dale) == 3 and not goldtree1 ==0 and not housing1 ==0:
                en = Energy(year1, month1, day1, goldtree1, housing1)
                data.append(en)

    return data

