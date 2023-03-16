import matplotlib
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import Slider, Button
from matplotlib.colorbar import Colorbar
from matplotlib.transforms import Bbox
from matplotlib import colors
#import matplotlib.style as mplstyle
import numpy as np

import math
import sys
import os
import time
import subprocess as subp

#mplstyle.use(['dark_background', 'ggplot', 'fast'])

def show_dict(w0):
    print('\n'.join(map(lambda x: '{:<20}: {}'.format(x, w0.__dict__[x]), list(w0.__dict__.keys()))))

def quick_plot(data, subplot=None):
    global fig
    global ax
    if subplot is None:
        fig = plt.figure('figure')
        ax = fig.add_subplot(2,1,1)
    else:
        if len(fig.axes) < subplot:
            ax = fig.add_subplot(2,1,subplot,sharex=ax)
    ax.plot(list(range(len(data))), data)

def find_val(array, start, direction, event=None):
    if direction == 'left':
        array = array[start::-1]
    elif direction == 'right':
        array = array[start:]
    else:
        raise Exception()

    if event == 'cross':
        signs = np.sign(array[:-1]) + np.sign(array[1:])
        index = np.where(np.abs(signs) == 0)[0][0]
        index = start + index if direction == 'right' else start - index
        return index
    else:
        raise Exception

N = 150
bounds = np.array([[-10, 10],
                    [-12, 0.3],
                    [-5, 30]])*2
# N = 4
# bounds = np.array([[0, 1],
#                    [2, 3],
#                    [4, 5]])
xvals = np.reshape(np.linspace(*bounds[0,:], N), [-1, 1, 1])
yvals = np.reshape(np.linspace(*bounds[1,:], N), [-1, 1, 1])
zvals = np.reshape(np.linspace(*bounds[2,:], N), [-1, 1, 1])

meshx = np.transpose(np.repeat(np.repeat(xvals, N, axis=1), N, axis=2), [0, 1, 2])
meshy = np.transpose(np.repeat(np.repeat(yvals, N, axis=1), N, axis=2), [1, 0, 2])
meshz = np.transpose(np.repeat(np.repeat(zvals, N, axis=1), N, axis=2), [2, 1, 0])
meshx = np.reshape(meshx, [N,N,N,1])
meshy = np.reshape(meshy, [N,N,N,1])
meshz = np.reshape(meshz, [N,N,N,1])
mesh = np.concatenate([meshx, meshy, meshz], axis=3)

# field = np.divide(1, np.sum(np.power(mesh, 2), axis=3))
# field[field == np.Inf] = 0
# print('{}, {}'.format(np.min(field), np.max(field)))
# field = np.log(field)

t0 = np.sqrt(np.sum(np.power(mesh,2), axis=3))
field = np.sum(np.sin(mesh), axis=3) + np.sum(np.cos(1.1*mesh), axis=3)/2 + np.sum(np.cos(1.6*mesh), axis=3)/4
field = np.divide(field, t0)
field[field == np.Inf] = 0
field = field + t0/8

# grad0 = np.diff(field, axis=0)
# grad0 = np.interp(xvals, xvals[:-1]+0.5, grad0)

def slice_data(data, dim_index, index):
    slices = np.s_[index,:,:]
    slices = np.concatenate([slices[1:dim_index+1], [slices[0]], slices[dim_index+1:]])
    return data[tuple(slices)]

def update_figure(val, data, dim_index, min_max, img, colorbar):
    global fig
    if val == 'inc':
        index = 1
    else:
        index = round((np.shape(data)[dim_index]-1)*val)
    img.set(norm=plt.Normalize(*min_max[:,index]))
    img.set(cmap=img.cmap._resample(15))
    img.set_array(slice_data(data, dim_index, index))
    colorbar.update_normal(img)
    fig.canvas.draw_idle()
    
def pos_translate(pos, index, repos_data):
    translation, scale = repos_data
    return list(pos + np.concatenate([np.array(translation), [0.0, 0.0]])
                    + np.concatenate([np.array(scale) * index, [0.0, 0.0]]))

