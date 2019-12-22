import os
import math
import random
import nltk
import numpy as np
from numba import jit
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from pprint import pprint


class RandomIndexing:
    def __init__(self, folderpath):
        # print(numba.__version__)
        documents, terms = self.preprocessing(folderpath)
        index_vector = self.create_index_vector(terms)
        print("Index Vector Created.\n")
        final_context_vector = self.create_context_vector(
            documents, index_vector)
        print("Context Vectors calculated.\n")
        print(
            "Calculating the similarity values of each term and sorting them.\n"
        )
        similar_terms = self.sort_similarity(final_context_vector)

        x = int(input("Enter x:"))
        print("Displaying Results.\n")
        for key in similar_terms.keys():
            print(key, similar_terms[key][:x])

    # @jit(nopython=True)
    def preprocessing(self, folderpath):
        documents = {}
        terms = []
        os.chdir(folderpath)
        tokenizer = RegexpTokenizer(r'\w+')
        stop_words = set(stopwords.words('english'))
        for filename in os.listdir():
            vector = []
            f = open(os.path.join(folderpath, filename), 'r')
            a = tokenizer.tokenize(f.read().lower())
            for i in a:
                if i not in stop_words:
                    vector.append(i)
            documents[filename] = np.array(vector)
            # print(set(vector))
            terms.extend(vector)
        return documents, np.array(list(set(terms)))

    # @jit(nopython=True)
    def create_index_vector(self, terms):
        index_vectors = {}
        for term in terms:
            x = ''
            for a in term:
                x += str(ord(a))
            x = int(x)
            random.seed(x)
            vector_length = 1024
            iv = []
            a = [1, -1]
            for i in range(vector_length):
                if random.uniform(1, 101) < 10:
                    iv.append(a[random.randint(0, 1)])
                else:
                    iv.append(0)
            index_vectors[term] = np.array(iv)
        return index_vectors

    # @jit(nopython=True)
    def create_context_vector(self, documents, index_vector):
        for doc in documents.keys():
            for i in range(len(documents[doc])):
                if i == 0:
                    index_vector[documents[doc][i]] = index_vector[
                        documents[doc][i]] + (
                            index_vector[documents[doc][i + 1]] *
                            0.5) + (index_vector[documents[doc][i + 2]] * 0.25)
                elif i == 1:
                    index_vector[documents[doc][i]] = (
                        index_vector[documents[doc][i - 1]] *
                        0.5) + index_vector[documents[doc][i]] + (
                            index_vector[documents[doc][i + 1]] *
                            0.5) + (index_vector[documents[doc][i + 2]] * 0.25)
                elif i == len(documents[doc]) - 2:
                    index_vector[documents[doc][i]] = (
                        index_vector[documents[doc][i + 1]] *
                        0.5) + index_vector[documents[doc][i]] + (
                            index_vector[documents[doc][i - 1]] *
                            0.5) + (index_vector[documents[doc][i - 2]] * 0.25)
                elif i == len(documents[doc]) - 1:
                    index_vector[documents[doc][i]] = index_vector[
                        documents[doc][i]] + (
                            index_vector[documents[doc][i - 1]] *
                            0.5) + (index_vector[documents[doc][i - 2]] * 0.25)
                else:
                    index_vector[documents[doc][i]] = (
                        index_vector[documents[doc][i + 1]] * 0.5) + (
                            index_vector[documents[doc][i + 2]] *
                            0.25) + index_vector[documents[doc][i]] + (
                                index_vector[documents[doc][i - 1]] * 0.5) + (
                                    index_vector[documents[doc][i - 2]] * 0.25)
        return index_vector

    # @jit(nopython=True)
    def sort_similarity(self, context_vector):
        sorted_terms = {}
        for term in context_vector.keys():
            mag_a = np.linalg.norm(context_vector[term])
            for term2 in context_vector.keys():
                mag_b = np.linalg.norm(context_vector[term2])
                score = np.sum(context_vector[term] *
                               context_vector[term2]) / (mag_a * mag_b)
                try:
                    sorted_terms[term] += [(term2, score)]
                except:
                    sorted_terms[term] = [(term2, score)]
        for key in sorted_terms.keys():
            sorted_terms[key].sort(reverse=True, key=lambda x: x[1])
        return sorted_terms


RandomIndexing('/home/gcoderx/Desktop/IR Assign - 3/1/')
