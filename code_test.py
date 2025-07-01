"""
Author: Sathvik Valluri, vallurs@purdue.edu
Assignment: 12.1 - Code Breakers
Date: 04/14/2024

Description:
    Describe your program here.

Contributors:
    Arnav Rao, arnavrao@purdue.edu 

My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor.

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""

import random as r
import string 
import datetime as dt


def generate_solution(min_val, max_val):
    length = r.randint(min_val, max_val)
    nums = r.choices(['0','1','2','3','4','5'], k=length)
    r.shuffle(nums)
    return ''.join(nums)

def find_pins(passcode, guess):
    red_pins, white_pins = 0, 0
    passcode_2 = list(passcode)
    guess_2 = list(guess)
    min_length = min(len(guess), len(passcode))

    for i in range(min_length):
        if guess[i] == passcode[i]:
            red_pins += 1
            passcode_2[i] = '^'
            guess_2[i] = '*'
    
    for j in range(min_length):
        if guess_2[j] in passcode_2:
            white_pins += 1
            passcode_2.remove(guess_2[j])

    return red_pins, white_pins

def save_game(choice, file_name, files, date_time, grid, passcode, red_pins, white_pins, chance):
    if choice == 2:
        file_name = ['first_game', 'second_game', 'third_game']
        print('Files:')
        for i in range(3):
            if date_time[i] == '0':
                print(f' {i+1}: {files[i]}')
            else:
                print(f' {i+1}: {files[i]} - Time: {date_time[i]}')
        
        while True:
            file_choice = str(input('What save would you like to overwrite (1, 2, 3, or c to cancel): '))
            if file_choice in '123c':
                break
            else:
                print('That is an invalid selection.')

        if file_choice == 'c':
            print('cancelled')
        else:
            file_choice = int(file_choice)
            while True:
                files[file_choice-1] = str(input('What is your name (no special characters): '))
                if not any(char in string.punctuation for char in files[file_choice-1]):
                    break
                else:
                    print('That is an invalid name.')
            print(f'Game saved in slot {file_choice} as {files[file_choice-1]}.')
            date_time[file_choice-1] = dt.datetime.now().isoformat(timespec="seconds")
            
            with open(f'{file_name[file_choice-1]}.txt', 'w') as file:
                file.write(files[file_choice-1] + '\n')
                file.write(date_time[file_choice-1] + '\n')
                file.write(passcode + '\n')
                file.write(str(chance) + '\n')
                for l in grid:
                    file.write(' '.join(l) + '\n')
                file.write(' '.join(map(str, red_pins)) + '\n')
                file.write(' '.join(map(str, white_pins)) + '\n')
    else:
        date_time = dt.datetime.now().isoformat(timespec="seconds")
        file_choice = 0
        with open(f'{file_name}.txt', 'w') as file:
                file.write(files + '\n')
                file.write(date_time + '\n')
                file.write(passcode + '\n')
                file.write(str(chance) + '\n')
                for l in grid:
                    file.write(' '.join(l) + '\n')
                file.write(' '.join(map(str, red_pins)) + '\n')
                file.write(' '.join(map(str, white_pins)) + '\n')

    return file_choice, files, date_time

def load_game(file_name):
    files = []
    date_time = []
    grid = []
    red_pins = []
    white_pins = []

    with open(f'{file_name}.txt', 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                files.append(line.strip())
            elif i == 1:
                date_time.append(line.strip())
            elif i == 2:
                passcode = line.strip()
            elif i == 3:
                chance = int(line.strip())
            elif 4 <= i <= 13:
                grid.append(line.strip().split(' '))
            elif i == 14:
                red_pins = list(map(int, line.strip().split(' ')))
            elif i == 15:
                white_pins = list(map(int, line.strip().split(' ')))

    return files, date_time, passcode, grid, red_pins, white_pins, chance

def play_game(choice, file_name, files, date_time, passcode, grid, red_pins, white_pins, chance):
    guess = 0
    file_choice = 0
    answer = ['o' for z in range(6)]
    while chance < 10:
        print('+------------------+-----+')
        print(f'| {"  ".join(answer)} | R W |')
        print('+------------------+-----+')
        for i in range(0, 10):
            print(f'| {"  ".join(grid[i])} | {red_pins[i]} {white_pins[i]} |')
        print('+------------------+-----+')
        while True:
            guess = str(input('What is your guess (q to quit, wq to save and quit): '))
            if guess == 'q' or guess =='Q':
                break
            elif guess == 'wq':
                file_choice, files, date_time = save_game(choice, file_name, files, date_time, grid, passcode, red_pins, white_pins, chance)
                break
            elif guess == passcode:
                chance += 1
                break
            elif guess == "" or (len(guess) < 4 and guess.isdigit()):
                print(f'Your guess was "{guess}". This is too short.')
                print('Guess lengths must be between 4 and 6.')
            elif len(guess) > 6 and guess.isdigit():
                print(f'Your guess was "{guess}". This is too long.')
                print('Guess lengths must be between 4 and 6.')
            elif guess.isdigit() and any(digit not in '012345' for digit in guess):
                print(f'Your guess was "{guess}". It must be only numbers 0 through 5.')
            elif not guess.isdigit() and guess != 'q':
                print(f'Your guess was "{guess}". It must be only numbers!')
            else:
                chance += 1
                break
        
        if guess == 'q' or guess =='Q' or (guess == 'wq' and file_choice != 'c'):
            break

        if guess != 'wq':
            for n in range(len(guess)):
                grid[10-chance][n] = guess[n]
            red_pins[10-chance], white_pins[10-chance] = find_pins(passcode, guess)

        if guess == passcode:
                break

    if guess == 'q' or guess =='Q' or file_choice in [1,2,3]:
        print('Ending Game.')
    else:
        answer[0:len(passcode)] = passcode
        print('+------------------+-----+')
        print(f'| {"  ".join(answer)} | R W |')
        print('+------------------+-----+')
        for i in range(0, 10):
            print(f'| {"  ".join(grid[i])} | {red_pins[i]} {white_pins[i]} |')
        print('+------------------+-----+')
        if guess == passcode:
            print('Congratulations, you broke the lock!')
            print('The grades are safe!')
    
        else:
            print('You hear a machine yell OUT OF TRIES!')
            print('  ...')
            print('Is that burning you smell?')
            print('  ...')
            print('OH, NO! It looks like IU has destroyed all the EBEC grades!')
            print('')
    return files, date_time
    

def main():
    print("You are part of Unladened Swallow Society trying to break the infamous Holy")
    print("Grail lock.  This lock protects a vault where IU has locked up all the EBEC")
    print("grades.  To get your grades you will have to break this lock.  Luckily")
    print("those silly IU students messed up when making this lock, and it will give")
    print("you hints on what the code is.  However, you don't know the length of the")
    print("passcode and only have 10 guesses.  You don't want to run out of these.")
    print("Maybe the vault will turn you into a newt!.  Maybe it will destroy the")
    print("grades.  What if you have to rewrite time-calculator!")
    print('')
    print('Will you be able to break this lock before your grades are lost forever?')
    print('')
    
    files = []
    date_time = []
    file_names = ['first_game', 'second_game', 'third_game']

    for file_name in file_names:
        try:
            with open(f'{file_name}.txt', 'r') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    if i == 0:
                        files.append(line.strip())
                    elif i == 1:
                        date_time.append(line.strip())
        except FileNotFoundError:
            files.append('empty')
            date_time.append('0')


    while True:
        print('Menu:')
        print('  1: Rules')
        print('  2: New Game')
        print('  3: Load Game')
        print('  4: Quit')
        choice = input('Choice: ')

        if choice == '1':
            print('')
            print('Code Breakers Rules:')
            print('1. You get 10 guesses to break the lock.')
            print('2. Guess the correct code to win the game.')
            print('3. Codes can be either 4, 5, or 6 digits in length.')
            print('4. Codes can only contain digits 0, 1, 2, 3, 4, and 5.')
            print('5. Clues for each guess are given by a number of red and white pins.')
            print('   a. The number of red pins in the R column indicates the number of digits')
            print('      in the correct location.')
            print('   b. The number of white pins in the W column indicates the number of')
            print('      digits in the code, but in the wrong location.')
            print('   c. Each digit of the solution code or guess is only counted once in the')
            print('      red or white pins.')
            print('')
        elif choice == '2':
            passcode = generate_solution(4,6)
            #print(passcode)
            chance = 0
            file_choice = 0
            
            grid = [['o' for k in range(6)] for l in range(10)]
            red_pins = [0 for m in range(10)]
            white_pins = [0 for p in range(10)]
            
            files, date_time = play_game(choice, files, date_time, passcode, grid, red_pins, white_pins, chance)
        elif choice == '3':
            file_name = ['first_game', 'second_game', 'third_game']
            print('Files:')
            for i in range(3):
                if date_time[i] == '0':
                    print(f' {i+1}: {files[i]}')
                else:
                    print(f' {i+1}: {files[i]} - Time: {date_time[i]}')
            while True:
                file_choice = str(input('What save would you like to load (1, 2, 3, or c to cancel): '))
                if file_choice in '123c':
                    if file_choice == 'c':
                        break
                    else:
                        file_choice = int(file_choice)
                        if files[file_choice-1] == 'empty': 
                            print('That file is empty!')
                        else:
                            break
                else:
                    print('That is an invalid selection.')

            if file_choice == 'c':
                print('cancelled')
            else:
                file_choice = int(file_choice)
                files, date_time, passcode, grid, red_pins, white_pins, chance = load_game(file_name[file_choice-1])

                files, date_time = play_game(choice, file_name[file_choice-1], files[file_choice-1], date_time, passcode, grid, red_pins, white_pins, chance)
        elif choice == '4':
            print('Goodbye')
            break       
        else:
            print('Please enter 1, 2, 3, or 4.')
    

"""Do not change anything below this line."""
if __name__ == "__main__":
    main()
    print("hello")
