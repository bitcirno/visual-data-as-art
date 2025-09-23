"""
SID: 25098892g
NAME: LUO DONGPU

This module requests tropical cyclone data from Hong Kong Observatory (HKO).

# tropical cyclone records. url: https://www.hko.gov.hk/dps/wxinfo/climat/warndb/tc.dat?s=20721
# ID  cyclone-type  cyclone-label signal direction start-time start-day start-month start-year direction end-time end-day end-month end-year direction last-time
# 202510	TD	MITAG	1	X	920	20	9	2025	X	1040	20	9	2025	X	0120

# tropical cyclone names. url: https://www.hko.gov.hk/dps/wxinfo/climat/warndb/tcname.dat?s=32084
# label chinese-name
# MITAG	米娜
"""

import requests
import datetime
import calendar
import os
from copy import deepcopy


DEBUG_MODE = False  # if enabled, data fetcher will read local cache data for faster speed
DATA_CACHE_DIR = "./data_cache"


class TCRecord:
    """
    This class defines a piece of tropical cyclone data
    """
    def __init__(self):
        self.id: int = 0
        self.tc_type: str = ""
        self.tc_type_short: str = ""
        self.tc_name_ch: str = ""
        self.tc_name_en: str = ""
        self.tc_signal: int = 0
        self.tc_signal_direction: str = ""
        self.tc_start_date: datetime.datetime = None
        self.tc_end_date: datetime.datetime = None

        # Using by DateNode
        self.from_last_to = 0  # 0:start, 1:last, 2:end, 3:start-end


