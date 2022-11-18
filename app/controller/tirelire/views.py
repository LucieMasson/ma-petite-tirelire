from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from controller.tirelire import serializers
from service.manager import TirelireManager


@api_view(["POST"])
def create(request):
    """Création d'une nouvelle tirelire"""

    input_serializer = serializers.TirelireCreationSerializer(data=request.query_params)
    if not input_serializer.is_valid():
        return JsonResponse(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    manager = TirelireManager()
    t = manager.create(**input_serializer.validated_data)
    output_serializer = serializers.TirelireSerializer(t)

    return JsonResponse(output_serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def save(request, tirelire_id: int):
    """Epargne dans une tirelire existante"""

    input_serializer = serializers.SavingSerializer(data=request.query_params)
    if not input_serializer.is_valid():
        return JsonResponse(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        manager = TirelireManager(tirelire_id=tirelire_id)
        t = manager.save(**input_serializer.validated_data)
        output_serializer = serializers.TirelireSerializer(t)
    except Exception as e:
        return JsonResponse(e.args, status=status.HTTP_400_BAD_REQUEST, safe=False)

    return JsonResponse(output_serializer.data, status=status.HTTP_201_CREATED)
