import pytest
import argparse
from src.class_defenitions import ParsedArg
from src.parser import handle_cli_args


def test_handle_cli_args():
    args = argparse.Namespace(input_file='input_file', output_dir='outputdir', per_base_seq_qual=False,
                              per_tile_seq_qual=False, per_seq_qual_scores=False, per_base_seq_content=False,
                              per_seq_GC_cont=False, per_base_N_cont=False, seq_len_dist=True, seq_dup=True,
                              over_seq=True, adap_cont=False, kmer_cont=False, all=False)

    result = handle_cli_args(args)

    expected_result = [
        ParsedArg(cli_argument='seq_len_dist', value=True),
        ParsedArg(cli_argument='seq_dup', value=True),
        ParsedArg(cli_argument='over_seq', value=True)
    ]

    assert result == expected_result
