# Introduction
This library can be used to quickly generate stl files from grid numpy arrays.

## Step 1: Create a grid


```python
from stl_utils import grid2vec,show_vec,vec2mesh
import numpy as np
from stl import mesh
```


```python
size = 11
_x = np.linspace(-3,3,size)
_y = np.linspace(-3,3,size)
x,y = np.meshgrid(_x,_y)
z = x**2+y**2
```


```python
grids = np.stack([x,y,z],axis=2)
```

## Turn grid into vectors


```python
vec = grid2vec(grids)
```


```python
# Visualize the created vectors before saving it
ax=show_vec(vec)

```


![png](files/vis.png)


## Turn the grid into Mesh


```python
m = vec2mesh(vec)
m
```




    <stl.mesh.Mesh at 0x125b7ae4160>



## Save as STL file


```python
m.save('sample.stl')
```

__View of STL file__



<img src='./files/stl-view.PNG'>
