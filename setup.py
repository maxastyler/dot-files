#!/bin/python3
import argparse
import json
import os
import shutil
import sys

backup_folder=os.path.expanduser("~/.mtyler_dotfiles_backup")

def load_json(file_name):
    with open(file_name) as data_file:
        data=json.load(data_file)
    prog_categories=[]
    for prog_type in data:
        prog_categories.append(prog_files(prog_type, data[prog_type]["files_to_link"], data[prog_type]["scripts_to_run"]))
    return prog_categories


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
            else:
                try:
                    os.makedirs(os.path.dirname(self.files[thing]))
                except: 
                    pass
            os.symlink(os.path.join(os.getcwd(), self.program, thing), self.files[thing])

    def delete_files(self):
        for thing in self.files:
            if os.path.exists(self.files[thing]):
                os.remove(self.files[thing])

    def restore_backup(self):
        for thing in self.files:
            if os.path.exists(os.path.join(backup_folder, self.program, thing)):
                if os.path.exists(self.files[thing]):
                    os.remove(self.files[thing])
                shutil.move(os.path.join(backup_folder, self.program, thing), self.files[thing])


def install():
    if os.path.exists(backup_folder):
        print("\n\nBackup directory detected at:", backup_folder, "\nIf you install, you'll overwrite any files here which may remove your original configs.")
        check=None
        while check!="y":
            check=input("Do you want to continue installing?[y/n]: ")
            if check=="n":
                sys.exit()
    prog_categories=load_json('locations.json')
    print("Writing files...")
    for prog in prog_categories:
        prog.write_files(True)
    print("Done")

def uninstall():
    prog_categories=load_json('locations.json')
    print("\n\nIf you choose to uninstall without having any backup files\nThis will delete your current config files. These may be your own carefully crafted ones!")
    check=None
    while check!="y":
        check=input("Are you sure you want to uninstall?[y/n]: ")
        if check=='n':
            sys.exit()
    print("Deleting files")
    for prog in prog_categories:
        prog.delete_files()
    print("Restoring backup")
    for prog in prog_categories:
        prog.restore_backup()
    if os.path.exists(backup_folder):
        shutil.rmtree(backup_folder)
    print("Done")

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
