from django.db import models

# Create your models here.

class BoardModel(models.Model):
    """an instance of a game board"""
    board_id = models.CharField(max_length=256, blank=False, primary_key = True)

    def __str__(self):
        return self.board_id

class DinoModel(models.Model):
    """an instance of a dinosaur"""

    #each robot is associated with a board
    board_id = models.ForeignKey(BoardModel, on_delete=models.CASCADE)

    #location of the dino on the board
    position_row = models.IntegerField()
    position_column = models.IntegerField()

    def __str__(self):
        return str(self.id)

class RobotModel(models.Model):
    """an instance of a robot"""

    #each robot is associated with a board
    board_id = models.ForeignKey(BoardModel, on_delete=models.CASCADE)

    #location of the robot on the board
    position_row = models.IntegerField()
    position_column = models.IntegerField()

    #which way is the robot facing
    #options will be 'N','S','E','W'
    direction = models.CharField(max_length=6,blank=False)

    def __str__(self):
        return str(self.id)
