# FastGeodis: Fast Generalised Geodesic Distance Transform
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
<img src="https://img.shields.io/pypi/dm/fastgeodis.svg?label=PyPI%20downloads&logo=python&logoColor=green"/>
[![status](https://joss.theoj.org/papers/d0b6e3daa4b22fec471691c6f1c60e2a/status.svg)](https://joss.theoj.org/papers/d0b6e3daa4b22fec471691c6f1c60e2a)
[![CI Build](https://github.com/masadcv/FastGeodis/actions/workflows/build.yml/badge.svg)](https://github.com/masadcv/FastGeodis/actions/workflows/build.yml)
[![PyPI version](https://badge.fury.io/py/FastGeodis.svg)](https://badge.fury.io/py/FastGeodis)
<img src="https://img.shields.io/badge/Python-3.6%20|%203.7%20|%203.8%20|%203.9-3776ab.svg"/>
<img src="https://img.shields.io/badge/PyTorch-%3E%3D%201.5.0-brightgreen.svg"/>

This repository provides CPU (OpenMP) and GPU (CUDA) implementations of Generalised Geodesic Distance Transform in PyTorch for 2D and 3D input data based on parallelisable raster scan ideas from [1, 3]. It includes methods for computing Geodesic, Euclidean distance transform and mixture of both. 

| 2D images, 1 of 4 passes | 3D volumes, 1 of 6 passes  |
|-------------------|-------------------------|
| <img src="https://raw.githubusercontent.com/masadcv/FastGeodis/master/figures/FastGeodis2D.png?raw=true" width="300" /> | <img src="https://raw.githubusercontent.com/masadcv/FastGeodis/master/figures/FastGeodis3D.png?raw=true" width="300" /> |


The above raster scan method can be parallelised for each row/plane on an available device (CPU or GPU). This leads to significant speed up as compared to existing non-parallelised raster scan implementations (e.g. [https://github.com/taigw/GeodisTK](https://github.com/taigw/GeodisTK)). Python interface is provided (using PyTorch) for enabling its use in deep learning and image processing pipelines.

In addition, implementation of generalised version of Geodesic distance transforms along with Geodesic Symmetric Filtering (GSF) is provided for use in interactive segmentation methods, that were originally proposed in [1, 2, 5].

> The raster scan based implementation provides a balance towards speed rather than accuracy of Geodesic distance transform and hence results in efficient hardware utilisation. On the other hand, in case of Euclidean distance transform, exact results can be achieved with other packages (albeit not on necessarilly on GPU) [6, 7, 8]

## Citation
If you use this code in your research, then please consider citing:

[![status](https://joss.theoj.org/papers/d0b6e3daa4b22fec471691c6f1c60e2a/status.svg)](https://joss.theoj.org/papers/d0b6e3daa4b22fec471691c6f1c60e2a)

***Asad, Muhammad, Reuben Dorent, and Tom Vercauteren. "FastGeodis: Fast Generalised Geodesic Distance Transform." Under review at Journal of Open Source Software (JOSS), 2022.***

## Installation instructions
The provided package can be installed using:

`pip install FastGeodis`

or

`pip install git+https://github.com/masadcv/FastGeodis`

or (on conda systems with existing installation of PyTorch with CUDA)

`pip install FastGeodis --no-build-isolation`

## Example usage

### Fast Geodesic Distance Transform
The following demonstrates a simple example showing FastGeodis usage:

To compute Geodesic Distance Transform:
```python
device = "cuda" if torch.cuda.is_available() else "cpu"
image = np.asarray(Image.open("data/img2d.png"), np.float32)

image_pt = torch.from_numpy(image).unsqueeze_(0).unsqueeze_(0)
image_pt = image_pt.to(device)
mask_pt = torch.ones_like(image_pt)
mask_pt[..., 100, 100] = 0

v = 1e10
# lamb = 0.0 (Euclidean) or 1.0 (Geodesic) or (0.0, 1.0) (mixture)
lamb = 1.0
iterations = 2
geodesic_dist = FastGeodis.generalised_geodesic2d(
    image_pt, mask_pt, v, lamb, iterations
)
geodesic_dist = np.squeeze(geodesic_dist.cpu().numpy())
```

To compute Euclidean Distance Transform:
```python
device = "cuda" if torch.cuda.is_available() else "cpu"
image = np.asarray(Image.open("data/img2d.png"), np.float32)

image_pt = torch.from_numpy(image).unsqueeze_(0).unsqueeze_(0)
image_pt = image_pt.to(device)
mask_pt = torch.ones_like(image_pt)
mask_pt[..., 100, 100] = 0

v = 1e10
# lamb = 0.0 (Euclidean) or 1.0 (Geodesic) or (0.0, 1.0) (mixture)
lamb = 0.0
iterations = 2
euclidean_dist = FastGeodis.generalised_geodesic2d(
    image_pt, mask_pt, v, lamb, iterations
)
euclidean_dist = np.squeeze(euclidean_dist.cpu().numpy())
```

For more usage examples see:
| Description  |  Python |  Colab link  |
|--------------|---------|--------------|
| **Simple 2D Geodesic and Euclidean Distance** | [`samples/simpledemo2d.py`](./samples/simpledemo2d.py) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/masadcv/FastGeodis/blob/master/samples/simpledemo2d.ipynb)  |
| **Simple Signed 2D Geodesic and Euclidean Distance** | [`samples/simpledemo2d_signed.py`](./samples/simpledemo2d_signed.py) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/masadcv/FastGeodis/blob/master/samples/simpledemo2d_signed.ipynb) |
| **2D Geodesic Distance** | [`samples/demo2d.py`](./samples/demo2d.py) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/masadcv/FastGeodis/blob/master/samples/demo2d.ipynb)  |
| **3D Geodesic Distance** | [`samples/demo3d.py`](./samples/demo3d.py) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/masadcv/FastGeodis/blob/master/samples/demo3d.ipynb)  |
| **2D GSF Segmentation Smoothing** |  [`samples/demoGSF2d_SmoothingSegExample.ipynb`](./samples/demoGSF2d_SmoothingSegExample.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/masadcv/FastGeodis/blob/master/samples/demoGSF2d_SmoothingSegExample.ipynb) | 

## Unit Tests
A number of unittests are provided, which can be run as:

```
pip install -r requirements-dev.txt
python -m unittest
```

## Documentation
Further details of each function implemented in FastGeodis can be accessed at the documentation hosted at: [https://masadcv.github.io/FastGeodis/index.html](https://masadcv.github.io/FastGeodis/index.html). 

## Comparison of Execution Time and Accuracy
FastGeodis (CPU/GPU) is compared with existing GeodisTK ([https://github.com/taigw/GeodisTK](https://github.com/taigw/GeodisTK)) in terms of execution speed as well as accuracy.


### Execution Time
| 2D images | 3D volumes  |
|-------------------|-------------------------|
|<img src="https://raw.githubusercontent.com/masadcv/FastGeodis/master/figures/experiment_2d.png?raw=true" width="400" />|<img src="https://raw.githubusercontent.com/masadcv/FastGeodis/master/figures/experiment_3d.png?raw=true" width="400" />|

<br>

### Accuracy
2D case
| Qualitative Comparison | Quantitative (joint histogram)  |
|-------------------|-------------------------|
|<img src="https://raw.githubusercontent.com/masadcv/FastGeodis/master/figures/fast_marching_compare_2d.png?raw=true?raw=true" width="800" />  |<img src="https://raw.githubusercontent.com/masadcv/FastGeodis/master/figures/fast_marching_compare_2d_jointhist.png?raw=true" width="400" /> |

3D case

| Qualitative Comparison | Quantitative (joint histogram)  |
|-------------------|-------------------------|
| <img src="https://raw.githubusercontent.com/masadcv/FastGeodis/master/figures/fast_marching_compare_3d.png?raw=true" width="800" /> | <img src="https://raw.githubusercontent.com/masadcv/FastGeodis/master/figures/fast_marching_compare_3d_jointhist.png?raw=true" width="400" /> |

## References
- [1] Criminisi, Antonio, Toby Sharp, and Khan Siddiqui. "Interactive Geodesic Segmentation of n-Dimensional Medical Images on the Graphics Processor." Radiological Society of North America (RSNA), 2009. [[pdf](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Criminisi_RSNA09_extendedAbstract1.pdf), [ppt](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/RSNA2009_Segmentation_Criminisi.ppt), [url](https://www.microsoft.com/en-us/research/publication/interactive-geodesic-segmentation-of-n-dimensional-medical-images-on-the-graphics-processor/)]

- [2] Criminisi, Antonio, Toby Sharp, and Andrew Blake. "Geos: Geodesic image segmentation." European Conference on Computer Vision. Springer, Berlin, Heidelberg, 2008. [[doi](https://doi.org/10.1007/978-3-540-88682-2_9)]

- [3] Weber, Ofir, et al. "Parallel algorithms for approximation of distance maps on parametric surfaces." ACM Transactions on Graphics (TOG), (2008). [[doi](https://doi.org/10.1145/1409625.1409626)]

- [4] GeodisTK: [https://github.com/taigw/GeodisTK](https://github.com/taigw/GeodisTK)

- [5] Criminisi, Antonio, Toby Sharp, Carsten Rother, and Patrick Pérez. "Geodesic image and video editing." ACM Trans. Graph. 29, no. 5 (2010): 134-1. [[doi](https://doi.org/10.1145/1857907.1857910)]

- [6] [https://github.com/seung-lab/euclidean-distance-transform-3d](https://github.com/seung-lab/euclidean-distance-transform-3d)

- [7] [https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.distance_transform_edt.html](https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.distance_transform_edt.html)

- [8] [https://www.tensorflow.org/addons/api_docs/python/tfa/image/euclidean_dist_transform](https://www.tensorflow.org/addons/api_docs/python/tfa/image/euclidean_dist_transform)
