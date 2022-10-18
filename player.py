from math import floor

import cairosvg
import numpy as np
import pyautogui as pyautogui
from PIL import Image
from paddleocr import PaddleOCR
from paddleocr.tools.infer.utility import draw_ocr

ocr = PaddleOCR(use_angle_cls=False, drop_score=0.1, lang='en',)


def click(_squares, _values, _width, _height, x, y):
    click_square = _squares[x * _width + y]
    click_left = click_square.left + click_square.width / 2
    click_top = click_square.top + click_square.height / 2
    pyautogui.leftClick(x=click_left, y=click_top)
    pyautogui.sleep(1.5)
    top_left_sq, bottom_right_sq = _squares[0], _squares[len(_squares) - 1]
    board_width, board_height = bottom_right_sq.left + bottom_right_sq.width - top_left_sq.left, \
                                bottom_right_sq.top + bottom_right_sq.height - top_left_sq.top
    board_im = pyautogui.screenshot(region=(top_left_sq.left, top_left_sq.top, board_width, board_height),
                                    imageFilename='tmp.png')
    data = ocr.ocr('tmp.png', det=True, rec=True, cls=False,)
    result = [hit[0] for hit in data[0]]
    image = Image.open('tmp.png').convert('RGB')
    im_show = draw_ocr(image, result, txts=None, scores=None)
    im_show = Image.fromarray(im_show)
    im_show.save('result.png')
    print(data)
    for hit in data[0]:
        bounding_box = hit[0]
        top_left_coord = bounding_box[0]
        number = hit[1][0]
        hit_x = int(round(_width * (top_left_coord[0]) / board_width))
        hit_y = int(round(_height * (top_left_coord[1]) / board_height))
        print("Number: {} | pos:{},{}".format(number, hit_x, hit_y))
        for ix, digit in enumerate(number):
            if digit.isdigit():
                digit = int(digit)
                _values[hit_y, hit_x + ix] = digit


squares = pyautogui.locateAllOnScreen('assets/closed.png', confidence=0.97)
squares = list(squares)
width, height = (16, 16)
values = np.zeros((width, height))
click(squares, values, width, height, 5, 4)
click(squares, values, width, height, 7, 5)
click(squares, values, width, height, 11, 11)
print(values)
# for square in squares:
#     print(square)
#     square_im = pyautogui.screenshot(region=square, imageFilename='tmp.jpg')
#     pyautogui.moveTo(square.left, square.top)
#     number = ocr.ocr('tmp.jpg', det=False, cls=False)
#     print(number)


# print(list(squares))
