from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from network import serializers, models
from network.permissions import IsActive


class FactoryViews(viewsets.ModelViewSet):
    queryset = models.Factory.objects.all()
    serializer_class = serializers.FactorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ["contact__city"]
    permission_classes = [IsActive]

    def update(self, request, *args, **kwargs):
        if request.data.get("indebtedness") and self.request.stream.method in ("PUT", "PATCH"):
            raise ValidationError({"error": "Нельзя менять задолжность"})

        return super().update(request, *args, **kwargs)


class RetailsNetViews(FactoryViews):
    queryset = models.RetailsNet.objects.all()
    serializer_class = serializers.RetailSerializer


class IndiPredViews(FactoryViews):
    queryset = models.IndiPred.objects.all()
    serializer_class = serializers.IndividualSerializer
