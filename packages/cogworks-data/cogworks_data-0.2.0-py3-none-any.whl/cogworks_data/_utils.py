import hashlib
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union, Final
import pooch

if TYPE_CHECKING:
    from hashlib import _Hash
else:
    _Hash = Any

__all__ = ["get_sha256_hash", "get_md5_hash"]



def _get_hash(file_path: Union[Path, str], hash_fn: _Hash) -> str:
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_fn.update(chunk)
    return hash_fn.hexdigest()


def get_sha256_hash(file_path: Union[Path, str]) -> str:
    """Reads in data from disk and returns md5 hash
    
    Examples
    --------
    >>> from cog_data._utils import get_sha256_hash
    >>> get_sha256_hash("./CogWeb/website_src/Language/Exercises/dat/stopwords.txt")
    '9aa3e6f003d6c0e07a2d6e049e43a5669d554622dbd38fef91b37d4a852e15a5'
    """
    return _get_hash(file_path, hashlib.sha256())


def get_md5_hash(file_path: Union[Path, str]) -> str:
    """Reads in data from disk and returns sha256 hash
    
    Examples
    --------
    >>> from cog_data._utils import get_md5_hash
    >>> get_md5_hash("./CogWeb/website_src/Language/Exercises/dat/stopwords.txt")
    'a25f9890bfa50457244792b4b5c15566'
    """
    return _get_hash(file_path, hashlib.md5())

audio_files: Final = {'BP_ET_minor.ogg': 'sha256:2bcb618d44bb46694f729b7c23eeb8e2925b34be3aef63c2ddd823cee892e796',
 'dow.txt': 'sha256:94bdebcf3b524134a34bbfadea392e36704d2116e2b309e54f79be77539e507e',
 'paws.txt': 'sha256:e4e3391ddcc6418b599cf8603030c7b0f3fd9c0c0329096d450562cd7ac10825',
 'piano.txt': 'sha256:c593cf60873be66ac2c0fa8a619d33c4445b69a41c7f50ef7589ae44000cd2b3',
 'sunspots.txt': 'sha256:a3e7bc07dd7067843de873157aff0bde6dc3f7aa6345e811d8b876561958e0d6',
 'trumpet.txt': 'sha256:82bc7c1b125c6465c28ee84cb3eebe8331ede85c863c20f2839af605513d8689',
 'trumpet.wav': 'sha256:618be790b3d6c0600f701a6edd29c359ec244ad8fc3cd6dae4138b20a118217c'}

vision_files: Final = {'nba_draft_measurements.nc': 'sha256:1cbb075e5b8a8d908d3eb70d9d28cab92c112079c0d9b7ccc7e2629b8d1484a8'}

language_files: Final = {'glove.6B.100d.txt.w2v.zip': 'sha256:b340ad2b7c08c6e12529cbc7370e71ceffd668e979895c97ffb03ce79736c5b4',
 'glove.6B.200d.txt.w2v.zip': 'sha256:6cbe88628045658c4175c50121b9ad6c61c39777ee42bdb19a255d26b0472b3a',
 "glove.6B.200d.txt.w2v":"dcee6ecdefebb5a884b23f2353561cc5f0527e59592525c0e3f4a31d81d91272",
 'glove.6B.300d.txt.w2v.zip': 'sha256:47efbb5004f34b6b6241deee0cf26b913fdef68497e9100480edbcfb3b3ae034',
 'glove.6B.50d.txt.w2v': 'sha256:9a8a78e2c6da3115e97044cbcfb40736d430961410bf732a4e80776412be5cd3',
 'glove.6B.50d.txt.w2v.zip': 'sha256:76ea7e013cba3c87a5d45c317bd436bf10cfd47e58a48c04797056bca3f3e298',
 'iris_data.npy': 'sha256:6b360479c8197bf132e0006224d97a7ac1091e855a445505d82ab917873904f6',
 'questions-words.txt': 'sha256:8d837381ec7c289bed2ae17fab028807e21eb2ba8dc29eb7df8f9c794201fb8d',
 'shakespeare_input.txt': 'sha256:90a59332a07bdea17e1b13088050e5a7e81e18db994e18b057b89fd50d2f49c4',
 'stopwords.txt': 'sha256:9aa3e6f003d6c0e07a2d6e049e43a5669d554622dbd38fef91b37d4a852e15a5',
 'wikipedia2text-encoded.npz': 'sha256:32fe610a6571cf79c2d38e0f0268e1cc4b9983fd53d8f3c57986f5303518280a',
 'wikipedia2text-extracted.txt': 'sha256:ed58b8b9b3e4d8607353016c55c973c4bbfde89f2b39d5fc673ac55003072eea',
 'captions_train2014.json': 'dd8c9636dc11740f956e36728866ea0c4ebe4988dcbdc5e712b7c2267f152d12',
 'resnet18_features.pkl': 'd56e267dacd39608b4aae581595f8fa8ec55457ab59b713df1eafa93e1023450',}

audio_data = pooch.create(
    base_url= "https://github.com/rsokl/cog_data/releases/download/audio-files/",
    path= pooch.os_cache("cog_data"), # placeholder
    registry= audio_files
)

vision_data = pooch.create(
    base_url= "https://github.com/rsokl/cog_data/releases/download/vision-files/",
    path= pooch.os_cache("cog_data"), # placeholder
    registry= vision_files
)

language_data = pooch.create(
    base_url= "https://github.com/rsokl/cog_data/releases/download/language-files/",
    path= pooch.os_cache("cog_data"), # placeholder
    registry= language_files
)
