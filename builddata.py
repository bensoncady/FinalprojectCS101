
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
    def __eq__(self, other):
        return self.year == other.year and self.month == other.month and self.day == other.day and self.goldtree == other.goldtree and self.housing == other.housing and type(self) == type(other)


def get_data():
    with open('Solar data cal poly csv.csv') as f:
        data = []
        for line in f:
            linesplit = line.split(",")
            date = linesplit[0].split(" ")
            datesplit = date[0].split("-")
            if len(datesplit) == 3:
                year1 = int(datesplit[0])
                month1 = int(datesplit[1])
                day1 = int(datesplit[2])
            if len(linesplit) == 5:
                goldtree1 = str_to_float(linesplit[3])
                housing1 = str_to_float(linesplit[4])
            if len(linesplit) == 5 and len(datesplit) == 3 and not goldtree1 ==0 and not housing1 ==0:
                en = Energy(year1, month1, day1, goldtree1, housing1)
                data.append(en)

    return data

