import argparse
from parser import handle_cli_args


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

    #TODO: make a function that will take in a ParsedArg and also args.input and args.output and return the data from the FastQC

    print(optional_args[0])
    #data = extract_from_arg(optional_args[0])



if __name__ == '__main__':
    main()
