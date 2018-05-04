#-*- coding:utf-8 -*-


import curses
from random import randrange, choice
from collections import defaultdict
from QiPan import GameField



actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']

actions_dict = dict(zip(letter_codes, actions*2))



def get_user_action(keyboard):
    char = "N"
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]


def invert(self, field):
    """矩阵的逆转，但不是逆矩阵"""
    #相当于矩阵的左右调换了一下
    return row[::-1] for row in field


    #矩阵的转置！！！！
def transpose(self, field):
    """实现矩阵的转置"""
    return [list(row) for row in zip(*field)]



        
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
        state = state_actions(state)()




curses.wrapper(main)
