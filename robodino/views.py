
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from robodino import serializers
from robodino import models
from robodino.gamerules import BOARD_MIN_VALUE, BOARD_MAX_VALUE
from django.core import serializers as jsr
import random



class BoardCreateApiView(APIView):
    #load serializers
    serializer_class = serializers.BoardSerializer

    #if this is a post request
    def post(self,request):

        #grab data
        serializer = self.serializer_class(data=request.data)

        #if data is valid
        if serializer.is_valid():
            #grab value of board_id
            board_id = serializer.validated_data.get('board_id')

            #check if board_id exists
            if models.BoardModel.objects.filter(board_id = board_id).exists():
                #if it exists, return an error
                return Response({'status':'FAILED',
                                 'error': 'BOARD_ID_CONFLICT'},
                                 status = status.HTTP_409_CONFLICT)
            else:
                #otherwise, create a new board
                new_board = models.BoardModel(board_id=board_id)
                new_board.save()
                return Response({'status':'SUCCESS',
                                 'board_id':board_id})

        #if data is invalid
        else:
            return Response(serializer.errors,
                            status = status.HTTP_400_BAD_REQUEST)

#this API was created for testing purposes only
#the goal is to automatically spawn a large number of pieces on the board
class BoardGenerateApiView(APIView):
    #load serializers
    serializer_class = serializers.BoardGenerateSerializer

    #if this is a post request
    def post(self,request):
        #grab data
        serializer = self.serializer_class(data=request.data)

        #if data is valid
        if serializer.is_valid():
            #grab value of board_id
            board_id = serializer.validated_data.get('board_id')

            #how many dinos to spawn
            dinos_spawn_quantity = serializer.validated_data.get('dinos_spawn_quantity')

            #how many robots to spawn
            robots_spawn_quantity = serializer.validated_data.get('robots_spawn_quantity')

            #check if board_id exists
            if models.BoardModel.objects.filter(board_id = board_id).exists():
                #if it exists, return an error
                return Response({'status':'FAILED',
                                 'error': 'BOARD_ID_CONFLICT'},
                                 status = status.HTTP_409_CONFLICT)
            else:
                #otherwise, create a new board
                new_board = models.BoardModel(board_id=board_id)
                new_board.save()

                #due to location conflicts, the actual number of items spawned could be less
                #so keep track of the actual spawns using these counters
                dino_counter = 0
                robot_counter = 0

                #spawn dinos
                for i in range(0,dinos_spawn_quantity):
                    x = random.randint(BOARD_MIN_VALUE,BOARD_MAX_VALUE)
                    y = random.randint(BOARD_MIN_VALUE,BOARD_MAX_VALUE)

                    #if the location is available, spawn item
                    if not position_is_not_available(new_board.board_id, x, y):
                        #if it exists, return an error
                        new_dino = models.DinoModel(board_id=new_board,
                                                    position_row = x,
                                                    position_column = y)
                        new_dino.save()
                        dino_counter += 1

                #spawn robots
                for i in range(0,robots_spawn_quantity):
                    x = random.randint(BOARD_MIN_VALUE,BOARD_MAX_VALUE)
                    y = random.randint(BOARD_MIN_VALUE,BOARD_MAX_VALUE)

                    #if the location is available, spawn item
                    if not position_is_not_available(new_board.board_id, x, y):
                        #if it exists, return an error
                        new_robot = models.RobotModel(board_id=new_board,
                                                      position_row = x,
                                                      position_column = y,
                                                      direction='up')
                        new_robot.save()
                        robot_counter += 1

                return Response({'status':'SUCCESS',
                                 'board_id':board_id,
                                 'dinos_spawned': dino_counter,
                                 'robots_spawned': robot_counter})
        #if data is invalid
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST)

