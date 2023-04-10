from django import template

register = template.Library()


@register.inclusion_tag('subcategory.html')
def subcategory(category, request):
    object_list = category.child.filter(status = category.status)
    return {
            'object_list' : object_list,
            'request' : request
            }
