# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 19:21:58 2018

final .py file where students got to group up and write the methods necessary to get the program running

@author: weissr
"""

import nltk
#nltk.download()
from nltk.book import *
from nltk.corpus import gutenberg
import csv
import re

'''
-------------------------
Features
-------------------------
'''
def avg_word_len(words):
    num_chars = 0
    for word in words:
        num_chars += len(word)
    return num_chars / len(words)

def lexical_div(words):
    n_vocab = len(set(words))
    l_div = n_vocab / len(words)
    return l_div

def n_hapax(words):
    fdist1 = FreqDist(words)
    one = len(fdist1.hapaxes())
    return one

def hapax_ratio(words):
    h_ratio = n_hapax(words)/len(words)
    return h_ratio

def avg_sent_len(words, sentences):
    sent_len = len(words) / len(sentences)
    return sent_len

def avg_sent_complexity(words, sentences):
    total_sents = len(sentences)
    empty = ''
    raw = empty.join(words)
    phrases = len(re.split('[.:,;]', raw))
    avg = total_sents / phrases
    return avg

'''
--------------------------
Compare Signatures
--------------------------
'''

def compute_signature(words, sentences, author):
    sig = [author]
    sig.append(avg_word_len(words))
    sig.append(lexical_div(words))
    sig.append(hapax_ratio(words))
    sig.append(avg_sent_len(words, sentences))
    sig.append(avg_sent_complexity(words, sentences))
    return sig



def compare_signatures(sig1, sig2, weights):
    '''Return a non-negative real number indicating the similarity of two
    linguistic signatures. The smaller the number the more similar the
    signatures. Zero indicates identical signatures.
    sig1 and sig2 are 6 element lists with the following elements
    0  : author name (a string)
    1  : average word length (float)
    2  : lexical diversity (float)
    3  : Hapax Legomana Ratio (float)
    4  : average sentence length (float)
    5  : average sentence complexity (float)
    weight is a list of multiplicative weights to apply to each
    linguistic feature. weight[0] is ignored.
    '''
    n_fields = len(sig1)
    score = 0.0
    for i in range(1,n_fields):
        score += abs(sig1[i] - sig2[i])*weights[i-1]
    return score

def get_signatures(sig_list, m_sig_list, weights):
    global scores_lst
    for i in m_sig_list:
        res = []
        for j in sig_list:
            values = []
            score = compare_signatures(i, j, weights)
            values.append(i[0])
            values.append(j[0])
            values.append(score)
            res.append(values)
        scores_lst.append(res)
    return scores_lst

def find_lowest(scores_lst, myst_num):
    scores = []
    authors = []
    for entry in scores_lst:
        if entry[0][0] == myst_num:
            for score in entry:
                authors.append(score[1])
                scores.append(score[2])
    top_scores = []
    top_authors =[]
    lowest = 0.0
    for i in range(4):
        for score in scores:
            if score == lowest:
                top_scores.append(score)
                index = scores.index(score)
                top_authors.append(authors[index])
                scores.remove(score)
                authors.remove(authors[index])
                lowest = min(scores)
    print('\n\nThe most likely matches are:')
    print('{:>12.4f}: {:>25}\n{:>12.4f}: {:>25}\n{:>12.4f}: {:>25}\n{:>12.4f}: {:>25}'.format(top_scores[0], top_authors[0], top_scores[1], top_authors[1], top_scores[2], top_authors[2], top_scores[3], top_authors[3]))

    return top_scores, top_authors

'''
--------------------------
Reading and Writing files
--------------------------
'''

def write_signatures(sig_list, o_filename):
    f_out = open(o_filename, 'w', newline = '')
    for sig in sig_list:
        for item in sig:
            f_out.write(str(item) + ' ')
        f_out.write('\n')
    f_out.close()

def read_signatures(in_filename):
    f_in = open(in_filename, 'r')
    infile = f_in.readlines()
    for line in infile:
        print(line)
    f_in.close()


def read_text(in_filename):
    try:
        path = 'corpora/gutenberg/' + in_filename
        file = nltk.data.find(path)
        f_in = open(file, 'r', encoding='utf-8')
        raw = f_in.read()
        f_in.close()
    except:
        print('failed to open', in_filename)
        return ''
    return raw


'''
--------------------------
Printing the output
--------------------------
'''

def print_sig_table(sig_list):
    '''
    for debugging
    '''
    print('\n{:>25} {:>12} {:>12} {:>12} {:>12} {:>12}\n'.format('File Name:', 'word_len:', 'lex_div:', 'hap_rat:', 'sent_len:', 'sent_comp:'))
    for sig in sig_list:
        print('{:>25} {:>12.4f} {:>12.4f} {:>12.4f} {:>12.4f} {:>12.4f}'.format(sig[0], sig[1], sig[2], sig[3], sig[4], sig[5]))

def print_scores(scores_lst, myst_num):
    for file in scores_lst:
        if file[0][0] == myst_num:
            print('\nScores for', file[0][0], ':\n')
            for entry in file:
                print('{:>25} {:>12.4f}'.format(entry[1], entry[2]))

'''
-------------------------
main
-------------------------
'''
if __name__ == '__main__':
    scores_lst = []
    weights = [11, 33, 50, 0.04, 4]
    sig_list = []
    fileids = gutenberg.fileids()
    print('\n\nCalculating Table of Signatures...')
    print('\n{:>25} {:>12} {:>12} {:>12} {:>12} {:>12}\n'.format('File Name:', 'word_len:', 'lex_div:', 'hap_rat:', 'sent_len:', 'sent_comp:'))
    for fid in fileids:
        # compute features, make a list of features
        words = gutenberg.words(fid)
        sents = gutenberg.sents(fid)
        sig = compute_signature(words, sents, fid)
        sig_list.append(sig)
        print('{:>25} {:>12.4f} {:>12.4f} {:>12.4f} {:>12.4f} {:>12.4f}'.format(sig[0], sig[1], sig[2], sig[3], sig[4], sig[5]))

    write_signatures(sig_list, 'out.txt')

    n_files = int(input('Enter Number of Mystery Files: '))
    m_sig_list = []
    for f in range(n_files):
        filename = input('Enter Name of Mystery File: ')
        raw_text = read_text(filename)
        m_words = gutenberg.words(filename)
        m_sents = gutenberg.sents(filename)
        m_sig = compute_signature(m_words, m_sents, filename)
        m_sig_list.append(m_sig)
        print('\nFile added to list of Mystery Files \n')

    get_signatures(sig_list, m_sig_list, weights)

    for i in range(n_files):
        file = input('Enter a Mystery File to Compare Signatures: ')
        print_scores(scores_lst, file)
        find_lowest(scores_lst, file)
