# Simulate a PDE for modeling the dynamics of a bubble.
# <PDE>

import asyncio
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from pprint import pprint
import re
import pdb

slopes = np.zeros((5000,1))
slope_index = 0

class SimpleLogger:
    log_record = []
    current_message = ''

    def __init__(self):
        pass

    def __getitem__(self, key):
        return self.log_record[key]

    def __len__(self):
        return len(self.log_record)

    def log(self, msg):
        if type(msg) != str:
            msg = str(msg)
        self.current_message += msg + '\n'

    def next_log(self):
        self.current_message += '\n'
        self.log_record.append(self.current_message)
        self.current_message = ''

log = SimpleLogger()

def main():
    global N, xs, grid, space, points, path, points1

    N = 5001;
    xs = np.linspace(-1,1,N)
    grid = np.array(np.meshgrid(xs, xs, indexing='ij'))

    space = compute_space(grid, 462)
    points = compute_curve_neighbors(space, [15.23, 15.25])
    points1 = compute_curve_neighbors(space.T, [15.23, 15.25])

    path = []; path = compute_curve(space)
    path = np.squeeze(np.array(path))


def compute_curve(space):
    print('Computing curve...')

    iso_line = 15.25

    log_diff = np.log(np.abs(space - iso_line))
    start_point = np.array(np.nonzero(log_diff == log_diff.min())).reshape((2,1))

    path = [start_point]
    point = start_point
    for i in range(20):
        diffs = compute_neighbor_diffs(space, point)
        print("***\n" + str(diffs))
        point = np.vectorize(int)(np.round(diffs[0,:].reshape((2,1))))
        path += [point]

    return path
    # iso_line = 15.25
    #
    # log_diff = np.log(np.abs(space - iso_line))
    # start_point = np.array(np.nonzero(log_diff == log_diff.min())).reshape((2,))
    # lpath = [start_point]
    # rpath = [start_point]
    #
    # while (len(rpath) != 200) and ((len(lpath) == 1) or (not np.array_equal(lpath[-1], rpath[-1]))):
    #     log.log('----------------------------------------------------')
    #     #l_diffs = compute_neighbor_diffs(metaball_space, lpath[-1])
    #     r_diffs = compute_neighbor_diffs(space, rpath[-1])
    #
    #     #l_next_point = compute_next_point(l_diffs)
    #     r_next_point = compute_next_point(rpath[-1], r_diffs)
    #
    #     log.log('Path: ' + str(rpath[-1]))
    #     log.log('DiffX: ' + str(r_diffs[:,0]))
    #     log.log('DiffY: ' + str(r_diffs[:,1]))
    #     log.log('Next: ' + str(r_next_point))
    #
    #     # lpath.append(l_next_point.reshape((2,)))
    #     rpath.append(r_next_point.reshape((2,)))
    #
    #     log.next_log()
    #
    # rpath = np.array(rpath) * 2 / space.shape[0] -1
    # return rpath


def compute_next_point(position, diffs):
    global slope, slope_index
    globals()['diffs'] = diffs
    log.log(position)
    avg_deltas = np.abs(diffs - position.reshape((1,2))).mean(0)
    delta_ratio = avg_deltas[1] / avg_deltas[0]
    log.log(avg_deltas)

    # compute which dimension we increment along
    dir_index = [0, 1]
    dir_index[0] = 0 if delta_ratio > 1.00 else 1
    dir_index[1] = (dir_index[0] + 1) % 2
    log.log('Ratio: ' + str(delta_ratio))
    log.log('Dir Index: ' + str(dir_index))

    # compute direction to move on increment axis
    #slope = diffs[2, dir_index[0]] - diffs[0, dir_index[0]]
    #move_dir = 1 if slope >= 0 else -1
    inc_dir_delta = position[dir_index[0]] - diffs[1, dir_index[0]]
    if inc_dir_delta > 0:
        move_dir = -1
    elif inc_dir_delta < 0:
        move_dir = 1
    else:
        move_dir = 0
    log.log('Inc Delta: ' + str(inc_dir_delta) + ', Move: ' + str(move_dir))
    #slopes[slope_index] = slope
    #slope_index += 1

    # # compute how far to move on non-increment axis
    noninc_pos_centered = diffs[1+move_dir,dir_index[1]] - position[dir_index[1]]
    noninc_delta = int(np.fix(noninc_pos_centered) + np.sign(noninc_pos_centered))
    log.log('NonInc Delta: ' + str(noninc_delta))
    # xy_slope = (diffs[2, dir_index[1]] - diffs[0, dir_index[1]]) / slope
    # non_increment_amount = int(np.round(move_dir * xy_slope))
    # log.log('XY Slope: ' + str(xy_slope))
    # log.log('NonInc Amount: ' + str(non_increment_amount))

    new_pos = position.copy()
    new_pos[dir_index[0]] += move_dir
    new_pos[dir_index[1]] += noninc_delta

    # Around 45-degree slopes, new_pos might cycle back to position
    if np.array_equal(new_pos, compute_next_point.last_position):
        new_pos = position.copy()
        new_pos[dir_index[0]] -= move_dir
        new_pos[dir_index[1]] -= noninc_delta

    compute_next_point.last_position = position

    return new_pos
