from django.urls import path
from .views import (
    ReportListCreateView,
    ReportRetrieveUpdateView,
    ReportLikeCreateView,
    ReportLikeDeleteView,
    ResourceByDistrictStatusCountView,
)

urlpatterns = [
    # Репорты
    path('reports/', ReportListCreateView.as_view(), name='report-list-create'),          # GET список, POST создать
    path('reports/<int:id>/', ReportRetrieveUpdateView.as_view(), name='report-detail'),  # GET/PUT/PATCH/DELETE конкретный отчет

    # Лайки к репортам
    path('reports/likes/', ReportLikeCreateView.as_view(), name='report-like-create'),    # POST поставить лайк
    path('reports/likes/<int:id>/', ReportLikeDeleteView.as_view(), name='report-like-delete'),  # DELETE убрать лайк

    path('district-report-counts/', ResourceByDistrictStatusCountView.as_view(), name='district-report-counts'),
]

