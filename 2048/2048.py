#!usr/bin/env python
#-*- coding:utf-8 -*-


import curses
from random import randrange, choice
from collections import defaultdict
#from QiPan import GameField



actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']

actions_dict = dict(zip(letter_codes, actions*2))



def get_user_action(keyboard):
    char = "N"
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]


def invert(field):
    """矩阵的逆转，但不是逆矩阵"""
    #相当于矩阵的左右调换了一下
    return row[::-1] for row in field


    #矩阵的转置！！！！
def transpose(field):
    """实现矩阵的转置"""
    return [list(row) for row in zip(*field)]





#"""一个用于创建字符棋盘的类"""


class GameField(object):

    def __init__(self, height = 4, width = 4, win_value = 2048):
        self.height = height
        self.width = width
        self.score = 0
        self.highscore = 0
        self.win_value = win_value
        self.reset()



    
    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        
        #以array形式存储4*4的矩阵
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()




    def spawn(self):
        new_element = 4 if randrange(100)>89 else 2
        (i,j) = choice([(i,j) for i in range(self.width) for j in range(self.height) \
                        if self.field[i][j] == 0])
        self.field[i][j] = new_element



        
    def is_win(self):
        return any([any([num >= self.win_value for num in row]) for row in self.field])


    def is_gameover(self):
        return  not any(self.move_is_possible(move) for move in actions)
    


    
    def draw(self, screen):
        
        def draw_line():
            """画水平分割线"""
            line = '+' + ('+-----'*self.width + '+')[1:]
            separator = defaultdict(lambda: line)
            if not hasattr(draw_line, "counter"):
                draw_line.counter = 0
                
            #绘制语句用screen.addstr('字符串'+'\n')
            screen.addstr(separator[draw_line.counter] + '\n')
            draw_line.counter += 1


          
        def draw_nums(row_num):
            """给定一行数字，如[0, 0, 0, 4]，以列表形式存放，该函数的作用是将其画在screen上"""
            screen.addstr(''.join('|{:^5}'.format(num) if num>0 else '|     ' for num in row_num)
                          +'|'+ '\n')

          
        screen.clear()
        screen.addstr('SCORE:0' + '\n')

        #field相当于矩阵，row相当于行
        for row in self.field:
            draw_line()
            draw_nums(row)
        draw_line()
        
        if self.is_win():
            screen.addstr('          YOU WIN!')
        elif self.is_gameover():
            screen.addstr('          GAME OVER!')
        else:
            screen.addstr('(W)Up (S)Down (A)Left (D)Right'+'\n')
        screen.addstr('     (R)Restart (Q)Exit')   




    def move(self, direction):       
        def move_row_left(row):
            """实现将某一行的非零元素移动到左边，且相邻的相同元素相加"""            
            def move_left(row):
                """实现将某一行的非零元素移动到左边"""
                new = [i for i in row if i != 0]
                zero_remain = [0 for i in range(len(row) - len(new))]
                #两部分列表相加，即实现了非零元素都挪到了列表左侧
                new_row = new + zero_remain

                return new_row


           
            def merge(row):
                """实现相邻的相同元素的合并"""
                new = []
                p = False

                for i in range(len(row)):
                    if p:
                        new.append(2*row[i])
                        p = False
                        self.score += 2*row[i]
                    else:
                        if i+1 < len(row) and row[i] == row[i+1]:
                            new.append(0)
                            p = True
                        else:
                            new.append(row[i])

                #设置一个assert断言，帮助出错时找到错误
                assert len(new) == len(row),'新产生的列表长度应该与原列表长度相同'
                
                return new
            #相邻的相同元素相加后，再次向左移
            return move_left(merge(move_left(row)))


        moves = {}
        moves['Left']  = lambda field_1: [move_row_left(row) for row in field_1]
        moves['Right'] = lambda field_2: invert(moves['left'](invert(field_2)))
        
        #上、下这两个动作很巧妙地使用了矩阵的转置
        moves['Up']    = lambda field_3: transpose(moves['Left'](transpose(field_3)))
        moves['Down']  = lambda field_4: transpose(moves['Right'](transpose(field_4)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False


        
    def move_is_possible(self, direction):
        """判断是否能够进行此步动作"""
        def row_left_is_movable(row):
            """用于检查某一行是否是可向左移动的"""
            def change(i):
                if row[i] == 0 and row[i+1] != 0:
                    return True
                if row[i] != 0 and row[i+1] == row[i]:
                    return True
                return False
            return any(change(i) for i in range(len(row)-1))

        check = {}
        check['Left'] = lambda field_1: any(row_left_is_movable(row) for row in self.field)
        check['Right'] = lambda field_2: check['Left'](invert(field_2))
        check['Up'] = lambda field_3: check['Left'](transpose(field_3))
        check['Down'] = lambda field_4: check['Right'](tranpose(field_4))

        if direction in check:
            return check[direction](self.field)
        else:
            return False
 


        
def main(stdscr):
    def init():
        game_field.reset()
        return 'Game'


    def not_game(state):
        
        #画出Gameover或Win的界面
        game_field.draw(stdscr)
        #读取用户输入得到action，判断是重启游戏还是结束游戏
        action = get_user_action(stdscr)

        #默认是当前状态,没有行为就会一直在当前界面循环
        responses = defaultdict(lambda: state)
        responses['Restart'] = 'Init'
        responses['Exit'] = 'Exit'

        return responses[action]



    def game():
        
        #画出当前棋盘
        game_field.draw(stdscr)
        #读取用户输入得到action
        action = get_user_action(stdscr)

        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'

        return 'Game'



    state_actions = {
            'Init': init,
            'Win': lambda: not_game('Win'),
            'Gameover': lambda: not_game('Gameover'),
            'Game': game  
        }

        
    curses.use_default_colors()
    game_field = GameField(win_value = 32)
    
    state = 'Init'
    #状态机开始循环
    while state != 'Exit':
        state = state_actions[state]()




curses.wrapper(main)
