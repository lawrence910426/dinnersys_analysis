from dateutil.parser import parse
import datetime

class reencode_date:
    def __init__(self, orders ,style):
        date_idx = {}
        for oid in orders:
            date = orders[oid].date
            date_idx[date] = True
        
        if style == "exists":
            self.exists(date_idx)
        elif style == "weekdays":
            self.weekdays(date_idx)
        
    def exists(self ,date_idx):
        i = 0
        tmp = {}
        for date in date_idx:
            tmp[date] = i
            i += 1

        self.encoder = tmp
        self.decoder = dict((tmp[key], key) for key in tmp)
    
    def weekdays(self ,date_idx):
        sort = sorted(date_idx.keys())
        mini ,maxi = parse(sort[0]) ,parse(sort[len(sort) - 1])
        tmp = {}

        count ,i = 0 ,mini
        while i <= maxi:
            tmp[i.strftime("%Y-%m-%d")] = count
            count += 1
            i += datetime.timedelta(days=1)
        
        self.encoder = tmp
        self.decoder = dict((tmp[key], key) for key in tmp)

    def get_count(self):
        return len(self.encoder)

    def get_id(self, date):
        return self.encoder.setdefault(date)

    def get_name(self, id):
        return self.decoder.setdefault(id)
