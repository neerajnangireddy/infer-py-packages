# Infer Python Packages

This script aims to find the external dependencies(python packages) of a python project.

## Installation (user wide)

### Linux

```console
curl --proto '=https' --tlsv1.2 -H 'Cache-Control: no-cache' -f https://raw.githubusercontent.com/neerajnangireddy/infer-py-packages/refs/heads/main/ipypk_install.sh | sh
```

## Usage

```console
ipypk -d "project_dir_path"

```

## Alternatively use without installing.

```console
git clone --depth=1 https://github.com/neerajnangireddy/infer-py-packages.git
cd infer-py-packages
# To run
python3 ipypk.py -d "project_folder_path"
```
