import subprocess
import shutil
import matplotlib.pyplot as plt
import scienceplots
import warnings
import os

def plot_style():
    plt.style.use(['science', 'ieee'])

def optimize_svg(path):
    # Run SVGO if available
    if shutil.which("svgo") is not None:
        subprocess.run([shutil.which("svgo"), path])

def save_plot(path):
    if path.split(".")[-1] != 'svg':
        warnings.warn(f"Filepath: {path} doesn't end with .svg and is added in code")
        path = f"{path}.svg" 

    plt.tight_layout()
    plt.savefig(path, transparent=True)
    optimize_svg(path)