class TCDataFetcher:
    """
    Requests the latest data from HKO and parse the data
    """
    tc_type2name = {
        "null": "Calm and Tranquil",
        "TD": "Tropical Depression",
        "TS": "Tropical Storm",
        "STS": "Severe Tropical Storm",
        "T": "Typhoon",
        "ST": "Severe Typhoon",
        "SuperT": "Super Typhoon"
    }

    def __init__(self):
        self.tc_name_list = {}
        self.tc_records: [TCRecord] = []  # records are following the time series
        self.month_record_cache = {}  # cache searched TC records

    def fetch_latest(self):
        """
        Get the latest tropical cyclone data from HKO
        """
        print(f"{'[Data]': <8} Fetching data from HKO...")

        if len(self.tc_name_list) == 0:
            self.__fetch_name_list()
            
        if DEBUG_MODE:
            path = os.path.join(DATA_CACHE_DIR, "TC_records.txt")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                f.close()
        else:
            content = requests.get("https://www.hko.gov.hk/dps/wxinfo/climat/warndb/tc.dat?s=20721").text

        # print(content)
        self.month_record_cache.clear()  # clear cache
        self.tc_records.clear()

        for line in content.split("\n"):
            if len(line) == 0:
                continue
            raw = line.replace("	", " ").split(" ")
            if len(raw) != 16:
                continue
            if len(raw[0]) != 6 or raw[0] == "0" or raw[0][:2] == "19":  # ignore 0 data and data before year 2000
                continue
            # print(" ".join(raw))
            # print(raw)
            self.tc_records.append(self.__parse_to_TCData(raw))

        print(f"{'[Data]': <8} Fetched the latest tropical cyclone records from HKO")

    def get_data_a_month(self, date: datetime.date) -> [TCRecord]:
        """
        Get the tropical cyclone data for a specific month
        """
        has_year_cache = date.year in self.month_record_cache
        if has_year_cache:
            month_record = self.month_record_cache[date.year]
            if date.month in month_record:
                # print("find cache:", date.year, date.month)
                return month_record[date.month]

        date_today = datetime.date.today()
        if date.year > date_today.year:
            return []
        if date.year == date_today.year and date.month > date_today.month:
            return []

        if len(self.tc_records) == 0:
            self.fetch_latest()

        _, num_days = calendar.monthrange(date.year, date.month)
        if date.year == date_today.year and date.month == date_today.month:
            num_days = min(num_days, date_today.day)
        dates: list[TCRecord | None]
        dates = [None] * num_days

        # Replace None by dates from start date to end date
        find_nodes = False
        for n in self.tc_records:
            s_date = n.tc_start_date
            e_date = n.tc_end_date
            if s_date.year == date.year and s_date.month == date.month:
                find_nodes = True
                for day in range(s_date.day, e_date.day+1):
                    node: TCRecord
                    node = deepcopy(n)
                    if s_date.day == e_date.day: node.from_last_to = 3
                    elif day == s_date.day: node.from_last_to = 0
                    elif day == e_date.day: node.from_last_to = 2
                    else: node.from_last_to = 1
                    dates[day-1] = node
            else:
                if find_nodes:
                    break

        # Fill the remaining None with no_tc data
        i: int
        for i in range(len(dates)):
            if dates[i]:
                continue
            e_date = TCRecord()
            e_date.tc_type_short = "null"
            e_date.tc_type = TCDataFetcher.tc_type2name["null"]
            e_date.tc_name_ch = " "
            e_date.tc_name_en = " "
            e_date.tc_start_date = datetime.datetime(year=date.year, month=date.month, day=i+1)
            e_date.tc_start_date = datetime.datetime(year=date.year, month=date.month, day=i+1)
            dates[i] = e_date

        if not has_year_cache:
            self.month_record_cache[date.year] = {}
            self.month_record_cache[date.year][date.month] = dates
        else:
            month_cache = self.month_record_cache[date.year]
            month_cache[date.month] = dates

        return dates

    def __fetch_name_list(self):
        """
        Get the tropical cyclone name list
        """
        if DEBUG_MODE:
            path = os.path.join(DATA_CACHE_DIR, "TC_name_list.txt")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                f.close()
        else:
            content = requests.get("https://www.hko.gov.hk/dps/wxinfo/climat/warndb/tcname.dat?s=32084").text
        for line in content.split("\n"):
            if len(line) == 0:
                continue
            name_label = line.replace("\t", " ").split(" ")
            if len(name_label) != 2:
                continue
            # print(name_label)
            self.tc_name_list[name_label[0]] = name_label[1]
        self.tc_name_list["null"] = " "
        # print(self.tc_name_list)

    @staticmethod
    def __parse_hour_minute(raw) -> tuple[int, int]:
        if len(raw) == 2:
            return 0, eval(raw)
        return int(raw[:-2]), int(raw[-2:])

    def __parse_to_TCData(self, raw: []) -> TCRecord:
        record = TCRecord()
        record.id = eval(raw[0])
        if raw[1] not in TCDataFetcher.tc_type2name:
            record.tc_type = "Type Unknown"
            record.tc_type_short = "TS"  # using default
        else:
            record.tc_type = TCDataFetcher.tc_type2name[raw[1]]
            record.tc_type_short = raw[1]
        if raw[2] not in self.tc_name_list:
            record.tc_name_en = "Name Unknown"
            record.tc_name_ch = "未知"
        else:
            record.tc_name_en = raw[2]
            record.tc_name_ch = self.tc_name_list[raw[2]]
        record.tc_signal = eval(raw[3])
        record.tc_signal_direction = "" if raw[4] == "X" else raw[4]
        h, m = self.__parse_hour_minute(raw[5])
        record.tc_start_date = datetime.datetime(hour=h, minute=m,
                                                 day=eval(raw[6]), month=eval(raw[7]), year=eval(raw[8]))
        h, m = self.__parse_hour_minute(raw[10])
        record.tc_end_date = datetime.datetime(hour=h, minute=m,
                                               day=eval(raw[11]), month=eval(raw[12]), year=eval(raw[13]))
        return record


if __name__ == "__main__":
    data_fetcher = TCDataFetcher()
    data_fetcher.fetch_latest()
    today = datetime.date.today()
    print(data_fetcher.get_data_a_month(today))
