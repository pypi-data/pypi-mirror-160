import argparse

from .version import __version__
from .b64to16 import Base64to16Converter


if __name__ == '__main__':
    about = 'Converts data in Base64 to Hexadecimal'
    parser = argparse.ArgumentParser(
        prog='b64to16', description=about)
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=__version__)
    parser.add_argument(
        'json_file',
        type=str,
        help='path to a JSON file')
    parser.add_argument(
        '-x',
        action='store_true',
        help="do not prefix hexadecimal strings with '0x'")
    parser.add_argument(
        '-k',
        action='store_true',
        help=("convert dictionary keys to hexadecimal strings too" +
              " (might cause conflicts)"))
    args = parser.parse_args()
    cvt = Base64to16Converter(
        hexprefix=(not args.x),
        cvtkeys=args.k,
    )
    json_data = cvt.convert_json(args.json_file)
    print(json_data)
