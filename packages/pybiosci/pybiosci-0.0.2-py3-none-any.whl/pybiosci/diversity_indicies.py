from .__diversity_indices.aindex import __alpha_index
from .__diversity_indices.bindex import __beta_index


def alpha_index(df, index='Shannon', q=None, keep=False):
    return __alpha_index(df, index, q, keep)


def beta_index(df, index='w'):
    return __beta_index(df, index)
