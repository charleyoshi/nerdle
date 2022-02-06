import sys
from bake import *

maxAttempt = 6
message = '_ _ _ _ _ _ _ _'

VALIDCHARACTERS = '1234567890+-*/= '

def main():
    # If you already have a database, comment the next line
    bake(1000)
    
    play('equationdatabase.txt')



def play(db):
    '''Take the name of .txt file of the eqauation database and play'''

    isWin = False
    equationList = []
    try:
        with open(db) as f:
            for line in f:
                equationList.append(line.strip())
    except:
        print('OOOPS! No such file called \'{0}\' in your directory. Make sure you get the right name for your .txt file.'.format(db))
        sys.exit()
           
    answer = random.choice(equationList)


    currentAttempt = 0
    while currentAttempt < maxAttempt:
        print('------------------------------------')
        print('\tLet\'s guess! You have {0} attempts left.'.format(maxAttempt - currentAttempt))
        
        if currentAttempt == 0:
            print(message)
        else: 
            print(userInput)
            print(hintstr.join(hint))

        isValidInput = False
        while isValidInput == False:

            userInput = input('Enter your guess:')
            if (len(userInput) - userInput.count(' ') == len(answer)):
                if userInput.count('=') != 1:
                    print('Make sure there is only one =')
                    continue

                if isEquationValid(userInput):
                    isValidInput = True
                    break
                else:
                    print('Make sure your equation is correct. Maybe you would like to check your math again.')

            else:

                if(len(userInput) != 0):
                    print('There are {} spaces!'.format(len(answer)))


        userInput = userInput.replace(' ', '')
        print(userInput)


        if userInput == answer:
            isWin = True
            break


        hintstr = ''
        hint = []
        for i in range(len(userInput)):
            if userInput[i] == answer[i]:
                hint.append('o')
            elif userInput[i] in answer:
                hint.append('s')
            else:
                hint.append('x')
        currentAttempt += 1


    
    if isWin:
        # show Win message
        print('\tYou won! The answer is {0}'.format(answer))
    else:
        #show Lose message
        print('\tSorry! You lose. You\'ve ran out of attempts')
        print('\tThe answer is: {0}'.format(answer))


def isEquationValid(userInput):

    for i in userInput:
        if i not in VALIDCHARACTERS:
            return False
    try:
        lhs = userInput[:userInput.index('=')].replace(' ', '')
        rhs = userInput[userInput.index('=') + 1:].replace(' ', '')
        if '+' in rhs or '-' in rhs or '*' in rhs or '/' in rhs :
            print('The right hand side of your equation should only contain numbers')
            return False

        try: 
            answer = calculate(lhs)
            if float(answer) == float(rhs):
                return True
        except:
            return False
    except: 
        # lhs or rhs is None
        return False
        
    return False



if __name__ == "__main__":
    main()