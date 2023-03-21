# Author: JERRICK GODWIN

# Declare variables
Total_credits = 0      # Total of credit_at_pass, credit_at_defer, and credit_at_fail
Input_count = 1        # Count on each user entry
Outcome_count = 0
progress_count = 0     # Count progress entries
trailing_count = 0
retriever_count = 0
excluded_count = 0
Progression_Data = {   # Dictionary to store user input
  "Progress": [],
  "Progress (module trailer)": [],
  "Module retriever": [],
  "Exclude": []
}
filename = 'Progression_Data.txt'   # File name to print student progression data
         
# Declare user-defined exceptions
'''References:
User-defiened exceptions (8.6): https://docs.python.org/3/tutorial/errors.html#raising-exceptions
Custom classes (9.7): https://docs.python.org/3/tutorial/classes.html#tut-classes'''
class CommonError(Exception): 
    pass  # Raised when the input is out of range or the Total is incorrect
class UpdateError(Exception): 
    pass  # Raised when the program fails to update user input
class GeneralOutputError(Exception): 
    pass  # Raised when the program fails to generate Histograms

# Validate progression outcome
def validation(credit_at_pass, credit_at_defer, credit_at_fail):
    if credit_at_pass == 120:
        return 'Progress'
    elif credit_at_pass == 100:
        return 'Progress (module trailer)'
    elif (credit_at_pass <= 80) and (credit_at_defer <= 120) and (credit_at_fail <= 60):
        return 'Module retriever'
    elif (credit_at_pass <= 40) and (credit_at_defer <= 40) and (credit_at_fail >= 80):
        return 'Exclude'

# Reset values upon progression outcome/ exception
def reset_values():
    global Total_credits, Input_count
    Total_credits = 0
    Input_count = 1

# Validate input
def validate(value):
    global Total_credits, Input_count
    Total_credits += value  # Add value to Total to make sure Total is correct upon the third input
    if value not in (0, 20, 40, 60, 80, 100, 120):
        raise CommonError('Out of range!')
    elif (Input_count == 3 and Total_credits != 120) or (Input_count == 2 and Total_credits > 120):
        raise CommonError('Total incorrect!')
    else: 
        Input_count += 1
        return value

# Update progression data
def update_data(result, total_pass, total_defer, total_fail):
    global Progression_Data 
    user_input = []  # An empty array to store current student record
    user_input += total_pass, total_defer, total_fail
    Progression_Data[result].append(user_input)  

# Update histogram & entries
def update_histogram(part_number, result, total_pass, total_defer, total_fail):
    global progress_count, trailing_count, retriever_count, excluded_count, Outcome_count
    Outcome_count += 1
    try:
        match result:
            case 'Progress':
                progress_count += 1               
                if part_number in (3, 4):
                    update_data(result, total_pass, total_defer, total_fail)         
                return 'Outcome: ' + result
            case 'Progress (module trailer)':
                trailing_count += 1
                if part_number in (3, 4):
                    update_data(result, total_pass, total_defer, total_fail)
                return 'Outcome: ' + result
            case 'Module retriever':
                retriever_count += 1
                if part_number in (3, 4):
                    update_data(result, total_pass, total_defer, total_fail)
                return 'Outcome: ' + result
            case 'Exclude':
                excluded_count += 1
                if part_number in (3, 4):
                    update_data(result, total_pass, total_defer, total_fail)
                return 'Outcome: ' + result    
    except: 
        raise UpdateError('Failed to update entries!')

# Vertical histogram
def vertical_histogram(progress, trailer, retriever, exclude):
    try:
        current_index = 0  # Current item in the list
        columns = max(progress, trailer, retriever, exclude)  # Determine no of columns to print
        progression_list = [progress, trailer, retriever, exclude]
        print('------------------------------------------------------------------------------------------')
        print('                                    Vertical Histogram                                    ')
        print('------------------------------------------------------------------------------------------\n')
        print('Progress {0} | Trailer {1} | Retriever {2} | Excluded {3}'.format(
            progress, trailer, retriever, exclude), '\n')
        for i in range(columns):
            for index in progression_list:
                if (index > 0):
                    print('{:^11}'.format('*'), end='  ')
                    progression_list[current_index] -= 1
                    current_index += 1
                else:
                    print('{:^11}'.format(' '), end='  ')
                    current_index += 1
            current_index = 0
            print()  # Move to the next line
        print('\n')
        print(Outcome_count, 'Outcome(s) in total.')
        print('------------------------------------------------------------------------------------------')
    except: 
        raise GeneralOutputError('Failed to generate vertical histogram!')

