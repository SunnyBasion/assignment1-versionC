#!/usr/bin/env python3

'''
OPS445 Assignment 1
Program: assignment1.py 
The python code in this file is original work written by
"Student Name". No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading. I understand
that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.

Author: Sunny Basion | 107827172    
Semester:Fall/2024
Description: Assignment1 for OPS445 
'''

import sys

def day_of_week(date: str) -> str:
    "Based on the algorithm by Tomohiko Sakamoto"
    # Converting/Splitting the date string into day,month, and year as integers 
    day_value, month_value, year_value = (int(x) for x in date.split('/'))
    days_list = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    offset_dict = {1:0, 2:3, 3:2, 4:5, 5:0, 6:3, 7:5, 8:1, 9:4, 10:6, 11:2, 12:4}
    # Adjusting the year if the month is January or February based on tomohiko sakamoto algorithm
    if month_value < 3:
        year_value -= 1
    # Utilizing the alogrithm to calculate the day of the week 
    num_day = (year_value + year_value//4 - year_value//100 + year_value//400 + offset_dict[month_value] + day_value) % 7
    return days_list[num_day]

def leap_year(year_value: int) -> bool:
    "return True if the year is a leap year"
    # Verify if the year can be divided by 4 --> leap year logic 
    if year_value % 4 == 0:
        if year_value % 100 == 0:
            if year_value % 400 == 0:
                return True
            return False
        return True
    return False

def mon_max(month_value:int, year_value:int) -> int:
    "returns the maximum day for a given month. Includes leap year check"
    days_in_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                     7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    # if the month is February and it's a leap year, it will return 29 days 
    if month_value == 2 and leap_year(year_value):
        return 29
    else:
        return days_in_month[month_value]

def after(date: str) -> str:
    '''
    after() -> date for next day in DD/MM/YYYY string format

    Return the date for the next day of the given date in DD/MM/YYYY format.
    This function has been tested to work for year after 1582
    '''
    # Converting date string --> day, month, and year as integers 
    day_value, month_value, year_value = (int(x) for x in date.split('/'))
    day_value += 1  # move to the next day

    leap_check = leap_year(year_value)  # Verify if it's a leap year

    days_in_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                     7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    # Update the maximum number of days for February if is a leap year
    if month_value == 2 and leap_check:
        max_days = 29
    else:
        max_days = days_in_month[month_value]
    # If the next day has more than the maximum number of days in the month  
    if day_value > max_days:
        month_value += 1
        if month_value > 12:
            year_value += 1
            month_value = 1
        day_value = 1  
    return f"{day_value:02}/{month_value:02}/{year_value}"

def before(date: str) -> str:
    "Returns previous day's date as DD/MM/YYYY"
    # Converting date string --> day, month, and year as integers 
    day_value, month_value, year_value = (int(x) for x in date.split('/'))
    day_value -= 1  # move to the previous day
    
    is_leap_year = False
    if year_value % 4 == 0: # year is divisible by 4 = leap year
        if year_value % 100 != 0 or year_value % 400 == 0: # checking century leap year rule
            is_leap_year = True
    
    days_in_month = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30,
                     7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    if month_value == 2 and is_leap_year:
        max_days = 29
    else:
        max_days = days_in_month[month_value]
    if day_value < 1:
        month_value -= 1
        if month_value < 1:
            year_value -= 1
            month_value = 12
        day_value = days_in_month[month_value]
        if month_value == 2 and is_leap_year:
            day_value = 29
     
    return f"{day_value:02}/{month_value:02}/{year_value}"

def usage():
    "Print a usage message to the user"
    print("Usage: " + str(sys.argv[0]) + " DD/MM/YYYY NN")
    sys.exit()

def valid_date(date: str) -> bool:
    "check validity of date"
    try:
        day_value, month_value, year_value = (int(x) for x in date.split('/'))
        if 1 <= month_value <= 12 and 1 <= day_value <= mon_max(month_value, year_value) and year_value > 0:
            return True
    except (ValueError, KeyError):
        pass
    return False

def day_iter(start_date: str, num_days: int) -> str:
    "iterates from start date by num to return end date in DD/MM/YYYY"
    current_date = start_date
    if num_days > 0:
        for _ in range(num_days):
            current_date = after(current_date)
    elif num_days < 0:
        for _ in range(num_days, 0):
            current_date = before(current_date)
    return current_date

if __name__ == "__main__":
    # Check length of arguments
    if len(sys.argv) != 3:
        usage()
    # Check first arg is a valid date
    start_date = sys.argv[1]
    # Check that second arg is a valid number (+/-)
    try:
        num_days = int(sys.argv[2])
    except ValueError:
        usage()  # If the conversion fails (invalid number), display usage information and exit
    # Check if the the start date format is correct 
    if not valid_date(start_date):
        usage()
    # Calculating the end date by using day_iter function from the start date and number of days specified
    end_date = day_iter(start_date, num_days)
    # Print (f'The end date is {day_of_week(end_date)}, {end_date}.')
    print(f"The end date is {day_of_week(end_date)}, {end_date}.")
pass
