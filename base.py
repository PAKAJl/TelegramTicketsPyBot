class Ticket:
    def __init__(self):
        self.dep_time = None
        self.arr_time = None
        self.free_space = None
        self.dep_place = None
        self.arr_place = None
        self.cost = None
        
        
class User:
    def __init__(self):
        self.first_town = None
        self.sec_town = None
        self.date = None
        self.day = None
        self.mounth = None
        self.year = None
    
    def date_split(self):
        dateArr = str(self.date).split('.')
        self.day = dateArr[0]
        self.mounth = dateArr[1]
        self.year = dateArr[2]