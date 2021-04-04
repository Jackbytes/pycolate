# pycolate :coffee:

![Banner](https://raw.githubusercontent.com/Jackbytes/pycolate/main/images/cover_image.png)

A python implementation of site percolation, generates datasets and illustrations.

## Aims.

This project primarily generates datasets and illustrations from square lattice site percolation. There is an auxillary program which carries out critical probability estimation using coarse graining with possible interactions.

## How to.

1. Install the latest version of pycolate:
```python
pip install pycolate
```
2.Import pycolate into your python file:
```python
import pycolate
```
### Creating illustrations.

The `pycolate.Percolation` class is used for creating a single instance of percolation. It takes the following arguments:
```python
Perc = Percolation(width, height, occupation probability)
```
We display the illustration in a window as so:
```python
...
Perc.display()
```
To save the illsutration we run:
```python
...
Perc.save()
```
So to generate an illustration of a 50x50 grid where each square has a 0.6 chance of being occupied:
```python
import pycolate

perc = pycolate.Percolation(50,50,0.6)

perc.display() 
perc.save('PATH')
```
The default size for a square is 10 by 10 pixels. To adjust this one can change the `Percolation.site_size` prior to running `Percolation.display()`.

 If we were running a large simulation we may want the sites to only be 1 pixel each, so we would run the following:
```python
import pycolate

perc = pycolate.Percolation(1000,1000,0.6)

perc.site_site = 1

perc.display() 

perc.save('PATH')
```
### The Percolation Class
Property | Explanation |
--- | --- |
mean_cluster_size | The mean cluster size, excluding the percolating cluster. |
sizes | A list of all the cluster sizes, excluding the percolating cluster. |
percolated_size | The size of the percolating cluster. |
percolated | A boolean. True if a percolating cluster formed. False if not |