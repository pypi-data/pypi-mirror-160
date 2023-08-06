from . import _utils

from typing_extensions import Literal


def get_data_path(
    file_name: Literal[
        "glove.6B.100d.txt.w2v.zip",
        "glove.6B.200d.txt.w2v.zip",
        "glove.6B.300d.txt.w2v.zip",
        "glove.6B.50d.txt.w2v",
        "glove.6B.50d.txt.w2v.zip",
        "iris_data.npy",
        "questions-words.txt",
        "shakespeare_input.txt",
        "stopwords.txt",
        "wikipedia2text-encoded.npz",
        "wikipedia2text-extracted.txt",
        "captions_train2014.json,"
        "resnet18_features.pkl",
    ]
) -> str:
    """Specify the name of a file in the a data-storage repository. This file
    will be downloaded to a cache location, unless it already exists, and a path
    to that file will be returned.
    
    Parameters
    ----------
    file_name : str
        A valid file name. See Notes section for details.
    
    Return
    ------
    path_to_file : str
    
    Notes
    -----
    Valid file names:
    - glove.6B.50d.txt.w2v.zip  : 50-dimensional Stanford GloVe embeddings
    - glove.6B.100d.txt.w2v.zip : 100-dimensional Stanford GloVe embeddings
    - glove.6B.200d.txt.w2v.zip : 200-dimensional Stanford GloVe embeddings
    - glove.6B.300d.txt.w2v.zip : 100-dimensional Stanford GloVe embeddings
    - iris_data.npy : The iris dataset (https://archive.ics.uci.edu/ml/datasets/iris)
    - questions-words.txt
    - shakespeare_input.txt : Andrej Karpathy's shakespeare_input.txt file
    - stopwords.txt : MySQL stop-words
    - wikipedia2text-encoded.npz
    - wikipedia2text-extracted.txt " : Text-only version of wikipedia http://www.evanjones.ca/software/wikipedia2text.html
    - captions_train2014.json : Images and associated captions from the MSCOCO 2014 dataset
    - resnet18_features.pkl : A shape- (1,512)  descriptor vector for each image from the MSCOCO dataset. Each of these was produced by processing each image with a pre-trained ResNet-18 classification model.

    """
    return _utils.language_data.fetch(file_name)