class BoardStatusApiView(APIView):
    #load serializers
    serializer_class = serializers.BoardSerializer

    #if this is a post request
    def post(self,request):
      #grab data
      serializer = self.serializer_class(data=request.data)

      #if data is valid
      if serializer.is_valid():
          board_id = serializer.validated_data.get('board_id')

          #get board object
          target_board = board_is_valid(board_id)

          #if the target board exists
          if target_board:
              #dictionaries to log pieces
              dino_pieces = {}
              robot_pieces={}

              #all dino pieces
              dinos = models.DinoModel.objects.filter(board_id = board_id)
              for dino in dinos:
                  dino_pieces[str((dino.position_row,dino.position_column))] = {'id':dino.id}

              #all robot pieces
              robots = models.RobotModel.objects.filter(board_id = board_id)
              for robot in robots:
                  robot_pieces[str((robot.position_row,robot.position_column))] = {'id':robot.id,
                                                                                   'direction':robot.direction}
              return Response({'status':'SUCCESS',
                               'dino_pieces':dino_pieces,
                               'robot_pieces': robot_pieces})
          else:
              return Response({'status':'FAILED',
                               'error': 'BOARD_ID_FAIL'},
                               status = status.HTTP_404_NOT_FOUND)
      else:
          return Response(
              serializer.errors,
              status = status.HTTP_400_BAD_REQUEST)

class DinoCreateApiView(APIView):
    #load serializers
    serializer_class = serializers.DinoCreateSerializer

    #if this is a post request
    def post(self,request):
        #grab data
        serializer = self.serializer_class(data=request.data)

        #if data is valid
        if serializer.is_valid():
            #grab parameters
            board_id = serializer.validated_data.get('board_id')
            position_row = serializer.validated_data.get('position_row')
            position_column = serializer.validated_data.get('position_column')

            #check if board_id exists
            target_board = board_is_valid(board_id)

            if target_board:
                #is the target location empty
                if position_is_not_available(board_id, position_row, position_column):
                    return Response({'status':'FAILED',
                                     'error': 'POSITION_CONFLICT'},
                                     status = status.HTTP_409_CONFLICT)
                else:
                    #create Dino objects
                    new_dino = models.DinoModel(board_id=target_board,
                                                position_row = position_row,
                                                position_column = position_column)
                    new_dino.save()
                    return Response({'status':'SUCCESS',
                                     'dino_id': new_dino.id,
                                     'board_id':board_id,
                                     'position_row':position_row,
                                     'position_column':position_column})
            else:
                return Response({'status':'FAILED',
                                 'error': 'BOARD_ID_FAIL'},
                                 status = status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST)


class RobotCreateApiView(APIView):
    #load serializers
    serializer_class = serializers.RobotCreateSerializer

    #if this is a post request
    def post(self,request):
        #grab data
        serializer = self.serializer_class(data=request.data)

        #if data is valid
        if serializer.is_valid():
            #grab parameters
            board_id = serializer.validated_data.get('board_id')
            position_row = serializer.validated_data.get('position_row')
            position_column = serializer.validated_data.get('position_column')
            direction = serializer.validated_data.get('direction')

            #check if board_id exists
            target_board = board_is_valid(board_id)
            if target_board:
                #is the location available
                if position_is_not_available(board_id, position_row, position_column):
                    return Response({'status':'FAILED',
                                     'error': 'POSITION_CONFLICT'},
                                     status = status.HTTP_409_CONFLICT)
                else:
                    #create Robot objects
                    new_robot = models.RobotModel(board_id=target_board,
                                                  position_row = position_row,
                                                  position_column = position_column,
                                                  direction = direction)
                    new_robot.save()
                    return Response({'status':'SUCCESS',
                                     'robot_id': new_robot.id,
                                     'board_id':board_id,
                                     'position_row':position_row,
                                     'position_column':position_column,
                                     'direction':direction})
            else:
                return Response({'status':'FAILED',
                                 'error': 'BOARD_ID_FAIL'},
                                 status = status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST)

