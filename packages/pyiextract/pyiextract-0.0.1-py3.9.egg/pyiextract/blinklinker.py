import typing
import os
import urllib
import argparse
import logging

import blink.main_dense as main_dense

from .linker import Linker
from .entity import Entity
from .pronouns import PRONOUNS


class BlinkLinker(Linker):
    def __init__(self) -> None:
        super().__init__("BLINK")
        cache_folder = os.path.expanduser(os.path.join("~", ".blink"))
        os.makedirs(cache_folder, exist_ok=True)
        biencoder_model = "biencoder_wiki_large.bin"
        biencoder_config = "biencoder_wiki_large.json"
        entity_catalogue = "entity.jsonl"
        entity_encoding = "all_entities_large.t7"
        crossencoder_model = "crossencoder_wiki_large.bin"
        crossencoder_config = "crossencoder_wiki_large.json"
        download_files = {
            f"http://dl.fbaipublicfiles.com/BLINK/{biencoder_model}",
            f"http://dl.fbaipublicfiles.com/BLINK/{biencoder_config}",
            f"http://dl.fbaipublicfiles.com/BLINK/{entity_catalogue}",
            f"http://dl.fbaipublicfiles.com/BLINK/{entity_encoding}",
            f"http://dl.fbaipublicfiles.com/BLINK/{crossencoder_model}",
            f"http://dl.fbaipublicfiles.com/BLINK/{crossencoder_config}",
        }
        for download_file in download_files:
            parsed_url = urllib.parse.urlparse(download_file)
            filename = os.path.basename(parsed_url.path)
            download_path = os.path.join(cache_folder, filename)
            if os.path.exists(download_path):
                continue
            logging.info(f"Downloading {download_file} to {download_path}")
            urllib.request.urlretrieve(download_file, download_path)
        config = {
            "test_entities": None,
            "test_mentions": None,
            "interactive": False,
            "top_k": 1,
            "biencoder_model": os.path.join(cache_folder, biencoder_model),
            "biencoder_config": os.path.join(cache_folder, biencoder_config),
            "entity_catalogue": os.path.join(cache_folder, entity_catalogue),
            "entity_encoding": os.path.join(cache_folder, entity_encoding),
            "crossencoder_model": os.path.join(cache_folder, crossencoder_model),
            "crossencoder_config": os.path.join(cache_folder, crossencoder_config),
            "fast": True,
            "output_path": os.path.join(cache_folder, "logs")
        }
        self._args = argparse.Namespace(**config)
        self._models = main_dense.load_models(self._args, logger=None)

    def link(self, entity: typing.Any, sentence: typing.Any) -> Entity:
        if str(entity) in PRONOUNS:
            return super().link(entity, sentence)
        sentence_str = str(sentence)
        _, _, _, _, _, predictions, scores, identifiers = main_dense.run(self._args, None, *self._models, test_data=[{
            "id": 0,
            "label": "unknown",
            "label_id": -1,
            "context_left": sentence_str[:entity.start_char].lower()[:127],
            "mention": str(entity).lower()[:127],
            "context_right": sentence_str[entity.end_char:].lower()[:127],
        }])
        predictions = predictions[0]
        scores = scores[0]
        identifiers = identifiers[0]
        if scores and predictions and identifiers:
            if scores[0] > 10.0:
                logging.info(f"Found entity link {identifiers[0]} {predictions[0]} for {str(entity)}")
                return Entity(predictions[0], str(identifiers[0]))
        return super().link(entity, sentence)
