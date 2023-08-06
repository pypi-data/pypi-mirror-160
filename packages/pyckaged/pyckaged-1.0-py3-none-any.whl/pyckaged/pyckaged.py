#this is pyckaged, a package manager made with python

import os
import sys
import colorama as clr
import requests as rq
import pyfiglet as fig
import platform as plt
#this is terminal-only

def main():
    fig.print_figlet("Pyckage'd")
    try:
        command = sys.argv[1]
    except IndexError:
        print(clr.Fore.RED + "Error: No command specified.")
        sys.exit(1)

    homedir = os.path.expanduser("~")

    if command == "install":
        #make sure there is an argument for the package name
        if len(sys.argv) < 3:
            print(clr.Fore.RED + "Error: No package name specified")
            clr.Fore.RED
            sys.exit(1)
        else:
            package = sys.argv[2]
            #make sure the package name is valid
            if package.find(" ") != -1:
                print(clr.Fore.RED + "Error: package name cannot contain spaces")
                sys.exit(1)
            elif package.find(".") != -1:
                print(clr.Fore.RED + "Error: package name cannot contain periods")
                sys.exit(1)
            elif package.find("/") != -1:
                print(clr.Fore.RED + "Error: package name cannot contain slashes")
                sys.exit(1)
            elif package.find("\\") != -1:
                print(clr.Fore.RED + "Error: package name cannot contain backslashes")
                sys.exit(1)
            elif package.find("|") != -1:
                print(clr.Fore.RED + "Error: package name cannot contain pipes")
                sys.exit(1)
            elif package.find("`") != -1:
                print(clr.Fore.RED + "Error: package name cannot contain backticks")
                sys.exit(1)
            elif package.find("~") != -1:
                print(clr.Fore.RED + "Error: package name cannot contain tildes")
                sys.exit(1)
            elif package.find("!") != -1:
                print(clr.Fore.RED + "Error: package name cannot contain exclamation points")
                sys.exit(1)
            #check the repository of package repositories
            if not os.path.exists("~/.pyckaged-repositories.txt"):
                #download the repository file
                #we can use requests to download the file
                repotext = rq.get("https://raw.githubusercontent.com/lewolfyt/pyckaged/master/pyckaged-repositories.txt")
                #save it to the user's home directory
                open(homedir + "/.pyckaged-repositories.txt", "x")
                #write the text to the file
                with open(homedir + "/.pyckaged-repositories.txt", "w") as f:
                    f.write(repotext.text)
            repos = open(homedir + "/.pyckaged-repositories.txt", "r")
            #check if the package is in the repository
            for line in repos:
                if line.find(package) != -1:
                    #get the repository
                    #file format: package name | repository url
                
                    #get the repository url
                    repo = line.split("|")[1]
                    #get the package name
                    name = line.split("|")[0]

                    #check if the package is already installed
                    if os.path.exists(homedir + "/.pyckaged-installed.txt"):
                        #check if the package is already installed
                        installed = open(homedir + "/.pyckaged-installed.txt", "r")
                        for line in installed:
                            if line.find(name) != -1:
                                print("Error: package already installed")
                                sys.exit(1)
                        else:
                            #create the installed file
                            open(homedir + "/.pyckaged-installed.txt", "x")
                            #write the package name to the file
                            with open(homedir + "/.pyckaged-installed.txt", "a") as f:
                                f.write(name)
                    #install the package
                    os.system("cd ~/")
                    #if a package supports pyckaged it will have a pyckaged.py file
                    #clone the repository
                    os.system("git clone " + repo + " " + homedir + "/.pyckaged-cache/" + name)
                    os.system("cd " + homedir +"/.pyckaged-cache/" + name)
                    try:
                        os.system("python3 ./pyckagedseetup.py")
                    except:
                       os.system("python ./pyckagedsetup.py")
                    #add the package to the installed file
                    installed = open(homedir + "/.pyckaged-installed.txt", "a")
                    installed.write(name + "\n")
                    #print the package name
                    print(clr.Fore.LIGHTGREEN_EX + "Installed " + name + " successfully!")
                    #close the install file
                    installed.close()
                    #close the repositories file
                    repos.close()
                    #close the package file
                    sys.exit(0)
                else:
                    print(clr.Fore.RED + "Error: Package not found")
                    #close the repositories file
                    repos.close()
                    #close the package file
                    sys.exit(1)
    elif command == "pipinstall":
        try:
            package = sys.argv[2]
        except IndexError:
            print(clr.Fore.RED + "Error: No package name specified")
            sys.exit(1)
        try:
            os.system("pip install " + package)
        except:
            os.system("pip3 install " + package)
        else:
            print(clr.Fore.LIGHTGREEN_EX + "Installed " + package + " successfully!")
    elif command == "help":
        print(clr.Fore.LIGHTGREEN_EX + "Pyckage'd Help")
        print("Pyckage'd is a package manager made with python")
        print("Usage: pyckaged <command> <package>")
        print("Commands:")
        print("Install: Install a package")
        print("Pipinstall: Install a package using pip")
        print("Help: Show this help")
    else:
        print(clr.Fore.RED + "Error: Invalid command")
        sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0)