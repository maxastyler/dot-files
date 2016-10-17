#!/bin/python3
import argparse
import json
import os

class prog_files:
    def __init__(self, program, files, scripts):
        self.program=program
        self.files=files
        self.scripts=scripts

    def print_files(self):
        for thing in self.files:
            print(thing)

    def write_files(self, backup=True):
        

backup_folder="~/.mtyler_dot_backup"

def install():
    with open('locations.json') as data_file:
        data=json.load(data_file)
    prog_categories=[]
    for prog_type in data:
        prog_categories.append(prog_files(prog_type, data[prog_type]["files_to_link"], data[prog_type]["scripts_to_run"]))
    for i in prog_categories:
        i.print_files()

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
    main()
