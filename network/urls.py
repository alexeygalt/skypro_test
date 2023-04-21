from rest_framework import routers

from network import views

router_factory = routers.SimpleRouter()
router_factory.register(r"factory", views.FactoryViews)

router_retail = routers.SimpleRouter()
router_retail.register(r"retail", views.RetailsNetViews)

router_indi = routers.SimpleRouter()
router_indi.register(r"indi", views.IndiPredViews)


urlpatterns = []

urlpatterns += router_factory.urls + router_indi.urls + router_retail.urls
