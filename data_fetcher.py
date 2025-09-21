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
import os


DEBUG_MODE = True  # if enabled, data fetcher will read local cache data for faster speed
DATA_CACHE_DIR = "./data_cache"


class TCData:
    """
    This class defines a piece of tropical cyclone data
    """
    def __init__(self):
        self.id: int = 0
        self.tc_type: str = ""
        self.tc_name_ch: str = ""
        self.tc_name_en: str = ""
        self.tc_signal: int = 0
        self.tc_signal_direction: str = ""
        self.tc_start_date: datetime.date = None
        self.tc_end_date: datetime.date = None


class TCDataFetcher:
    """
    Requests the latest data from HKO and parse the data
    """
    tc_type2name = {
        "TD": "Tropical Depression",
        "TS": "Tropical Storm",
        "STS": "Severe Tropical Storm",
        "T": "Typhoon",
        "ST": "Severe Typhoon",
        "SuperT": "Super Typhoon"
    }

    def __init__(self):
        self.tc_name_list = {}
        self.tc_records : [TCData] = []

    def fetch_latest(self):
        """
        Get the latest tropical cyclone data from HKO
        """
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

        print("[DataFetcher] Fetched the latest tropical cyclone warning records")

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
        # print(self.tc_name_list)

    def __parse_to_TCData(self, raw: [str]) -> TCData:
        record = TCData()
        record.id = eval(raw[0])
        if raw[1] not in TCDataFetcher.tc_type2name:
            record.tc_type = "Type Unknown"
        else:
            record.tc_type = TCDataFetcher.tc_type2name[raw[1]]
        if raw[2] not in self.tc_name_list:
            record.tc_name_en = "Name Unknown"
            record.tc_name_ch = "未知"
        else:
            record.tc_name_en = raw[2]
            record.tc_name_ch = self.tc_name_list[raw[2]]
        record.tc_signal = eval(raw[3])
        record.tc_signal_direction = "" if raw[4] == "X" else raw[4]
        record.tc_start_date = datetime.date(day=eval(raw[6]), month=eval(raw[7]), year=eval(raw[8]))
        record.tc_end_date = datetime.date(day=eval(raw[11]), month=eval(raw[12]), year=eval(raw[13]))
        return record


if __name__ == "__main__":
    data_fetcher = TCDataFetcher()
    data_fetcher.fetch_latest()
