from django.contrib import admin
from robodino.models import BoardModel, DinoModel, RobotModel
# Register your models here.

admin.site.register(BoardModel)
admin.site.register(DinoModel)
admin.site.register(RobotModel)
