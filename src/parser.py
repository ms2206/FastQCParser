from argparse import Namespace
from typing import List
from class_defenitions import ParsedArg


def handle_cli_args(args: Namespace) -> list[ParsedArg]:
    '''
    :param args: cli arguments passed from user
    :return: a list of ParsedArg objects that have been configured to have their "Required outputs"
    adjusted based on expected output property.
    '''

    # unpack args and create dict of all True items (optional args only)
    args_dict = {k: v for k, v in vars(args).items() if v == True}

    # initiate list to hold ParsedArg
    list_of_class_args = list()

    # initiate ParsedArg Class objects
    for k, v in args_dict.items():
        list_of_class_args.append(ParsedArg(k, v))

    # changes in-place the required_outputs from class ParsedArg
    [a.configure_outputs() for a in list_of_class_args]

    return list_of_class_args

def extract_from_arg(input_file: str, optional_arg: ParsedArg):
    '''
    :param
    input_file: filepath for input FASTQC
    optional_arg: An object of ParsedArg class e.g. ParsedArg(cli_argument='per_base_seq_qual', value=True, required_outputs=['R', 'P', 'F'])
    :return:
    '''

