# GSI

GPU-friendly Subgraph Isomorphism 

We target at a one-to-one mapping at a time, the query graph is small(vertices less than 100), while the data graph can be very large.
(but all can be placed in GPU's global memory)

---

#### Installation

This code was tested with the following dependencies:
- nvcc
- CUDA, version 12.5
- GCC, version 11.4

This code was tested with the following hardware / software:
- Fedora 40 (CUDA 12.5 does not officially support Fedora 40, see notes)
- NVIDIA GeForce RTX 3070 (SM_86)

Find your GPU architecture by looking up your NVIDIA GPU on this website: [https://arnon.dk/matching-sm-architectures-arch-and-gencode-for-various-nvidia-cards/]

You can install GCC-11 with homebrew, which is what I did:
```$ brew install gcc@11```
Whatever you do, find the path to your GCC-11 install. Mine was ```/home/linuxbrew/.linuxbrew/Cellar/gcc@11/11.4.0```. If you also run Linux and used homebrew, this may be the same for you.

Next, install CUDA and NVCC. If you run a supported OS, you can just follow the instructions [here.](https://developer.nvidia.com/cuda-downloads)
Otherwise, you will have to do some googling online to see exactly how to install CUDA-12.5

You can check your CUDA install version with the following command; Ensure that it is CUDA-12.5.
- ```nvcc --version```

You also need to update your ```$PATH``` in order for the make file to work properly
```
export CUDA_PATH=/path/to/your/cuda
export GCC_PATH=/path/to/your/gcc
```

To build this project, simply run ```make``` within this directory.

---

#### Usage

To be written...

---

####  Dataset

NOTICE: we add 1 to labels for both vertex and edge, to ensure the label is positive!

see `data/readme` and `data/*.g`

---

#### Publication

Li Zeng, Lei Zou, M. Tamer Özsu, Lin Hu, Fan Zhang. **GSI: GPU-friendly Subgraph Isomorphism**. *International Conference on Data Engineering*, 2020.

---

#### Others

Implementation of [GunrockSM](https://github.com/bookug/GunrockSM), [GpSM](https://github.com/bookug/GpSM), and [GPU utilities](https://github.com/bookug/gutil).

