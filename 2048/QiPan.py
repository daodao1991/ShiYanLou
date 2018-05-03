"""一个用于创建字符棋盘的类"""


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
        (i,j) = choice([(i,j) for i in range(self.width) for j in range(self.heigh) \
                        if self.field[i][j] == 0])
        self.field[i][j] = new_element



    def invert(self, field):
        """矩阵的逆转，但不是逆矩阵"""
        #相当于矩阵的左右调换了一下
        return row[::-1] for row in field


        #矩阵的转置！！！！
    def transpose(self, field):
        """实现矩阵的转置"""
        return [list(row) for row in zip(*field)]



        
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




    def move(self, direction):
        
        def move_row_left(row):
            """实现将某一行的非零元素移动到左边，且相邻的相同元素相加"""            
            def move_lef(row):
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
            return move_lef(merge(move_lef(row)))


        moves = {}
        moves['Left']  = lambda field_1: [move_row_left(row) for row in field_1]
        moves['Right'] = lambda field_2: self.invert(moves['left'](self.invert(field_2)))
        
        #上、下这两个动作很巧妙地使用了矩阵的转置
        moves['Up']    = lambda field_3: self.transpose(moves['Left'](self.transpose(field_3)))
        moves['Down']  = lambda field_4: self.transpose(moves['Right'](self.transpose(field_4)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False


        
    def move_is_possible(self, direction):
        """判断是否能够进行此步动作"""

        def 
            
                        
                























            
            
