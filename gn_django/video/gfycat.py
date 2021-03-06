import re


def get_id(url):
    """
    Extract the Gfycat ID from a Gfycat URL.

    Args:
        * `url` - `string` - The URL to pull the ID from
    Returns:
        * A `string` if successful or `None` if not
    """
    if "gfycat" in url:
        match = re.search(r'^https?:\/\/(?:www.)?gfycat.com\/ifr\/([A-Za-z0-9\-_]+)(?:\/)?(?:\?.*)?$', url)
        if match:
            return match.group(1)
    return None
