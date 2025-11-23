from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def dict_key(dictionary, key):
    """فیلتر برای دسترسی به مقدار dictionary با کلید"""
    if dictionary and key in dictionary:
        return dictionary[key]
    return None