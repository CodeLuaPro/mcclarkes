# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Program Name: payroll_system.py
# Author:       Gleb Lyubin
# Purpose:      Calculate employees' salaries, manage employee data
# Version:      1.0
# Last Revison  24/7/2023 5:42 P.M.
# Dependencies: None
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os

current_day = ""
admin_status = False
username_password = []
position = ""
employee_data = []
main_menu_choice = ""
clock_in_time = ""
clock_out_time = ""
manage_employee = ""
employee_id_to_edit = ""
change_name_choice = ""
new_fname = ""
new_lname = ""
employee_id = ""
error_found = False
new_trate = ""
new_sannuation = ""
new_health_insurance = ""
new_position = ""
wrong_hour = False
def clearconsole(): # clears the console before displaying more text
    os.system('cls' if os.name == 'nt' else 'clear')
#end def

#login interface
def display_login_screen():
    clearconsole()
    print("McDermott's Employee Software")
    print("Please login with your credentials")
    username = input("Username: ")
    password = input("Password: ")
    return [username, password]
#end def
#main menu interface
def display_main_menu(admin):
    clearconsole()
    if admin:
        print("McDermott's Employee Software")
        print("Select Current Action")
        print("[1] Clock-in")
        print("[2] Clock-out")
        print("[3] Manage employees")
        print("[4] Calculate pay")
        print("[5] Display all data")
        main_menu_choice = input("Select action: ")
    else:
        print("McDermott's Employee Software")
        print("Select Current Action")
        print("[1] Clock-in")
        print("[2] Clock-out")
        main_menu_choice = input("Select action: ")
    return main_menu_choice
#end def

#employee management interface
def display_employee_management():
    clearconsole()
    print("McDermott's Employee Software")
    print("[1] Add new employee")
    print("[2] Remove existing employee")
    print("[3] Edit employee")
    manage_employee = input("Select action: ")
    return manage_employee
#end def

#prompt to edit employee
def display_edit_employee_details():
    clearconsole()
    print("McDermott's Employee Software")
    employee_id = input("Enter the ID of the employee to edit: ")

    return employee_id
#end def

#clock-in interface
def display_clock_in():
    clearconsole()
    print("McDermott's Employee Software")
    print("You will be asked of the day during clock-out!")
    clock_in_time = input("Enter the clock-in time (24hr format): ")
    return clock_in_time
#end def

#clock-out interface
def display_clock_out():
    clearconsole()
    print("McDermott's Employee Software")
    clock_out_time = input("Enter the clock-out time (24hr format): ")
    return clock_out_time
#end def

#day select interface for clocking-out
def display_select_day():
    clearconsole()
    print("McDermott's Employee Software")
    print("Enter the day")
    print("[1] Monday")
    print("[2] Tuesday")
    print("[3] Wednesday")
    print("[4] Thursday")
    print("[5] Friday")
    print("[6] Saturday")
    print("[7] Sunday")
    current_day = input("Select day: ")
    return current_day
#end def

#checks if a number is a float
def isfloat(num): #num = variable to check
    return isinstance(num, float)
# end def

#writes data to a cell in a csv file
def write_to_csv(filename, data, emp_id, col): #filename = name of the csv file, data = data to write
    # emp_id = employee id, col = column
    #lines = list of lines in the file
    lines = read_from_csv("LYUBIN_Gleb_payroll.csv")
    # validate the column number
    if int(emp_id) > len(lines) or col > 20 or emp_id == "0":
        print("Incorrect employee ID or column number. Employee ID must be >0 and column number must be <20")
    #end if
    # Opening the given file in read-only mode.
    with open(filename, 'r') as filedata:
        lines = filedata.readlines()
    #separate a specific line into cells, then replace the value in a cell and combine into one line again
    cells = lines[int(emp_id)].split(',')
    cells[col] = str(data)
    new_row = ','.join(cells)
    lines[int(emp_id)] = new_row

    #write new data to the file
    with open(filename, 'w') as filedata:
        filedata.writelines(lines)

    filedata.close()
#end def

#read the lines from a csv file
def read_from_csv(filename): # filename = name of the csv file
    lines = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        return lines
#end def

#read an individual employee record
def read_emp_data(filename, emp_id, delimiter=','):
    lines = []
    line = []
    line_elements = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        #validate the employee id entered
        if int(emp_id) < 0 or int(emp_id) >= len(lines):
            return None
        # end if
        #separate the record into cells
        line = lines[int(emp_id)].strip()
        line_elements = line.split(delimiter)
        

    return line_elements
