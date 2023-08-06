import numpy as np
import itertools


from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

okt = Okt()

def get_keyword_mmr(input_text,top_n=3,diversity=0.2):
    '''

    MMR strives to minimize duplication and maximize the diversity of results in text summarization tasks.

    :param input_text: insert your text
    :param top_n: number of keyword results
    :param diversity: If you set a low diversity value, the result is very similar to using the conventional cosine similarity alone.
                     However, a relatively high diversity value creates a variety of keywords.
    :return: keywords
    '''

    tokenized_doc = okt.pos(input_text)
    tokenized_nouns = ' '.join([word[0] for word in tokenized_doc if word[1] == 'Noun'])

    n_gram_range = (0,1)

    count = CountVectorizer(ngram_range=n_gram_range).fit([tokenized_nouns])
    candidates = count.get_feature_names_out()

    model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
    text_embedding = model.encode([input_text])
    candidate_embeddings = model.encode(candidates)

    words = candidates

    word_doc_similarity = cosine_similarity(candidate_embeddings, text_embedding)

    word_similarity = cosine_similarity(candidate_embeddings)

    keywords_idx = [np.argmax(word_doc_similarity)]

    candidates_idx = [i for i in range(len(words)) if i != keywords_idx[0]]

    for _ in range(top_n - 1):
        candidate_similarities = word_doc_similarity[candidates_idx, :]
        target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)

        mmr = (1 - diversity) * candidate_similarities - diversity * target_similarities.reshape(-1, 1)
        mmr_idx = candidates_idx[np.argmax(mmr)]

        keywords_idx.append(mmr_idx)
        candidates_idx.remove(mmr_idx)

    return [words[idx] for idx in keywords_idx]


def get_keyword_mss(input_text,top_n=3,nr_candidates=10):
    '''
    The intent here is to maximize the similarity of the candidate to the document while minimizing the similarity between the candidates.

    :param input_text: insert your text
    :param top_n: number of keyword results
    :param nr_candidates: Using a low nr_candidates results in a similar result to conventional cosine similarity.
                         However, the relatively high nr_candidates make the keyword more diverse.
    :return:keywords
    '''

    tokenized_doc = okt.pos(input_text)
    tokenized_nouns = ' '.join([word[0] for word in tokenized_doc if word[1] == 'Noun'])

    n_gram_range = (0, 1)

    count = CountVectorizer(ngram_range=n_gram_range).fit([tokenized_nouns])
    candidates = count.get_feature_names_out()

    model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
    text_embedding = model.encode([input_text])
    candidate_embeddings = model.encode(candidates)

    distances = cosine_similarity(text_embedding, candidate_embeddings)

    distances_candidates = cosine_similarity(candidate_embeddings, candidate_embeddings)

    words_idx = list(distances.argsort()[0][-nr_candidates:])
    words_vals = [candidates[index] for index in words_idx]
    distances_candidates = distances_candidates[np.ix_(words_idx, words_idx)]

    min_sim = np.inf
    candidate = None
    for combination in itertools.combinations(range(len(words_idx)), top_n):
        sim = sum([distances_candidates[i][j] for i in combination for j in combination if i != j])
        if sim < min_sim:
            candidate = combination
            min_sim = sim

    return [words_vals[idx] for idx in candidate]
