# coding:utf-8
# 状态：
# S0表示易感者S
# S1表示感染者I
# S2表示治愈者R
# S3表示潜伏者E


# 1. 当S=S0时，为易感者
# 2. 当S=S1时，为感染者
# 3. 当S=S2时，为治愈者
# 4. 当S=S3时,为潜伏者
from pylab import *
import random
import numpy as np
import pygame
import sys
import matplotlib.pyplot as plt

# 初始化相关数据
f_p = 0.8 #感染概率
t1_max=10 #潜伏时间
t_p = 0.1 #治愈概率



def probablity_fun():
    np.random.seed(0)
    # p = np.array([(self.s1_0*k+self.s1_1*l),1-(self.s1_0*k+self.s1_1*l)])
    p = np.array([0.6, 0.4])
    probability = np.random.choice([True, False],
                                   p=p.ravel())  # p(感染or潜伏)=(self.s1_0*k+self.s1_1*l) p(易感)=1-(self.s1_0*k+self.s1_1*l)
    return probability

RED = (255, 0, 0)
GREY = (127, 127, 127)
Green = (0, 255, 0)
BLACK = (0, 0, 0)

"""细胞类，单个细胞"""
class Cell:
    # 初始化
    stage = 0

    def __init__(self, ix, iy, stage):
        self.ix = ix
        self.iy = iy
        self.stage = stage            #状态，初始化默认为0，易感者
        # self.neighbour_count = 0    #周围细胞的数量
        self.s1_0 = 0                 #上下左右为感染者的数量
        self.s1_1 = 0                 #左上左下右上右下感染者的数量
        self.T_ = 0                   #免疫时间 此处设置
        self.t_ = 0                   #患病时间
        self.t1_ = 0                  #潜伏时间

    # 计算周围有多少个感染者
    def calc_neighbour_count(self):
        count_0 = 0
        count_1 = 0
        pre_x = self.ix - 1 if self.ix > 0 else 0
        for i in range(pre_x, self.ix+1+1):
            pre_y = self.iy - 1 if self.iy > 0 else 0
            for j in range(pre_y, self.iy+1+1):
                if i == self.ix and j == self.iy:   # 判断是否为自身
                    continue
                if self.invalidate(i, j):           # 判断是否越界
                    continue
                if CellGrid.cells[i][j].stage == 1 or CellGrid.cells[i][j].stage == 3 :  #此时这个邻居是感染者
                    #如果是在上下左右
                    if (i==self.ix and j==self.iy-1) or \
                       (i==self.ix and j==self.iy+1) or \
                       (i==self.ix-1 and j==self.iy) or \
                       (i==self.ix+1 and j==self.iy):
                        count_0+=1
                    else:
                        count_1+=1
        # print(count_0)
        self.s1_0 = count_0
        # if self.s1_1!=0:
        #     print(count_1,count_0,self.ix,self.iy)
        self.s1_1 = count_1

    # 判断是否越界
    def invalidate(self, x, y):
        if x >= CellGrid.cx or y >= CellGrid.cy:
            return True
        if x < 0 or y < 0:
            return True
        return False

    # 定义规则
    def next_iter(self):
        # 规则1，易感者
        if self.stage==0:
            probability=random.random()#生成0到1的随机数
            s1_01 = self.s1_0+self.s1_1
            if (probability<f_p) and (s1_01!=0):
                self.stage=3
            else:
                self.stage = 0
        # 规则2，感染者
        elif self.stage == 1:
            p1 = random.random()
            if p1<t_p:
                self.stage = 2
        # 规则3，治愈者(永久免疫规则)
        elif self.stage == 2:
            pass
        # 规则4,潜伏者
        elif self.stage == 3:
            p1 = random.random()
            if p1<(1/t1_max):
                self.stage = 1


"""细胞网格类，处在一个长cx,宽cy的网格中"""
class CellGrid:

    cells = []
    cx = 0
    cy = 0

    # 初始化
    def __init__(self, cx, cy):
        CellGrid.cx = cx
        CellGrid.cy = cy
        for i in range(cx):
            cell_list = []
            for j in range(cy):
                cell = Cell(i, j, 0)            #首先默认为全是易感者or (i==cx/2+1 and j==cy/2) or (i==cx/2+1 and j==cy/2+1)
                if (i == cx/2 and j ==cy/2):#看26行就可以了
                    cell_list.append(Cell(i,j,3))
                else:
                    cell_list.append(cell)
            CellGrid.cells.append(cell_list)

    def next_iter(self):
        for cell_list in CellGrid.cells:
            for item in cell_list:
                item.next_iter()

    def calc_neighbour_count(self):
        for cell_list in CellGrid.cells:
            for item in cell_list:
                item.calc_neighbour_count()


    def num_of_nonstage(self):
        # global count0_,count1_,count2_
        count0 = 0
        count1 = 0
        count2 = 0
        count3 = 0
        for i in range(self.cx):
            for j in range(self.cy):
                # 计算全部的方格数
                cell = self.cells[i][j].stage
                if cell == 0:
                    count0 += 1
                elif cell == 1:
                    count1 += 1
                elif cell == 2:
                    count2 += 1
                elif cell == 3:
                    count3 += 1
        return count0, count1, count2, count3

'''界面类'''
class Game:
    screen = None
    count0 = 0
    count1 = 9
    count2 = 0
    count3 = 0
    def __init__(self, width, height, cx, cy):#屏幕宽高，细胞生活区域空间大小
        self.width = width
        self.height = height
        self.cx_rate = int(width / cx)
        self.cy_rate = int(height / cy)
        self.screen = pygame.display.set_mode([width, height])#
        self.cells = CellGrid(cx, cy)

    def show_life(self):
        for cell_list in self.cells.cells:
            for item in cell_list:
                x = item.ix
                y = item.iy
                if item.stage == 0:
                    pygame.draw.rect(self.screen, GREY,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])
                elif item.stage == 2:
                    pygame.draw.rect(self.screen, Green,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])
                elif item.stage == 1:
                    pygame.draw.rect(self.screen, RED,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])
                elif item.stage == 3:
                    pygame.draw.rect(self.screen, BLACK,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])

    # def count_num(self):
    #     self.count0, self.count1, self.count2,self.count3 = self.cells.num_of_nonstage()
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
if __name__ == '__main__':
    count0_ = []
    count1_ = []
    count2_ = []
    count3_ = []
    pygame.init()
    pygame.display.set_caption("传染病模型")
    game = Game(800, 800, 100, 100)

    clock = pygame.time.Clock()
    k1 = 0
    for i in range(1500):
        k1 += 1
        print(k1)

        # game.screen.fill(GREY)#底部全置灰
        clock.tick(1)  # 每秒循环10次
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        game.cells.calc_neighbour_count()
        count0, count1, count2,count3 = game.cells.num_of_nonstage()
        # count0,count1,count2 = game.count_num()
        count0_.append(count0)
        count1_.append(count1)
        count2_.append(count2)
        count3_.append(count3)
        if count2 > 200*190:  # 退出条件
            break

        plt.plot(count0_, color='r', label='易感者')
        plt.plot(count3_, color='b', label='潜伏者')
        plt.plot(count1_, color='y', label='感染者')
        plt.plot(count2_, color='g', label='治愈者')
        # plt.ylim([0,80000])
        plt.legend()
        plt.xlabel('时间单位')
        plt.ylabel('人数单位')
        plt.pause(1)#0.1秒停一次
        plt.clf()#清除

        # plt.close()#退出
        game.show_life()
        pygame.display.flip()
        game.cells.next_iter()

    # plt.show()#显示