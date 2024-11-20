import argparse
from parser import handle_cli_args, extract_raw, parse_raw
from plotter import plot_adap_cont, plot_per_base_seq_qual, plot_per_tile_seq_qual, plot_per_seq_qual_scores, \
    plot_per_base_seq_content, plot_per_seq_GC_cont, plot_per_base_N_cont, plot_seq_len_dist, plot_seq_dup, \
    plot_kmer_cont
import os
from tabulate import tabulate
from pyfiglet import figlet_format
import emoji
from utils import qotd_call
import sys


def parse_arguments():
    # Initiate Parser
    parser = argparse.ArgumentParser(description='Parse and plot FASTQC data.')

    # Add Required Args
    parser.add_argument('input_file', type=str, help='Path to the FASTQC file.')
    parser.add_argument('output_dir', type=str, help='Directory to save plots.')

    # Add Optional Args
    parser.add_argument('-b', '--per_base_seq_qual', action='store_true', help='Extract and plot per base sequence '
                                                                               'quality.')
    parser.add_argument('-t', '--per_tile_seq_qual', action='store_true', help='Extract and plot per tile sequence '
                                                                               'quality.')
    parser.add_argument('-s', '--per_seq_qual_scores', action='store_true', help='Extract and plot per sequence '
                                                                                 'quality scores')
    parser.add_argument('-c', '--per_base_seq_content', action='store_true', help='Extract and plot per base sequence '
                                                                                  'content')
    parser.add_argument('-g', '--per_seq_GC_cont', action='store_true', help='Extract and plot per sequence GC content')
    parser.add_argument('-n', '--per_base_N_cont', action='store_true', help='Extract and plot per base N content')
    parser.add_argument('-l', '--seq_len_dist', action='store_true', help='Extract sequence length distribution')
    parser.add_argument('-d', '--seq_dup', action='store_true', help='Extract and plot sequence duplication levels')
    parser.add_argument('-o', '--over_seq', action='store_true', help='Extract overrepresented sequences')
    parser.add_argument('-p', '--adap_cont', action='store_true', help='Extract and plot adapter content')
    parser.add_argument('-k', '--kmer_cont', action='store_true', help='Extract and plot K-mer Content')
    parser.add_argument('-a', '--all', action='store_true', help='Extract and plot all metrics')

    args = parser.parse_args()

    return args


def main():
    # Parse Args
    args = parse_arguments()

    # Extract Basic Statistics
    try:
        basic_stats_raw = extract_raw(args.input_file, 'Basic Statistics')
        formatted_df = parse_raw(basic_stats_raw)
    except UnicodeDecodeError as e:
        print(f'Check file format\n{e}')
        exit(1)

    ## CLI Output and Welcome Page

    # ASCII Art Title
    title = figlet_format('FastQC Parser', font='slant')
    print(title)

    # Author and Project Information
    print('Author: Matthew Spriggs')
    print('GitHub: https://github.com/ms2206/FastQCParser.git')
    print('See technical documentation: https://ms2206.github.io/FastQCParser/')
    print('Email: matthew.spriggs.452@cranfield.ac.uk')
    print('Version: 1.0.0')
    print(emoji.emojize('Donations Welcome :red_heart:'))
    print('____________________________________________________________________________________\n')

    # Divider
    print('#' * 84)
    print()
    print('BASIC STATISTICS')
    print(tabulate(formatted_df, headers=[], tablefmt='grid'))
    print()
    print('#' * 84)
    print(f'INPUT FILE USED: {args.input_file}')
    print(f'OUTPUT DIRECTORY USED: /FastQCParser/data/processed/{args.output_dir}/')
    print('__\n')
    print(emoji.emojize('Loading Reports ... :thinking_face:'))
    print()

    # returns a list of configured ParsedArg objects
    optional_args = handle_cli_args(args)

    for optional_arg in optional_args:
        if optional_arg.cli_argument == 'all':
            # recreate optional_args with all options as True
            optional_args = argparse.Namespace(input_file=args.input_file, output_dir=args.output_dir,
                                               per_base_seq_qual=True,
                                               per_tile_seq_qual=True, per_seq_qual_scores=True,
                                               per_base_seq_content=True,
                                               per_seq_GC_cont=True, per_base_N_cont=True, seq_len_dist=True,
                                               seq_dup=True,
                                               over_seq=True, adap_cont=True, kmer_cont=True)

            optional_args = handle_cli_args(optional_args)

    for optional_arg in optional_args:
        # extract raw lines from fastqc
        raw_data = extract_raw(args.input_file, optional_arg.search_string)

        # parse into df
        parsed_data = parse_raw(raw_data.iloc[1:])

        # make dir and then save files

        #TODO: make the output dir the users Downloads folder
        os.makedirs(f'data/processed/{args.output_dir}/{optional_arg.cli_argument}', exist_ok=True)
        parsed_data.to_csv(
            f'data/processed/{args.output_dir}/{optional_arg.cli_argument}/{optional_arg.cli_argument}_report.csv')

        # flag
        # first row of the raw_data, tab split
        flag = raw_data.iloc[0].apply(lambda x: x.split('\t')).tolist()[0][1]
        with open(f'data/processed/{args.output_dir}/{optional_arg.cli_argument}/flag.txt', 'w') as file:
            file.write(flag.upper())

        if optional_arg.value:
            if 'P' in optional_arg.required_outputs:
                if optional_arg.cli_argument == 'per_base_seq_qual':
                    plot_per_base_seq_qual(optional_arg.cli_argument, args.output_dir)

                elif optional_arg.cli_argument == 'per_tile_seq_qual':
                    plot_per_tile_seq_qual(optional_arg.cli_argument, args.output_dir)

                elif optional_arg.cli_argument == 'per_seq_qual_scores':
                    plot_per_seq_qual_scores(optional_arg.cli_argument, args.output_dir)

                elif optional_arg.cli_argument == 'per_base_seq_content':
                    plot_per_base_seq_content(optional_arg.cli_argument, args.output_dir)

                elif optional_arg.cli_argument == 'per_seq_GC_cont':
                    plot_per_seq_GC_cont(optional_arg.cli_argument, args.output_dir)

                elif optional_arg.cli_argument == 'per_base_N_cont':
                    plot_per_base_N_cont(optional_arg.cli_argument, args.output_dir)

                elif optional_arg.cli_argument == 'seq_len_dist':
                    ## NO PLT CURRENTLY REQUIRED ##
                    plot_seq_len_dist(optional_arg.cli_argument, args.output_dir)

                elif optional_arg.cli_argument == 'seq_dup':
                    plot_seq_dup(optional_arg.cli_argument, args.output_dir)

                elif optional_arg.cli_argument == 'over_seq':
                    ## NO PLT CURRENTLY REQUIRED ##
                    continue

                elif optional_arg.cli_argument == 'adap_cont':
                    plot_adap_cont(optional_arg.cli_argument, args.output_dir)

                elif optional_arg.cli_argument == 'kmer_cont':
                    plot_kmer_cont(optional_arg.cli_argument, args.output_dir)

                else:
                    print(optional_arg)

    print(emoji.emojize('... Complete! :smiling_face_with_sunglasses:'))
    print(qotd_call())


if __name__ == '__main__':
    main()
