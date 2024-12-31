# Subclone

This is a simple python script to download a github subdirectory (folder) instead of cloning the whole repo.

### Usage

```sh
python3 subclone.py [-h] [--name NAME_OPTIONAL] [-k] url
```

- `-h` displays help menu.
- `[--name NAME_OPTIONAL]` Optional. Change the name of the downloaded directory to `NAME_OPTIONAL`.
- `[-k]` or `[--keep-git]` Optional. Keep the original repo structure instead of moving the target directory to current working directory.

> Note: You cannot use `-k` and `--name` at the same time.

### Example

`python3 subclone.py --name firebird24 https://github.com/sajjadium/ctf-archives/tree/main/ctfs/HKUSTFirebird/2024`

### Platform support
Both Linux (recommended) and Windows (NTFS) are supported. However, if the repo you are trying to clone into has filenames that contain illegal characters (a problem more common on NTFS, especially with files with `.` in the name), the script will not work.