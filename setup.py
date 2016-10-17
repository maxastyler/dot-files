#!/bin/python3
import argparse
import json
import os
import shutil
import sys

backup_folder=os.path.expanduser("~/.mtyler_dotfiles_backup")

class prog_files:
    def __init__(self, program, files, scripts):
        self.program=program
        self.files={}
        self.scripts={}
        self.files=files
        for thing in self.files:
            self.files[thing]=os.path.expanduser(self.files[thing])
        for thing in self.scripts:
            self.scripts[thing]=os.path.expanduser(self.scripts[thing])
        self.scripts=scripts
        """for thing in files:
            self.files[os.path.join(os.getcwd(), program, thing)]=os.path.expanduser(files[thing]) 
        for thing in scripts:
            self.scripts[os.path.join(os.getcwd(), program, thing)]=os.path.expanduser(scripts[thing])"""

    def print_files(self):
        for thing in self.files:
            print(thing, "->", self.files[thing])

    def write_files(self, backup=True):  
        if backup:
            if not os.path.exists(os.path.join(backup_folder, self.program)):
                os.makedirs(os.path.join(backup_folder, self.program))
        for thing in self.files:
            if os.path.exists(self.files[thing]):
                if backup:
                    if os.path.exists(os.path.join(backup_folder, self.program, thing)):
                        os.remove(os.path.join(backup_folder, self.program, thing))
                    shutil.move(self.files[thing], os.path.join(backup_folder, self.program, thing))
                else:
                    os.remove(self.files[thing])
            os.symlink(os.path.join(os.getcwd(), self.program, thing), self.files[thing])


def install():
    with open('locations.json') as data_file:
        data=json.load(data_file)
    prog_categories=[]
    for prog_type in data:
        prog_categories.append(prog_files(prog_type, data[prog_type]["files_to_link"], data[prog_type]["scripts_to_run"]))
    if os.path.exists(backup_folder):
        print("\n\nBackup directory detected at:", backup_folder, "\nIf you install, you'll overwrite any files here which may remove your original configs.")
        check=None
        while check!="y":
            check=input("Do you want to continue installing?[y/n]: ")
            if check=="n":
                sys.exit()
    print("Writing files...")
    for prog in prog_categories:
        prog.write_files(True)
    print("Done")

def uninstall():
    pass

def main():
    parser = argparse.ArgumentParser(description='Setup and remove script for my dotfiles')
    parser.add_argument("option", type=str, help='Tells this script what to do eg. install, uninstall')
    args=parser.parse_args()
    if args.option=='install':
        install()
    elif args.option=='uninstall':
        uninstall()
    else:
        parser.print_help()


if __name__=='__main__':
    #Change the current working directory, so all the files can be found
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    main()
