import pathlib
import typing
import zipfile
from functools import lru_cache
from xml.etree import ElementTree

THIS_DIR = pathlib.Path(__file__).parent
ARCHIVE_NAME = THIS_DIR / 'archive.zip'
PATH_ATTRS = {'stroke-linecap', 'stroke-linejoin', 'stroke-width', 'vector-effect'}


class IconDoesNotExists(Exception):  # pragma: nocover
    ...


class Stringable(typing.Protocol):  # pragma: nocover
    def __str__(self) -> str:
        ...


@lru_cache(maxsize=128)
def extract_icon(name: str) -> str:
    with zipfile.ZipFile(ARCHIVE_NAME) as zip_ref:
        try:
            return zip_ref.read(f'{name}.svg').decode().strip()
        except KeyError:
            raise IconDoesNotExists(f'The icon {name} does not exist.')


def get_icon(name: str, size: Stringable = 20, **svg_attrs: Stringable) -> str:
    contents = extract_icon(name)
    svg = ElementTree.fromstring(contents)
    for node in svg.iter():
        node.tag = str(ElementTree.QName(node.tag.removeprefix("{http://www.w3.org/2000/svg}")))

    svg.attrib['class'] = f'tabler-icon tabler-icon-{name}'
    svg.attrib['width'] = svg.attrib['height'] = str(size)
    extra_svg_attrs = {}
    extra_path_attrs = {}
    for attr_name, attr_value in svg_attrs.items():
        attr_name = attr_name.replace('_', '-')
        if attr_name in PATH_ATTRS:
            extra_path_attrs[attr_name] = str(attr_value)
        else:
            extra_svg_attrs[attr_name] = str(attr_value)

    svg.attrib.update(extra_svg_attrs)

    if extra_path_attrs:
        for path_tag in svg.findall('path'):
            path_tag.attrib.update(extra_path_attrs)

    svg_string = ElementTree.tostring(svg, encoding='utf8').decode()
    svg_string = svg_string.replace("<?xml version='1.0' encoding='utf8'?>", '')
    svg_string = svg_string.replace(' xmlns="http://www.w3.org/2000/svg"', '', 1)
    return svg_string.strip()
