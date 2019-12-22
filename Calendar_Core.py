import calendar
import os


class GenerateYear:

    def __init__(self, year):
        self.year = year
        self.calendar = calendar.TextCalendar(0)
        self.months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                       9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        self.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.month_days = ''
        self.master_list = [[] for i in range(12)]
        
        # Checks if folder already exists for given year, if not creates
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.new_dir = self.current_dir + "\\" + str(self.year)
        if not os.path.exists(self.new_dir):
            os.makedirs(self.new_dir)
            for i in range(12):
                self.build_month(i+1)
        
    def build_month(self, month):
        month_data = self.calendar.formatmonth(self.year, month, w=0, l=0)
        self.month_days = self.get_dates(month_data)
        list_days = self.month_days.split()
        initial_weekday = self.get_initial_weekday()

        for i in list_days:
            date_day = self.format_date_entry(i)
            date_month = self.format_date_entry(month)
            date = date_day + "/" + date_month + "/" + str(self.year)
            weekday = self.get_weekday(int(i), initial_weekday)
            
            self.master_list[month-1].append(Day(date, weekday))
            # string = weekday+" - "+str(i)+"/"+str(month)+"/"+str(self.year)+"\n\n"
        
    def write_month(self):
        # Separate file handling from master_list class construction
        for m in range(len(self.master_list)):
            month = m+1
            
            # add 0 before single digit months
            if month < 10:
                filename = str(self.year) + "-0" + str(month) + "-" + self.months[month] + ".txt"
            else:
                filename = str(self.year) + "-" + str(month) + "-" + self.months[month] + ".txt"
            
            complete_name = os.path.join(self.new_dir, filename)
            OpenFile = open(complete_name, 'w+')
            for d in self.master_list[m]:
                string = d.weekday+" - "+d.date+"\n\n"
                OpenFile.write(string)
            OpenFile.close()

    @staticmethod
    def get_dates(month):
        # Strips extra print info provided by calendar.Textcalendar.formatmonth
        for x in range(len(month)):
            if month[x] == 'S':
                if month[x+1] == 'u':
                    return month[x+3:]

    @staticmethod
    def format_date_entry(date):
        # Adds 0 to beginning of month or day date
        strdate = str(date)
        if len(strdate) == 1:
            return "0"+strdate
        else:
            return strdate
    
    def get_initial_weekday(self):
        # Calendar data must be in get_dates format
        count = 0
        for char in self.month_days:
            if char == ' ':
                count+=1
            else:
                break
        weekday = count/3
        return self.weekdays[int(weekday)]
    
    def get_weekday(self, day_count, initial_weekday):
        # Given the first day of the month and a specific date,
        # returns the day of the week
        
        initial_index = self.weekdays.index(initial_weekday)
        new_index = initial_index+day_count
        
        counter = 0
        first = True
        first_counter = 0
        previous_day = ''
        while True:
            for i in self.weekdays:
                if first:
                    if first_counter < initial_index:
                        first_counter += 1
                    else:
                        first = False
                elif counter == new_index:
                    return previous_day
                previous_day = i
                counter += 1
                
        # if index > 6, subtract 6 to go back... if > certain value must divide?

    @staticmethod
    def format_data(day_date_string):
        border = "*"*30+"\n"
        string = border+day_date_string
        print(string)
            
    
class Day:

    def __init__(self, date, weekday):
        # date = dd/mm/yyyy
        self.date = date
        self.day = date[:2]
        self.month = date[3:5]
        self.year = date[6:]
        self.weekday = weekday
        self.events = []
    
    def print_info(self):
        print("Day : " + self.day)
        print("Month : " + self.month)
        print("Year : " + self.year)
    
    def get_day_formatted(self):
        # returns day without 0 in [0] to pass on to calendar library
        if self.day[0] == '0':
            return self.day[1]
        else:
            return self.day
        
    def get_month_formatted(self):
        # returns month without 0 in [0] to pass on to calendar library
        if self.month[0] == '0':
            return self.month[1]
        else:
            return self.month
        
    def print_events(self):
        for event in self.events:
            event.print_event()


class Event:

    # Handles and manages events added to the calendar
    def __init__(self, time='00:00'):
        self.time = time
        self.description = ''
        
    def add_description(self, string):
        self.description = string
        
    def print_event(self):
        print(self.time+" -- "+self.description)


if __name__ == "__main__":
    GenerateYear(2016)
