"""
Задание №7
✔ Создайте функцию для сортировки файлов по директориям: видео, изображения, текст и т.п.
✔ Каждая группа включает файлы с несколькими расширениями.
✔ В исходной папке должны остаться только те файлы, которые не подошли для сортировки.
"""

from contextlib import chdir
from pathlib import Path


def sort_files(path: str | Path, groups: dict[Path, list[str]] = None) -> None:
    chdir(path)
    if groups is None:
        groups = {
            Path('Photo'): ['jpg', 'jpeg', 'png', 'svg', 'gif'],
            Path('Video'): ['mp4', 'avi', 'mkv', 'mov'],
            Path('Music'): ['mp3', 'wav', 'ogg', 'flac']
        }
        reversed_groups = {}
        for directory, extension_list in groups.items():
            if not directory.is_dir():
                directory.mkdir()
            for extension in extension_list:
                reversed_groups[f'.{extension}'] = directory
        for file in path.iterdir():
            print(file.name)
            if file.is_file() and file.suffix in reversed_groups:
                file.replace(reversed_groups[file.suffix] / file.name)


if __name__ == '__main__':
    dir_work = Path.cwd()
    sort_files(dir_work)
