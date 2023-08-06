import argparse
import sys

from main import Sherlockeys
import lib.utils.const


def main():
    try:
        parser = argparse.ArgumentParser(description=f'{lib.utils.const.__header__}',
                                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                         epilog='Sherlockeys currently supports the following applications:'
                                                '\n Gitlab Personal Token'
                                                '\n Github Personal Token'
                                                '\n Heroku Api Key',
                                         add_help=False)
        parser.add_argument('key', help='key to be tested')
        parser.add_argument('-c', metavar='<id>', help='additional key to act as a client/app identifier')
        parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')
        parser.add_argument('-v', '--version', action='version', version=f'sherlockeys {lib.utils.const.__version__}')
        parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                            help='Show this help message and exit.')

        args = parser.parse_args()

        sherlockeys = Sherlockeys(args)
        sherlockeys.run()

    except KeyboardInterrupt:
        print()
        sys.exit(0)


if __name__ == "__main__":
    main()
