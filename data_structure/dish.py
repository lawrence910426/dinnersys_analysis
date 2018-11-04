class dish:
    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.factory = kwargs["factory"]
        self.raw = kwargs["raw"]


def get_dish(fetcher):
    data = fetcher.get_dish()
    ret = {}
    for row in data:
        ret[row["dish_id"]] = dish(
            id=row["dish_id"],
            name=row["dish_name"],
            factory=row["factory"]["name"],
            raw=row
        )
    return ret