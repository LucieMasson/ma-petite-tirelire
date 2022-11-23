from rest_framework import serializers


class PiggybankCreationSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class BiggybankSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    broken = serializers.BooleanField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class SavingSerializer(serializers.Serializer):
    coins = serializers.ListField(
        child=serializers.FloatField(), required=False, default=[]
    )
    notes = serializers.ListField(
        child=serializers.FloatField(), required=False, default=[]
    )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
