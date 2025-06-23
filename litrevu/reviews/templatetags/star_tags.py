from django import template

register = template.Library()


@register.inclusion_tag("components/stars.html")
def display_stars(rating):
    full = range(int(rating))
    empty = range(5 - int(rating))
    return {"full": full, "empty": empty}
