# /!usr/bin/env python
# encoding=utf-8
import os
from random import uniform, shuffle
from cStringIO import StringIO
from PIL import ImageFont, Image, ImageDraw
import numpy
import pylab
from mpl_toolkits.mplot3d import Axes3D
from argparse import ArgumentParser


def preprocess(len_of_txt):
    variable_dic = {}
    if len_of_txt == 3:
        rstride = 1
        cstride = 1
        zlim1 = -1.3
        zlim2 = 1.3
        xlim1 = 1.1
        xlim2 = 1.9
        ylim1 = 1.9
        ylim2 = 1.1
        elev = 80
        azim = -90

    if len_of_txt == 5:
        rstride = 1
        cstride = 1
        zlim1 = -1.3
        zlim2 = 1.3
        xlim1 = 1.1
        xlim2 = 1.9
        ylim1 = 1.9
        ylim2 = 1.1
        elev = 80
        azim = -90

    if len_of_txt == 8:
        rstride = 1
        cstride = 2
        zlim1 = -1.1
        zlim2 = 1.1
        xlim1 = 1.1
        xlim2 = 1.9
        ylim1 = 1.9
        ylim2 = 1.1
        elev = 80
        azim = -90

    else:
        rstride = 1
        cstride = 1
        zlim1 = -1.3
        zlim2 = 1.3
        xlim1 = 1.1
        xlim2 = 1.9
        ylim1 = 1.9
        ylim2 = 1.1
        elev = 80
        azim = -90
    variable_dic = {'rstride': rstride, 'cstride': cstride, 'zlim1': zlim1, 'zlim2': zlim2,
                    'xlim1': xlim1, 'xlim2': xlim2, 'ylim1': ylim1, 'ylim2': ylim2, 'elev': elev, 'azim': azim}
    return variable_dic


def make_image(text, font_path, len_text, width=400, height=200, angle=None):
    '''Generate a 3d CAPTCHA image.
    Args:
        text: Text in the image.
        width: Image width in pixel.
        height: Image height in pixel.
        angle: The angle between text and X axis.
        len_text: calculate the best param for that len
    Returns:
        Binary data of CAPTCHA image in PNG format.
    '''
    variables = preprocess(len_text)
    angle = angle if angle != None else uniform(-20, 20)
    try:
        font = ImageFont.truetype(font_path, 24)
    except IOError:
        raise IOError(
            'Font file doesn\'t exist. Please set `font_path` correctly.')
    txtW, txtH = font.getsize(text)
    img = Image.new('L', (txtW * 3, txtH * 3), 255)
    drw = ImageDraw.Draw(img)
    drw.text((txtW, txtH), text, font=font)

    fig = pylab.figure(figsize=(width/100.0, height/100.0))
    ax = Axes3D(fig)
    X, Y = numpy.meshgrid(range(img.size[0]), range(img.size[1]))
    Z = 1 - numpy.asarray(img) / 255
    ax.plot_wireframe(
        X, -Y, Z, rstride=variables['rstride'], cstride=variables['cstride'])
    ax.set_zlim((variables['zlim1'], variables['zlim2']))
    ax.set_xlim((txtW * variables['xlim1'], txtW * variables['xlim2']))
    ax.set_ylim((-txtH * variables['ylim1'], -txtH * variables['ylim2']))
    ax.set_axis_off()
    ax.view_init(elev=variables['elev'], azim=variables['azim'] + angle)

    fim = StringIO()
    fig.savefig(fim, format='png')
    binData = fim.getvalue()
    fim.close()
    return binData


def randStr(length=7):
    '''Generate a random string composed of lowercase and digital.
    Indistinguishable characters have been removed.
    '''
    characters = list('bcdghijkmnpqrtuvwxyz23456789')
    shuffle(characters)
    return str(characters[:length])


def read_line(model_path):
    with open(model_path, 'r') as f:
        lines = f.readlines()
        return lines


def fill_line_len(lines):
    line_len = []
    for line in lines:
        line_space = ' '.join(line)
        line_len.append([line_space, len(line)-1])
    return line_len


def main():
    if not os.path.exists:
        os.makedirs(os.path.join(os.path.dirname(__file__), 'captcha'))
    ap = ArgumentParser()
    ap.add_argument("-f", "--font_path", required=True, type=str,
                    help='the path of font that you want to use')
    ap.add_argument("-p", "--sample_path", required=True,
                    type=str, help="the path of sample.txt")
    args = vars(ap.parse_args())
    font = args['font_path']
    sample = args['sample_path']
    i = 1
    lines = read_line(sample)
    len_line = fill_line_len(lines)
    for line, len_line in len_line:
        img = make_image(str(line), font, len_line, width=512)
        with open(os.path.join(os.path.dirname(__file__), 'captcha', '{}.png'.format(i)), 'wb') as f:
            f.write(img)
        i += 1


if __name__ == '__main__':
    main()
