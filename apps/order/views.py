from django.shortcuts import render
from .models import Report, ReportLike
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import generics, permissions
from .serializers import ReportSerializer, ReportLikeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
from apps.order.models import Report
from apps.map.models import DISTRICT_CHOICES
from apps.map.models import RESOURCE_TYPE_CHOICES


class ReportListCreateView(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReportRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Редактировать может только автор отчёта")
        serializer.save()


class ReportLikeCreateView(generics.CreateAPIView):
    queryset = ReportLike.objects.all()
    serializer_class = ReportLikeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportLikeDeleteView(generics.DestroyAPIView):
    queryset = ReportLike.objects.all()
    serializer_class = ReportLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("Вы можете удалять только свои лайки.")
        return obj


class ResourceByDistrictStatusCountView(APIView):
    def get(self, request):
        result = []

        # Для каждого типа ресурса соберём статистику по всем районам
        for res_key, res_label in RESOURCE_TYPE_CHOICES:
            districts_data = []
            for dist_key, dist_label in DISTRICT_CHOICES:
                qs = Report.objects.filter(resource=res_key, district=dist_key)
                counts = qs.aggregate(
                    unresolved=Count('id', filter=Q(problem_status='unresolved')),
                    resolved=Count('id', filter=Q(problem_status='resolved')),
                )
                districts_data.append({
                    "district": dist_label,
                    "unresolved": counts["unresolved"],
                    "resolved": counts["resolved"],
                })

            result.append({
                "resource": res_label,
                "districts": districts_data
            })

        return Response(result)