# Horizontal histogram
def horizontal_histogram(progress, trailer, retriever, exclude):
    try:
        print('------------------------------------------------------------------------------------------')
        print('                                   Horizontal Histogram                                   ')
        print('------------------------------------------------------------------------------------------\n')
        print('Progress {0}   : {1}'.format(progress, '*'*progress))
        print('Trailer {0}    : {1}'.format(trailer, '*'*trailer))
        print('Retriever {0}  : {1}'.format(retriever, '*'*retriever))
        print('Excluded {0}   : {1}'.format(exclude, '*'*exclude), end='\n\n')
        print(Outcome_count, 'outcome(s) in total.')
        print('------------------------------------------------------------------------------------------')
    except: 
        raise GeneralOutputError('Failed to generate horizontal histogram!')

# Progression Data
def progression_data(student_data):
    try:
        print('------------------------------------------------------------------------------------------')
        print('                                     Progression Data                                     ')
        print('------------------------------------------------------------------------------------------\n')
        for key, value in student_data.items():
            for i in range(len(value)):
                List = value[i]  # Create a variable to store the current list in nested list
                print('{0} - {1}, {2}, {3}'.format(key, List[0], List[1], List[2]))
        print('\n')
        print(Outcome_count, 'outcome(s) in total.')
        print('------------------------------------------------------------------------------------------')
    except: 
        raise GeneralOutputError('Failed to generate progression data!')

# Print to file
def print_to_file(student_data, file_name):
    try:      
        file = open(file_name, 'w')  # Create a file or overwrite the existing file
        file.write('--------------------------------------------------')
        file.write('\n                 Progression Data             \n')
        file.write('--------------------------------------------------\n\n')
        for key, value in student_data.items():
            for i in range(len(value)):
                List = value[i]  # Create a variable to store the current list in nested list
                file.write('{0} - {1}, {2}, {3}\n'.format(key, List[0], List[1], List[2]))
        file.write('\n\n{0} outcome(s) in total.\n'.format(Outcome_count))
        file.write('--------------------------------------------------')
        file.close()
        print('------------------------------------------------------------------------------------------')
        print('Student data exported to:', file_name)
        print('------------------------------------------------------------------------------------------')
    except: 
        raise GeneralOutputError('Failed to print to file!')

# Read a text file
def read_file(file_name):
    try:
        with open(file_name, 'r') as file:  # Open the file in read mode
            print('------------------------------------------------------------------------------------------')
            print('Reading from', file_name)
            print('------------------------------------------------------------------------------------------')
            print(file.read())
            file.close()
        print('------------------------------------------------------------------------------------------')
        print('End of file data')
        print('------------------------------------------------------------------------------------------')
    except: 
        raise GeneralOutputError('Data file is either corrupted or does not exist!')
    
# Get input from a staff member upon progression outcome
def staff_input():
    print('------------------------------------------------------------------------------------------')           
    prompt = input('''
Would you like to enter another set of data?
Press 'y' for yes | Press 'q' to quit and view results

Enter option: ''')
    while True:
        match prompt.lower():
            case 'y': 
                return 'y'
            case 'q':
                return 'q'
            case _:
                print('Invalid input!')
                prompt = input('\nEnter option: ')

# Main program of the staff version
def main_staff(part_number):
    prompt = 'y'
    print('------------------------------------------------------------------------------------------')
    print('\n                  Progression Outcome - Staff Version with Histogram                  \n')
    print('------------------------------------------------------------------------------------------')
    while prompt != 'q' and prompt == 'y':
        reset_values()  # Total and Count set to zero
        try:
            Total_pass = validate(int(input('\nEnter your total PASS credits  : ')))        
            Total_defer = validate(int(input('Enter your total DEFER credits : ')))               
            Total_fail = validate(int(input('Enter your total FAIL credits  : ')))    
            outcome = validation(Total_pass, Total_defer, Total_fail)
            print('\n' + update_histogram(part_number, outcome, Total_pass, Total_defer, Total_fail), end='\n')
        except ValueError:           
            print('Integer required!')
            continue
        except (KeyboardInterrupt, CommonError) as e:
            print(str(e))
            continue
        except (UpdateError, Exception) as e:
            print(str(e))
            break  
        prompt = staff_input()  # Get input from a staff member whether or not to continue
    else:      
        try:
            match part_number:  # Validate the part number to print histograms, progression data, and print to a file
                case 1: 
                    horizontal_histogram(progress_count, trailing_count, retriever_count, excluded_count)
                case 2:
                    horizontal_histogram(progress_count, trailing_count, retriever_count, excluded_count)
                    vertical_histogram(progress_count, trailing_count, retriever_count, excluded_count)
                case 3:
                    horizontal_histogram(progress_count, trailing_count, retriever_count, excluded_count)
                    vertical_histogram(progress_count, trailing_count, retriever_count, excluded_count)
                    progression_data(Progression_Data)
                case 4:
                    horizontal_histogram(progress_count, trailing_count, retriever_count, excluded_count)
                    vertical_histogram(progress_count, trailing_count, retriever_count, excluded_count)
                    progression_data(Progression_Data)
                    print_to_file(Progression_Data, filename)    
        except GeneralOutputError as e:
            print(str(e))      