class RobotMoveApiView(APIView):
    #load serializer
    serializer_class = serializers.RobotMoveSerializer

    #if this is a post request
    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            robot_id = serializer.validated_data.get('robot_id')
            move = serializer.validated_data.get('move')

            #if the robot id is valid
            try:
                robot = models.RobotModel.objects.filter(id = robot_id).get()

                #are we trying to move in the direction the piece is already facing
                if robot.direction == move:
                    #if the direction of move is same the direction the piece is facing
                    #then move one step in that direction

                    #get coordinates for the new position
                    new_position = get_new_position(move,robot.position_row,robot.position_column)
                    print("got new pos")

                    #is the new position within the boundaries of the board
                    if new_position:
                        print("new pos is valid")

                        #ensure location is available
                        if position_is_not_available(robot.board_id, new_position[0], new_position[1]):
                            print(" new post taken")

                            return Response({'status':'FAILED',
                                             'error': 'POSITION_CONFLICT'},
                                             status = status.HTTP_409_CONFLICT)
                        else:
                            #move robot
                            robot.position_row = new_position[0]
                            robot.position_column = new_position[1]
                            robot.save()
                            return Response({'status':'SUCCESS',
                                             'action': 'MOVED',
                                             'position_row':robot.position_row ,
                                             'position_column':robot.position_column})
                    else:
                        return Response({'status':'FAILED',
                                         'error': 'POSITION_OUT_OF_BOUNDS'},
                                         status = status.HTTP_400_BAD_REQUEST)
                else:
                    #if the move is for a different direction,
                    #then just turn the piece
                    robot.direction = move
                    robot.save()
                    return Response({'status':'SUCCESS',
                                     'action': 'TURNED',
                                     'new_direction':robot.direction})

            except:
                return Response({'status':'FAILED',
                                 'error': 'ROBOT_ID_FAIL'},
                                 status = status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )


class RobotAttackApiView(APIView):
    #load serialiers
    serializer_class = serializers.RobotAttackSerializer

    #if this is a post request
    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            robot_id = serializer.validated_data.get('robot_id')

            #dict to track attack results
            attack_status = {}
            try:
                #does this robot exist
                robot = models.RobotModel.objects.filter(id = robot_id).get()

                #attack up
                try:
                    models.DinoModel.objects.filter(board_id = robot.board_id,
                                                    position_row = robot.position_row-1,
                                                    position_column = robot.position_column).get().delete()
                    attack_status['up'] = 'TARGET_DESTROYED'
                except:
                    attack_status['up'] = 'TARGET_NOT_FOUND'

                #attack down
                try:
                    models.DinoModel.objects.filter(board_id = robot.board_id,
                                                    position_row = robot.position_row+1,
                                                    position_column = robot.position_column).get().delete()
                    attack_status['down'] = 'TARGET_DESTROYED'
                except:
                    attack_status['down'] = 'TARGET_NOT_FOUND'

                #attack left
                try:
                    models.DinoModel.objects.filter(board_id = robot.board_id,
                                                    position_row = robot.position_row,
                                                    position_column = robot.position_column-1).get().delete()
                    attack_status['left'] = 'TARGET_DESTROYED'
                except:

                    attack_status['left'] = 'TARGET_NOT_FOUND'

                #attack right
                try:
                    models.DinoModel.objects.filter(board_id = robot.board_id,
                                                    position_row = robot.position_row,
                                                    position_column = robot.position_column+1).get().delete()
                    attack_status['right'] = 'TARGET_DESTROYED'
                except:
                    attack_status['right'] = 'TARGET_NOT_FOUND'

                return Response({'status':'SUCCESS',
                                 'action': 'ATTACKED',
                                 'results': attack_status})

            except:
                return Response({'status':'FAILED',
                                 'error': 'ROBOT_ID_FAIL'},
                                 status = status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

#check if the board exists
def board_is_valid(board_id):
    target_board = models.BoardModel.objects.filter(board_id = board_id).first()
    if target_board:
        return target_board
    else:
        return False

#calculate new position of robot
def get_new_position(direction, position_row, position_column):
    if direction == 'up':
        if (position_row-1)< BOARD_MIN_VALUE:
            return False
        position_row -= 1
    elif direction == 'down':
        if (position_row+1)>BOARD_MAX_VALUE:
            return False
        position_row += 1
    elif direction == 'left':
        if (position_column-1)<BOARD_MIN_VALUE:
            return False
        position_column -= 1
    elif direction == 'right':
        if (position_column+1)>BOARD_MAX_VALUE:
            return False
        position_column += 1
    new_position = (position_row,position_column)
    return(new_position)

#check if a certain location is available
def position_is_not_available(board_id, position_row, position_column):
    if models.DinoModel.objects.filter(board_id = board_id,
                                       position_row = position_row,
                                       position_column = position_column).exists() or models.RobotModel.objects.filter(board_id = board_id,
                                                                                                                       position_row = position_row,
                                                                                                                       position_column = position_column).exists():
        return True
    else:
        return False
