import re

class VCD():
    def __init__(self):
        self.working_file = None
        self.vcd_contents = {'header': {'scopes': {}}}
        self.keywords = ['comment', 'timescale', 'date', 'upscope',
                         'var', 'scope', 'version']
        self.var_keys = ['type', 'size', 'identifier', 'reference']
        self.delimiters = r'\s+|\$'

    def open_file(self, filename):
        """
            Docstring
        """
        self.working_file = open(filename, 'r', encoding='utf-8')

    def parse_header_section(self):
        """
            Parse the header section of a Verilog VCD file dump

            Args:
                None
            Returns:
                None
        """

        var_count = 0
        in_scope = False
        while True:
            cur_line = self.working_file.readline().strip()
            split_line = list(filter(None, re.split(self.delimiters, cur_line)))
            #Check if the line only contains the keyword
            if len(split_line) == 1 and split_line[0] in self.keywords:
                keyword = split_line[0]
                # Go to the next line to get the associated keyword value
                cur_line = self.working_file.readline().strip()
                keyword_value = cur_line
            # Check if the line contains both keyword and data
            elif len(split_line) > 1 and split_line[0] in self.keywords:
                keyword = split_line[0]
                end_line = split_line.index('end')
                # If the keyword is a variable, we need to extract more data
                if keyword == 'var':
                    # Create a new dict to store the 4 pieces of var data
                    keyword_value = dict(zip(self.var_keys, split_line[1:end_line]))
                else:
                    keyword_value = ' '.join(split_line[1:end_line])
            # Stop the loop if we run out of header section
            elif split_line[0] == "enddefinitions":
                break

            # If multiple scopes are included in the file, save the variables
            # under each scope.
            if keyword == 'scope':
                in_scope = True
                scope = keyword_value
                self.vcd_contents['header']['scopes'][scope] = {}
                continue

            if keyword == 'upscope':
                in_scope = False
                continue

            # Make sure we can save several variables as the keyword is always the same
            if in_scope:
                if keyword == 'var':
                    self.vcd_contents['header']['scopes'][scope][keyword + str(var_count)] = keyword_value
                    var_count += 1
                else:
                    self.vcd_contents['header']['scopes'][scope][keyword] = keyword_value
            else:
                if keyword == 'var':
                    self.vcd_contents['header'][keyword + str(var_count)] = keyword_value
                    var_count += 1
                else:
                    self.vcd_contents['header'][keyword] = keyword_value

    def parse_variable_section(self):
        """
            Docstring
        """
        return None

    def parse_dumpvars_section(self):
        """
            Docstring
        """
        return None

    def parse_value_change_section(self):
        """
            Docstring
        """
        return None



if __name__ == "__main__":
    parser = VCD()
    parser.open_file("vcd_dump.vcd")
    parser.parse_header_section()
    print(parser.vcd_contents)