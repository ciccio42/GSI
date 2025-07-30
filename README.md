# GSI

GPU-friendly Subgraph Isomorphism

We target at a one-to-one mapping at a time, the query graph is small (vertices less than 100), while the data graph can be very large (but all can be placed in GPU's global memory).

---

#### Installation

This code was tested with the following dependencies:
- nvcc
- CUDA, version 12.5
- GCC, version 11.4

This code was tested with the following hardware/software:
- Fedora 40 (CUDA 12.5 does not officially support Fedora 40, see notes)
- NVIDIA GeForce RTX 3070 (SM_86)

Find your GPU architecture by looking up your NVIDIA GPU on this website: [https://arnon.dk/matching-sm-architectures-arch-and-gencode-for-various-nvidia-cards/]

You can install GCC-11 with homebrew, which is what I did:
```sh
$ brew install gcc@11
```
Whatever you do, find the path to your GCC-11 install. Mine was ```/home/linuxbrew/.linuxbrew/Cellar/gcc@11/11.4.0```. If you also run Linux and used homebrew, this may be the same for you.

Next, install CUDA and NVCC. If you run a supported OS, you can just follow the instructions [here](https://developer.nvidia.com/cuda-downloads). Otherwise, you will have to do some googling online to see exactly how to install CUDA-12.5.

You can check your CUDA install version with the following command; Ensure that it is CUDA-12.5.
```sh
$ nvcc --version
```

You also need to update your ```$PATH``` in order for the makefile to work properly:
```sh
export CUDA_PATH=/path/to/your/cuda
export GCC_11_PATH=/path/to/your/gcc_11
```

### Makefile Parameters

The makefile provided requires defining paths to CUDA and GCC installations. Here are the key sections to update:

#### CUDA Path
If `CUDA_PATH` is not already defined, use the default path:
```sh
CUDA_PATH ?= /usr/local/cuda-12.5
```

#### GCC Path
If `GCC_11_PATH` is not already defined, use the default path installed by Linuxbrew:
```sh
GCC_11_PATH ?= /home/linuxbrew/.linuxbrew/Cellar/gcc@11/11.4.0
```

#### Compilation Flags
Ensure the correct paths and flags for compiling CUDA and C++ code:
```sh
CC = $(GCC_11_PATH)/bin/gcc-11
CXX = $(GCC_11_PATH)/bin/g++-11
NVCC = $(CUDA_PATH)/bin/nvcc

CFLAGS = -std=c++14 -c -O2 -I$(CUDA_PATH)/include
EXEFLAG = -O2 -shared
LDFLAGS = -L$(CUDA_PATH)/lib64 -lcudart -lcudadevrt
INCLUDES = -I$(CUDA_PATH)/include
GPU_ARCHITECTURE = sm_86

PYBIND11_INCLUDES = $(shell python3 -m pybind11 --includes)
PYTHON_LDFLAGS = $(shell python3-config --ldflags)

NVCCFLAGS = -arch=$(GPU_ARCHITECTURE) -rdc=true --ptxas-options=-v -Xcompiler -fPIC $(INCLUDES) --compiler-bindir $(GCC_11_PATH)/bin -std=c++14 -c -O2 -I$(CUDA_PATH)/include
```

### Building the Project

To build this project, simply run `make` within this directory:
```sh
$ make
```

This will compile all necessary object files and create the shared library `libisomorphism.so` and the Python extension `isomorphism$(shell python3-config --extension-suffix)`.

---

#### Usage

A simple python wrapper module for the CUDA and C++ code has been created.
Using the wrapper module, you can test for the isomorphism between a query graph and a data graph using the GPU.

A example of the usage may be found in ```GSI_example.py```


---

#### Dataset

NOTICE: we add 1 to labels for both vertex and edge, to ensure the label is positive!

see `data/readme` and `data/*.g`

---

#### Publication

Li Zeng, Lei Zou, M. Tamer Özsu, Lin Hu, Fan Zhang. **GSI: GPU-friendly Subgraph Isomorphism**. *International Conference on Data Engineering*, 2020.

---

#### Others

Implementation of [GunrockSM](https://github.com/bookug/GunrockSM), [GpSM](https://github.com/bookug/GpSM), and [GPU utilities](https://github.com/bookug/gutil).

---

