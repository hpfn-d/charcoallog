from rest_framework import serializers

from charcoallog.bank.models import Extract, Schedule


class ExtractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extract
        fields = ('payment', 'category', 'description', 'money', 'date', 'pk')

    def update(self, instance, validated_data):
        instance.pk = validated_data.get('pk', instance.pk)
        instance.date = validated_data.get('date', instance.date)
        instance.money = validated_data.get('money', instance.money)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.payment = validated_data.get('payment', instance.payment)
        instance.user_name = validated_data.get('user_name', instance.user_name)

        instance.save()

        return instance


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('payment', 'category', 'description', 'money', 'date', 'pk')

    def update(self, instance, validated_data):
        instance.pk = validated_data.get('pk', instance.pk)
        instance.date = validated_data.get('date', instance.date)
        instance.money = validated_data.get('money', instance.money)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.payment = validated_data.get('payment', instance.payment)
        instance.user_name = validated_data.get('user_name', instance.user_name)

        instance.save()

        return instance
