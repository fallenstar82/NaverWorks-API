import argparse

parser = argparse.ArgumentParser(add_help=False)
group = parser.add_mutually_exclusive_group()
group.add_argument("-a", help="add file", action="store_true")
group.add_argument("-b",help="hoho", action="store_true")

parser2 = argparse.ArgumentParser(parents = [parser])
parser2.add_argument("--q","--quit-prog", help="my parents is parser")

parser3 = argparse.ArgumentParser(parents = [parser])
parser3.add_argument("--q","--shutup")

args=parser.parse_args()
sub2 = parser2.parse_args()
sub3 = parser3.parse_args()
print(args)

if args.a :
    
    print(sub2)

if args.b :
    
    print(sub3)