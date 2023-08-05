import json
import base64
import binascii


class Base64to16Converter:
    """Base64 to Hexadecimal converter
    """

    def __init__(self, hexprefix=True, cvtkeys=False):
        """Initialize the converter

        Arguments:
            hexprefix - prefix hexadecimal strings with '0x'
            cvtkeys - convert dictionary keys to hex. strings
                      (might cause key conflicts)
        """
        self.hexprefix = hexprefix
        self.cvtkeys = cvtkeys

    def convert_string(self, string):
        """Converts a string from Base64 to Hexadecimal
        If data is not well formatted, it raises a binascii.Error

        Arguments:
            string - a string in base64 format

        Returns:
            the hexadecimal equivalent of data
        """
        hexstring = base64.b64decode(string).hex()
        if self.hexprefix:
            return '0x' + hexstring
        else:
            return hexstring

    def convert_data(self, data):
        """Traverses a data object decoded from a JSON file and converts all
        string values in Base64 format into hexadecimal strings.
        Assumes that all objects reachable from data are of either
        one of the following types: dict, list, str, int, float, bool, None
        (as assumed by the conversion table of json.JSONDecoder).
        Also assumes there are no self-references, which would cause
        infinite loops. Dictionary keys are not transformed by default
        because they could cause key conflicts in the transformed object.

        Arguments:
            data - data object to be traversed

        Returns:
            transformed object
        """
        if isinstance(data, dict):
            if self.cvtkeys:
                return {
                    self.convert_data(k): self.convert_data(v)
                    for k, v in data.items()
                }
            else:
                return {
                    k: self.convert_data(v)
                    for k, v in data.items()
                }
        elif isinstance(data, list):
            return [
                self.convert_data(v)
                for v in data
            ]
        elif isinstance(data, str):
            try:
                return self.convert_string(data)
            except binascii.Error:
                return data
        else:
            return data

    def convert_json(self, json_file):
        """Processes a JSON file, converting all string values in Base64 format
        into hexadecimal strings. Assumes file is in JSON format.
        If not, raises a json.JSONDecodeError.

        Arguments:
            json_file - path to the JSON file

        Returns:
            transformed JSON string
        """
        with open(json_file) as fp:
            json_data = json.load(fp)
            data = self.convert_data(json_data)
            return json.dumps(data)
