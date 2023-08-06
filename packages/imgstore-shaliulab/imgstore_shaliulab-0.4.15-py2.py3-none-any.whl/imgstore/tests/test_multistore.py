import time
import os.path
import tqdm
import numpy as np

import imgstore.stores.multi as imgstore
from imgstore.tests import TEST_DATA_DIR
from imgstore.constants import STORE_MD_FILENAME

MULTISTORE_PATH = os.path.join(TEST_DATA_DIR, "imgstore_slow_high_fps", STORE_MD_FILENAME)
MULTISTORE_PATH = "/Users/FlySleepLab Dropbox/Data/flyhostel_data/videos/6X/2022-05-15_17-03-36/metadata.yaml"

def test_get_image(store):

    took = []

    idx = range(100000, 100200, 5)
    for i in tqdm.tqdm(idx, desc="Benchmarking get_image"):
        before = time.time()
        img, (frame_number, frame_time) = store.get_image(i)
        after = time.time()
        took.append(after-before)

    print(f"Estimated max playback fps: {1 / np.mean(took)}")


def test_get_nearest_image(store):
    # TODO
    img, (frame_number, frame_time) = store.get_nearest_image(45)

def test_get_next_image(store):

    # TODO
    took = []
    store.set(1, 100200)

    for _ in tqdm.tqdm(range(100), desc="Benchmarking get_next_image"):
        before = time.time()
        img, (frame_number, frame_time) = store.get_next_image()
        print(frame_number)
        after = time.time()
        took.append(after-before)

    print(f"Estimated max playback fps: {1 / np.mean(took)}")

def test_multistore():

    with imgstore.new_for_filename(MULTISTORE_PATH) as multistore:
        multistore.select_store("lowres/metadata.yaml")
        # test_get_image(multistore)
        test_get_nearest_image(multistore)
        test_get_next_image(multistore)



test_multistore()
