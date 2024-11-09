class ParsedArg(dict):
    """
    A class to represent parsed command-line arguments for sequence quality analysis.

    This class maps command-line arguments to their corresponding search string and manages
     the required output types based on the argument.

    Attributes:
        cli_argument (str): The command-line argument provided by the user.
        value (bool): The bool command-line argument from 'store_true'
        required_outputs (list): A list of required output types, defaulting to ['R', 'P', 'F'].
        search_string (str): Search string to extract from FASTQC - retrieved from the arg_key_map.

    Class Attributes:
        arg_key_map (dict): A mapping of command-line argument keys to their descriptions.

    Methods:
        configure_outputs(): Adjusts the required outputs based on the command-line argument.
                             If the argument is 'seq_len_dist' or 'over_seq', 'P' is removed
                             from the required outputs.

    Example:
        >>> parsed_arg = ParsedArg('per_base_seq_qual', 'some_value')
        >>> parsed_arg.configure_outputs()
        ['R', 'P', 'F']
    """

    arg_key_map = dict([('per_base_seq_qual', 'Per base sequence quality'),
                        ('per_tile_seq_qual', 'Per tile sequence quality'),
                        ('per_seq_qual_scores', 'Per sequence quality scores'),
                        ('per_base_seq_content', 'Per base sequence content'),
                        ('per_seq_GC_cont', 'Per sequence GC content'),
                        ('per_base_N_cont', 'Per base N content'),
                        ('seq_len_dist', 'Sequence Length Distribution'),
                        ('seq_dup', 'Sequence Duplication Levels'),
                        ('over_seq', 'Overrepresented sequences'),
                        ('adap_cont', 'Adapter Content'),
                        ('kmer_cont', 'Kmer Content')
                        ])

    def __init__(self, cli_argument: str, value: str):
        self.cli_argument = cli_argument
        self.value = value
        self.required_outputs: list = ['R', 'P', 'F']
        self.search_string = self.arg_key_map.get(self.cli_argument)


    def configure_outputs(self):
        """
        Removes 'P' from ['seq_len_dist', 'over_seq']
        :return:
        """
        if self.cli_argument in ['seq_len_dist', 'over_seq']: # Could be made CONSTANT.
            self.required_outputs.remove('P')
        return self.required_outputs

    def __repr__(self):
        return (f'ParsedArg(cli_argument={self.cli_argument!r}, '
                f'value={self.value!r}, '
                f'required_outputs={self.required_outputs!r}, '
                f'search_string={self.search_string!r})')