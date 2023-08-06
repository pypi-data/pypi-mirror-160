import argparse
import sys

import numpy as np
import pandas as pd

from tedana_regressors import __version__
from tedana_regressors.utils import df_to_matrix


def _get_parser():
    """
    Parse command line inputs for this function.

    Returns
    -------
    parser.parse_args() : argparse dict

    Notes
    -----
    # Argument parser follow template provided by RalphyZ.
    # https://stackoverflow.com/a/43456577
    """
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    required = parser.add_argument_group("Required Arguments:")

    # Required arguments
    required.add_argument("-ctab", "--ctab", help="Component table", required=True, dest="ctab")
    required.add_argument("-mix", "--mix", help="Mixing matrix", required=True, dest="mix")
    required.add_argument(
        "-prefix", "--prefix", help="Prefix of output file", required=True, dest="prefix"
    )
    optional.add_argument("-v", "--version", action="version", version=("%(prog)s " + __version__))

    parser._action_groups.append(optional)

    return parser


def tedana_regressors(ctab, mix, prefix):

    # Load component table and mixing matrix into pandas dataframes
    print("Loading component table and mixing matrix...")
    ctab_df = pd.read_csv(ctab, sep="\t", index_col=0)
    mix_df = pd.read_csv(mix, sep="\t", index_col=None)

    # Extract the indices of the components that have "accepted" in the "classification" column of
    # ctab_df
    print("Extracting and saving accepted components...")
    accepted_components = ctab_df.loc[ctab_df["classification"] == "accepted"].index

    # Create matrix with the columns of the mixing matrix corresponding to keys in
    # accepted_components and save it
    np.savetxt(prefix + "_accepted.1D", df_to_matrix(mix_df, accepted_components), delimiter=" ")

    # Extract the indices of the components that have "rejected" in the "classification" column of
    # ctab_df
    print("Extracting and saving rejected components...")
    rejected_components = ctab_df.loc[ctab_df["classification"] == "rejected"].index

    # Create matrix with the columns of the mixing matrix corresponding to keys in
    # rejected_components and save it
    np.savetxt(prefix + "_rejected.1D", df_to_matrix(mix_df, rejected_components), delimiter=" ")

    # Extract the indices of the components that have "ignored" in the "classification" column of
    # ctab_df
    print("Extracting and saving ignored components...")
    ignored_components = ctab_df.loc[ctab_df["classification"] == "ignored"].index

    # Create matrix with the columns of the mixing matrix corresponding to keys in
    # ignored_components and save it
    np.savetxt(prefix + "_ignored.1D", df_to_matrix(mix_df, ignored_components), delimiter=" ")

    print("Done.")


def _main(argv=None):
    options = _get_parser().parse_args(argv)
    tedana_regressors(**vars(options))


if __name__ == "__main__":
    _main(sys.argv[1:])
