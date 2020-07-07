# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from PIL import Image

bp = Blueprint('bitface', __name__, url_prefix='/api/bitface')


def init():
    # 设置每个像素区块的大小
    block_size = 20
    img = Image.open("./a.jpg")
    # 获取图片的宽高
    width, height = img.size
    # 获取像素点对应RGB颜色值，可以改变img_array中的值来改变颜色值
    img_array = img.load()
    # 为了处理最后的区块，加了一次循环
    max_width = width + block_size
    max_height = height + block_size
    for x in range(block_size - 1, max_width, block_size):
        for y in range(block_size - 1, max_height, block_size):
            # 如果是最后一次循环，则x坐标等于width - 1
            if x == max_width - max_width % block_size - 1:
                x = width - 1
            # 如果是最后一次循环，则x坐标等于height - 1
            if y == max_height - max_height % block_size - 1:
                y = height - 1
            # 改变每个区块的颜色值
            change_block(x, y, block_size, img_array)
            y += block_size
        x += block_size
    img.save(r'./awesome_copy.png')


def change_block(x, y, black_size, img_array):
    """
    :param x坐标 x:
    :param y坐标 y:
    :param 区块大小 black_size:
    :param 可操作图片数组 img_array:
    """
    color_dist = {}
    block_pos_list = []
    for pos_x in range(-black_size + 1, 1):
        for pos_y in range(-black_size + 1, 1):
            # todo print(x + pos_x,y + pos_y)
            block_pos_list.append([x + pos_x, y + pos_y])
    for pixel in block_pos_list:
        if not str(img_array[pixel[0], pixel[1]]) in color_dist.keys():
            color_dist[str(img_array[pixel[0], pixel[1]])] = 1
        else:
            color_dist[str(img_array[pixel[0], pixel[1]])] += 1
    # key-->value => value-->key
    new_dict = {v: k for k, v in color_dist.items()}
    max_color = new_dict[max(color_dist.values())]
    # 将区块内所有的颜色值设置为颜色最多的颜色
    for a in block_pos_list:
        img_array[a[0], a[1]] = tuple(list(map(int, max_color[1:len(max_color) - 1].split(","))))


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]


if __name__ == '__main__':
    init()