def arrange_graph(index, data, title, xlabel, ylabel):
    translation = [-0.145, 0]
    index_scale = [0.325, 0.0]
    
    slice_index_start = 0.5
    field, dim_index = data
    start_index = round((np.shape(field)[dim_index]-1)*slice_index_start)
    field_slice = slice_data(field, dim_index, start_index)
    dims = list(range(len(np.shape(field)))); dims.pop(dim_index)
    field_dim_ordered = np.transpose(field, [dim_index] + dims)
    field_dim_ordered = np.reshape(field_dim_ordered, [np.shape(field_dim_ordered)[0], -1])
    dim_min_max = np.array([np.min(field_dim_ordered, axis=1), np.max(field_dim_ordered, axis=1)])
    global fig
    plot = fig.add_axes(pos_translate([0.0, 0.3, 0.5, 0.58], index, [translation, index_scale]))

    global vlims
    img = plot.matshow(field_slice)
    img.set(interpolation='bilinear', interpolation_stage='data')
    img.set(cmap='RdBu') # twilight, twilight_shifted, seismic, RdBu, -RdGy
    img.set(norm=plt.Normalize(*dim_min_max[:,start_index]))
    img.set(cmap=img.cmap._resample(15))

    plot.set_title(title)
    plot.set_xlabel(xlabel)
    plot.set_ylabel(ylabel)
    plot.xaxis.set_ticks_position('bottom')
    plot.yaxis.set_ticks_position('left')
    plot.invert_yaxis()
    
    #colorbar_ax = fig.add_axes(pos_translate([0.11, 0.30, 0.5, 0.58], index, [translation, index_scale]),
    #                           aspect=20)
    colorbar_ax = matplotlib.colorbar.make_axes(plot, location='right',
                                                orienation='vertical', ticklocation='left',
                                                pad=0.015)[0]
    colorbar = Colorbar(ax=colorbar_ax, cmap=img.cmap, norm=img.norm, format='%0.1f')
    
    slider = fig.add_axes(pos_translate([0.25, 0.08, 0.15, 0.2], index, [translation, index_scale]))
    slice_slider = Slider(ax=slider,
        label='Slice Ratio',
        valmin=0.0,
        valmax=1.0,
        valinit=slice_index_start,
    )
    update_clbk = lambda val: update_figure(val, field, dim_index, dim_min_max, img, colorbar)
    slice_slider.on_changed(update_clbk)
    slider.set_aspect(aspect=0.1, anchor='SW')
    
    # slider_inc = fig.add_axes(pos_translate([0.175, 0.08, 0.15, 0.2], index, [translation, index_scale]))
    # slider_inc_button = Button(ax=slider_inc, label='+')
    # inc_button_update_clbk = lambda val: update_figure(val='inc', field, dim_index, dim_min_max, img)
    # slider_inc_button.on_clicked(inc_button_update_clbk)
    # slider_inc_button.set_aspect(aspect=1.)
    
    return plot, slider, img, slice_slider
    

fig, axs = plt.subplots()
axs.remove()

# objs0 = arrange_graph(axs[0,0], axs[1,0], field[2,:,:], 'X Slice', 'y axis', 'x axis')
# objs1 = arrange_graph(axs[0,1], axs[1,1], field[:,3,:], 'Y Slice', 'x axis', 'z axis')
# objs2 = arrange_graph(axs[0,2], axs[1,2], field[:,:,0], 'Z Slice', 'x axis', 'y axis')
#vlims = [-50, 400]
objs0 = arrange_graph(0, [field, 0], 'X Slice', 'y axis', 'z axis')
objs1 = arrange_graph(1, [field, 1], 'Y Slice', 'x axis', 'z axis')
objs2 = arrange_graph(2, [field, 2], 'Z Slice', 'x axis', 'y axis')

#update_figure(0.4, field, 1, objs0[2])

def scroll_zoom(event):
    ax = event.inaxes
    scale_constant = 3
    if event.step > 0:
        scale_amount = 1.0/scale_constant
    elif event.step < 0:
        scale_amount = -((2-1)/scale_constant+1)
    else:
        print('zoom warning')
        return
    lims = np.array([list(ax.get_xlim()), list(ax.get_ylim())])
    center = np.sum(lims,axis=1)/2
    window_diff = np.subtract(lims, np.reshape(center, [2, 1])) * scale_amount
    translation = (np.array([event.xdata, event.ydata]) - center) * scale_amount
    window = lims - window_diff + np.reshape(translation, [2, 1])
    
    max_window_size = np.max(ax.bbox._transform.get_affine()._boxout._transform._mtx) * 8
    if np.sum((np.abs(window[:,1] - window[:,0]) > max_window_size) * 1) > 0:
        return
    ax.set_xlim(*window[0,:])
    ax.set_ylim(*window[1,:])
    ax.figure.canvas.draw()
plt.connect('scroll_event', scroll_zoom)

#fig.set_tight_layout('tight')
fig.set_size_inches(9, 3)
fig.set_dpi(200)
plt.draw()

plt.show()
pass