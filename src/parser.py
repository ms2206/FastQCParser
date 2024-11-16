from argparse import Namespace
from typing import List
from class_definitions import ParsedArg
import pandas as pd
from pandas import DataFrame
import sys


def handle_cli_args(args: Namespace) -> list[ParsedArg]:
    """
    This function further parses args from the ArgParse command line input. It unpacks all args with store_true. Then
    initiates and configures an instance of Class::ParsedArg for each optional arg that was supplied by the user.

    :param args: cli arguments passed from user :return: a list of ParsedArg objects that have been configured to
    have their "Required outputs" adjusted based on expected output property.
    """

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


def extract_raw(filepath: str, search_string: str) -> DataFrame:
    """
    Extracts a section of a CSV file based on a search string and returns it as a DataFrame.

    This function reads a CSV file into a DataFrame, searches for a specified string within the 'raw' column,
    and extracts rows from the first occurrence of the search string to the corresponding 'END_MODULE' marker.
    The function uses a predefined mapping to determine the correct 'END_MODULE' for each search string.

    Parameters:
    filepath (str): The path to the CSV file to be read.
    search_string (str): The string to search for within the 'raw' column of the DataFrame.

    Returns:
    DataFrame: A DataFrame containing the rows from the first occurrence of the search string to the corresponding 'END_MODULE'.

    Raises:
    FileNotFoundError: If the specified file does not exist, the function prints an error message and exits the program.

    Example:
    >>> extract_raw('path/to/your/file.csv', 'Basic Statistics')
    """

    fastq_order_map = dict([
        ('Basic Statistics', 0),
        ('Per base sequence quality', 1),
        ('Per tile sequence quality', 2),
        ('Per sequence quality scores', 3),
        ('Per base sequence content', 4),
        ('Per sequence GC content', 5),
        ('Per base N content', 6),
        ('Sequence Length Distribution', 7),
        ('Sequence Duplication Levels', 8),
        ('Overrepresented sequences', 9),
        ('Adapter Content', 10),
        ('Kmer Content', 11),
        ('All the above', 11) # if all return from last END_MODULE
    ])

    try:
        df = pd.read_csv(filepath, names=['raw'])
    except FileNotFoundError as e:
        print(f'\033[91mWarning!\033[0m The file: \'{filepath}\' has vanished into hyperspace. Double-check your coordinates and try again:\n{e}')
        sys.exit(1)



    index_start = df[df['raw'].str.contains(search_string)].index.tolist()
    index_ends = df[df['raw'].str.contains('END_MODULE')].index.tolist()

    # from search_string TO first END_MODULE
    try:
        raw_df = df.iloc[index_start[0]:index_ends[fastq_order_map[search_string]]]
    except IndexError as e:
        if search_string == 'All the above':
            raw_df = df
        else:
            print(f'\033[91mError!\033[0m {search_string} could not be found within {filepath}: {e}')
            print('Please check file is of expected format, the input file should be FASTQC')
            exit(1)

    return raw_df


def parse_raw(raw_data: DataFrame) -> DataFrame:
    """
    Parses raw data from extract_raw().

    This function further processes a DataFrame from extract_raw().
    It gathers all lines that do not start with '#' and splits on tab characters. These are the values from the FASTQC
    file. It also extracts the headers as lines that start with '#' and uses these two lists to return a pandas DataFrame.

    Parameters:
    raw_data (DataFrame): The output from extract_raw()

    Returns:
    DataFrame: A formatted DataFrame with the extracted values and headers.

    Example:
    >>> raw_data = extract_raw('data/raw/fastqc_data1.txt', 'Sequence Duplication Levels')
    >>> formatted_df = parse_raw(raw_data)
    >>> print(formatted_df)
    """

    # make sure incoming object is DataFrame
    df_raw = pd.DataFrame(raw_data)

    # extract lines NOT '#'
    values_raw = df_raw[~df_raw['raw'].str.startswith('#')]
    # convert to list by splitting on '\t'
    values_list = values_raw['raw'].apply(lambda x: x.split('\t'))
    values_list = values_list.tolist()

    # extract line '#
    headers_raw = df_raw[df_raw['raw'].str.startswith('#')]
    headers_list = headers_raw['raw'].apply(lambda x: x.split('\t'))  # sometimes len > 1
    if len(headers_list) > 1:
        headers_list = headers_list.tolist()[-1]  # headers
        # misc_out = headers_list.tolist()[0]                             # misc
        #TODO: handle this case
    else:
        headers_list = headers_list.tolist()

    formatted_df = pd.DataFrame(values_list, columns=headers_list)

    return formatted_df