compute_next_point.last_position = None


def compute_neighbor_diffs(space, point):
    iso_line = 15.25

    close_xs = point[0] + np.array((-1,0,1)).reshape((1,3))
    close_ys = point[1] + np.array((-1,0,1)).reshape((3,1))
    neighborhood = space[close_xs, close_ys]
    iso_diffs = neighborhood - iso_line

    lr_diffs = np.diff(neighborhood, 1, 1)
    ud_diffs = np.diff(neighborhood, 1, 0)

    log.log(('LR_Diffs: ' + str(lr_diffs[:,0]) + '\n'
             '          ' + str(lr_diffs[:,1])))
    log.log(('UD_Diffs: ' + str(ud_diffs[0,:]) + '\n'
             '          ' + str(ud_diffs[1,:])))

    lr_ind_diffs_l = np.append(iso_diffs[:,0:2] / lr_diffs, np.zeros((3,1)), axis=1)
    lr_ind_diffs_r = np.append(np.zeros((3,1)), iso_diffs[:,1:] / lr_diffs, axis=1)
    lr_ind_diffs = lr_ind_diffs_l + lr_ind_diffs_r
    lr_ind_diffs[:,1] /= 2

    ud_ind_diffs_u = np.append(iso_diffs[0:2,:] / ud_diffs, np.zeros((1,3)), axis=0)
    ud_ind_diffs_d = np.append(np.zeros((1,3)), iso_diffs[1:,:] / ud_diffs, axis=0)
    ud_ind_diffs = ud_ind_diffs_u + ud_ind_diffs_d
    ud_ind_diffs[1,:] /= 2

    log.log(('LR_Ind_Diffs: ' + str(lr_ind_diffs[0,:]) + '\n'
             '              ' + str(lr_ind_diffs[1,:]) + '\n'
             '              ' + str(lr_ind_diffs[2,:])))
    log.log(('UD_Ind_Diffs: ' + str(ud_ind_diffs[0,:]) + '\n'
             '              ' + str(ud_ind_diffs[1,:]) + '\n'
             '              ' + str(ud_ind_diffs[2,:])))

    diff_x = (close_xs - lr_ind_diffs).mean(1)
    diff_y = (close_ys - ud_ind_diffs).mean(0)

    return np.append(diff_x.reshape((3,1)), diff_y.reshape((3,1)), axis=1)


def compute_space(grid, seed=None):
    print('Computing metaball space...')

    # check if we have already cached this seed
    if not seed is None:
        matcher = lambda name: [name, re.findall(r'.*?(\d+)(?=\.dat)', name)[0]]
        files = list(map(matcher, os.listdir('space_dumps/')))
        seed_cache = list(filter(lambda filematch: filematch[1] == str(seed), files))[0]
        if seed_cache != []:
            print('  Found cached space.dat file.')
            import pickle
            return pickle.load(open('space_dumps/' + seed_cache[0], 'rb'))

    randseed = np.random.randint(10000)
    np.random.seed(randseed)

    Nballs = 10

    metaball_vectorizer = np.vectorize(Metaball, signature='(2),()->()')
    ball_positions = np.random.normal(scale=0.3, size=(Nballs, 2))
    ball_weights = np.random.normal(loc=0.5, scale=0.1, size=Nballs)
    balls = metaball_vectorizer(ball_positions, ball_weights)

    metaball_space = sum(np.array(list(map(lambda ball: ball.weigh_space(grid), balls))), 0)

    return metaball_space


