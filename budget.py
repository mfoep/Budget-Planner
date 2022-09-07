import os, subprocess
path = os.path.dirname(os.path.abspath(__file__))+"/"
#print(path)

percentages = {
    "house": 0.35,
    "transport": 0.15,
    "food": 0.2,
    "debt": 0.05,
    "personal": 0.1,
    "saving": 0.1,
    "utilities": 0.04,
    "other": 0.01
}

names = ["house","transport","food","debt","personal","saving","utilities","other"]
budget = {}

def importBudget():
    """Imports the contents of budget.txt to the budget dictionary"""
    f = open(path+"budget.txt","r")
    line = f.readline()
    i = 0
    while line != "":
        budget[names[i]] = float(line.strip("\n"))
        i += 1
        line = f.readline()
    f.close()

def capfstltr(wrd):
    """Returns the input string with the first letter capitalised"""
    return wrd[0].upper()+wrd[1:]

#print(capfstltr("hello world"))

def money(flt):
    """Converts a floating point number or integer to a money format"""
    return '${:,.2f}'.format(flt)

def display(dic):
    """Returns a dictionary containing categories as keys and their amount as values as a simple string easily printed"""
    rstr = 24*"="+"\n"
    tot = 0
    for key in dic.keys():
        rstr += "|"+capfstltr(key)+":"+(21-len(key)-len(money(dic[key])))*" "+money(dic[key])+"|\n"
        tot += dic[key]
    rstr += 24*"-"+"\n"
    rstr += "|Total:"+(22-len("Total:")-len(money(tot)))*" "+money(tot)+"|\n"
    rstr += 24*"="
    return rstr

def add(amount):
    """Adds an amount to all categories according to their percentages"""
    print(40*"=")
    oldTot = 0
    for key in percentages.keys():
        print("|"+capfstltr(key)+":"+(21-len(key)-len(money(budget[key])))*" "+money(budget[key])+" ",end="")
        oldTot += budget[key]
        budget[key] += amount*percentages[key]
        print("-> "+(12-len(money(budget[key])))*" "+money(budget[key])+"|")
    tot = oldTot + amount
    print(40*"-")
    print("|Total:"+(22-len("Total:")-len(money(oldTot)))*" "+money(oldTot)+" ",end="")
    print("-> "+(12-len(money(tot)))*" "+money(tot)+"|")
    print(40*"=")

def addTo(key, amount):
    """Adds an amount to a specific category"""
    oldTot = 0
    for val in budget.values():
        oldTot += val
    print(40*"=")
    print("|"+capfstltr(key)+":"+(21-len(key)-len(money(budget[key])))*" "+money(budget[key])+" ",end="")
    budget[key] += amount
    print("-> "+(12-len(money(budget[key])))*" "+money(budget[key])+"|")
    tot = oldTot + amount
    print(40*"-")
    print("|Total:"+(22-len("Total:")-len(money(oldTot)))*" "+money(oldTot)+" ",end="")
    print("-> "+(12-len(money(tot)))*" "+money(tot)+"|")
    print(40*"=")


def take(amount):
    """Takes an amount from all categories according to their percentages"""
    print(40*"=")
    oldTot = 0
    for key in percentages.keys():
        print("|"+capfstltr(key)+":"+(21-len(key)-len(money(budget[key])))*" "+money(budget[key])+" ",end="")
        oldTot += budget[key]
        budget[key] -= amount*percentages[key]
        print("-> "+(12-len(money(budget[key])))*" "+money(budget[key])+"|")
    tot = oldTot-amount
    print(40*"-")
    print("|Total:"+(22-len("Total:")-len(money(oldTot)))*" "+money(oldTot)+" ",end="")
    print("-> "+(12-len(money(tot)))*" "+money(tot)+"|")
    print(40*"=")

