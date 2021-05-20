'''
MIT License

Copyright (c) 2021 Masanori Hirata(ch-suginami)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from PIL import Image, ImageDraw, ImageFont
import sys, os

BOARD_COORDS = 15
FIG_SIZE = 1020
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FRAME_LEFT = 70
FRAME_TOP = 40
BETWEEN = 65
LINE_WIDTH = 2
DOTS  = 5
STONE = 28
ALPHABET = [chr(ord('A') + i) for i in range(26)]

# font setting
font_coords = ImageFont.truetype('SourceHanSans-Normal.otf', 26)
font_num = ImageFont.truetype('SourceHanSans-Normal.otf', 26)

# drawing lines
def draw_pos(drawing):
    for i in range(BOARD_COORDS):
        if i == 0 or i== 14:
            drawing.line((FRAME_LEFT + i*BETWEEN, FRAME_TOP - LINE_WIDTH, FRAME_LEFT + i*BETWEEN, FRAME_TOP + (BOARD_COORDS-1)*BETWEEN + LINE_WIDTH), fill = BLACK, width = 5)
            drawing.line((FRAME_LEFT - LINE_WIDTH, FRAME_TOP + i*BETWEEN, FRAME_LEFT + (BOARD_COORDS-1)*BETWEEN + LINE_WIDTH, FRAME_TOP + i*BETWEEN), fill = BLACK, width = 5)
        else:
            drawing.line((FRAME_LEFT + i*BETWEEN, FRAME_TOP, FRAME_LEFT + i*BETWEEN, FRAME_TOP + (BOARD_COORDS-1)*BETWEEN + LINE_WIDTH), fill = BLACK, width = 1)
            drawing.line((FRAME_LEFT, FRAME_TOP + i*BETWEEN, FRAME_LEFT + (BOARD_COORDS-1)*BETWEEN, FRAME_TOP + i*BETWEEN), fill = BLACK, width = 1)
    # drawing dots
    drawing.ellipse((FRAME_LEFT + 3*BETWEEN - DOTS, FRAME_TOP + 3*BETWEEN - DOTS, FRAME_LEFT + 3*BETWEEN + DOTS, FRAME_TOP + 3*BETWEEN + DOTS), fill = BLACK, outline = BLACK)
    drawing.ellipse((FRAME_LEFT + 3*BETWEEN - DOTS, FRAME_TOP + 11*BETWEEN - DOTS, FRAME_LEFT + 3*BETWEEN + DOTS, FRAME_TOP + 11*BETWEEN + DOTS), fill = BLACK, outline = BLACK)
    drawing.ellipse((FRAME_LEFT + 11*BETWEEN - DOTS, FRAME_TOP + 3*BETWEEN - DOTS, FRAME_LEFT + 11*BETWEEN + DOTS, FRAME_TOP + 3*BETWEEN + DOTS), fill = BLACK, outline = BLACK)
    drawing.ellipse((FRAME_LEFT + 11*BETWEEN - DOTS, FRAME_TOP + 11*BETWEEN - DOTS, FRAME_LEFT + 11*BETWEEN + DOTS, FRAME_TOP + 11*BETWEEN + DOTS), fill = BLACK, outline = BLACK)
    drawing.ellipse((FRAME_LEFT + 7*BETWEEN - DOTS, FRAME_TOP + 7*BETWEEN - DOTS, FRAME_LEFT + 7*BETWEEN + DOTS, FRAME_TOP + 7*BETWEEN + DOTS), fill = BLACK, outline = BLACK)
    return drawing

# drawing letters of coordinates
def draw_letters(drawing):
    for i in range(1, BOARD_COORDS + 1):
        if i < 10:
            drawing.text((18, (BOARD_COORDS - i)*BETWEEN + 20), str(i), font = font_coords, fill = BLACK)
        else:
            drawing.text((10, (BOARD_COORDS - i)*BETWEEN + 20), str(i), font = font_coords, fill = BLACK)
        drawing.text((i*BETWEEN - 3, FIG_SIZE - 40), ALPHABET[i-1], font = font_coords, fill = BLACK)
    return drawing

# convert alphabet to number
def conv2num(letter):
    return ALPHABET.index(letter)

# drawing stones
def draw_stones(drawing, pos_x, pos_y, color, num = 0, last = False):
    DIFF = 8
    if color == "B":
        drawing.ellipse((FRAME_LEFT + pos_x*BETWEEN - STONE, FRAME_TOP + pos_y*BETWEEN - STONE, FRAME_LEFT + pos_x*BETWEEN + STONE, FRAME_TOP + pos_y*BETWEEN + STONE), fill = BLACK, outline = BLACK)
        if num >= 10:
            drawing.text((FRAME_LEFT + pos_x*BETWEEN - STONE//2, FRAME_TOP + pos_y*BETWEEN - STONE*3//4), str(num), font = font_num, fill = WHITE)
        elif 0 < num < 10:
            drawing.text((FRAME_LEFT + pos_x*BETWEEN - STONE//4, FRAME_TOP + pos_y*BETWEEN - STONE*3//4), str(num), font = font_num, fill = WHITE)
        if last:
            drawing.ellipse((FRAME_LEFT + pos_x*BETWEEN - int(DOTS*0.7), FRAME_TOP + pos_y*BETWEEN - STONE//2 - int(DOTS*0.7) - DIFF, FRAME_LEFT + pos_x*BETWEEN + int(DOTS*0.7), FRAME_TOP + pos_y*BETWEEN - STONE//2 + int(DOTS*0.7) - DIFF), fill = WHITE, outline = BLACK)
    else:
        drawing.ellipse((FRAME_LEFT + pos_x*BETWEEN - STONE, FRAME_TOP + pos_y*BETWEEN - STONE, FRAME_LEFT + pos_x*BETWEEN + STONE, FRAME_TOP + pos_y*BETWEEN + STONE), fill = WHITE, outline = BLACK)
        if num >= 10:
            drawing.text((FRAME_LEFT + pos_x*BETWEEN - STONE//2, FRAME_TOP + pos_y*BETWEEN - STONE*3//4), str(num), font = font_num, fill = BLACK)
        elif 0 < num < 10:
            drawing.text((FRAME_LEFT + pos_x*BETWEEN - STONE//4, FRAME_TOP + pos_y*BETWEEN - STONE*3//4), str(num), font = font_num, fill = BLACK)
        if last:
            drawing.ellipse((FRAME_LEFT + pos_x*BETWEEN - int(DOTS*0.7), FRAME_TOP + pos_y*BETWEEN - STONE//2 - int(DOTS*0.7) - DIFF, FRAME_LEFT + pos_x*BETWEEN + int(DOTS*0.7), FRAME_TOP + pos_y*BETWEEN - STONE//2 + int(DOTS*0.7) - DIFF), fill = BLACK, outline = BLACK)
    return drawing

# draw letters for explanations
def draw_tree(drawing, pos_x, pos_y, letter):
    BOX = 25
    drawing.rectangle((FRAME_LEFT + pos_x*BETWEEN - BOX, FRAME_TOP + pos_y*BETWEEN - BOX, FRAME_LEFT + pos_x*BETWEEN + BOX, FRAME_TOP + pos_y*BETWEEN + BOX), fill = WHITE)
    drawing.text((FRAME_LEFT + pos_x*BETWEEN - STONE//4, FRAME_TOP + pos_y*BETWEEN - STONE*3//4), letter, font = font_num, fill = BLACK)
    return drawing

# splitting notation
def split_notation(file_in):
    notation = []
    ans = []
    with open(file_in, 'r') as f:
        # read dummy data
        for _ in range(3):
            data = f.readline()
        data = f.readline().split(';')
        # when choice of swap
        if data[1][0:3] == 'QPR':
            notation.append([0, 'B', data[1][4:6]])
            notation.append([0, 'W', data[1][7:9]])
            notation.append([0, 'B', data[1][10:12]])
            if data[2] == 'QSLB[]':
                for i in range(3, len(data)):
                    notation.append([1, data[i][0], data[i][2:4]])
            else:
                notation.append([3, 'W', data[2][5:7]])
                for i in range(3, len(data)):
                    notation.append([i+1, data[i][0], data[i][2:4]])
        for i in range(1, len(data)):
            notation.append([i-1, data[i][0], data[i][2:4]])
        num = int(f.readline())
        tree = int(f.readline())
        for i in range(tree):
            data = f.readline().split(',')
            data[-1] = data[-1].replace('\n', '')
            wr_data = []
            for j in range(len(data)):
                n_data = data[j].split('[')
                wr_data.append([n_data[0], n_data[1][:-1]])
            ans.append(wr_data)
    return [num, notation, ans]

#main part
def main():
    args = sys.argv
    if len(args) != 2:
        print('Wrong Input!')
        sys.exit()

    notation = split_notation(args[1])

    im_q = Image.new('RGB', (FIG_SIZE, FIG_SIZE), WHITE)
    im_a = Image.new('RGB', (FIG_SIZE, FIG_SIZE), WHITE)
    draw_q = ImageDraw.Draw(im_q)
    draw_a = ImageDraw.Draw(im_a)
    draw_q = draw_pos(draw_q)
    draw_a = draw_pos(draw_a)
    draw_q = draw_letters(draw_q)
    draw_a = draw_letters(draw_a)

    # drawing base
    for i in range(notation[0]):
        if i == notation[0] - 1:
            pos_x = conv2num(notation[1][i][2][0].upper())
            pos_y = conv2num(notation[1][i][2][1].upper())
            draw_q = draw_stones(draw_q, pos_x, pos_y, notation[1][i][1], last = True)
            draw_a = draw_stones(draw_a, pos_x, pos_y, notation[1][i][1])
            # odd = Black, even = White
            order = i % 2 + 1
        else:
            pos_x = conv2num(notation[1][i][2][0].upper())
            pos_y = conv2num(notation[1][i][2][1].upper())
            draw_q = draw_stones(draw_q, pos_x, pos_y, notation[1][i][1])
            draw_a = draw_stones(draw_a, pos_x, pos_y, notation[1][i][1])

    fq_out = "Q" + os.path.splitext(os.path.basename(args[1]))[0] + '.png'
    im_q.save(fq_out)

    # drawing answer part
    for i in range(len(notation[2])):
        fa_out = "A" + os.path.splitext(os.path.basename(args[1]))[0]+ '_' + str(i+1) + '.png'
        im_ai = im_a.copy()
        draw_ai = ImageDraw.Draw(im_ai)
        for j in range(len(notation[2][i])):
            letter = notation[2][i][j][0]
            if (order + 1) % 2 == 0:
                color = 'W'
            else:
                color = 'B'
            if letter.isdecimal():
                pos_x = conv2num(notation[2][i][j][1][0].upper())
                pos_y = BOARD_COORDS - int(notation[2][i][j][1][1:])
                draw_ai = draw_stones(draw_ai, pos_x, pos_y, color = color, num = int(letter))
            else:
                pos_x = conv2num(notation[2][i][j][1][0].upper())
                pos_y = BOARD_COORDS - int(notation[2][i][j][1][1:])
                draw_ai = draw_tree(draw_ai, pos_x, pos_y, letter)
            order += 1
        im_ai.save(fa_out)

if __name__ == '__main__':
    main()