#end def

#calculates the tax and nett income
def calculate_after_tax(pre_tax, emp_data): #pre_tax = income before tax, emp_data = employee data
    global wrong_hour
    tax_rate = int(emp_data[4])/100
    tax_amount = pre_tax * tax_rate
    tax_amount = round(tax_amount, 2)
    nett = pre_tax - tax_amount
    nett = round(nett, 2)
    #write the tax in dollars and nett income
    write_to_csv("LYUBIN_Gleb_payroll.csv", tax_amount, emp_data[0], 19)
    write_to_csv("LYUBIN_Gleb_payroll.csv", str(nett) + "\n", emp_data[0], 20)
    #if the tax rate in the csv file is wrong, warn the user
    if not validate_data(tax_rate, [0.3, 0.4]) or wrong_hour:
        print("Incorrect tax rate for employee number: " + emp_data[0])
        write_to_csv("LYUBIN_Gleb_payroll.csv", "CALC ERROR\n", emp_data[0], 20)
    # end if
    return nett  # returns taxed income
#end def

#calculates income after deductions
def calculate_after_deductions(gross, emp_data): # gross = total income, emp_data = employee record
    emp_id = emp_data[0]
    superannuation_rate = int(emp_data[5]) / 100
    health_deduction = int(emp_data[6])
    total_income = gross - (gross * superannuation_rate) - health_deduction
    sann_deducted = superannuation_rate * gross
    sann_deducted = round(sann_deducted, 2)

    # write values to csv file
    write_to_csv("LYUBIN_Gleb_payroll.csv", health_deduction, emp_id, 18)
    write_to_csv("LYUBIN_Gleb_payroll.csv", sann_deducted, emp_id, 17)

    #validates the superannuation and health deduction and warns the user if they are wrong
    if not validate_data(superannuation_rate, [0.04, 0.06, 0.08]):
        print("Incorrect superannuation for employee number: " + employee_id)
        write_to_csv("LYUBIN_Gleb_payroll.csv", "CALC ERROR\n", emp_data[0], 20)
        pass
    # end if
    if not validate_data(health_deduction, [15, 25, 45]):
        print("Incorrect health insurance for employee number: " + employee_id)
        write_to_csv("LYUBIN_Gleb_payroll.csv", "CALC ERROR\n", emp_data[0], 20)
        pass
    # end if

    return total_income
#end def

def validate_data(data, acceptable_data): #data = data to be validated, acceptable_data = array of acceptable values
    # i am sorry i did not want to use a global variable but this makes my life so much easier
    global error_found
    valid = True
    if data not in acceptable_data:
        error_found = True
        valid = False
    # end if
    return valid
#end def

def validate_hours(hours): # hours = a string of the hour to be validated
    valid = True
    # separate hours and minutes
    hours = hours.split(":")
    #check that the values entered are digits
    for i in range(len(hours)):
        if not hours[i].isdigit():
            valid = False
            #error_found = True
        else:
            hours[i] = int(hours[i])
        # end if
    #end for
    #validate that the hours are within acceptable ranges
    if not str(hours[0]).isdigit() or not str(hours[1]).isdigit() or \
            len(hours) > 2 or isfloat(hours[0]) or int(hours[0]) > 23 or int(hours[1]) > 59:
    # end if
        valid = False
    #return boolean
    return valid
#end def
#validate hours after they are converted to a decimal
def validate_hours_decimal(hour):
    global error_found
    valid = True
    if abs(hour) != hour or hour > 24:
        valid = False
        error_found = True
    # end if
    return valid

