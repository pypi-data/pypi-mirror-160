from asyncore import read
from rest_framework import serializers
from .models import TransitionManager , workevents , workflowitems , Action


class Workeventsserializer(serializers.ModelSerializer):
    event_user = serializers.SlugRelatedField(read_only=True,slug_field = "username")
    class Meta:
        model = workevents
        fields = [
            'id',
            'action',
            'subaction',
            'initial_state',
            'interim_state',
            'final_state',
            'event_user',
            'from_party',
            'to_party'
        ]




class Workitemserializer(serializers.ModelSerializer):
    WorkFlowEvents = Workeventsserializer(many=True, read_only=True)
    class Meta:
        model = workflowitems
        fields = [
            'id',
            'transitionmanager',
            'initial_state',
            'interim_state',
            'final_state',
            'event_user',
            'current_from_party',
            'current_to_party',
            'WorkFlowEvents',
        ]






class TransitionManagerserializer(serializers.ModelSerializer):
    workflowitems = Workitemserializer(read_only = True)
    class Meta:
        model = TransitionManager
        fields = [
            'id',
            'type',
            'workflowitems'
        ]



class Actionseriaizer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'



class workflowitemslistserializer(serializers.ModelSerializer):
    class Meta:
        model = workflowitems
        fields = '__all__'


class workeventslistserializer(serializers.ModelSerializer):
    class Meta:
        model = workevents
        fields = '__all__'