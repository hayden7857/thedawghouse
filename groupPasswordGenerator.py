# Password generator + storage functions
# Team Kaizen
# Author Tommy Hayden
# date 9/20/19
import os
import random
import signal
import string
import atexit

def main():
    os.system("mode con cols=45 lines=13")
    os.system("title PassSafe")

    def getLen(characterOption):
        try:
            plen = int(input("Enter the length of the password you want to generate.\n"))
        except:
            print("The length must be a whole number.")
            plen = getLen(characterOption)
        finally:
            return makepassword(plen, characterOption)

    '''This uses the plen from getLen and characterOption from the GUI to generate a password'''

    def makepassword(plen, characterOption):
        charTypes = [list(string.digits), list(string.ascii_uppercase), list(string.ascii_lowercase),
                     list(string.punctuation)]
        password = ''
        hasUpper = False
        hasLower = False
        hasNumber = False
        hasSpec = False
        '''True for special characters'''
        if characterOption:
            for x in range(plen):
                '''Pick a random character type list then pick a random character from that list'''
                nextChar = random.choice(random.choice(charTypes))
                if nextChar.isalpha():
                    if nextChar.isupper():
                        hasUpper = True
                    else:
                        hasLower = True
                elif nextChar.isnumeric():
                    hasNumber = True
                elif nextChar in list(string.punctuation):
                    hasSpec = True
                password = password + nextChar
            '''This checks that the password meets all requirements and if not the function recursivly calls itself'''
            if not (hasUpper and hasLower and hasNumber and hasSpec):
                password = makepassword(plen, characterOption)
        else:
            for x in range(plen):
                nextChar = random.choice(random.choice(charTypes[:3]))
                if nextChar.isalpha():
                    if nextChar.isupper():
                        hasUpper = True
                    else:
                        hasLower = True
                elif nextChar.isnumeric():
                    hasNumber = True
                password = password + nextChar
        return password

    def accountExist(file, site, uname):
        doc = open(file, 'r')
        contents = doc.read()
        doc.close()
        if contents.find(site + '\n' + uname) != -1:
            return True
        else:
            return False

    '''This takes site, uname, and pwd from the GUI inputs and appends them to the data filepath if they are not already 
    in use '''

    def writeNewEntry(file, site, uname, pwd):
        doc = open(file, 'r')
        contents = doc.read()
        doc.close()
        if contents.find(site + '\n' + uname) == -1:
            doc = open(file, 'a')
            doc.write('\n' + site + '\n' + uname + '\n' + pwd + '\n')
            doc.close()
        else:
            print("You've already saved a", uname, "account for", site, '\n')

    '''This takes an updated uname and pwd for an exsiting uname on a site from the GUI and updates the data filepath 
    with the new info '''

    def updateExistingPwd(file, site, uname, pwd):
        doc = open(file, 'r')
        contents = doc.read()
        doc.close()
        start = contents.find(site + '\n' + uname)
        pstart = start + len(uname) +len(site) + 2 # \n
        snip = contents[pstart:]
        end = snip.find('\n')
        oldPwd = snip[:end]
        contents = contents.replace(site + '\n' + uname + '\n' + oldPwd, site + '\n' + uname + '\n' + pwd)
        doc = open(file, 'w').close()
        doc = open(file, 'a').write(contents)


    '''Uses site and uname from GUI and retives the pwd from the data filepath'''

    def retrievePwd(file, site, uname):
        if type(uname) is list:
            uname=uname[0]
        doc = open(file, 'r')
        contents = doc.read()
        doc.close()
        start = contents.find(str(site + '\n' + uname))
        pstart = start + len(uname) +len(site) + 2  # \n
        snip = contents[pstart:]
        end = snip.find('\n')
        if end>0:
            pwd = snip[:end]
        else:
            pwd=snip
        return pwd

    def retrieveUnames(file, site):
        doc = open(file, 'r')
        contents = doc.read()
        doc.close()
        unames = list()
        while contents.find(site) != -1:
            start = contents.find(site) + len(site) + 1
            snip = contents[start:]
            end = snip.find('\n')
            uname = snip[:end]
            unames.append(uname)
            contents = contents[start + end:]
        return unames

    def firstLogin(file):
        print('=========================================')
        name = str(input("\tWelcome to PassSafe,\na password storage and generator program.\n"
                         "========================================="
                         "\nPlease enter your name.\n>"))
        while name=='':
            name=str(input('Your name has to be at least one character\nTry again.\n>'))
        pwd1 = str(input("Hello, " + name + '\nPlease enter a password\n>'))
        pwd2 = str(input("Reenter password to confirm\n>"))
        while pwd1 != pwd2:
            print("The entered passwords did not match\n")
            pwd1 = str(input("Please enter a password\n>"))
            pwd2 = str(input("Reenter password to confirm\n>"))

        writeNewEntry(file, 'RootUser', name, pwd1)
        homeMenu(file, name)

    def homeMenu(file, name):
        if type(name) is list:
            name = name[0]
        print('=================================')
        choice = input('\tWelcome ' + name.strip().title() +
                       '\nTo retieve logins enter \tr\nTo update existing logins enter u\n' +
                       'To create new login enter\tn\nAnything else to encode and close\n'+
                       '=================================\n\n\n\n\n\n>')
        choice = choice.strip().lower()





        if choice == 'r':
            print('==========================')
            print('\tRetrieve')
            site = str(input('Please enter the site name\n==========================\n\n\n\n\n\n\n\n\n'))
            site = site.strip().lower()
            print('\n\n\n\n\n\n\n')
            unames = retrieveUnames(file, site)
            if len(unames) > 1:
                print('Usernames associated with', site.title(), 'are:')
                counter=0
                for x in unames:
                    if counter==6:
                        print('...')
                        break
                    else:
                        print('['+x+']')
                        counter+=1
                    newLines='\n\n\n\n\n\n\n\n\n\n'
                    newLines=newLines[:-counter]
                uname = input(newLines+'Enter a username\n>')
                try:
                    print('==================')
                    print('Password for',uname+':\n'+ retrievePwd(file, site, uname))
                    print('==================\n\n\n\n\n\n\n\n')
                    input('Press enter to continue')
                except TypeError:
                    print('You entered an invalid username')
            elif len(unames) == 1:
                uname = unames[0]
                print('===========================\nUsername:\n\t' + uname + '\nPassword:\n\t' +
                      retrievePwd(file, site, uname)+'\n===========================')
                input('Press enter to continue\n')
            else:
                print('There are no accounts for that site')
            print('\n\n\n')
            homeMenu(file, name)




        elif choice == 'u':
            print('===========================\nUpdate Existing Account\n===========================')
            site = str(input('Please enter the site name\n\n\n\n\n\n\n\n\n>'))
            site = site.strip().lower()
            unames = retrieveUnames(file, site)
            if len(unames)==0:
                print('You haven\'t recorded',site.title(),'before.')
                input("Press Enter to continue")
                homeMenu(file,name)
            if len(unames) > 1:
                print('Usernames associated with', site.title(), 'are:')
                for x in unames:
                    print('['+x+']')
                try:
                    uname = str(input("Please enter the Username for\nthe password you wish to update\n>")).strip()
                except TypeError:
                    print('error')
                if accountExist(file, site, uname):
                    randpwd = str(input("Do you want to randomly generate a password?(y/n)\n>")).lower()
                    if randpwd == 'y' or randpwd == 'yes':
                        try:
                            length = int(
                                input("Enter the length of the password (int only) you want to generate\n>"))
                        except TypeError:
                            length = int(input("password length must be an integer value.\nTry again\n>"))
                        spec = input("Do you want to include special characters?(y/n)\n>").lower().strip()
                        if spec == 'y' or spec == 'yes':
                            newPwd = makepassword(length, True)
                        else:
                            newPwd = makepassword(length, False)
                    else:
                        newPwd = input('Enter the new Password\n')
                    try:
                        updateExistingPwd(file, site, uname, newPwd)
                        print('======================================')
                        print("Account Updated for",site.title(),'\nUsername:\n\t', uname, "Password:\n\t", newPwd)
                        print('======================================')
                    except TypeError:
                        print("EERRROR")
                else:
                    print("No account on", site, 'for', uname, 'exist.')
                input("Press Enter to continue")
                print('\n\n\n\n\n')
                homeMenu(file, name)
            elif len(unames) == 1:
                uname = unames[0]
                if accountExist(file, site, uname):
                    print("Updating the", uname, 'account\nfor site', site.title())
                    randpwd = str(input("Do you want to randomly generate a password?\n(y/n)\n\n\n\n\n\n\n\n\n>")).lower()
                    if randpwd == 'y' or randpwd == 'yes':
                        try:
                            length = int(
                                input("Enter the length of the password (int only)\nyou want to generate\n\n\n\n\n\n\n\n\n\n\n>"))
                        except TypeError:
                            length = int(input("password length must be an integer value.\nTry again\n"))
                        spec = input("Do you want to include special characters?\n(y/n)\n").lower().strip()
                        if spec == 'y' or spec == 'yes':
                            newPwd = makepassword(length, True)
                        else:
                            newPwd = makepassword(length, False)
                    else:
                        newPwd = input('Enter the new Password\n')
                    try:
                        updateExistingPwd(file, site, uname, newPwd)
                        print('======================================')
                        print("Password for", uname, "on site", site, "is now:\n"+ newPwd)
                        print('======================================')
                    except TypeError:
                        print("EERRROR")
                else:
                    print("No account on", site, 'for', uname, 'exist.')
                input("Press Enter to continue")
                print('\n\n\n\n\n')
                homeMenu(file, name)
            else:
                encodefile(file)
                input('Goodbye')




        elif choice == 'n':
            print('===========================\n\tNew Entry')
            site = str(input('Please enter the site name\n==========================='
                             '\n\n\n\n\n\n\n\n\n>')).strip().lower()
            uname = str(input('Please enter the username of the account\non site '+site.title()+
                              '\n\n\n\n\n\n\n\n\n\n\n>')).strip()
            pwd = str(input('Please enter the passsword for\n'+uname+'\nor enter r to randomly generate one'
                                                                     '\n\n\n\n\n\n\n\n\n\n>'))
            if pwd == 'r':
                try:
                    plen = int(input('Enter the number of characters you\nwant in the password\n\n\n\n\n\n\n\n\n\n\n>'))
                except TypeError:
                    plen= int(input('Int values only'))
                characterOption = str(input('Do you want to use special characters? (y/n)\n')).strip().lower()
                if characterOption == 'n':
                    pwd = makepassword(plen, False)
                else:
                    pwd = makepassword(plen, True)
            writeNewEntry(file, site, uname, pwd)
            print('=====================================')
            print('New account added for', site.title(), '\nUsername:\n\t', uname, '\nPassword:\n\t', pwd)
            print('=====================================\n\n\n\n')
            input('Press Enter to continue\n>')
            print('\n\n\n\n\n')
            homeMenu(file, name)

    def findDatafile():
        cwd = os.path.dirname(os.path.realpath(__file__))
        if cwd.find('\\') == -1:
            filepath = cwd + '/data.txt'
        else:
            filepath = cwd + '\\data.txt'
        if os.path.exists(filepath):
            print(' ==========================')
            print(' Welcome to PassSafe     ')
            if authenticate(filepath):
                decodefile(filepath)
                homeMenu(filepath, retrieveUnames(filepath, 'RootUser'))
            else:
                findDatafile()
        else:
            file = open('data.txt', 'w+').close()
            firstLogin('data.txt')
        return filepath

    def authenticate(file):
        doc=open(file,'r')
        contents=doc.read()
        doc.close()
        if len(contents)==0:
            print('Data file corrupt!\n\n\n\n\n\n\n\n\n\n\n')
            input('Press Enter to start a new data file')
            os.remove('data.txt')
            print('\n\n\n\n\n\n\n\n\n')
            findDatafile()
        if contents.find('\n')!=-1:
            encodefile(file)
            doc=open(file,'r')
            contents=doc.read()
        plen=snagChar(1,contents)
        pwd=snagChar(plen,contents)
        pwd=pwd[1:]
        inputpwd=str(input(' Please enter your password \n ==========================\n'))
        print()
        if pwd==inputpwd:
            print('\n\n\n\n')
            return True
        else:
            print('Incorrect password')
            return False

    def reverse(s):
        if len(s) == 0:
            return s
        else:
            return reverse(s[1:]) + s[0]

    def snagChar(numberofchar,string):
        string=string.split('-')
        string.reverse()
        stringList=list()
        nChar=0
        for char in string:
            stringList.append(char)
            nChar+=1
            if 1==numberofchar and nChar==numberofchar:
                return stringList[0]
            elif int(numberofchar)==nChar:
                stringList='-'.join(stringList)
                tmp=open('tmp.txt','w+')
                tmp.write(stringList)
                tmp.close()
                decodefile('tmp.txt')
                tmp=open('tmp.txt','r')
                pwd=tmp.read()
                tmp.close()
                os.remove('tmp.txt')
                return pwd

    def encodefile(file):
        pwd = retrievePwd(file, 'RootUser', retrieveUnames(file, 'RootUser'))
        switchswap="\nabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+|/?.>,<\\\"|[{]}"
        doc=open(file,'r')
        contents=doc.read()
        contents=contents.split()
        bucket=list()
        tmp=''
        for x in contents:
            for y in x:
                yswitch = str(switchswap.find(y))+' '
                tmp += yswitch
            tmp=tmp.strip()
            tmp=tmp.replace(' ','-')
            bucket.append(tmp)
            tmp=''
        contents='-0-'.join(bucket)
        plen=len(pwd)+1
        pwd=reverse(pwd)
        for x in pwd:
            pwd=pwd.replace(x,str(switchswap.find(x))+' ')
        pwd=pwd.strip()
        pwd=pwd.replace(' ','-')

        contents='-0-'.join(bucket)
        doc=open(file,'w').close()
        doc=open(file, 'a')
        doc.write(contents+'-0-'+str(pwd)+'-'+str(plen))
        doc.close()

    def decodefile(file):
        switchswap = "\nabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+|/?.>,<\\\"|[{]}"
        doc=open(file,'r')
        contents=doc.read()
        doc.close()
        contents=contents.replace('-0-',' ')
        lines=contents.split()
        cleartext=''
        if len(lines)>1:
            for line in lines:
                line=line.replace('-',' ')
                line=line.split()
                for char in line:
                    cleartext+=str(switchswap[int(char)])
                cleartext+='\n'
            doc=open(file,'w').close()
            doc=open(file,'w')
            doc.write(cleartext[:cleartext[:cleartext.rfind('\n')].rfind('\n')])
            doc.close()
        elif len(lines)==1:
            cleartext=lines[0].replace('-',' ')
            cleartext=cleartext.split()
            tmp=''
            for x in cleartext:
                x=str(switchswap[int(x)])
                tmp+=x
            cleartext=tmp
            doc = open(file, 'w').close()
            doc = open(file, 'w')
            doc.write(cleartext)
            doc.close()

    #encodefile('data.txt')

    findDatafile()
    try:
        atexit.register(encodefile('data.txt'))
    except:
        print('GoodBye')
    else:
        signal.signal(signal.SIGKILL, encodefile('data.txt'))
        signal.signal(signal.SIGTERM, encodefile('data.txt'))
main()
