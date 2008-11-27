from django import template


register = template.Library()


@register.inclusion_tag("core/pagination.html")
def paginate(pager, page, pager_url):
    """
    Creates the page list, according to the current page
    """
    ON_EACH_SIDE = 6
    ON_ENDS = 5
    DOT = "."
    
    # If there are 10 or fewer pages, display links to every page.
    # Otherwise, do some fancy
    if pager.num_pages <= 10:
    	page_range = range(1, pager.num_pages + 1)
    else:
    	# Insert "smart" pagination links, so that there are always ON_ENDS
    	# links at either end of the list of pages, and there are always
    	# ON_EACH_SIDE links at either end of the "current page" link.
    	page_range = []
    	
    	if page.number > (ON_EACH_SIDE + ON_ENDS):
    		page_range.extend(range(1, ON_EACH_SIDE))
    		page_range.append(DOT)
    		page_range.extend(range(page.number - ON_EACH_SIDE, page.number))
    	else:
    		page_range.extend(range(1, page.number))
    	
    	if page.number < (pager.num_pages - ON_EACH_SIDE - ON_ENDS):
    		page_range.extend(range(page.number, page.number + ON_EACH_SIDE))
    		page_range.append(DOT)
    		page_range.extend(range(pager.num_pages - ON_ENDS, pager.num_pages + 1))
    	else:
    		page_range.extend(range(page.number, pager.num_pages + 1))
    
    page_range.reverse()
    
    return {
        "page": page,
        "pager": pager,
        "pager_url": pager_url,
        "page_range": page_range,
    }


@register.simple_tag
def paginate_url(url, page):
    return url % page
