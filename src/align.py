#!/usr/bin/env python

'''
This module is used to align sequences. Currently, there is only a single
alignment algorithm implementented; it is a hybrid between Needleman-Wunsch
and Smith-Waterman and is used to find the subsequence within a larger sequence
that best aligns to a reference.
'''

from biotools.blosum62 import blosum62
from biotools.translate import translate
import biotools.analysis.options as options

DIAG_MARK, VGAP_MARK, HGAP_MARK = 3, 2, 1
bl = blosum62()


def OptimalCTether(reference, translation, gp=1, c=10):
    '''
    This function will take two sequences: a `reference` sequence and  another
    protein sequence (`translation`; usually, this is an open reading frame
    that has been translated). Needleman-Wunsch alignment will be performed
    and the substring of translation with the highest identity that begins
    with a start codon [default: `['ATG']`] is reported.

    This function returns a dictionary of relevent information from the
    alignment; specifically, the alignments itself [keys: `query`, `subject`],
    the score [key: `score`], the length of the alignment [key: `length`], the
    length of the substring of translation used [key: `sublength`], the number
    of identities [key: `identities`], the theoretical perfect score for that
    alignment [key: `perfect`], and the number of gaps [key: `gaps`].
    '''

    starts = set(translate(s) for s in options.START_CODONS)
    v, w = reference, translation

    try:
        v = v.seq
    except AttributeError:
        pass
    try:
        w = w.seq
    except AttributeError:
        pass
    if not starts & set(w):
        raise ValueError("Open reading frame does not contain a start codon.")

    v, w = v[::-1], w[::-1]
    lv, lw = len(v), len(w)
    gpc = [[int(not (i | j)) for i in range(lw + 1)] for j in range(lv + 1)]
    mat = [[-(i + j) * gp - c * (not (i | j) and w[0] != v[0])
           for i in range(lw + 1)] for j in range(lv + 1)]
    pnt = [[VGAP_MARK if i > j else HGAP_MARK if j > i else DIAG_MARK
           for i in range(lw + 1)] for j in range(lv + 1)]
    ids = [[0 for i in range(lw + 1)] for j in range(lv + 1)]
    optimal = [None, 0, 0]
    for i in range(lv):
        for j in range(lw):
            vals = [[mat[i][j] + bl[v[i], w[j]], DIAG_MARK],
                    [mat[i + 1][j] - gp - c * gpc[i + 1][j], VGAP_MARK],
                    [mat[i][j + 1] - gp - c * gpc[i][j + 1], HGAP_MARK]]
            mat[i + 1][j + 1], pnt[i + 1][j + 1] = max(vals)
            gpc[i + 1][j + 1] = int(pnt[i + 1][j + 1] == DIAG_MARK)
            if w[j] in starts:
                if (optimal[0] is None or mat[i + 1][j + 1] > optimal[0]) and \
                        abs(lv - i) / float(lv) <= options.LENGTH_ERR:
                    optimal = [mat[i + 1][j + 1], i + 1, j + 1]

    i, j = optimal[1], optimal[2]
    seq, ids = ['', ''], 0
    gapcount, length, sublen = 0, 0, 0
    while [i, j] != [0, 0]:
        length += 1
        direction = pnt[i][j]
        if direction == VGAP_MARK:
            seq = ['-' + seq[0], w[j - 1] + seq[1]]
            j -= 1
            sublen += 1
            gapcount += 1
        elif direction == DIAG_MARK:
            seq = [v[i - 1] + seq[0], w[j - 1] + seq[1]]
            i -= 1
            j -= 1
            sublen += 1
            ids += int(w[j - 1] == v[i - 1])
        elif direction == HGAP_MARK:
            seq = [v[i - 1] + seq[0], '-' + seq[1]]
            i -= 1
            gapcount += 1
        else:
            break

    return {
        'subject': seq[0][::-1],
        'query': seq[1][::-1],
        'score': optimal[0],
        'gaps': gapcount,
        'length': length,
        'sublength': sublen,
        'identities': ids
    }
