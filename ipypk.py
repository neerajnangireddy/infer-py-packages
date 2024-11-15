#!/usr/bin/env python

"""
This script scans all the python files in project directory
and prints out the external packages that the project depends on.
""" 

import re
import os
import sys
import argparse


def extract_packages(line, compiled_regex):
    """
    Extract the packages name from the import/from statements.
    """

    if not line.strip().startswith(("import", "from")):
        return None

    # This function should return a list. (I fucking ment a list.)
    match = compiled_regex.match(line)
    if match:
        match = match.group()
        # print(match)
        match = filter(None, re.split(r"import |from | as.*|,| +", match))
        return [m.split(".", maxsplit=1)[0] for m in match]
        
    return None


def extract_imports(filepath, local_dirs_and_files, compiled_regex):
    """
    Extact the import statements from a file.
    And then extract the packages.
    """

    if not filepath.endswith(".py"):
        return None

    packages_jar = []
    with open(filepath, mode="r", encoding="utf-8") as file:
        for line in file:
            if line.strip().startswith(("import", "from")):
                packages = extract_packages(line, compiled_regex=compiled_regex)
                if packages:
                    packages_jar.extend(packages)

    # Remove the local packages.
    return set(packages_jar) - set(local_dirs_and_files)


def travel_project(project_dir_path, exclude_dirs):
    """
    Walk along the project and extract the packages from the .py files.

    """

    # White space infront of import statements should be checked.
    # As import statements can also be found in functions. 
    from_and_import_regex = re.compile(r"( *from +[a-zA-Z0-9_.]+ +import )|( *import *(\w *, *|\w *)+) as?")
    packages_jar = set()

    for root, dirs, files in os.walk(project_dir_path):
        # Construct a list with filenames(no ext) and dir names 
        # To remove local packages and modules.
        local_dirs_and_files = [f.rsplit(".")[0] for f in files if f.endswith(".py")]
        local_dirs_and_files.extend(dirs)
        for file in files:
            if file.endswith(".py"):
                print("processing: ", os.path.join(root, file))
                packages = extract_imports(os.path.join(root, file), local_dirs_and_files=local_dirs_and_files, compiled_regex=from_and_import_regex)
                if packages:
                    packages_jar.update(packages)

        for ex_dir in exclude_dirs:
            if ex_dir in dirs:
                dirs.remove(ex_dir)

    # Remove standard library modules and builtin modules.
    return set(packages_jar) - (set(sys.stdlib_module_names) | set(sys.builtin_module_names))


def main(project_dir_path: str):
    """
    The entry point for script.
    """

    exclude_dirs = ["venv", "__pycache__"]
    packages = travel_project(project_dir_path, exclude_dirs)
    print("\nPackages Found:")
    for pack in packages:
        print(pack)
    print()    


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
            prog="Infer py packages.",
            description="This script scans all the python files in project directory\
                            and prints out the external packages that the project depends on."
            )
    arg_parser.add_argument("-d", "--dir", help="Project Directory.", required=True)
    args = arg_parser.parse_args()

    if os.path.exists(args.dir):
        main(args.dir)
    else:
        print(f"{args.main} Doesn't Exists")


