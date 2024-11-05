class ParsedArg(dict):

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
                        ('kmer_cont', 'K-mer Content'),
                        ('all', 'All the above')
                        ])

    def __init__(self, cli_argument: str, value: str):
        self.cli_argument = cli_argument
        self.value = value
        self.required_outputs: list = ['R', 'P', 'F']
        self.search_string = self.arg_key_map.get(self.cli_argument)


    def configure_outputs(self):
        if self.cli_argument in ['seq_len_dist', 'over_seq']:
            self.required_outputs.remove('P')
        return self.required_outputs

    def __repr__(self):
        return (f'ParsedArg(cli_argument={self.cli_argument!r}, '
                f'value={self.value!r}, '
                f'required_outputs={self.required_outputs!r}, '
                f'search_string={self.search_string!r})')