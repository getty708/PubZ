from django import template

register = template.Library()

print("TAGS")


@register.inclusion_tag('dashboard/components/search_box.html')
def search_box(display_mode, *args, **kwargs):    
    return {"display_mode": display_mode,}
