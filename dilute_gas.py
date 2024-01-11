# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 15:03:02 2024

@author: replica
"""

### 필요한 라이브러리 선언 ###
from vectortools import *
from atom import *
import sys
### 필요한 라이브러리 선언 ###

#=============== 새로 추가된 부분 ===============#
e = 100 # 상수 설정
softening_length = 0 # 아직뭔지 몰라도 됨.
L = 10
class Atom(Atom):
    def __init__(self, element, pos, vel = Vector(0, 0)):
        self.element = element
        self.pos = pos
        self.vel = vel
        
    ### 상호작용 추가 ###
    def acc(self, other):
        r = self.pos - other.pos
        if not self == other and r.dot(r) < (10*L)**2:
            r_ = L/(abs(r)+softening_length)
            return 4*e*(12*r_**14-6*r_**8)*r/(L**2)
        else:
            return Vector(0, 0)
    ### 상호작용 추가 ###
        
        
class Simulator(Simulator):
    def __init__(self, dt, world, render, grid_size = 100):
        self.dt = dt
        self.world = world
        self.render = render
        self.count_screen = 0
        self.count_snapshot = 0
        self.grid_size = grid_size
        self.grid = None
        
    def main(self):
        x_ = []
        v_ = []
        self.make_grid()
        for atom in self.world.atoms:
            atom_acc = Vector(0, 0)
            ### 상호작용 추가 ###
            atoms = self.get_near_atoms(atom)
            for other_atom in atoms:
                #self.render.polygon([atom.pos, other_atom.pos], red)
                atom_acc += atom.acc(other_atom)
            new_v = atom.vel + atom_acc*self.dt + self.world.gravity*self.dt# - 0.1*atom.vel*self.dt
            ### 상호작용 추가 ###
            v_.append(new_v)
            x_.append(atom.pos + new_v*self.dt)
        
        count = 0
        for atom in self.world.atoms:
            atom.pos = x_[count]
            atom.vel = v_[count]
            count = count + 1
#=============== 새로 추가된 부분 ===============#

### render 설정 ###
# 시뮬레이션 화면에 뭔가 그리는 함수는 다 render에 있음
width = 800 #시뮬레이션 공간의 가로길이
height = 800 #시뮬레이션 공간의 세로길이
screen = pg.display.set_mode((width, height)) # 시뮬레이션 화면 설정

render = Render(screen, width, height) # render 설정
### render 설정 ###

### 시뮬레이션 업데이트 시간 설정 ###
clock = pg.time.Clock()
### 시뮬레이션 업데이트 시간 설정 ###

### 색깔 선언 ###
black = pg.Color('black')
white = pg.Color('white')
red = pg.Color('red')
green = pg.Color('green')
blue = pg.Color('blue')
### 색깔 선언 ###

### 벽 선언 ###
# Wall(가로 길이, 세로 길이, 회전 각도, 중심의 위치 벡터, 색깔)
wall1 = Wall(800, 50, 0, Vector(-400, -400), blue)
wall2 = Wall(50, 800, 0, Vector(-400, -400), blue)
wall3 = Wall(50, 800, 0, Vector(350,-400), blue)
wall4 = Wall(800, 50, 0, Vector(-400, 350), blue)
# wall5 = Wall(100, 50, m.pi/4, Vector(-300, 0), blue)
### 벽 선언 ###

### 원소 선언 ###
# Element(원소의 이름, 질량, 반지름, 색깔)
e1 = Element(name = 'Helium', mass = 1, radius = 3, color = red)
### 원소 선언 ###

### 원자 선언 ###
# Atom(원소, 위치벡터, 속도벡터(디폴트 0벡터))
# atom1 = Atom(e1, Vector(-200, 0), Vector(50, 0))
# atom2 = Atom(e1, Vector(0, 0))
# atom3 = Atom(e1, Vector(25, -10))
# atom4 = Atom(e1, Vector(25, 10))
# atom5 = Atom(e1, Vector(50, -20))
# atom6 = Atom(e1, Vector(50, 0))
# atom7 = Atom(e1, Vector(50, 20))
### 원자 선언 ###

### 벽들과 원자들 선언 ###
walls = [wall1, wall2, wall3, wall4]
# atoms = [atom1, atom2, atom3, atom4, atom5, atom6, atom7]


#=============== 새로 추가된 부분 ===============#
### 2체 문제 ###
# e2 = Element(name = 'Heavy', mass = 100, radius = 10, color = blue)
# atom1 = Atom(e1, Vector(20, 0), Vector(0, 0))
# atom2 = Atom(e1, Vector(0, 0), Vector(0, 0))
# walls = []
# atoms = [atom1, atom2]
### 2체 문제 ###

# ### 3체 문제 ###
# atom1 = Atom(e1, Vector(200, 0), Vector(0, 0))
# atom2 = Atom(e1, Vector(0, -200), Vector(0, 0))
# atom3 = Atom(e1, Vector(-200, 50), Vector(0, 0))
# walls = []
# atoms = [atom1, atom2, atom3]
# ### 3체 문제 ###

## 구상성단 코드 ###
# walls = []
import random
atoms = []
for i in range(-10,10):
    for j in range(-10,10):
        position =  Vector(35*i + 25 + 10*random.random(), 35*j + 25 + 10*random.random())
        atoms.append(Atom(e1, position))
## 구상성단 코드 ###
#=============== 새로 추가된 부분 ===============#


### 벽들과 원자들 선언 ###

### 시뮬레이션 전체 외력(외부 가속도) 설정 ###
gravity = Vector(0, 0)
### 시뮬레이션 전체 외력(외부 가속도) 설정 ###

### 시뮬레이션 월드 선언 ###
# World(초기시간, 원자들, 벽들, 외부 가속도)
world = World(0, atoms, walls, gravity)
### 시뮬레이션 월드 선언 ###

### 시뮬레이터 선언 ###
# Simulator(시간간격, 시뮬레이션 월드, 렌더)
simulator = Simulator(0.01, world, render, 10*L)
### 시뮬레이터 선언 ###

### 기존 시뮬레이션 스냅샷을 로드하는 코드 ###
#simulator.load_snapshot('snapshots/pocket_ball_demo/snapshot_00000700.txt')
### 기존 시뮬레이션 스냅샷을 로드하는 코드 ###

while True:
    ### 시뮬레이션 시간 출력 ###
    # 꼭 필요한 코드가 아니지만 시뮬레이션 시간을 출력하려면 
    # 이렇게 할 수 있다는 걸 보여줄려고 추가한 코드 
    t = simulator.clock()
    print(t)
    ### 시뮬레이션 시간 출력 ###
    
    ### 시뮬레이션 메인 부분 ###
    simulator.draw_background(white) #시뮬레이션 배경화면 그리기
    simulator.draw_grid(100) #격자그리기
    simulator.draw_wall() #벽그리기
    simulator.atom_wall_collision() #원자와 벽 사이의 충돌 고려
    #simulator.atom_atom_collision() #원자와 원자 사이의 충돌 고려 
    #simulator.atom_atom_fusion() #원자와 원자의 병합 고려
    simulator.main() #원자의 위치와 속력을 업데이트 하는 함수
    simulator.draw_atom() # 원자 그리기
    ### 시뮬레이션 메인 부분 ###

    ### 시뮬레이션 화면에 텍스트 그리기 ###
    # render.text(텍스트, 폰트, 크기, 위치벡터, 색깔)
    # render.text('pos = (%.2f, %.2f)'%(atom1.pos.x, atom1.pos.y) , None, 30, Vector(atom1.pos.x -100, atom1.pos.y - 30), black)
    # render.text('vel = (%.2f, %.2f)'%(atom1.vel.x, atom1.vel.y) , None, 30, Vector(atom1.pos.x -100, atom1.pos.y - 50), black)

    # render.text('pos = (%.2f, %.2f)'%(atom7.pos.x, atom7.pos.y) , None, 30, Vector(atom7.pos.x -100, atom7.pos.y - 30), blue)
    # render.text('vel = (%.2f, %.2f)'%(atom7.vel.x, atom7.vel.y) , None, 30, Vector(atom7.pos.x -100, atom7.pos.y - 50), blue)
    ### 시뮬레이션 화면에 텍스트 그리기 ###
    
    ### 이거 없음 에러남 ###
    for event in pg.event.get():
       if event.type == pg.QUIT:
           sys.exit()
    ### 이거 없음 에러남 ###
    
    ### 시뮬레이션 화면 업데이트 ###
    clock.tick(100)# 시뮬레이션 화면 업데이트 시간간격
    pg.display.update() #시뮬레이션 화면 업데이트
    ### 시뮬레이션 화면 업데이트 ###
        
    ### 매시간 마다 시뮬레이션 화면을 png로 저장하는 코드 ###
    # simulator.save_screen(저장위치, 건너뛸 개수(디폴트 0))
    #simulator.save_screen('images/pocket_ball_demo')
    ### 매시간 마다 시뮬레이션 화면을 png로 저장하는 코드 ###
    
    ### 매시간 마다 시뮬레이션 스냅샷을 저장하는 코드 ###
    # simulator.save_screen(저장위치, 건너뛸 개수(디폴트 0))
    #simulator.save_snapshot('snapshots/pocket_ball_demo', 99)
    ### 매시간 마다 시뮬레이션 스냅샷을 저장하는 코드 ###