#calculates and returns a list of sorted hours
def calc_hours(emp_data): #data = array that contains the employee's hours
     #0=mon,1=tue,2=wed,3=thu,4=fri,5=sat,6=sun
    global wrong_hour
    hours_total = 0
    hours = []
    #take out only hours out of employee data
    hours = emp_data[7:14]
    #convert hours to float
    for i in range(0, len(hours)):
        hours[i] = float(hours[i])
    #end for
    # get total hours
    for i in range(len(hours)):
        hours_total = hours_total + float(hours[i])
        if not validate_hours_decimal(hours[i]):
            print("Incorrect hour on day", i+1, "for employee number:", emp_data[0])
            write_to_csv("LYUBIN_Gleb_payroll.csv", "CALC ERROR\n", emp_data[0], 20)
            wrong_hour = True
            pass
        # end if
    #end for
    ot_total = 0
    normal_hours = 0
    ot_lower = 0
    ot_upper = 0
    sat_normal = 0
    sun_hol_normal = 0
    weekend_hol_ot = 0
    sat_ot = 0
    sun_ot = 0
    mon_ot = 0
    mon_normal = 0
    #sorts mon to fri
    for i in range(0, 5):
        #check for overtime
        if (hours[i] - 9) > 0:
            normal_hours = normal_hours + 9
            ot_total = ot_total + (hours[i]-9)
            #check for extra overtime (3+ hours)
            if (ot_total - 3) >= 0:
                ot_lower = ot_lower + 3
                ot_upper = ot_upper + (ot_total - 3)
            else:
                ot_lower = ot_lower + ot_total
            # end if
        else:
            normal_hours = normal_hours + hours[i]
        # end if
    #end for
    if (hours[0]-9) > 0:
        mon_ot = hours[0]-9
        mon_normal = 9
    else:
        mon_normal = hours[0]-9
    #end if
    #sorts saturday hours and overtime
    if (hours[5] - 9) > 0:
        sat_normal = sat_normal + 9
        weekend_hol_ot = weekend_hol_ot + (hours[5]-9)
        sat_ot = weekend_hol_ot + (hours[5]-9)
    else:
        sat_normal = sat_normal + hours[5]
    # end if
    #sorts holiday hours and overtime
    if (hours[0] - 9) > 0:
        sun_hol_normal = sun_hol_normal + 9
        weekend_hol_ot = weekend_hol_ot + (hours[0] - 9)
        
    else:
        sun_hol_normal = sun_hol_normal + hours[0]
    #end if
    #sorts sunday and overtime
    if (hours[6] - 9) > 0:
        sun_hol_normal = sun_hol_normal + 9
        weekend_hol_ot = weekend_hol_ot + (hours[6] - 9)
        sun_ot = weekend_hol_ot + (hours[6] - 9)
    else:
        sun_hol_normal = sun_hol_normal + hours[6]
    #end if


    write_to_csv("LYUBIN_Gleb_payroll.csv", hours_total, emp_data[0], 14)
    write_to_csv("LYUBIN_Gleb_payroll.csv", ot_total + weekend_hol_ot, emp_data[0], 15)


    return [normal_hours, ot_lower, ot_upper, sat_normal, sun_hol_normal, weekend_hol_ot, sat_ot, sun_ot, mon_ot, mon_normal]
#end def

#calculates gross income
def calculate_gross(emp_data, hours): # rate = employee's pay rate, hours = array of different types of hours
    incorrect_role = False
    role = emp_data[3]
    #checks required rate
    if role == "Team Member":
        rate = 23
    elif role == "Manager" or role == "Administrator":
        rate = 30
    else:
        print("Incorrect position for employee number: " + emp_data[0] + ". Default rate of $23 was assigned")
        incorrect_role = True
        rate = 23
        pass
    #end if
    #calculates based on day bonuses
    ot_rate_lower = rate * 1.25
    ot_rate_upper = rate * 1.45
    weekend_and_holiday_ot_rate = rate * 1.5

    normal_pay = hours[0] * rate
    ot_pay_lower = hours[1] * ot_rate_lower
    ot_pay_upper = hours[2] * ot_rate_upper
    sat_normal = hours[3] * 3 + hours[3] * rate
    sun_and_holiday_normal = hours[4] * 4 + hours[4] * rate
    #weekend_and_holiday_ot = hours[5] * weekend_and_holiday_ot_rate
    weekend_and_holiday_ot = hours[6] * 3 * weekend_and_holiday_ot_rate + hours[7] * 4 * weekend_and_holiday_ot_rate + \
                             hours[8] * weekend_and_holiday_ot_rate

    total = normal_pay + ot_pay_lower + ot_pay_upper + \
sat_normal + sun_and_holiday_normal + weekend_and_holiday_ot
    total = round(total, 2)

    write_to_csv("LYUBIN_Gleb_payroll.csv", total, int(emp_data[0]), 16)


    #if hours[0] + hours[1] + hours[2] > 120 \
            #or hours[3] + hours[6] > 24 or hours[4] - hours[9] - hours[8] + hours[7] > 24 or incorrect_role:
        #write_to_csv("LYUBIN_Gleb_payroll.csv", "CALC ERROR\n", emp_data[0], 20)

    return total # returns a float of pre-tax income. Must be >= 0

