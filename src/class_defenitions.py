class ParsedArg(dict):

    def __init__(self, cli_argument: str, value: str):
        self.cli_argument = cli_argument
        self.value = value
        self.required_outputs: list = ['R', 'P', 'F']

    def configure_outputs(self):
        if self.cli_argument in ['seq_len_dist', 'over_seq']:
            self.required_outputs.remove('P')
        return self.required_outputs

    def __repr__(self):
        return (f'ParsedArg(cli_argument={self.cli_argument!r}, '
                f'value={self.value!r}, '
                f'required_outputs={self.required_outputs!r})')