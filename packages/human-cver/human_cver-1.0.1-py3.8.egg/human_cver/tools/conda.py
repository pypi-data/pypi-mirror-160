"""conda"""
import os


def export_env(yaml_filename: str = "env.yaml"):
    """导出conda环境"""
    os.system(f"conda env export > {yaml_filename}")
