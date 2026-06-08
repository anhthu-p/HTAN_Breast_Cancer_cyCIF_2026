# GPU Setup for Jupyter Notebook (Windows + Conda)

## 1. Check your CUDA version

```
nvidia-smi
```

Look for **CUDA Version** in the top-right corner of the output.

## 2. Install PyTorch with CUDA

Activate your environment first, then install the matching PyTorch build.

| Your CUDA version | Install command |
|-------------------|----------------|
| 11.8 | `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118` |
| 12.1 / 12.2 | `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121` |
| 12.4 | `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124` |

Example for this project (CUDA 12.2):

```
conda activate instanseg
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

## 3. Register the environment as a Jupyter kernel

```
conda activate instanseg
pip install ipykernel
python -m ipykernel install --user --name instanseg --display-name "Python (instanseg)"
```

Then in Jupyter: **Kernel → Change Kernel → Python (instanseg)**

## 4. Verify GPU is available

```python
import torch
print(torch.cuda.is_available())    # True
print(torch.cuda.get_device_name(0))
print(torch.version.cuda)           # should match your CUDA version
```

## Notes

- The conda environment must be re-registered as a kernel any time you create a new environment.
- `cu121` is compatible with CUDA 12.1 and 12.2.
- If `torch.cuda.is_available()` returns `False`, you likely installed the CPU-only build — reinstall using the index URL above.