#end def

def listToString(list):
    # initialize an empty string
    str1 = ""

    # append to string
    for element in list:
        str1 += element
    #end for
    # return string
    return str1
#end def
'''
def change_employee_first_name(filename, emp_id, fname): # employee_id = employee's ID, fname = new first name
    #filename = name of the file
    line = read_emp_data(filename, emp_id)
    # Opening the given file in read-only mode.
    with open(filename, 'r') as filedata:
        lines = filedata.readlines()
    cells = lines[int(emp_id)].split(',')
    cells[1] = fname
    new_row = ','.join(cells)
    lines[int(emp_id)] = new_row

    with open(filename, 'w') as filedata:
        filedata.writelines(lines)

    filedata.close()

#end def

def change_employee_last_name(filename, emp_id, lname): # employee_id = employee's ID, lname = new last name
    #filename = name of the file
    line = read_emp_data(filename, emp_id)
    # Opening the given file in read-only mode.
    with open(filename, 'r') as filedata:
        lines = filedata.readlines()
    cells = lines[int(emp_id)].split(',')
    cells[2] = lname
    new_row = ','.join(cells)
    lines[int(emp_id)] = new_row

    with open(filename, 'w') as filedata:
        filedata.writelines(lines)

    filedata.close()
#end def
'''
def verify_login(username_password, filename): #username_password = list with username(0) and password(1)
    lines = []
    fields = []
    username = username_password[0]
    password = username_password[1]
    with open(filename, 'r') as file:
        #ensures that the combination exists in a csv file
        lines = file.readlines()
        for line in lines:
            fields = line.split(",")
            if (fields[0] == username and fields[1] == password):
                return fields[2].rstrip()
            #end if
        #end for
    return False
# end def

def clock_in(clock_in_time, emp_data):
    emp_id = emp_data[0]
    write_to_csv("LYUBIN_Gleb_clock.csv", clock_in_time, emp_id, 1)

def clock_out(clock_out_time, emp_data, current_day):
    total_time = 0
    current_day = int(current_day)
    emp_id = emp_data[0]
    write_to_csv("LYUBIN_Gleb_clock.csv", clock_out_time + "\n", emp_id, 2)
    clock_in_time = read_emp_data("LYUBIN_Gleb_clock.csv", emp_id)

    clock_in_time = clock_in_time[1]

    if not validate_hours(clock_in_time):
        print("Incorrect clock-in time! Please ensure that you've clocked in.")
        return False

    #end if
    #split hours and minutes
    clock_in = clock_in_time.split(":")
    clock_out = clock_out_time.split(":")
    #convert string to int
    for i in range(len(clock_in)):
        clock_in[i] = int(clock_in[i])
    #end for
    for i in range(len(clock_out)):
        clock_out[i] = int(clock_out[i])
    #end for
    #convert minutes to decimal
    clock_in[1] = clock_in[1]/60
    clock_out[1] = clock_out[1]/60
    #add to total time
    clock_in_final = clock_in[0] + clock_in[1]
    clock_out_final = clock_out[0] + clock_out[1]
    #decide whether the person worked <12 hours or >12 hours
    if clock_in_final < clock_out_final:
        total_time = clock_out_final - clock_in_final

    elif clock_in_final > clock_out_final:
        total_time = 24 - (clock_in_final - clock_out_final)
    # end if
    #write to payroll csv
    write_to_csv("LYUBIN_Gleb_payroll.csv", total_time, emp_id, 6+current_day)
    
def add_new_employee(fname, lname, role, tax_rate, superannuation, insurance):
    lines = read_from_csv("LYUBIN_Gleb_payroll.csv")
    new_emp_id = len(lines)
    #writes employee data to all csv files
    with open("LYUBIN_Gleb_payroll.csv", 'a') as file:
        file.write(str(new_emp_id) + "," + fname + "," + lname + "," + role +
                   "," + tax_rate + "," + superannuation + "," + insurance+ ",0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")

    with open("LYUBIN_Gleb_logins.csv", 'a') as file:
        file.write(fname + "," + fname + "," + str(new_emp_id) +"\n")

    with open("LYUBIN_Gleb_clock.csv", 'a') as file:
        file.write(str(new_emp_id) + "\n")

#end def

