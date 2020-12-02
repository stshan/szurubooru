import pytest

from szurubooru.func import mime


@pytest.mark.parametrize(
    "input_path,expected_mime_type",
    [
        ("mp4.mp4", "video/mp4"),
        ("webm.webm", "video/webm"),
        ("flash.swf", "application/x-shockwave-flash"),
        ("png.png", "image/png"),
        ("jpeg.jpg", "image/jpeg"),
        ("gif.gif", "image/gif"),
        ("webp.webp", "image/webp"),
        ("text.txt", "application/octet-stream"),
    ],
)
def test_get_mime_type(read_asset, input_path, expected_mime_type):
    assert mime.get_mime_type(read_asset(input_path)) == expected_mime_type


def test_get_mime_type_for_empty_file():
    assert mime.get_mime_type(b"") == "application/octet-stream"


@pytest.mark.parametrize(
    "mime_type,expected_extension",
    [
        ("video/mp4", "mp4"),
        ("video/webm", "webm"),
        ("application/x-shockwave-flash", "swf"),
        ("image/png", "png"),
        ("image/jpeg", "jpg"),
        ("image/gif", "gif"),
        ("image/webp", "webp"),
        ("application/octet-stream", "dat"),
    ],
)
def test_get_extension(mime_type, expected_extension):
    assert mime.get_extension(mime_type) == expected_extension


@pytest.mark.parametrize(
    "input_mime_type,expected_state",
    [
        ("application/x-shockwave-flash", True),
        ("APPLICATION/X-SHOCKWAVE-FLASH", True),
        ("application/x-shockwave", False),
    ],
)
def test_is_flash(input_mime_type, expected_state):
    assert mime.is_flash(input_mime_type) == expected_state


@pytest.mark.parametrize(
    "input_mime_type,expected_state",
    [
        ("video/webm", True),
        ("VIDEO/WEBM", True),
        ("video/mp4", True),
        ("VIDEO/MP4", True),
        ("video/anything_else", False),
        ("application/ogg", True),
        ("not a video", False),
    ],
)
def test_is_video(input_mime_type, expected_state):
    assert mime.is_video(input_mime_type) == expected_state


@pytest.mark.parametrize(
    "input_mime_type,expected_state",
    [
        ("image/gif", True),
        ("image/png", True),
        ("image/jpeg", True),
        ("IMAGE/GIF", True),
        ("IMAGE/PNG", True),
        ("IMAGE/JPEG", True),
        ("image/anything_else", False),
        ("not an image", False),
    ],
)
def test_is_image(input_mime_type, expected_state):
    assert mime.is_image(input_mime_type) == expected_state


@pytest.mark.parametrize(
    "input_path,expected_state",
    [
        ("gif.gif", False),
        ("gif-animated.gif", True),
    ],
)
def test_is_animated_gif(read_asset, input_path, expected_state):
    assert mime.is_animated_gif(read_asset(input_path)) == expected_state
