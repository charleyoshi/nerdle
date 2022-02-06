import random
import re

TOTALSPACE = 8
EQUALSIGNPOSITIONS = [6, 7]
# symbols with weighting (I want more +, less /)    eg. ['+', '+', '+', '+', '-', '-', '-','*', '*', '*', '/'] 
symbols = ['+'] * 4 + ['-'] * 3 + ['*'] * 2 + ['/'] * 1
numbersWith0 = ['1'] + ['2'] + ['3'] + ['4'] + ['5'] + ['6'] + ['7'] + ['8'] + ['9'] + ['0']
numbersWithout0 = ['1'] + ['2'] + ['3'] + ['4'] + ['5'] + ['6'] + ['7'] + ['8'] + ['9']



def bake(times):
    list = []
    for i in range(times):
        equalSignPosition = random.choice(EQUALSIGNPOSITIONS)
        leftHandSide = generateEquations(equalSignPosition) # '211*3'
        
        try:
            rightHandSide = float(calculate(leftHandSide)) # 633.0
        except:
            rightHandSide = None 
            
        # Condition 1: the equation is valid (Invalid examples: '12/0+3', '217998', '21799+')
        # Condition 2: Answer(RHS) must be an integer
        # Condition 3: Number of space the answer occupies eg. -12 => 3 spaces, 20 => 4 spaces
        # Condition 4: To get rid of negative numbers and extremely small float eg. 0.000052 (Python handle small numbers is out of scope of difficulty of this project, so we just assume we won't have equations = 0)
        isEquationValid = rightHandSide is not None
        if isEquationValid: 
            
            isInteger = rightHandSide == int(rightHandSide or 0) 
            isSpaceValid = len(str(int(rightHandSide or 0))) == TOTALSPACE - equalSignPosition
            isNotSmallNum = rightHandSide >= 1
            
            if isInteger and isSpaceValid and isNotSmallNum:
                list.append((leftHandSide, '=', int(rightHandSide)))

   
    # write into the text file
    with open('equationdatabase.txt','w') as f:
        for i in list:
            f.write(''.join(str(s) for s in i) + '\n')





def generateEquations(equalSignPosition):
    '''generate an equation into list eg. ['5', '1', '/', '7', '9'] then convert to string'''
    LHSList = []
    for i in range(equalSignPosition - 1):
        if i == 0:
            a = random.choice(numbersWithout0)
        elif i == (equalSignPosition - 1 - 1):
            a = random.choice(numbersWith0)
        else:
            if(LHSList[-1] in symbols):
                a = random.choice(numbersWithout0)
            else:
                a = random.choice(numbersWith0 + symbols)
        LHSList.append(a)
    
    LHSString = listToString(LHSList)
    return LHSString 


def listToString(list):
    '''Convert a list into string. e.g ['2', '1', '1', '*', '3']    =>  '211*3'       '''
    returnString = ''
    for i in list:
        returnString += i 
    return returnString


def calculate(string):
    '''Take a string of LHS as input and return a float of RHS'''
    res = re.split(r'(\D)', string) #  ['2', '/', '17', '+', '9']
    if len(res) <= 2: # Incomplete eg. ['217998'] or ['21799', '+']
        return None

    while len(res) > 2:
        for i in range(len(res)):
            if res[i] == '*':
                newMath = float(res[i - 1]) * float(res[i+1])
                res.insert( i + 1 + 1, newMath)
                del res[i - 1 : i + 1 + 1 ]
                break
            # Although generateEquations() won't generate zeroDivisionError, still have to implement {try and catch}, because users may input something like 1/0
            elif res[i] == '/': 
                try:
                    newMath = float(res[i - 1]) / float(res[i+1]) # This is very important. float(1/10) gives 0.0, but float(1)/10 or 1/float(10) gives 0.1
                except ZeroDivisionError:
                    return None
                res.insert( i + 1 + 1, newMath)
                del res[i - 1 : i + 1 + 1 ]
                break
            elif res[i] == '+' and '*' not in res and '/' not in res:
                newMath = float(res[i - 1]) + float(res[i+1])
                res.insert( i + 1 + 1, newMath)
                del res[i - 1 : i + 1 + 1 ]
                break
            elif res[i] == '-' and '*' not in res and '/' not in res:
                newMath = float(res[i - 1]) - float(res[i+1])
                res.insert( i + 1 + 1, newMath)
                del res[i - 1 : i + 1 + 1 ]
                break
    
    return res[0]



    


