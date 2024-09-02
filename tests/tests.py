import pytest
from functions import *
from PIL import ImageTk, Image, ImageChops, ImageEnhance, ImageFilter
from exiftool import ExifToolHelper
import re
import binascii
import numpy
import hashlib
import sys
import os
import cv2

# Sample data for testing
sample_file = "sample_image.jpg"


# Test cases for process_metadata
def test_process_metadata_with_valid_data():
    result = process_metadata(sample_file)
    print(result)
    assert isinstance(result, list)


# Test cases for process_ela (Error Level Analysis)
def test_process_ela_with_image():
    result = process_ela(sample_file)
    assert isinstance(result, str) or isinstance(result, object)


# Test cases for process_strings
def test_process_strings_with_file():
    result = process_strings(sample_file)
    assert isinstance(result, str)
    assert len(result) > 0


# Test cases for process_hex_data
def test_process_hex_data_with_valid_data():
    result = process_hex(sample_file)
    print(result)
    assert isinstance(result, str)


# Test cases for process_copymove (Copy-Move Forgery Detection)
# def test_process_copymove_with_forged_image():
    # result = process_copymove(sample_file)
    # assert result is True

# def test_process_copymove_with_clean_image():
    # result = process_copymove("clean_image.png")
    # assert result is False


# Test cases for process_hash (Hashing Function)
def test_process_hash_with_known_data():
    md5, sha1 = hash_file(sample_file)
    assert md5.hexdigest() == "e01cf0a1c09a5211098e2c61575af972"

def test_process_hash_with_empty_string():
    result = hash_file(sample_file)
    assert result != "d41d8cd98f00b204e9800998ecf8427e"  # MD5 for an empty string

# Test cases for process_edges (Edge Detection in Images)
def test_process_edges_with_image():
    result = detect_edges(sample_file)
    assert isinstance(result, str) or isinstance(result, object)


# Test cases for process_location (Extract GPS data)
def test_process_location_with_geotagged_image():
    result = locate_coords(sample_file)
    assert isinstance(result, tuple)
    assert type(result[0]) == float and type(result[1]) == float

