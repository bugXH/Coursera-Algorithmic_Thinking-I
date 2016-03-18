"""
Coursera Algorithmic Thinking Project4
Implementation of "Computing alignments of sequences"
"""


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Takes as input a set of characters alphabet and three scores diag_score,
    off_diag_score, and dash_score.
    The function returns a dictionary of dictionaries whose entries are
    indexed by pairs of characters in alphabet plus '-'.
    The score for any entry indexed by one or more dashes is dash_score.
    The score for the remaining diagonal entries is diag_score.
    Finally, the score for the remainingoff-diagonal entries is
    off_diag_score.

    Parameters
    ----------
    alphabet: set
    a set of characters

    diag_score: int
    the score for the remaining diagonal entries

    off_diag_score: int
    the score for the remaining off-diagonal entries

    dash_score: int
    the score for any entry indexed by one or more dashes


    Returns
    -------
    result: dict of dicts
    a dictionary of dictionaries whose entries are indexed by pairs of
    characters in alphabet plus '-'
    """
    alphas = ['-'] + list(alphabet)
    result = {alpha_i: {alpha_j: off_diag_score for alpha_j in alphas}
              for alpha_i in alphas}
    for idx in alphas:
        result[idx][idx] = diag_score
        result['-'][idx] = dash_score
        result[idx]['-'] = dash_score
    return result


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Takes as input two sequences seq_x and seq_y whose elements share
    a common alphabet with the scoring matrix scoring_matrix.
    The function computes and returns the alignment matrix for seq_x
    and seq_y as described in the Homework.
    If global_flag is True, each entry of the alignment matrix is
    computed using the method described in Question 8 of the Homework.
    If global_flag is False, each entry is computed using the method
    described in Question 12 of the Homework.

    Parameters
    ----------
    seq_x / seq_y: list
    two sequences seq_x and seq_y whose elements share
    a common alphabet with the scoring matrix scoring_matrix

    scoring_matrix: dict of dicts
    the scoring matrix

    global_flag: boolean
    If global_flag is True, each entry of the alignment matrix is
    computed using the method described in Question 8 of the Homework.
    If global_flag is False, each entry is computed using the method
    described in Question 12 of the Homework.


    Returns
    -------
    align_matrix: list of lists
    alignment matrix for seq_x and seq_y as described in the Homework
    """
    len_m, len_n = len(seq_x), len(seq_y)
    align_matrix = [[0 for _ in range(len_n + 1)] for _ in range(len_m + 1)]

    for idx_x in range(1, len_m + 1):
        align_matrix[idx_x][0] = align_matrix[idx_x - 1][0] +\
                                     scoring_matrix[seq_x[idx_x - 1]]['-']
        if global_flag is False:
            align_matrix[idx_x][0] = max(align_matrix[idx_x][0], 0)

    for idx_y in range(1, len_n + 1):
        align_matrix[0][idx_y] = align_matrix[0][idx_y - 1] +\
                                     scoring_matrix['-'][seq_y[idx_y - 1]]
        if global_flag is False:
            align_matrix[0][idx_y] = max(align_matrix[0][idx_y], 0)

    for idx_x in range(1, len_m + 1):
        for idx_y in range(1, len_n + 1):
            vert = align_matrix[idx_x - 1][idx_y] +\
                   scoring_matrix[seq_x[idx_x - 1]]['-']

            horiz = align_matrix[idx_x][idx_y - 1] +\
                scoring_matrix['-'][seq_y[idx_y - 1]]

            diag = align_matrix[idx_x - 1][idx_y - 1] +\
                scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]]

            align_matrix[idx_x][idx_y] = max(vert, horiz, diag)

            if global_flag is False:
                align_matrix[idx_x][idx_y] = max(align_matrix[idx_x][idx_y], 0)

    return align_matrix


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a
    common alphabet with the scoring matrix scoring_matrix.
    This function computes a global alignment of seq_x and seq_y using the
    global alignment matrix alignment_matrix.

    The function returns a tuple of the form (score, align_x, align_y)
    where score is the score of the global alignment align_x and align_y.
    Note that align_x and align_y should have the same length and may include
    the padding character '-'.

    Parameters
    ----------
    seq_x / seq_y: list
    two sequences seq_x and seq_y whose elements share
    a common alphabet with the scoring matrix scoring_matrix

    scoring_matrix: dict of dicts
    the scoring matrix

    align_matrix: list of lists
    alignment matrix for seq_x and seq_y as described in the Homework


    Returns
    -------
    a tuple of the form (score, align_x, align_y)
    score: int
    the score of the global alignment align_x and align_y.

    align_x / align_y:
    Note that align_x and align_y should have the same length and may include
    the padding character '-'.
    """
    idx_x, idx_y = len(seq_x), len(seq_y)
    score = alignment_matrix[idx_x][idx_y]

    align_x = ''
    align_y = ''

    while idx_x != 0 and idx_y != 0:
        current_score = alignment_matrix[idx_x][idx_y]
        if current_score == alignment_matrix[idx_x - 1][idx_y - 1] +\
                scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]]:
            align_x = seq_x[idx_x - 1] + align_x
            align_y = seq_y[idx_y - 1] + align_y

            idx_x -= 1
            idx_y -= 1

        elif current_score == alignment_matrix[idx_x - 1][idx_y] +\
                scoring_matrix[seq_x[idx_x - 1]]['-']:
            align_x = seq_x[idx_x - 1] + align_x
            align_y = '-' + align_y

            idx_x -= 1

        else:
            align_x = '-' + align_x
            align_y = seq_y[idx_y - 1] + align_y

            idx_y -= 1

    while idx_x != 0:
        align_x = seq_x[idx_x - 1] + align_x
        align_y = '-' + align_y
        idx_x -= 1

    while idx_y != 0:
        align_x = '-' + align_x
        align_y = seq_y[idx_y - 1] + align_y
        idx_y -= 1

    return (score, align_x, align_y)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a
    common alphabet with the scoring matrix scoring_matrix.
    This function computes a local alignment of seq_x and seq_y using
    the local alignment matrix alignment_matrix.
    The function returns a tuple of the form (score, align_x, align_y)
    where score is the score of the optimal local alignment align_x and
    align_y.
    Note that align_x and align_y should have the same length and may
    include the padding character '-'.

    Parameters
    ----------
    seq_x / seq_y: list
    two sequences seq_x and seq_y whose elements share
    a common alphabet with the scoring matrix scoring_matrix

    scoring_matrix: dict of dicts
    the scoring matrix

    align_matrix: list of lists
    alignment matrix for seq_x and seq_y as described in the Homework


    Returns
    -------
    a tuple of the form (score, align_x, align_y)
    score: int
    the score of the global alignment align_x and align_y.

    align_x / align_y:
    Note that align_x and align_y should have the same length and may include
    the padding character '-'.

    """
    scores = [-float('Inf'), 0, 0]

    for idx_x in range(len(alignment_matrix)):
        for idx_y in range(len(alignment_matrix[0])):
            if alignment_matrix[idx_x][idx_y] > scores[0]:
                scores = [alignment_matrix[idx_x][idx_y], idx_x, idx_y]

    score, idx_x, idx_y = scores
    align_x = ''
    align_y = ''

    while idx_x != 0 and idx_y != 0:
        current_score = alignment_matrix[idx_x][idx_y]

        if current_score <= 0:
            break

        if current_score == alignment_matrix[idx_x-1][idx_y-1] +\
                scoring_matrix[seq_x[idx_x-1]][seq_y[idx_y-1]]:
            align_x = seq_x[idx_x-1] + align_x
            align_y = seq_y[idx_y-1] + align_y
            idx_x -= 1
            idx_y -= 1

        elif current_score == alignment_matrix[idx_x-1][idx_y] +\
                scoring_matrix[seq_x[idx_x-1]]['-']:
            align_x = seq_x[idx_x-1] + align_x
            align_y = '-' + align_y
            idx_x -= 1

        else:
            align_x = '-' + align_x
            align_y = seq_y[idx_y-1] + align_y
            idx_y -= 1
    return (score, align_x, align_y)

if __name__ == '__main__':
    score = build_scoring_matrix(['A','C','T','G'], 10, 4, -6)
    S = compute_alignment_matrix('AA', 'TAAT', score, False)
    print S[2][3]
    print compute_local_alignment('AA', 'TAAT', score, S)