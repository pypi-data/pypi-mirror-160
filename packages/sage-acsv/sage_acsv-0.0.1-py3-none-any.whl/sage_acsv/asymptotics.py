"""Functions for determining asymptotics of the coefficients
of multivariate rational functions.
"""

# just a test import and function to see that
# everything integrates correctly with SageMath

from sage.rings.asymptotic.asymptotic_expansion_generators import asymptotic_expansions
from sage.rings.integer_ring import ZZ

def binomial_kn_choose_n_asy(k):
    r"""Asymptotics of the binomial coefficient 2n choose n.

    INPUT:

    * ``k`` -- the factor k in ``binomial(k*n, n)``

    OUTPUT:

    An asymptotic expansion.

    Examples::

        >>> from sage_acsv import binomial_kn_choose_n_asy
        >>> binomial_kn_choose_n_asy(2)
        1/sqrt(pi)*4^n*n^(-1/2) + O(4^n*n^(-3/2))
        >>> binomial_kn_choose_n_asy(7)
        1/2*sqrt(7/3)/sqrt(pi)*(823543/46656)^n*n^(-1/2) + O((823543/46656)^n*n^(-3/2))
    """
    return asymptotic_expansions.Binomial_kn_over_n('n', ZZ(k), precision=2)
