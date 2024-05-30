# Define compilers and options

# CUDA Path
# If CUDA_PATH is not already defined, use the default path
CUDA_PATH ?= /usr/local/cuda-12.5

# Path to gcc-11
# If GCC_11_PATH is not already defined, use the default path installed by Linuxbrew
GCC_11_PATH ?= /home/linuxbrew/.linuxbrew/Cellar/gcc@11/11.4.0

# Compilation flags
# CFLAGS: Compilation flags for compiling the source files into object files
# EXEFLAG: Flags for creating the final executable
# LDFLAGS: Flags for linking with the CUDA runtime libraries
# INCLUDES: Include path for CUDA headers
CFLAGS = -std=c++14 -c -O2
EXEFLAG = -O2
LDFLAGS = -lcudart -lcudadevrt
INCLUDES = -I$(CUDA_PATH)/include

# NVCC command
# NVCC: Command for compiling CUDA source files
# -arch=sm_86: Specify the architecture for the target GPU
# -rdc=true: Enable relocatable device code
# --ptxas-options=-v: Enable verbose output from the PTX assembler
# -Xcompiler -rdynamic: Pass dynamic linking flag to the host compiler
# $(INCLUDES): Include paths for header files
# --compiler-bindir: Specify the directory for the host compiler
NVCC = $(CUDA_PATH)/bin/nvcc -arch=sm_86 -rdc=true --ptxas-options=-v \
    -Xcompiler -rdynamic $(INCLUDES) --compiler-bindir $(GCC_11_PATH)/bin

# Object directory and files
# objdir: Directory to store object files
# objfile: List of object files to be linked to create the final executable
objdir = ./objs/
objfile = $(objdir)Util.o $(objdir)IO.o $(objdir)Match.o $(objdir)Graph.o $(objdir)run.o

# Default target
# The target 'all' will build the final executable GSI.exe
all: GSI.exe

# Link all object files to create the final executable
# GSI.exe: $(objfile): List of object files to be linked
# $(NVCC) $(EXEFLAG) -o GSI.exe $(objfile): Command to link the object files and create the executable
GSI.exe: $(objfile)
	$(NVCC) $(EXEFLAG) -o GSI.exe $(objfile)

# Compile source files into object files
# Each target compiles a specific source file into its corresponding object file

# Compile Util.cpp into Util.o
$(objdir)Util.o: util/Util.cpp util/Util.h
	$(GCC_11_PATH)/bin/gcc-11 $(CFLAGS) util/Util.cpp -o $(objdir)Util.o

# Compile Graph.cpp into Graph.o
$(objdir)Graph.o: graph/Graph.cpp graph/Graph.h
	$(GCC_11_PATH)/bin/gcc-11 $(CFLAGS) graph/Graph.cpp -o $(objdir)Graph.o

# Compile IO.cpp into IO.o
$(objdir)IO.o: io/IO.cpp io/IO.h
	$(GCC_11_PATH)/bin/gcc-11 $(CFLAGS) io/IO.cpp -o $(objdir)IO.o

# Compile Match.cu into Match.o
$(objdir)Match.o: match/Match.cu match/Match.h
	$(NVCC) $(CFLAGS) match/Match.cu -o $(objdir)Match.o

# Compile run.cu into run.o
$(objdir)run.o: main/run.cu
	$(NVCC) $(CFLAGS) main/run.cu -o $(objdir)run.o

# Phony targets
# Targets that do not correspond to actual files
.PHONY: clean dist tarball test sumlines doc

# Clean target
# Remove all object files
clean:
	rm -f $(objdir)*

# Dist target
# Clean the directory and remove additional files
dist: clean
	rm -f *.txt *.exe
	rm -f *.g
	rm -f cuda-memcheck.*

# Tarball target
# Create a tarball of the project files
tarball:
	tar -czvf gsi.tar.gz main util match io graph Makefile README.md objs

# Test target
# Compile and link the test executable
test: $(objfile) main/test.cpp
	$(GCC_11_PATH)/bin/gcc-11 $(EXEFLAG) -o test main/test.cpp $(objfile)

# Sumlines target
# Run a script to sum lines of code
sumlines:
	bash script/sumline.sh

# Doc target
# Generate documentation using Doxygen
doc: 
	doxygen
