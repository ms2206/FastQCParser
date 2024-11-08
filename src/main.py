import argparse
from parser import handle_cli_args, extract_raw, parse_raw
from plotter import plot_adap_cont, plot_per_base_seq_qual, plot_per_tile_seq_qual, plot_per_seq_qual_scores, \
    plot_per_base_seq_content, plot_per_seq_GC_cont, plot_per_base_N_cont, plot_seq_len_dist
import os


def parse_arguments():
    # Initiate Parser
    parser = argparse.ArgumentParser(description='Parse and plot FASTQC data.')

    # Add Required Args
    parser.add_argument('input_file', type=str, help='Path to the FASTQ file.')
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

    return parser.parse_args()


def main():
    args = parse_arguments()

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
        parsed_data = parse_raw(raw_data)

        # make dir and then save files
        os.makedirs(f'../data/processed/{optional_arg.cli_argument}', exist_ok=True)
        parsed_data.to_csv(f'../data/processed/{optional_arg.cli_argument}/{optional_arg.cli_argument}.csv')

        if optional_arg.value:
            if optional_arg.cli_argument == 'per_base_seq_qual':
                plot_per_base_seq_qual(optional_arg.cli_argument)

            elif optional_arg.cli_argument == 'per_tile_seq_qual':
                plot_per_tile_seq_qual(optional_arg.cli_argument)

            elif optional_arg.cli_argument == 'per_seq_qual_scores':
                plot_per_seq_qual_scores(optional_arg.cli_argument)

            elif optional_arg.cli_argument == 'per_base_seq_content':
                plot_per_base_seq_content(optional_arg.cli_argument)

            elif optional_arg.cli_argument == 'per_seq_GC_cont':
                plot_per_seq_GC_cont(optional_arg.cli_argument)

            elif optional_arg.cli_argument == 'per_base_N_cont':
                plot_per_base_N_cont(optional_arg.cli_argument)

            elif optional_arg.cli_argument == 'seq_len_dist':
                plot_seq_len_dist(optional_arg.cli_argument)

            elif optional_arg.cli_argument == 'seq_dup':
                print(f'I dont have a function yet for {optional_arg.cli_argument}')
            elif optional_arg.cli_argument == 'over_seq':
                print(f'I dont have a function yet for {optional_arg.cli_argument}')
            elif optional_arg.cli_argument == 'adap_cont':
                plot_adap_cont(optional_arg.cli_argument)

            elif optional_arg.cli_argument == 'kmer_cont':
                print(f'I dont have a function yet for {optional_arg.cli_argument}')
            else:
                print(optional_arg)

if __name__ == '__main__':
    main()


