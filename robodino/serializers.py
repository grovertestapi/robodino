from rest_framework import serializers
from robodino.gamerules import BOARD_MIN_VALUE, BOARD_MAX_VALUE

class BoardSerializer(serializers.Serializer):
    board_id = serializers.CharField(max_length=256)

class BoardStatusSerializer(serializers.Serializer):
    board_id = serializers.CharField(max_length=256)

class BoardGenerateSerializer(serializers.Serializer):
    board_id = serializers.CharField(max_length=256)
    dinos_spawn_quantity = serializers.IntegerField(min_value=BOARD_MIN_VALUE, max_value=(BOARD_MAX_VALUE*BOARD_MAX_VALUE))
    robots_spawn_quantity = serializers.IntegerField(min_value=BOARD_MIN_VALUE, max_value=(BOARD_MAX_VALUE*BOARD_MAX_VALUE))

class DinoCreateSerializer(serializers.Serializer):
    board_id = serializers.CharField(max_length=256)
    position_row = serializers.IntegerField(min_value=BOARD_MIN_VALUE, max_value=BOARD_MAX_VALUE)
    position_column = serializers.IntegerField(min_value=BOARD_MIN_VALUE, max_value=BOARD_MAX_VALUE)

class RobotCreateSerializer(serializers.Serializer):
    board_id = serializers.CharField(max_length=256)
    position_row = serializers.IntegerField(min_value=BOARD_MIN_VALUE, max_value=BOARD_MAX_VALUE)
    position_column = serializers.IntegerField(min_value=BOARD_MIN_VALUE, max_value=BOARD_MAX_VALUE)
    direction = serializers.ChoiceField(choices=['up','down','left','right'])

class RobotMoveSerializer(serializers.Serializer):
    robot_id = serializers.IntegerField()
    move = serializers.ChoiceField(choices=['up', 'down', 'left','right'])

class RobotAttackSerializer(serializers.Serializer):
    robot_id = serializers.IntegerField()
