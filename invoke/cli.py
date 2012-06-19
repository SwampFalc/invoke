import sys

from .loader import Loader
from .parser import Parser, Context, Argument


def parse(argv):
    # Initial/core parsing (core options can affect the rest of the parsing)
    initial_context = Context(args=(
        # TODO: make collection a list-building arg, not a string
        Argument(names=('collection', 'c')),
        Argument(names=('root', 'r'))
    ))
    # 'core' will result an .unparsed attribute with what was left over.
    core = Parser(initial=initial_context, ignore_unknown=True).parse_argv(argv)
    args = core[0].args

    # Load collection (default or specified) and parse leftovers
    collection = Loader(root=args.root.value).load_collection(args.collection.value)
    tasks = Parser(contexts=collection.to_contexts()).parse_argv(core.unparsed)

    # Now we can take action based on 'core' options and the 'tasks' found
    for context in tasks:
        print context


def main():
    parse(sys.argv[1:])
