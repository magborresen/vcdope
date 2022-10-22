import re
import pandas as pd

class VCD():
    """
        Class used to parse a 4-state VCD file from
        the Verilog standard 1364 2005.
        A four state file can contain the following value changes:
        1, 0, x, z - No strength information is provided.
    """

    def __init__(self, filename):
        self.working_file = filename
        self.vcd_contents = {'header': {'scopes': {}}}
        self.vcd_dump_df = None
        self.keywords = ['comment', 'timescale', 'date', 'upscope',
                         'var', 'scope', 'version']
        self.var_keys = ['type', 'size', 'identifier', 'reference', 'index']
        self.delimiters = r'\s+|\$'

    def open_file(self):
        """
            Docstring
        """
        self.working_file = open(self.working_file, 'r', encoding='utf-8')

    def parse_header_info(self):
        """
            Parse the header section of a Verilog VCD file dump

            Args:
                None
            Returns:
                None
        """

        var_count = 0
        in_scope = False
        multi_line = []
        for line in self.working_file:
            if '$end' not in line:
                multi_line.append(line.strip())
                continue

            if len(multi_line) == 0 and line.strip() != '$end':
                split_line = line.strip().split(" ")[:-1]
            else:
                split_line = multi_line
            multi_line = [] 

            keyword = split_line[0].strip("$")
            if keyword == "enddefinitions":
                break

            if keyword == 'scope':
                var_count = 0
                in_scope = True
                scope = " ".join(split_line[1:])
                self.vcd_contents['header']['scopes'][scope] = {}
                continue

            if keyword == 'upscope':
                in_scope = False
                continue

            if in_scope:
                if keyword == 'var':
                    keyword_value = dict(zip(self.var_keys, split_line[1:]))
                    self.vcd_contents['header']['scopes'][scope][keyword + str(var_count)] = keyword_value
                    var_count += 1
                else:
                    self.vcd_contents['header']['scopes'][scope][keyword] = keyword_value
            else:
                keyword_value = " ".join(split_line[1:])
                self.vcd_contents['header'][keyword] = keyword_value

        self.vcd_dump_df = pd.DataFrame(self.vcd_contents['header']['scopes']['module shifter_mod']).T

    def parse_node_info(self):
        """
            Parse the node information section of the VCD file
        """
        return None

    def parse_value_changes(self):
        """
            Parse the value change section of the VCD file
        """
        return None



if __name__ == "__main__":
    parser = VCD("vcd_dump_advanced.vcd")
    parser.open_file()
    parser.parse_header_info()
    #print(parser.vcd_contents)
    print(parser.vcd_dump_df)