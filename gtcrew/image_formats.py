# image_formats.py
from wagtail.images.formats import Format, register_image_format

register_image_format(Format('responsive', 'Full-width Responsive', 'img-fluid', 'width-800'))
