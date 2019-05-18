from data_structure.dish import *
from datetime import datetime, timedelta


class order:
    black_list = [
        "閒置的餐點",
        "初始設定餐點",
        "閒置中的餐點"
    ]

    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.dish = kwargs["dish"]
        self.date = kwargs["date"]
        self.seatno = kwargs["seatno"]
        self.name = kwargs["name"]
        self.raw = kwargs["raw"]

    @staticmethod
    def get_order(fetcher):
        data = fetcher.get_orders()
        ret = {}
        for row in data:
            if row["money"]["payment"][0]["paid"] == "false":
                continue
            ret[row["id"]] = order(
                id=row["id"],
                dish=dish(
                    id=row["dish"][0]["dish_id"],
                    name=row["dish"][0]["dish_name"],
                    factory=row["dish"][0]["department"]["factory"]["name"],
                    raw=row["dish"]
                ),
                date=row["recv_date"].split(" ")[0],
                seatno=row["user"]["seat_no"],
                name=row["user"]["name"],
                raw=row
            )
        return ret

    @staticmethod
    def select_order(orders, start, end):
        start = datetime.strptime(start, '%Y-%m-%d')
        end = datetime.strptime(end, "%Y-%m-%d")
        result = {}
        for oid in orders:
            row = orders[oid]

            recv = datetime.strptime(row.date, "%Y-%m-%d")
            if not (start <= recv <= end):
                continue
            if row.dish.name in order.black_list:
                continue

            result[oid] = row
        return result
