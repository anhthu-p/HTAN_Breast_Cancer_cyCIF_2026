# How to Create a New Conda Environment

## Why mamba instead of conda?

`mamba` is a faster drop-in replacement for `conda` — same commands, but solves dependencies much quicker. Install it once, use it everywhere.

```
conda install -n base -c conda-forge mamba
```

---

## Option 1 — Create from scratch

```
mamba create -n your_env_name python=3.11
mamba activate your_env_name
mamba install numpy pandas matplotlib scikit-image tifffile zarr jupyter ipykernel
```

To install in a custom location (like `D:\conda_envs\`):

```
mamba create -p D:\conda_envs\your_env_name python=3.11
mamba activate D:\conda_envs\your_env_name
```

---

## Option 2 — Create from environment.yml

```
mamba env create -f environment.yml
mamba activate your_env_name
```

To export your current environment to a yml file:

```
conda env export --no-builds > environment.yml
```
##### What if I have a yml already and I want to create the env in a specific location
mamba env create -f environment.yml -p D:\conda_envs\your_env_name


> **Tip:** `--no-builds` makes the file cross-platform (removes OS-specific build strings).

---

## Register as Jupyter kernel

After creating the environment, register it so Jupyter can see it:

```
mamba activate your_env_name
pip install ipykernel
python -m ipykernel install --user --name your_env_name --display-name "Python (your_env_name)
# or 
conda install --prefix D:\conda_envs\qualifai ipykernel --update-deps --force-reinstall # ALERT: pretty slow 
```

Then in Jupyter: **Kernel → Change Kernel → Python (your_env_name)**

---

## Install PyTorch with GPU (CUDA 12.2)

```
mamba activate your_env_name
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

See [gpu_setup.md](gpu_setup.md) for details on matching CUDA versions.
con
---

## Common commands

| Task | Command |
|------|---------|
| List all environments | `conda env list` |
| Remove an environment | `mamba env remove -n your_env_name` |
| List installed packages | `mamba list` |
| Update a package | `mamba update package_name` |
| Deactivate environment | `conda deactivate` |