def takeFrom(key,amount):
    """Takes an amount from a specific category"""
    oldTot = 0
    for val in budget.values():
        oldTot += val
    print(40*"=")
    print("|"+capfstltr(key)+":"+(21-len(key)-len(money(budget[key])))*" "+money(budget[key])+" ",end="")
    budget[key] -= amount
    print("-> "+(12-len(money(budget[key])))*" "+money(budget[key])+"|")
    tot = oldTot - amount
    print(40*"-")
    print("|Total:"+(22-len("Total:")-len(money(oldTot)))*" "+money(oldTot)+" ",end="")
    print("-> "+(12-len(money(tot)))*" "+money(tot)+"|")
    print(40*"=")

def save():
    """Saves the current budget to 'budget.txt'"""
    f = open(path+"budget.txt","w")
    wstr = ""
    for val in budget.values():
        wstr += str(val)+"\n"
    f.write(wstr)
    f.close()
    print("Saved")

def clear():
    """Resets all the budget value to 0"""
    uIn = input("This will delete all saved amount.\nAre you sure? (y/N) >> ")
    if uIn.lower() == "y":
        for key in budget.keys():
            budget[key] = 0
        print("Cleared Avtive Budget")

def receip():
    """This function will print the budget to a receip using EST/POS"""
    pass

def debug():
    importBudget()
    #print(display(budget))
    add(1234)
    take(500)
    addTo("food",100)
    takeFrom("personal",30)
    clear()
    save()
    print(display(budget))

def email():
    """sends the budget by email to the address inputed using thunderbird"""
    f = open(path+"budgetPrint.txt","w")
    f.write(display(budget))
    f.close()
    os.system("thunderbird -compose from="+input("From >> ")+",to="+input("To >> ")+",subject=budget,attachment="+path+"budgetPrint.txt")

def main():
    importBudget()
    print(display(budget),end="\n\n")
    saved = True
    while 1:
        uIn = input(">> ").lower()
        uIn = uIn.split()
        
        if uIn[0] == "exit":
            if not saved:
                uIn = input("Would you like to save? (Y/n) >> ").lower()
                if uIn == "n":
                    pass
                else:
                    save()
            break
        elif uIn[0] == "save":
            save()
            saved = True
        elif uIn[0] == "clear":
            clear()
            saved = False
        elif uIn[0] == "display" or uIn[0] == "show" or uIn[0] == "budget":
            if len(uIn) == 1:
                print(display(budget))
            else:
                try:
                    print(24*"="+"\n"+"|"+capfstltr(uIn[1])+":"+(21-len(uIn[1])-len(money(budget[uIn[1]])))*" "+money(budget[uIn[1]])+"|\n"+24*"=")
                except:
                    print("Error: "+uIn[1]+" is not in in the budget plan")
        elif uIn[0] == "add":
            if len(uIn) == 2:
                try:
                    add(float(uIn[1]))
                    saved = False
                except:
                    print("Error: "+uIn[1]+" is not a number")
            else:
                try:
                    addTo(uIn[1],float(uIn[2]))
                    saved = False
                except:
                    if uIn[1] not in budget.keys():
                        print("Error: "+uIn[1]+" is not in the budget plan")
                    else:
                        print("Error: "+uIn[2]+" is not a number")
        elif uIn[0] == "take":
            if len(uIn) == 2:
                try:
                    take(float(uIn[1]))
                    saved = False
                except:
                    print("Error: "+uIn[1]+" is not a number")
            else:
                try:
                    takeFrom(uIn[1],float(uIn[2]))
                    saved = False
                except:
                    if uIn[1] not in budget.keys():
                        print("Error: "+uIn[1]+" is not in the budget plan")
                    else:
                        print("Error: "+uIn[2]+" is not a number")
        elif uIn[0] == "help":
            print("\texit\t\t\texits the program and asks to saved unsaved work")
            print("\tsave\t\t\tsaves the work")
            print("\tclear\t\t\tresets every value to 0")
            print("\tdisplay\t\t\tshows the budget")
            print("\tadd [category]\t\tadds to the budget or a category")
            print("\ttake [category]\t\ttakes from the budget or a category")
        elif uIn[0] == "send":
            email()
        else:
            print("Error: "+uIn[0]+" command not found")

if __name__ == "__main__":
    main()
