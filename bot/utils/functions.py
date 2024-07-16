import datetime
import os as _os
import pkgutil as _pkgutil
from typing import Iterator as _Iterator

import disnake


def protected(user_id: str):
    with open("./data/protected.txt", "r") as file:
        if str(user_id) in file.read():
            return True
        
        return False
    

def create_error_embed(err : str) -> disnake.Embed:
    err_embed = disnake.Embed(title="We Got an Error!",
                              color=disnake.Color.from_rgb(255, 3, 7),
                              description="<:tiredskull:1195760828134211594> "+str(err),
                              timestamp=datetime.datetime.now())

    return err_embed

def chunker(text, chunk_size: int) -> list:
    length = len(text)
    num = 0
    chunks = []

    while num < len(text):
        chunks.append(text[num:length-(length-(chunk_size))+num:])
        num+=chunk_size

    return chunks

def list_all_dirs(root_dir):
    """
    List all directories in the given root directory and its subdirectories.
    
    Parameters:
    root_dir (str): The root directory to start searching from.
    
    Returns:
    List[str]: A list of all directories.
    """
        
    for dirpath, dirnames, filenames in _os.walk(root_dir):
        for dirname in dirnames:
            full_path = _os.path.join(dirpath, dirname)
            yield full_path
    
def search_directory(path: str) -> _Iterator[str]:
    """Walk through a directory and yield all modules.

    Parameters
    ----------
    path: :class:`str`
        The path to search for modules

    Yields
    ------
    :class:`str`
        The name of the found module. (usable in load_extension)
    """
    relpath = _os.path.relpath(path)  # relative and normalized
    if ".." in relpath:
        raise ValueError("Modules outside the cwd require a package to be specified")

    abspath = _os.path.abspath(path)
    if not _os.path.exists(relpath):
        raise ValueError(f"Provided path '{abspath}' does not exist")
    if not _os.path.isdir(relpath):
        raise ValueError(f"Provided path '{abspath}' is not a directory")

    prefix = relpath.replace(_os.sep, ".")
    if prefix in ("", "."):
        prefix = ""
    else:
        prefix += "."

    for _, name, ispkg in _pkgutil.iter_modules([path]):
        if ispkg:
            yield from search_directory(_os.path.join(path, name))
        else:
            yield prefix + name