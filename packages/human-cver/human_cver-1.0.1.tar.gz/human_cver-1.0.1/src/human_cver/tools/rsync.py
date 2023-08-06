"""同步数据
rsync 教程
https://www.ruanyifeng.com/blog/2020/08/rsync.html
"""
import os
import os.path as osp


def __fix_path(path: str) -> str:
    if not path.endswith("/"):
        path = path + "/"
    return path


def rsync(src_path: str, dst_path: str, delete: bool = False):
    """同步数据 copy src_path to dst_path

    Args:
        src_path (str): 源头文件夹
        dst_path (str): 目标文件夹
        delete (bool): 是否删除目标文件夹多余的文件(镜像)
    """
    if not osp.exists(dst_path):
        os.makedirs(dst_path, exist_ok=True)

    src_path = __fix_path(src_path)
    dst_path = __fix_path(dst_path)
    delete_text = " --delete " if delete else " "
    order = f"rsync -atvz{delete_text}{src_path} {dst_path}"
    print("[order]", order)
    os.system(order)


def rsync_ssh_upload(local_path: str, server_path: str, ip: str, port: int, user: str, password: str, delete: bool = False):
    """上传数据

    Args:
        local_path (str): 本地文件夹
        server_path (str): 服务器文件夹
        ip (str): 服务器IP
        port (int): 端口
        user (str): 用户名
        password (str): 密码
        delete (bool): 是否删除目标文件夹多余的文件(镜像)
    """
    local_path = __fix_path(local_path)
    server_path = __fix_path(server_path)
    delete_text = " --delete " if delete else " "
    order = f"sshpass -p {password} rsync -atvz{delete_text}-e 'ssh -p {port}' {local_path} {user}@{ip}:{server_path}"
    print("[order]", order)
    os.system(order)


def rsync_ssh_download(server_path: str, local_path: str, ip: str, port: int, user: str, password: str, delete: bool = False):
    """下载数据

    Args:
        server_path (str): 服务器文件夹
        local_path (str): 本地文件夹
        ip (str): 服务器IP
        port (int): 端口
        user (str): 用户名
        password (str): 密码
        delete (bool): 是否删除目标文件夹多余的文件(镜像)
    """
    if not osp.exists(local_path):
        os.makedirs(local_path, exist_ok=True)
    server_path = __fix_path(server_path)
    local_path = __fix_path(local_path)
    delete_text = " --delete " if delete else " "
    order = f"sshpass -p {password} rsync -atvz{delete_text} -e 'ssh -p {port}' {user}@{ip}:{server_path} {local_path}"
    print("[order]", order)
    os.system(order)
