from __future__ import annotations

from django import template
from django.utils.safestring import SafeString, mark_safe

from ..icons import Stringable, get_icon

register = template.Library()


@register.simple_tag
def tabler_icon(name: str, size: Stringable = 24, **svg_attrs: Stringable) -> str:
    fixed_kwargs = {key: (value + "" if isinstance(value, SafeString) else value) for key, value in svg_attrs.items()}
    return mark_safe(get_icon(name, size, **fixed_kwargs))