def compute_curve_neighbors(space, limits):
    print('Computing curve neighbors...')

    # clip space
    limit = 5*space.mean()
    space[space > limit] = limit

    # find desired curve
    N = space.shape[0]
    points = space.copy()
    points[points < limits[0]] = 0
    points[points > limits[1]] = 0
    points = np.array(np.nonzero(points > 0)) * 2 / N - 1

    return points.T


        # var_string = ','.join(list(filter(lambda key: key[0] != '_', list(locals().keys()))))
        # exec('global ' + var_string)

        # # get index of points less than iso_line, furthest along each dimension
        # lr_inds = np.array(np.nonzero(iso_diffs < 0))
        # dim_1_furthest = np.unique(np.flip(lr_inds[0,:]), return_index=True)[1]
        # dim_1_furthest = lr_inds.shape[1] - 1 - dim_1_furthest
        # dim_1_furthest = lr_inds[:,dim_1_furthest]
        #
        # # np.unique searches deep dimensions first, transpose to search along dim_0 first
        # ud_inds = np.array(np.nonzero((iso_diffs < 0).T))
        # dim_0_furthest = np.unique(np.flip(ud_inds[0,:]), return_index=True)[1]
        # dim_0_furthest = np.flip(ud_inds, 1)[:,dim_0_furthest]
        # dim_0_furthest = np.flip(dim_0_furthest,0) # account for transposed iso_diff
        #
        # # remo()ve indicies that mean all values in that column or row
        # # (depending on which dimension we are considering) are less than iso_line
        # # That means iso_line cannot pass through that indicies' column or row
        # dim_1_furthest = np.delete(dim_1_furthest, np.nonzero(dim_1_furthest[1,:] == 2)[0], axis=1)
        # #dim_0_furthest = np.delete(dim_0_furthest, np.nonzero(dim_0_furthest[0,:] == 0)[0], axis=1)
        #
        # # construct masks to index into iso_diffs array to find border value
        # lr_mask = np.ndarray((3,3), dtype='bool')
        # lr_mask[:,:] = False
        # lr_mask[dim_1_furthest[0,:], dim_1_furthest[1,:]] = True
        #
        # ud_mask = np.ndarray((3,3), dtype='bool')
        # ud_mask[:,:] = False
        # ud_mask[dim_0_furthest[0,:], dim_0_furthest[1,:]] = True
        #
        # # compute differential indicies for where iso_line actually is
        # lr_diffs = np.diff(neighborhood, 1, 1)
        # lr_diffs = lr_diffs[dim_1_furthest[0,:], dim_1_furthest[1,:]]
        # lr_inds = iso_diffs[lr_mask] / lr_diffs + dim_1_furthest[1,:] + 1
        #
        # ud_diffs = np.diff(neighborhood, 1, 0)
        # # first dimension gets shifted down by one, we're going along ud direction in reverse
        # ud_diffs = ud_diffs[dim_0_furthest[0,:]-1, dim_0_furthest[1,:]]
        # ud_inds = iso_diffs[ud_mask] / ud_diffs + dim_0_furthest[1,:] + 1

    # input()
    # fig, ax = plt.subplots()
    # scatter = ax.scatter(paths[0,:,0], paths[1,:,0])
    # ani = mpl.animation.FuncAnimation(fig,
    #                                   update_plot,
    #                                   interval=40,
    #                                   blit=True)
    # plt.show()

def update_plot(i):
    scatter.set_offsets(paths[:,:,i].T)
    return scatter,

#    test = list(filter(lambda point: (point - np.array([2824, 2080]))**2 < 50, points.transpose()))


#     plt.contour(grid[0,:,:], grid[1,:,:],metaball_space, 150)
# #    plt.show()
#
#     fig = plt.figure()
#     axes = fig.gca(projection='3d')
#     surf = axes.plot_surface(grid[0,:,:],
#                              grid[1,:,:],
#                              metaball_space)
#     plt.show()

    #breakpoint()

    #axes.plot(np.sin(2*np.pi*xs))

    #plt.ion()
    #plt.show()

    #while plt.fignum_exists(fig.number):
    #plt.pause(0.01)

    #input_task = asyncio.create_task(get_input())
    #plot_task = asyncio.create_task(draw_plots(fig.number))

    #for i in asyncio.all_tasks():
    #    print(i)

    #await plot_task
    #input_task.cancel()

# async def draw_plots(fig_num):
#     while(plt.fignum_exists(fig_num)):
#         plt.show()
#         plt.pause(0.1)
#
# async def get_input():
#     #print('>>> ', end='')
#     #in_line = input()
#     if in_line == '_quit':
#         plt.close()
#     else:
#         res = exec(in_line)
#         return res

class Metaball:
    pos = np.array([0, 0]).reshape(2,1)
    weight = 0.0

    def __init__(self, pos, weight):
        self.pos = np.array(pos).reshape(2,1)
        self.weight = weight

    def weigh_space(self, space):
        translated = space - self.pos.reshape(2,1,1)
        weighed = self.weight * (sum(translated ** 2, 0) ** -0.5)
#        breakpoint()
        return weighed

if __name__ == '__main__':
    #main_task = asyncio.create_task(main())
    main()