# Main program of the student version
def main_student(part_number):
    print('------------------------------------------------------------------------------------------')
    print('\n                        Progression Outcome - Student Version                         \n')
    print('------------------------------------------------------------------------------------------')
    while True:
        reset_values()  # Total and Count set to zero
        try:
            credit_at_pass = validate(int(input('Please enter your credits at pass  : ')))
            credit_at_defer = validate(int(input('Please enter your credits at defer : ')))            
            credit_at_fail = validate(int(input('Please enter your credits at fail  : ')))       
            print('\nOutcome:', validation(credit_at_pass, credit_at_defer, credit_at_fail), end='\n')
            input('\nPress any key to continue...')
            return Sub_main(part_number)
        except ValueError:           
            print('Integer required!\n')
            continue
        except (KeyboardInterrupt, CommonError) as e:
            print(str(e), '\n')
            continue
        except Exception as e:
            print(str(e))
            break    

# Menu for read previous progression records
def previous_progression_record(part_number):
    print('------------------------------------------------------------------------------------------')
    print('\n                    progression Outcome - Staff Version (Advanced)                    \n')
    print('------------------------------------------------------------------------------------------')
    prompt = input('''
Please choose an option below:
    
1. Press 1 to review previous student records
2. Press 2 to enter a set of new student records
3. Press 3 to Sub Menu

Enter option: ''')
    while True:
        match prompt:
            case '1':
                try:
                    read_file(filename)
                    input('\nPress any key to continue...')
                except GeneralOutputError as e:
                    print(str(e), '\n')
                    input('\nPress any key to continue...')
                return previous_progression_record(part_number)
            case '2': 
                return main_staff(part_number)    
            case '3': 
                return Sub_main(part_number)                      
            case _:
                print('\nInvalid input!')
                prompt = input('\nEnter option: ')

# Sub Menu of the program
def Sub_main(part_number):
    print('------------------------------------------------------------------------------------------')
    print('\n                            Progression Outcome - Sub Menu                            \n')
    print('------------------------------------------------------------------------------------------')
    prompt = input('''
Please choose an option below:
    
1. Press 1 to enter Student version
2. Press 2 to enter Staff version
3. Press 3 to Main Menu

Enter option: ''')
    while True:
        match prompt:
            case '1': 
                return main_student(part_number)            
            case '2':
                if part_number == 4:
                    return previous_progression_record(part_number)
                else: 
                    return main_staff(part_number)
            case '3': 
                return main()                      
            case _:
                print('\nInvalid input!')
                prompt = input('\nEnter option: ')

# Main Menu of the program
def main():
    print('------------------------------------------------------------------------------------------')
    print('\n                              Progression Outcome - Main Menu                         \n')
    print('------------------------------------------------------------------------------------------')
    prompt = input('''
Welcome to Progression Outcome program
Please choose an option below:
    
1. Press 1 to enter Part 1
2. Press 2 to enter Part 2
3. Press 3 to enter Part 3
4. Press 4 to enter Part 4
5. Press Q to Quit

Enter option: ''')
    while prompt.lower() != 'q':
        match prompt.lower():
            case '1': 
                return Sub_main(1)           
            case '2': 
                return Sub_main(2)               
            case '3': 
                return Sub_main(3)              
            case '4': 
                return Sub_main(4)               
            case _:
                print('\nInvalid input!')
                prompt = input('\nEnter option: ')

# Execute the main program
if __name__ == '__main__':
	main()