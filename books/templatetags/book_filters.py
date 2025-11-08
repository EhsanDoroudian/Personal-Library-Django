from django import template

register = template.Library()

@register.simple_tag
def url_replace(request, **kwargs):
    query = request.GET.copy()
    for key, value in kwargs.items():
        if value:
            query[key] = value
        else:
            query.pop(key, None)
    return query.urlencode()

@register.filter
def status_display(status):
    status_map = {
        'R': 'خوانده شده',
        'NR': 'خوانده نشده', 
        'B': 'امانت گرفته شده'
    }
    return status_map.get(status, status)

@register.filter
def get_category_title(categories, category_id):
    """Get category title from category ID"""
    try:
        category_id = int(category_id)
        for category in categories:
            if category.id == category_id:
                return category.title
    except (ValueError, TypeError):
        pass
    return ''