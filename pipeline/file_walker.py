import os
from typing import List

def get_python_files(root_dir: str) -> List[str]:
    """遍历指定目录，获取所有Python文件路径（过滤无关目录）"""
    python_files = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('__pycache__', 'tests')]
        for file in files:
            if file.endswith('.py') and not file.startswith('.'):
                python_files.append(os.path.abspath(os.path.join(root, file)))
    return python_files

def get_project_versions(project_root: str) -> dict:
    """获取所有项目的版本目录（3个项目×5个版本）"""
    projects = {}
    if not os.path.exists(project_root):
        raise FileNotFoundError(f"项目根目录不存在：{project_root}")
    
    for project_name in os.listdir(project_root):
        project_dir = os.path.join(project_root, project_name)
        if not os.path.isdir(project_dir):
            continue
        
        versions = {}
        for version_name in sorted(os.listdir(project_dir)):
            version_dir = os.path.join(project_dir, version_name)
            if os.path.isdir(version_dir):
                versions[version_name] = version_dir
        
        if not versions:
            versions["default"] = project_dir
        projects[project_name] = versions
    
    return projects