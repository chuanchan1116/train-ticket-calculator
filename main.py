#!/usr/bin/env python3

import argparse
import os

from rail_api_enum import CabinClass, FareClass, TicketType, TrainType
from ticket_calculator import TicketCalculator

FROM = "臺北"
TO = [
    "基隆",
    "宜蘭",
    "桃園",
    "新竹",
    "苗栗",
    "臺中",
    "彰化",
    "斗六",
    "員林",
    "嘉義",
    "臺南",
    "高雄",
    "屏東",
    "花蓮",
    "臺東",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", default=os.environ.get("CLIENT_ID"))
    parser.add_argument(
        "--client-secret", default=os.environ.get("CLIENT_SECRET")
    )
    args = parser.parse_args()

    calculator = TicketCalculator(
        TrainType.TZECHIANG,
        TicketType.NORMAL,
        FareClass.ADULT,
        CabinClass.RESERVED,
        args.client_id,
        args.client_secret,
    )
    for i in TO:
        print(f"{i}: {calculator.price(FROM, i)}")


if __name__ == "__main__":
    main()
