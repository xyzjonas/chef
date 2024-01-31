import pillow_avif
from PIL import Image


def test_avif(dummy_image, tmp_path):
    image = Image.open(dummy_image)
    image.thumbnail((91, 91))

    new_path = f"{tmp_path}.avif"
    image.save(new_path, quality=70, save_all=True)

    assert Image.open(new_path).format == 'AVIF'

