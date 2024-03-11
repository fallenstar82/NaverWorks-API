import argparse


parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('-parent', type=int)
parent_args = parent_parser.parse_known_args()

foo_parser = argparse.ArgumentParser(parents=[parent_parser], add_help=True)
foo_parser.add_argument('-foo', type=str)

args=foo_parser.parse_args()
# print(parent_args)
print(args)