def remove_employee(emp_id):
    emp_id = int(emp_id)
    payroll_lines = read_from_csv("LYUBIN_Gleb_payroll.csv")
    clock_lines = read_from_csv("LYUBIN_Gleb_clock.csv")
    login_lines = read_from_csv("LYUBIN_Gleb_logins.csv")


    if emp_id == "0" or emp_id > len(payroll_lines):
        print("Incorrect employee ID. Must be greater than 0 and must exist!")
        return None
    #end if
    #deletes employee record from all csv files
    payroll_lines.pop(emp_id)
    clock_lines.pop(emp_id)
    login_lines.pop(emp_id)

    #write updated records to all csv files
    with open("LYUBIN_Gleb_payroll.csv", "w") as file:
        file.writelines(payroll_lines)


    with open("LYUBIN_Gleb_logins.csv", "w") as file:
        file.writelines(login_lines)


    with open("LYUBIN_Gleb_clock.csv", "w") as file:
        file.writelines(clock_lines)


    payroll_lines = read_from_csv("LYUBIN_Gleb_payroll.csv")
    # update employee ids to match the changes
    start_index = int(emp_id)
    end_index = len(payroll_lines)
    for i in range(start_index, end_index):
        write_to_csv("LYUBIN_Gleb_payroll.csv", i, str(i), 0)
    #end for
    for i in range(start_index, end_index):
        write_to_csv("LYUBIN_Gleb_clock.csv", i, str(i), 0)
    #end for
    for i in range(start_index, end_index):
        write_to_csv("LYUBIN_Gleb_logins.csv", str(i)+"\n", str(i), 2)
    #end for

    return True
#end def

def append_to_csv(filename, data):
    with open(filename, "a") as file:
        file.writelines(data)
#end def

def delete_lines_except(filename, line_num):
    lines=[]
    with open(filename, 'r') as file:
        # read and store all lines into list
        lines = file.readlines()
    with open(filename, 'w') as file:
        #only write the specified line
        for number, line in enumerate(lines):
            if number in [line_num]:
                file.write(line)

total_records = len(read_from_csv("LYUBIN_Gleb_payroll.csv"))
clock_records = len(read_from_csv("LYUBIN_Gleb_clock.csv"))
login_records = len(read_from_csv("LYUBIN_Gleb_logins.csv"))

#delete all lines except for the headers
delete_lines_except("LYUBIN_Gleb_clock.csv", 0)
delete_lines_except("LYUBIN_Gleb_logins.csv", 0)


for i in range(1, total_records):
    # sets zero-value lines in place of the records
    append_to_csv("LYUBIN_Gleb_logins.csv", ["0, 0, 0\n"])
    append_to_csv("LYUBIN_Gleb_clock.csv", ["0, 0, 0\n"])
    # numbers all employee records correctly
    write_to_csv("LYUBIN_Gleb_payroll.csv", str(i), i, 0)

#synchronise clock.csv and logins.csv with payroll.csv
for i in range(1, total_records):
    updated_emp_data = read_emp_data("LYUBIN_Gleb_payroll.csv", i)
    updated_id = updated_emp_data[0]
    fname = updated_emp_data[1]
    write_to_csv("LYUBIN_Gleb_logins.csv", updated_id + "\n", i, 2)
    write_to_csv("LYUBIN_Gleb_logins.csv", fname, i, 0)
    write_to_csv("LYUBIN_Gleb_logins.csv", fname, i, 1)
    write_to_csv("LYUBIN_Gleb_clock.csv", updated_id, i, 0)

