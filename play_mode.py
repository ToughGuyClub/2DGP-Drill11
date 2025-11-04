import random
from pico2d import *

import game_framework
import game_world

from boy import Boy
from grass import Grass
from ball import Ball
from zombie import Zombie

boy = None
balls=[]
def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global boy
    global balls
    #잔디도 충돌처리를 위해 dict에 넣기
    grass = Grass()
    game_world.add_object(grass, 0)
    game_world.add_collision_pair('grass:ball', grass, None)  #그룹, a,b형태임 [[grass],[]] 이런 리스트가 만들어짐

    boy = Boy()
    game_world.add_object(boy, 1)
    game_world.add_collision_pair('boy:zombie', boy,None)

    balls =[Ball(random.randint(100, 1500), 60,0) for i in range(10)]
    game_world.add_objects(balls, 1)

    # 소년-공 사이에 대한 충돌검사가 필요하다는 정보 추가
    game_world.add_collision_pair('boy:ball',boy,None)  # 그룹,a,b형태임 [[boy],[]] 이런 리스트가 만들어짐
    for ball in balls:  #리스트를 함수에 넣는거 구현안해놔서 for문으로 하나씩 넣어야함
        game_world.add_collision_pair('boy:ball',None,ball)     # [[boy],[ball,ball,ball...]]이렇게 들어가있음

    #좀비 한번 생성해봄
    zombie=[Zombie() for i in range(5)]
    game_world.add_objects(zombie,1)
    for z in zombie:
        game_world.add_collision_pair('zombie:ball',z,None)
        game_world.add_collision_pair('boy:zombie',None,z)


def update():
    game_world.update()
    # global boy
    # for ball in balls.copy():   #카피본을 만들어서 검사하면 더 안정적이라고함
    #     if game_world.collide(boy, ball):
    #         print('충돌')
    #         boy.ball_count += 1
    #         game_world.remove_object(ball)
    #         #게임월드에서도 제거하고 이 balls리스트에서도 제거해야함
    #         balls.remove(ball)
    game_world.handle_collisions()



def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass

