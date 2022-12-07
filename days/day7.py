"""
No Space Left On Device
"""
from functools import reduce

LIST_COMMAND = "$ ls"
CHANGE_TO_ROOT = "$ cd /"
NAVIGATE_OUT = "$ cd .."
DIR_KEYWORD = "dir"
PROMPT_KEYWORD = "$"


class File(object):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Directory(object):
    def __init__(self, name: str, files: list[File] = [], child_directories: list = [], parent=None):
        self.name = name
        self.files = files
        self.child_directories = child_directories
        self.parent = parent
        self.size = 0

    def calculate_size(self):
        for child in self.child_directories:
            child.calculate_size()
        self.size = sum(map(lambda file: file.size, self.files)) + sum(
            map(lambda directory: directory.size, self.child_directories))

    def __repr__(self):
        return self.name + " children: " + str(self.child_directories) + " size: " + str(self.size)


def is_not_command(command_or_output: str):
    return not command_or_output.startswith(PROMPT_KEYWORD)


def pop_files_and_directories(parent: Directory, commands_and_output: list[str]):
    output = []
    while len(commands_and_output) > 0 and is_not_command(commands_and_output[0]):
        file_or_directory = commands_and_output.pop(0)
        if file_or_directory.startswith(DIR_KEYWORD):
            _, directory_name = file_or_directory.split(" ")
            output.append(Directory(directory_name, parent=parent))
        else:
            size, name = file_or_directory.split(" ")
            output.append(File(name, int(size)))
    return output


def process_command(root_directory: Directory, current_directory: Directory, command: str,
                    commands_and_output: list[str]) -> Directory:
    if command == LIST_COMMAND:
        output = pop_files_and_directories(current_directory, commands_and_output)
        current_directory.child_directories = list(filter(lambda x: isinstance(x, Directory), output))
        current_directory.files = list(filter(lambda x: isinstance(x, File), output))
        return current_directory
    elif command == CHANGE_TO_ROOT:
        return root_directory
    elif command == NAVIGATE_OUT:
        return current_directory.parent
    else:
        # is change up a level
        _, _, directory_name = command.split(" ")
        matching_directories = list(
            filter(lambda directory: directory.name == directory_name, current_directory.child_directories))
        return matching_directories[0]


def create_file_tree(commands_and_output: list[str]) -> Directory:
    commands_and_output = list(map(lambda s: s.strip(), commands_and_output))
    root_directory = Directory('/')
    current_directory = root_directory
    while len(commands_and_output) > 0:
        command = commands_and_output.pop(0)
        current_directory = process_command(root_directory, current_directory, command, commands_and_output)

    return root_directory


def flatten(directory: Directory) -> list[Directory]:
    return [directory] + reduce(lambda a, b: a + b, map(lambda x: flatten(x), directory.child_directories), [])


def part_1(commands_and_output: list[str]) -> str:
    file_tree = create_file_tree(commands_and_output)
    file_tree.calculate_size()
    MAX_SIZE = 100000
    flattened = flatten(file_tree)
    total = sum(filter(lambda size: size <= MAX_SIZE, map(lambda directory: directory.size, flattened)))
    return str(total)


def part_2(commands_and_output: list[str]) -> str:
    SPACE_REQUIRED = 30000000
    TOTAL_DISK_SPACE = 70000000
    file_tree = create_file_tree(commands_and_output)
    file_tree.calculate_size()
    free_space = TOTAL_DISK_SPACE - file_tree.size
    threshold = SPACE_REQUIRED - free_space
    flattened = flatten(file_tree)
    minimum_directory_above_size = \
        sorted(filter(lambda size: size >= threshold, map(lambda directory: directory.size, flattened)))[0]
    return str(minimum_directory_above_size)
