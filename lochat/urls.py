from . import views

urlpatterns = [
    ('/', views.index, ['GET']),
]
