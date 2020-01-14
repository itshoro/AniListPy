from datetime import date

class FuzzyDate():
    def __init__(self, year, month, day):
        if year == None or month == None or day == None:
            self.isValid = False
        else:
            self.year = year
            self.month = month
            self.day = day
            self.isValid = True

    def toDate(self):
        if self.isValid:
            return date(self.year, self.month, self.day)
        raise TypeError("Date is not Valid!")