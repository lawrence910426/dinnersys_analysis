from data_structure.dish import *


class order:
    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.dish = kwargs["dish"]
        self.date = kwargs["date"]
        self.seatno = kwargs["seatno"]
        self.name = kwargs["name"]


def get_order(fetcher, start, end):
    dishes = get_dish(fetcher)
    data = fetcher.get_orders(start, end)
    ret = {}
    for row in data:
        ret[row["id"]] = order(
            id=row["id"],
            dish=dishes[row["dish"]["dish_id"]],
            date=row["recv_date"],
            seatno=row["user"]["seat_no"],
            name=row["user"]["name"]
        )
    return ret
