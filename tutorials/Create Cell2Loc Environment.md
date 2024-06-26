# Create Cell2Location Environment to Use with GPU/CPU

A large part of the code below was borrowed from cell2location's documention, which can be found [here](https://github.com/BayraktarLab/cell2location#installation-of-dependecies-and-configuring-environment). 

Before creating the environment, we need to tell python to not use user site for installing packages. This needs to be run  every time before activating the conda environment in a new terminal session 

`export PYTHONNOUSERSITE="literallyanyletters"`

### If you want to create an environment to use only with CPU:

Create and activate environment with python 3.9. Install cell2location. 

```
conda create -y -n cell2loc_env python=3.9
conda activate cell2loc_env
pip install cell2location[tutorials]
```

### If you want to create an environment to use with A100 GPU.

```
export PYTHONNOUSERSITE="literallyanyletters"
conda create -y -n cell2loc_env python=3.9
conda activate cell2loc_env 
pip install scvi-tools
pip install git+https://github.com/BayraktarLab/cell2location.git#egg=cell2location[tutorials]
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121
pip install --upgrade "jax[cuda12]"
```

### Add Jupyter Kernel

```
conda activate cell2loc_env
conda install anaconda::ipykernel
python -m ipykernel install --user --name=cell2loc_env --display-name='Environment (cell2loc_env)'
```

### Downloading the necessary dependencies for downstream analysis

Remove any packages from this list that you will not be using.

```
conda install -c conda-forge scanpy python-igraph leidenalg
conda install scipy
pip install squidpy
pip install gtfparse
```

### For Mount Sinai Users: Requesting Jupyter with GPU to use cell2location:

```
minerva-jupyter-module-web.sh --mem 50000 --timelimit 12:00 --ncpus 4 -mm anaconda3/2021.5,cuda/12.1.1 -env /insert/path/to/cell2loc_env -q gpuexpress -R a100 --ngpus 2
```