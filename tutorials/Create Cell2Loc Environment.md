# Create Cell2Location Environment to Use with GPU/CPU

Before creating the environment, we need to tell python to NOT use user site for installing packages. This needs to be run  every time before activating the conda environment in a new terminal session 

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
pip3 install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 -f https://download.pytorch.org/whl/torch_stable.html
```

### Add Jupyter Kernel

```
conda activate cell2loc_env
python -m ipykernel install --user --name=cell2loc_env --display-name='Environment (cell2loc_env)'
```

### Downloading the necessary dependencies for downstream analysis

Remove any packages from this list that you will not be using.


