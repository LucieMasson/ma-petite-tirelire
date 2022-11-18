from rest_framework import serializers


class TirelireCreationSerializer(serializers.Serializer):
    name = serializers.CharField()


class TirelireSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    broken = serializers.BooleanField()


class SavingSerializer(serializers.Serializer):
    coins = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=[]
    )
    notes = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=[]
    )


class RichesseSerializer(serializers.Serializer):
    montant = serializers.IntegerField()
