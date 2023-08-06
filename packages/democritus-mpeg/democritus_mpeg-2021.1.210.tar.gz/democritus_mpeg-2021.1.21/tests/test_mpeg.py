# -*- coding: utf-8 -*-

import pytest

from democritus_mpeg import (
    mp4_download,
    mp3_download,
)


@pytest.mark.network
def test_mp4_download_1():
    url = 'https://archive.org/download/user-mp4-test/ac3.mp4'
    result = tuple(mp4_download(url))
    result_bytes = b''.join(result)
    assert len(result_bytes) == 528002


@pytest.mark.network
def test_mp3_download_1():
    url = 'https://archive.org/download/testmp3testfile/mpthreetest.mp3'
    result = tuple(mp3_download(url))
    result_bytes = b''.join(result)
    assert len(result_bytes) == 198658
