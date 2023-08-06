def test():
    print("hrantPOG is installed in your Python program")
    
# RELATED TO: LISTS

def list2str(li, split):
    string = ""
    for i in range(len(li) - 1):
        string += li[i]
        string += split
    string += li[len(li) - 1]
    
    return string

def fliplist(li):
    nlist = []
    for i in range(len(li)):
        nlist.append("")
    for index in range(len(li)):
        nlist[len(li) - index - 1] = li[index]
        
    return nlist

def listrand(li):
    import random
    return li[random.randint(0, len(li) - 1)]

# RELATED TO: GENERATION

def rand(n1, n2):
    import random
    
    return random.randint(n1, n2)

def randstr(l):
    import random
    r = ""
    txt = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%&()"
    txt = list(txt)
    for i in range(l):
        r += txt[random.randint(0, len(txt) - 1)]
        
    return r

def randcustom(txt, l):
    import random
    r = ""
    txt = list(txt)
    for i in range(l):
        r += txt[random.randint(0, len(txt) - 1)]
        
    return r

def randcode(l):
    return randcustom("0123456789", l)

# RELATED TO: TIME
def yeartosec(year):
    return year * 365 * 24 * 60 * 60

def hourtosec(hour):
    return hour * 60 * 60

def wait(sec):
    import time
    time.sleep(sec)
    return 0

def fakeprogbar(lim, tpa, clear):
    import os
    prog = 0
    
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')
        
    cls()
        
    while True:
        if clear == True:
            wait(tpa)
            prog += 1
            cls()
        else:
            wait(tpa)
            prog += 1
        print(str(prog) + "/" + str(lim))
        
        if prog == lim:
            break
    
def fakeprogbar_extra(lim, tpa, clear, nerd, txt1, txt2):
    import os
    prog = ""
    progn = 0
            
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')
        
    if clear == True:
        cls()
        
    for i in range(progn):
            prog += txt1
    for i in range(lim - progn):
            prog += txt2
            
    print(prog)
        
    while True:
        if clear == True:
            progn += 1
            wait(tpa)
            cls()
        else:
            progn += 1
            wait(tpa)
        
        prog = ""
        
        for i in range(progn):
            prog += txt1
        for i in range(lim - progn):
            prog += txt2
            
        print(prog)
        
        if nerd == True:
            print(str(progn) + "/" + str(lim))
        
        if progn == lim:
            break
        
# RELATED TO: INTERNET
def openweb(website):
    import webbrowser
    webbrowser.open_new_tab(website)
    
def google(search):
    import webbrowser
    search = search.replace(" ", "+")
    webbrowser.open_new_tab("https://www.google.com/search?q=" + search)
    
# RELATED TO: 
