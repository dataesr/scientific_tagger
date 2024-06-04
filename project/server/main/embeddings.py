import os
import spacy
from sklearn import preprocessing
from sentence_transformers import SentenceTransformer, util

from project.server.main.logger import get_logger

logger = get_logger(__name__)

nlp = spacy.load("en_core_sci_scibert")
model_multilingual = SentenceTransformer('distiluse-base-multilingual-cased-v1')
model_small = SentenceTransformer('thenlper/gte-small')
model_large = SentenceTransformer('thenlper/gte-large')

def get_embeddings(embed_type, text, normalize=True):
    if not isinstance(text, str) or text is None or len(text) == 0:
        return None
    if embed_type == 'scibert':
        return get_scibert_embeddings(text, normalize)
    elif embed_type == 'multilingual':
        return get_multilingual_embeddings(text, normalize)
    elif embed_type == 'small':
        return get_small_embeddings(text, normalize)
    elif embed_type == 'large':
        return get_large_embeddings(text, normalize)
    else:
        logger.debug(f'unknown {embed_type} embedding type!')

def get_scibert_embeddings(text, normalize=True):
    doc = nlp(text)
    tokvecs = doc._.trf_data.tensors[-1]
    if normalize:
        tokvecs = preprocessing.normalize(tokvecs, norm='l2')
    tokvecs = tokvecs[0]
    assert(len(tokvecs) == 768)
    # converting to float for json serialization
    return { 'embeddings': [float(e) for e in tokvecs] }

def get_multilingual_embeddings(text, normalize=True):
    tokvecs = model_multilingual.encode(text, normalize_embeddings=normalize)
    assert(len(tokvecs) == 512)
    return { 'embeddings': [float(e) for e in tokvecs] }

def get_small_embeddings(text, normalize=True):
    tokvecs = model_small.encode(text, normalize_embeddings=normalize)
    return { 'embeddings': [float(e) for e in tokvecs] }

def get_large_embeddings(text, normalize=True):
    tokvecs = model_large.encode(text, normalize_embeddings=normalize)
    return { 'embeddings': [float(e) for e in tokvecs] }
