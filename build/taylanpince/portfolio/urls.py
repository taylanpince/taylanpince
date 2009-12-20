from django.conf.urls.defaults import *


urlpatterns = patterns("portfolio.views",
    # Portfolio Detail
    url(r"^(?P<slug>[-\w]+)/$", "detail", name="portfolio_detail"),
)
