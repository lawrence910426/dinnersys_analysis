import re

class regex_dish:
    keyword = [
        (re.compile(r"(焗)|(拌飯)|(炒飯)|(飯糰)") ,"雜類 Anything"), 
        (re.compile(r"(烏龍)|(麵)|(湯)") ,"湯麵類 Noodles"),
        (re.compile(r"(副菜)|(飯)") ,"便當類 Bang Dang"), 
        (re.compile(r"((餃)|(蔥抓餅)|(鍋貼)|(板條)|(粄條))") ,"小吃類 Snacks"),
        (re.compile(r"(鍋)|(粥)") ,"鍋類 Pots")
    ]
    allow_other = False

    def __init__(self ,regex=None):
        self.keyword = (self.keyword if regex is None else regex)

    def get_count(self):
        return len(self.keyword) + (1 if self.allow_other else 0)

    def get_id(self, name):
        count = 0
        for item in self.keyword:
            if re.search(item[0] ,name) is not None:
                return count
            count += 1

        if self.allow_other:
            return len(self.keyword)
        else:
            raise Exception("Do not allow other. " + name)

    def get_name(self, id):
        if id == len(self.keyword):
            if self.allow_other:
                return "其他類"
            else:
                raise Exception("Do not allow other. " + id)
        else:
            return self.keyword[id][1]