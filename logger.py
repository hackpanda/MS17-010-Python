red = "\033[1;31m"
blue = "\033[1;34m"
yellow = "\033[1;33m"
green = "\033[1;32m"

greenbg = "\033[42;1m"
redbg = "\033[41;1m"
remove = "\033[0m"

def RED(string): return (red + string + remove)
def BLUE(string): return (blue + string + remove)
def YELLOW(string): return (yellow + string + remove)
def GREEN(string): return (green + string + remove)

def GREENBG(string): return (greenbg + string + remove)
def REDBG(string): return (redbg + string + remove)


def info(string): print(BLUE("[#] : ") + string)
def action(string): print(YELLOW("[!] : ") + string)
def error(string): print(RED("[-] : ") + string)
def success(string): print(GREEN("[+] : ") + string)

def title(string): print (GREENBG(string))
def announce(title, string): print (GREENBG(title),string)