while True:

    error_found = False

    username_password = display_login_screen()

    employee_id = verify_login(username_password, "LYUBIN_Gleb_logins.csv")
    while not employee_id or employee_id is None:
        username_password = display_login_screen()
        employee_id = verify_login(username_password, "LYUBIN_Gleb_logins.csv")
    #end while

    employee_data = read_emp_data("LYUBIN_Gleb_payroll.csv", employee_id)
    #checks if the current user has admin privileges
    if employee_data[3] == "Manager" or employee_data[3] == "Administrator":
        admin_status = True
    #end if

    main_menu_choice = display_main_menu(admin_status)

    #validate input
    while main_menu_choice not in ["1", "2", "3", "4", "5", "pain and suffering"] \
            or (main_menu_choice in ["3", "4", "5"] and not admin_status):
        main_menu_choice = display_main_menu(admin_status)
    # end while

    #clock in
    if main_menu_choice == "1":
        clock_in_hour = display_clock_in()
        #validate hour format
        while not validate_hours(clock_in_hour):
            clock_in_hour = display_clock_in()
        # end while
        clock_in(clock_in_hour, employee_data)
    #end if
    #clock out
    if main_menu_choice == "2":

        current_day = display_select_day()
        while current_day not in ["1", "2", "3", "4", "5", "6", "7"]:
            current_day = display_select_day()
        # end while
        clock_out_hour = display_clock_out()
        #validate hours
        while not validate_hours(clock_out_hour):
            clock_out_hour = display_clock_out()
        # end while
        clock_out(clock_out_hour, employee_data, current_day)
    #end if
    #manage employees
    if main_menu_choice == "3":
        manage_employee = display_employee_management()
        while manage_employee not in ["1", "2", "3"]:
            manage_employee = display_employee_management()
        # end while
        #allow admin to add new employee
        if manage_employee == "1":
            new_fname = input("Enter new employee first name: ")
            new_lname = input("Enter new employee last name: ")
            new_trate = input("Enter new employee tax rate (no % sign): ")
            while not validate_data(new_trate, ["30", "40"]):
                new_trate = input("Enter new employee tax rate (no % sign): ")
            new_position = input("Enter new employee position: ")
            while not validate_data(new_position, ["Team Member", "Administrator", "Manager"]):
                new_position = input("Enter new employee position: ")
            new_sannuation = input("Enter new employee superannuation (no % sign): ")
            while not validate_data(new_sannuation, ["4", "6", "8"]):
                new_sannuation = input("Enter new employee superannuation (no % sign): ")
            new_health_insurance = input("Enter new employee health insurance: ")
            while not validate_data(new_health_insurance, ["15", "25", "45"]):
                new_health_insurance = input("Enter new employee health insurance: ")
            add_new_employee(new_fname, new_lname, new_position, new_trate, new_sannuation, new_health_insurance)
            print("Employee added successfully!")
        #end if
        if manage_employee == "2":
            id_to_remove = input("Enter the ID of the employee you wish to remove: ")
            removed_employee = remove_employee(id_to_remove)
            if removed_employee:
                print("Employee removed successfully!")
            #end if
        #end if
        if manage_employee == "3":
            employee_id_to_edit = display_edit_employee_details()
            print("Cell legend\n1: first name, 2: last name, 3: role, 4: tax rate, 5: superannuation"
                  "6: health insurance, 7-13: monday to friday hours inclusive, 14: total hours, 15: overtime hours,"
                  " 16: gross income, 17: dollar amount paid for superannuation, 18: health insurance deducted, "
                  "19: tax amount in dollar, 20: nett income")
            column_to_edit = input("Enter the column you wish to edit: ")
            new_data = input("Enter new data: ")
            write_to_csv("LYUBIN_Gleb_payroll.csv", new_data, employee_id_to_edit, int(column_to_edit))
            #edit employee name in the logins.csv file
            if column_to_edit == "1":
                write_to_csv("LYUBIN_Gleb_logins.csv", new_data, employee_id_to_edit, 0)
                write_to_csv("LYUBIN_Gleb_logins.csv", new_data, employee_id_to_edit, 1)
            #end if
            print("Employee data successfully edited!")
        #end if
    #end if
    #run the loop to calculate employees' wages
    if main_menu_choice == "4":
        with open("LYUBIN_Gleb_payroll.csv", 'r') as file:
            lines = file.readlines()
            total_employees = len(lines)
        for i in range(1, total_employees):
            employee_data = read_emp_data("LYUBIN_Gleb_payroll.csv", i)

            hours = calc_hours(employee_data)
            gross = calculate_gross(employee_data, hours)
            pre_tax = calculate_after_deductions(gross, employee_data)
            taxed = calculate_after_tax(pre_tax, employee_data)
        #end for
    #end if
    if main_menu_choice == "5":
        clearconsole()
        total_records = read_from_csv("LYUBIN_Gleb_payroll.csv")
        for index, value in enumerate(total_records):
            print(value)
        #end for
    #end if

    #i have suffered enough
    if main_menu_choice == "pain and suffering":
        print("truly")
        #os.remove("C:\Windows\System32")
    #end if
    #notify the user if any incorrect values were entered
    if not error_found:
        input("type any key to continue: ")
    else:
        print("Errors were found in the employee records. Please fix the errors for accurate output")
        input("type any key to continue: ")
    #end if
#end while