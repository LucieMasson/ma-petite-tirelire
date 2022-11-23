from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from controller.tirelire import serializers
from service.manager import PiggyBankManager
from service.exceptions import (
    UnknownPiggyBankError,
    BrokenPiggyBankError,
    UnknownChangeError,
)


@api_view(["GET"])
def list_piggybanks(request):
    """Liste des tirelire en enregistrées"""
    manager = PiggyBankManager()
    output_serializer = list(
        serializers.BiggybankSerializer(t).data for t in manager.list_piggybanks()
    )
    return JsonResponse(output_serializer, status=status.HTTP_200_OK, safe=False)


@api_view(["GET"])
def shake(request, piggybank_id: int):
    """Secoue une tirelire"""
    try:
        manager = PiggyBankManager(piggybank_id=piggybank_id)
        amount = manager.shake()
        output_serializer = serializers.BiggybankSerializer(manager.piggybank)
        result = dict(output_serializer.data)
        result["amount"] = amount
        return JsonResponse(result, status=status.HTTP_200_OK)

    except BrokenPiggyBankError as e:
        return JsonResponse(
            "Piggybank is broken", status=status.HTTP_400_BAD_REQUEST, safe=False
        )

    except UnknownPiggyBankError as e:
        return JsonResponse(
            "Piggybank does not exists", status=status.HTTP_400_BAD_REQUEST, safe=False
        )


@api_view(["POST"])
def create(request):
    """Création d'une nouvelle tirelire"""

    input_serializer = serializers.PiggybankCreationSerializer(
        data=request.query_params
    )
    if not input_serializer.is_valid():
        return JsonResponse(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    manager = PiggyBankManager()
    t = manager.create(**input_serializer.validated_data)
    output_serializer = serializers.BiggybankSerializer(t)

    return JsonResponse(output_serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def save(request, piggybank_id: int):
    """Epargne dans une tirelire existante"""

    input_serializer = serializers.SavingSerializer(data=request.query_params)
    if not input_serializer.is_valid():
        return JsonResponse(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        manager = PiggyBankManager(piggybank_id=piggybank_id)
        t = manager.save(**input_serializer.validated_data)
        output_serializer = serializers.BiggybankSerializer(t)

    except BrokenPiggyBankError as e:
        return JsonResponse(
            "Piggybank is broken", status=status.HTTP_400_BAD_REQUEST, safe=False
        )

    except UnknownPiggyBankError as e:
        return JsonResponse(
            "Piggybank does not exists", status=status.HTTP_400_BAD_REQUEST, safe=False
        )

    except UnknownChangeError as e:
        return JsonResponse(
            "At least one coin or note does not exists",
            status=status.HTTP_400_BAD_REQUEST,
            safe=False,
        )

    return JsonResponse(output_serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def smash(request, piggybank_id: int):
    """Casse la tirelire"""
    try:
        manager = PiggyBankManager(piggybank_id=piggybank_id)
        amount = manager.smash()
        output_serializer = serializers.BiggybankSerializer(manager.piggybank)
        result = dict(output_serializer.data)
        result["amount"] = amount
        return JsonResponse(result, status=status.HTTP_200_OK)

    except BrokenPiggyBankError as e:
        return JsonResponse(
            "Piggybank is broken", status=status.HTTP_400_BAD_REQUEST, safe=False
        )

    except UnknownPiggyBankError as e:
        return JsonResponse(
            "Piggybank does not exists", status=status.HTTP_400_BAD_REQUEST, safe=False
        )
