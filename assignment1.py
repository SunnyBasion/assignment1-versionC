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
    day, month, year = (int(x) for x in date.split('/'))
    days_list = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    offset_dictionary = {1:0, 2:3, 3:2, 4:5, 5:0, 6:3, 7:5, 8:1, 9:4, 10:6, 11:2, 12:4}
    # Adjusting the year if the month is January or February based on tomohiko sakamoto algorithm
    if month < 3:
        year -= 1
    # Utilizing the alogrithm to calculate the day of the week 
    num = (year + year//4 - year//100 + year//400 + offset_dictionary[month] + day) % 7
    return days_list[num]

def leap_year(year: int) -> bool:
    "return True if the year is a leap year"
    # Verify if the year can be divided by 4 --> leap year logic 
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            return False
        return True
    return False

def mon_max(month:int, year:int) -> int:
    "returns the maximum day for a given month. Includes leap year check"
    month_dictionary = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    # if the month is February and it's a leap year, it will return 29 days 
    if month == 2 and leap_year(year):
        return 29
    else:
        return month_dictionary[month]

def after(date: str) -> str:
    '''
    after() -> date for next day in DD/MM/YYYY string format

    Return the date for the next day of the given date in DD/MM/YYYY format.
    This function has been tested to work for year after 1582
    '''
    # Converting date string --> day, month, and year as integers 
    day, mon, year = (int(x) for x in date.split('/'))
    day += 1  # move to the next day

    leap_flag = leap_year(year)  # Verify if it's a leap year

    mon_dictionary= {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
           7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    # Update the maximum number of days for February if is a leap year
    if mon == 2 and leap_flag:
        mon_max = 29
    else:
        mon_max = mon_dictionary[mon]
    # If the next day has more than the maximum number of days in the month  
    if day > mon_max:
        mon += 1
        if mon > 12:
            year += 1
            mon = 1
        day = 1  
    return f"{day:02}/{mon:02}/{year}"

def before(date: str) -> str:
    "Returns previous day's date as DD/MM/YYYY"
    # Converting date string --> day, month, and year as integers 
    day, mon, year = (int(x) for x in date.split('/'))
    day -= 1  # move to the previous day
    
    # Determine if the current year is a leap year
    leap_flag = False
    if year % 4 == 0: #year is divisble by 4 = leap year
        if year % 100 != 0 or year % 400 == 0: #checking century leap year rule
            leap_flag = True
    # Dictionary defining the maximum number of days in each month 
    mon_dictionary = {1:31,2:28,3: 31,4: 30,5:31,6:30,
           7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    # If the month is February and a leap year, set February to have 29 days
    if mon == 2 and leap_flag:
        mon_max = 29
    else:
        mon_max = mon_dictionary [mon]
    # If the day goes below (less than) 1, adjust to the previous month 
    if day < 1:
        mon -= 1
        if mon < 1:  # If the month is less than January, revert back to December of the previous year
            year -= 1
            mon = 12 #Sets month variable back to decemeber 
        day = mon_dictionary[mon]  #Gets the maximum days for the new month 
        # If it's February and a leap year, update the day
        if mon == 2 and leap_flag:
            day = 29
     
    return f"{day:02}/{mon:02}/{year}"


def usage():
    "Print a usage message to the user"
    print("Usage: " + str(sys.argv[0]) + " DD/MM/YYYY NN")
    sys.exit()

def valid_date(date: str) -> bool:
    "check validity of date"
    try:
       # Converting date string --> day, month, and year as integers 
       day, mon, year = (int(x) for x in date.split('/'))
       # Verification of the day, month, and year 
       if 1 <= mon <= 12 and 1 <= day <= mon_max(mon, year) and year > 0:
            return True
    except (ValueError, KeyError) :
        pass # Will ignore errors caused by invalid input format
    return False

def day_iter(start_date: str, num: int) -> str:
    "iterates from start date by num to return end date in DD/MM/YYYY"
    date = start_date # Current date is set to the provided start date 
    if num > 0: # If the number is positive, greater than 0, move forward in time 
        for _ in range(num):
            date = after(date) # Calculating the next day using the after function 
    elif num < 0: # If the number is negative, less than 0, move backward in time
        for _ in range(num, 0):
            date = before(date) # Calculating the previous day using the before function
    return date


if __name__ == "__main__":
   #Check length of arguments
   if len(sys.argv) != 3:
       usage()
    #Check first arg is a valid date
   start_date = sys.argv[1]
   # Check that second arg is a valid number (+/-)
   try:
       num = int(sys.argv[2])
   except ValueError:
       usage() # If the conversion fails (invalid number), display usage information and exit
  # Check if the the start date format is correct 
   if not valid_date(start_date):
       usage()
  # Calculating the end date by using day_iter function from the start date and number of days specified | call day_iter function to get end date, save to x(end_date)
   end_date = day_iter(start_date, num)
  # Print (f'(The end date is {day_of_week(end_date)}, {end_date}.')
   print(f"The end date is {day_of_week(end_date)}, {end_date}.")
pass