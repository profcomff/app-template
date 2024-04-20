from msilib.schema import File

PATH = "backend/pictures/"
FILE_NUMBER = 0


def safe_file(file: File):
    global FILE_NUMBER
    with open(f'{PATH}{FILE_NUMBER}.png', "wr") as f:
        f.write(file)
    FILE_NUMBER += 1
    return FILE_NUMBER - 1


def get_file_path(number: int):
    return f'{PATH}{number}.png' if number < FILE_NUMBER else None
