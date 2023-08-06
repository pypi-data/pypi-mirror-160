from pathlib import Path
from typing import Union


class LoaderException(Exception):
    pass


class Queries:
    def from_str(self, sql: str):
        sql = "\n".join([line for line in sql.split("\n") if line.strip()])
        units = sql.split(";")[:-1]

        for u in units:
            if "name:" not in u:
                continue

            name_comment, query = u.strip().split("\n", 1)
            name = name_comment.split(":", 1)[1].strip()
            name = name.replace(" ", "_")

            query = query.replace("\n", " ").strip() + ";"
            if hasattr(self, name):
                raise LoaderException(f'Name "{name}" already exists.')

            setattr(self, name, query)

        return self

    def from_file(self, file_path: Union[str, Path]):
        path = Path(file_path)

        if not path.exists():
            raise LoaderException(f"File doesn't exist: {path}.")

        if path.is_dir():
            raise LoaderException(f"The sql_file must be a file: {path}.")

        with path.open() as f:
            s = f.read()

        try:
            self.from_str(s)
        except LoaderException as e:
            raise LoaderException(f'File "{file_path}": ' + str(e))

        return self

    def from_dir(self, dir_path: Union[str, Path]):
        path = Path(dir_path)

        if not path.is_dir():
            raise LoaderException(f"The path {dir_path} must be a directory.")

        def _recursive(path: Path):

            if not path.exists():
                raise LoaderException(f"File doesn't exist: {path}.")

            if path.is_file():
                with path.open() as f:
                    s = f.read()

                self.from_str(s)

            elif path.is_dir():
                for p in path.iterdir():
                    if p.is_file() and p.suffix != ".sql":
                        continue
                    elif p.is_file() and p.suffix == ".sql":
                        with p.open() as f:
                            s = f.read()
                        self.from_str(s)
                    elif p.is_dir():
                        _recursive(path)
                    else:
                        raise LoaderException(
                            f"The path must be a directory or a file, got {p}."
                        )

        _recursive(path)

        return self

    def merge(self, *queries_objects: "Queries"):
        for queries in queries_objects:
            for key, value in queries.__dict__.items():
                if hasattr(self, key):
                    raise LoaderException(f'Name "{key}" already exists.')

                setattr(self, key, value)

        return self
