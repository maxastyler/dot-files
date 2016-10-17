import argparse

def install():
    pass

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
