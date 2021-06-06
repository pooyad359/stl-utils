from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import numpy as np
from stl import mesh


def grid2vec(grid, base_level=None):
    '''
    grid: NxMx3 array containing x, y, and z values.
    base_level: If a value passed in, it creates a flat surface with base_level 
    elevation and connects it to the main grid.
    
    returns STL vectors 2(M-1)(N-1)x3x3 which is groups of three points for 3D plotting.
    '''
    m, n, _ = grid.shape
    p1 = grid[:-1, :-1, :].reshape((-1, 3))
    p2 = grid[:-1, 1:, :].reshape((-1, 3))
    p3 = grid[1:, :-1, :].reshape((-1, 3))
    p4 = grid[1:, 1:, :].reshape((-1, 3))
    v1 = np.stack([p1, p2, p3], axis=1)
    v2 = np.stack([p2, p3, p4], axis=1)
    vec = np.concatenate((v1, v2))
    if base_level is not None:
        if type(base_level) in ('float', 'int'):
            raise (TypeError(
                f'base_level can only be int or float but recieved {type(base_level)}'
            ))

        base_grid = grid.copy()
        base_grid[:, :, 2] = base_level
        base_vec = grid2vec(base_grid)

        # Create Wall
        # Front
        p1 = grid[:-1, 0, :]
        p2 = grid[1:, 0, :]
        p3 = base_grid[:-1, 0, :]
        p4 = base_grid[1:, 0, :]
        front_vec = points2vec(p1, p2, p3, p4)

        # Back
        p1 = grid[:-1, -1, :]
        p2 = grid[1:, -1, :]
        p3 = base_grid[:-1, -1, :]
        p4 = base_grid[1:, -1, :]
        back_vec = points2vec(p1, p2, p3, p4)

        # Left
        p1 = grid[0, :-1, :]
        p2 = grid[0, 1:, :]
        p3 = base_grid[0, :-1, :]
        p4 = base_grid[0, 1:, :]
        left_vec = points2vec(p1, p2, p3, p4)

        # Right
        p1 = grid[-1, :-1, :]
        p2 = grid[-1, 1:, :]
        p3 = base_grid[-1, :-1, :]
        p4 = base_grid[-1, 1:, :]
        right_vec = points2vec(p1, p2, p3, p4)

        vec = np.concatenate((
            vec,
            base_vec,
            back_vec,
            front_vec,
            left_vec,
            right_vec,
        )).copy()

    return vec.copy()


def points2vec(p1, p2, p3, p4):
    '''
    Takes four adjacent grid points and returns the associated vectors.
    p1, p2, p3, and p4 are (3,) arrays
    
    returns two STL vectors
    '''
    v1 = np.stack([p1, p2, p3], axis=1)
    v2 = np.stack([p2, p3, p4], axis=1)
    return np.concatenate((v1, v2)).copy()


def show_vec(vectors):
    '''
    3D visualization of a set of STL vectors.
    '''
    
    figure = plt.figure()
    axes = mplot3d.Axes3D(figure)
    for vec in vectors:
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(vec))
    
    xmin=vectors[:,:,0].min()
    xmax=vectors[:,:,0].max()
    ymin=vectors[:,:,1].min()
    ymax=vectors[:,:,1].max()
    zmin=vectors[:,:,2].min()
    zmax=vectors[:,:,2].max()
    axes.xy_viewLim = Bbox([[xmin,ymin],[xmax,ymax]])
    axes.zz_viewLim= Bbox([[zmin,zmin],[zmax,zmax]])
    return axes


def vec2mesh(vectors):
    '''
    Converts STL vectors to STL Mesh which can be saved as STL files.
    '''
    length = vectors.shape[0]
    mesh_data = np.zeros(length, dtype=mesh.Mesh.dtype)
    for i in range(length):
        mesh_data['vectors'][i] = vectors[i]
    return mesh.Mesh(mesh_data)
