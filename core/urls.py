from rest_framework.routers import DefaultRouter

from .views import AuthorViewSet, MaterialViewSet

router = DefaultRouter()
router.register('user', AuthorViewSet)
router.register('materials', MaterialViewSet)


urlpatterns = router.urls
