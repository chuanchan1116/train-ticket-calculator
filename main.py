#!/usr/bin/env python3

from ticket_calculator import TicketCalculator
from rail_api_enum import TrainType, TicketType, FareClass, CabinClass

FROM = "臺北"
TO = [
    "基隆",
    "宜蘭",
    "桃園",
    "新竹",
    "苗栗",
    "臺中",
    "彰化",
    "雲林",
    "嘉義",
    "臺南",
    "高雄",
    "屏東",
]


def main():
    calculator = TicketCalculator(
        TrainType.TZECHIANG,
        TicketType.NORMAL,
        FareClass.ADULT,
        CabinClass.RESERVED,
    )
    for i in TO:
        print(f"{i}: {calculator.price(FROM, i)}")


if __name__ == "__main__":
    main()
