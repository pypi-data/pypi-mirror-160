import requests


def fetch_and_save_binary(url: str, dest: str, **kwargs) -> int:
    kwargs["stream"] = True
    resp = requests.get(url, **kwargs)
    resp.raise_for_status()

    bytes_read = 0
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                bytes_read += len(chunk)

    return bytes_read
