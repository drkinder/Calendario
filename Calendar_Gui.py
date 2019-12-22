from tkinter import *
import datetime
import Calendar_Core
import os


class CalendarGUI:

    def __init__(self, master, width=1200, height=720):
        self.master = master
        self.master.resizable(False, False)
        self.master.title("Kinder Calendar")
        self.width=width
        self.height=height
        
        now = datetime.datetime.now()
        self.date_today = now.strftime("%Y-%m-%d")
        self.flip_screen(0,[now.strftime("%Y"),now.strftime("%m")])
        # self.screen_full_month(now.strftime("%Y"),now.strftime("%m"))
        
    def flip_screen(self, screen_index, data_list):
        screens = {0: self.screen_full_month(data_list[0], data_list[1])}
        screens[0]
    
    def screen_full_month(self, year, month):
        get_year = Calendar_Core.GenerateYear(int(year))
        widget_list = []
        
        print(month)
        #Month_Label
        #Single digit months & double digit months must be handled differently
        try:
            month_label_text = get_year.months[int(month)]
        except KeyError:
            month_label_text = get_year.months[int(month[1])]
        month_label = Label(self.master, text=month_label_text)
        month_label.config(font=("Courier", 44))
        month_label.pack()
        widget_list.append(month_label)
        
        #Pack Canvas to begin drawing framework
        window = Canvas(self.master, width=self.width, height=self.height)
        window.pack()
        widget_list.append(window)
        
        #Calendar Framework
        base_x = 40
        base_y = 20
        window.create_rectangle(base_x,base_y,self.width-base_x,self.height-base_y)
        window.create_line(base_x,base_y+40,self.width-base_x,base_y+40)
        
        #Generate Labels for Days of the week
        days_list = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        day_labels = []
        space = 160
        new_base_x = base_x+50
        new_base_y = base_y+75
        for i in range(len(days_list)):
            this_base_x = new_base_x+(i*space)
            day_labels.append(Label(self.master, text=days_list[i]))
            day_labels[i].config(font=("Courier", 16))
            day_labels[i].pack()
            widget_list.append(day_labels[i])
            day_labels[i].place(x=this_base_x,y=new_base_y)
        
        #Create horizontal lines for weeks
        for i in range(1,6):
            space = 107
            new_base_y = base_y+40
            new_base_y = new_base_y+(i*space)
            window.create_line(base_x,new_base_y,self.width-base_x,new_base_y)
       
        #Create vertical lines for days
        for i in range(1,7):
            space = 160
            new_base_x = base_x+(i*space)
            window.create_line(new_base_x,base_y,new_base_x,self.height-base_y)
        
        #Populate board with dates
        dates_days = self.get_days(year, month)
        date_labels = []
        new_base_x = base_x+140
        new_base_y = base_y+115
        xspace = 160
        yspace = 107
        for y in range(len(dates_days)):
            date_labels.append([])
            this_base_y = new_base_y+(y*yspace)
            for x in range(len(dates_days[y])):
                if dates_days[y][x] != '?':
                    this_base_x = new_base_x+(x*xspace)
                    date_labels[y].append(Label(self.master, text=dates_days[y][x]))
                    date_labels[y][x].pack()
                    widget_list.append(date_labels[y][x])
                    date_labels[y][x].place(x=this_base_x,y=this_base_y)
                else:
                    date_labels[y].append('?')
                    
        #Create buttons
        next_month_year = year
        if month[0] == '0' and month[1] != '9':
            next_month = month[0]+str(int(month[1])+1)
        elif month[1] == '9':
            next_month = '10'
        elif month == '12':
            next_month = '01'
            next_month_year = str(int(year)+1)
        else:
            next_month = str(int(month)+1)
        print(next_month+" : "+next_month_year)
        button_next_month = Button(self.master,text="Next Month",
                                   command=lambda: self_destruct(0,[next_month_year, next_month]))
        button_next_month.pack()
        widget_list.append(button_next_month)
        button_next_month.place(x=self.width-base_x*2,y=base_y)
        
        def self_destruct(new_screen_index, year_month_list):
            for widget in widget_list:
                widget.destroy()
            self.flip_screen(new_screen_index, year_month_list)
            

    def get_days(self, year, month):
        #Return weekdays in [][] matrix [[]]
        #Connected to: screen_current_month
        days_dict = {'Monday':0,'Tuesday':1,'Wednesday':2,'Thursday':3,
                     'Friday':4,'Saturday':5,'Sunday':6}
        
        date_days = []
        for y in range(0,6):
            date_days.append([])
            for x in range(0,7):
                date_days[y].append('?')
                
        main_dir = os.path.dirname(os.path.realpath(__file__))
        target_dir = main_dir+ "\\" +str(year)
        
        target_txt = ''
        for file in os.listdir(target_dir):
            filename = os.fsdecode(file)
            if filename[5:7] == month:
                target_txt = filename
                break

        file = open(target_dir+"\\"+target_txt,"r")
        content = file.readlines()
        content = [x.strip() for x in content]
        file.close()
        first_day = content[0]
        last_day = content[-2]
        print(first_day)
        print(last_day)
        
        last_day = int(last_day[-10:-8])
        
        day = ''
        for char in first_day:
            if char != ' ':
                day+=char
            else:
                break
    
        day_index = days_dict[day]

        day_count = 1
        flag = False
        if day_index == 0:
            flag = True
        for y in range(len(date_days)):
            for x in range(len(date_days[y])):
                if not flag:
                    if x < day_index-1:
                        pass
                    elif x == day_index-1:
                        flag = True
                else:
                    if day_count <= last_day:
                        date_days[y][x] = day_count
                        day_count+=1
                    else:
                        date_days[y][x] = '?'
                        
        return date_days
                    
        
        #Cycle through two-dimensional array 'date_days'
        #Skip the first 4 indexes (0:3) in the loop
        #to begin the month on Friday (4th index)


if __name__ == "__main__":
    root = Tk()
    my_gui = CalendarGUI(root)
    root.mainloop()

