class reencode_date:
    def __init__(self, orders):
        date_idx = {}
        for oid in orders:
            date = orders[oid].date.replace("-", "")[4:]
            date_idx[date] = True

        i = 0
        tmp = {}
        for date in date_idx:
            tmp[date] = i
            i += 1

        self.encoder = tmp
        self.decoder = dict((tmp[key], key) for key in tmp)

    def get_count(self):
        return len(self.encoder)

    def get_id(self, date):
        return self.encoder.setdefault(date.replace("-", "")[4:])

    def get_name(self, id):
        return self.decoder.setdefault(id)
