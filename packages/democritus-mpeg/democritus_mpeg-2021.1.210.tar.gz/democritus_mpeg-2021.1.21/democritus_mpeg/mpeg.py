from typing import Iterable


# TODO: may want to use the request_first_arg_url decorator for the mp4_download function and pass in a flag to return the response object rather than the url content


def mp4_download(url: str) -> Iterable[bytes]:
    """."""
    from democritus_networking import get

    result = get(url)

    for chunk in result.iter_content(chunk_size=255):
        if chunk:
            yield chunk


def mp3_download(url: str) -> Iterable[bytes]:
    yield from mp4_download(url)
