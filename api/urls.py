from MySQLdb import ROWID
from rest_framework import routers
from records.views import RecordsViewSet

router = routers.SimpleRouter()
router.register(r"records", RecordsViewSet, basename="record")

urlpatterns = router.urls
