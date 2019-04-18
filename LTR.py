#!/usr/bin/env python 
# encoding=utf-8
import os
from random import uniform, shuffle
from cStringIO import StringIO
from PIL import ImageFont, Image, ImageDraw
import numpy, pylab
from mpl_toolkits.mplot3d import Axes3D

fontPath = 'D:/visual stadio/fonts/OpenSans-Bold.ttf'

def preProcess(len_of_txt):
    #to Do : find the best variable to diffrent len
    variable_dic = {}
    # if len_of_txt == 1:
    #     rstride = 
    #     cstride = 
    #     zlim1 = 
    #     zlim2 = 
    #     xlim1 = 
    #     xlim2 = 
    #     ylim1 = 
    #     ylim2 = 
    #     elev = 
    #     azim = 
    # if len_of_txt == 2:
    #     rstride = 
    #     cstride = 
    #     zlim1 = 
    #     zlim2 = 
    #     xlim1 = 
    #     xlim2 = 
    #     ylim1 = 
    #     ylim2 = 
    #     elev = 
    #     azim = 
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
    # if len_of_txt == 4:
    #     rstride = 
    #     cstride = 
    #     zlim1 = 
    #     zlim2 = 
    #     xlim1 = 
    #     xlim2 = 
    #     ylim1 = 
    #     ylim2 = 
    #     elev = 
    #     azim = 
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
    # if len_of_txt == 6:
    #     rstride = 
    #     cstride = 
    #     zlim1 = 
    #     zlim2 = 
    #     xlim1 = 
    #     xlim2 = 
    #     ylim1 = 
    #     ylim2 = 
    #     elev = 
    #     azim = 
    # if len_of_txt == 7:
    #     rstride = 
    #     cstride = 
    #     zlim1 = 
    #     zlim2 = 
    #     xlim1 = 
    #     xlim2 = 
    #     ylim1 = 
    #     ylim2 = 
    #     elev = 
    #     azim = 
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
    # if len_of_txt == 9:
    #     rstride = 
    #     cstride = 
    #     zlim1 = 
    #     zlim2 = 
    #     xlim1 = 
    #     xlim2 = 
    #     ylim1 = 
    #     ylim2 = 
    #     elev = 
    #     azim = 
    variable_dic = {'rstride':rstride,'cstride':cstride,'zlim1':zlim1,'zlim2':zlim2,'xlim1':xlim1,'xlim2':xlim2,'ylim1':ylim1,'ylim2':ylim2,'elev':elev,'azim':azim}
    return variable_dic
    
def makeImage(text,len_text, width=400, height=200, angle=None):
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
    variables = preProcess(len_text)
    angle = angle if angle != None else uniform(-20, 20)
    try:
        font = ImageFont.truetype(fontPath, 24)
    except IOError:
        raise IOError(
            'Font file doesn\'t exist. Please set `fontPath` correctly.')
    txtW, txtH = font.getsize(text)
    img = Image.new('L', (txtW * 3, txtH * 3), 255)
    drw = ImageDraw.Draw(img)
    drw.text((txtW, txtH), text, font=font)

    fig = pylab.figure(figsize=(width/100.0, height/100.0))
    ax = Axes3D(fig)
    X, Y = numpy.meshgrid(range(img.size[0]), range(img.size[1]))
    Z = 1 - numpy.asarray(img) / 255
    ax.plot_wireframe(X, -Y, Z, rstride=variables['rstride'], cstride=variables['cstride'])
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




def readFile():
    with open(os.path.join(os.getcwd(),'model.txt'),'r') as f:
        lines= f.readlines()
        return lines
    
def fill_line_len(lines):
    line_len = []
    for line in lines:
        line_space = ' '.join(line)
        line_len.append([line_space,len(line)-1])
    return line_len

def main():
    i = 1
    lines = readFile()
    len_line = fill_line_len(lines)
    for line,len_line in len_line:
        img = makeImage(str(line),len_line,width=512)
        with open('%d.png' % i, 'wb') as f:
            f.write(img)
        i +=1

if __name__ == '__main__':
    
    main()

