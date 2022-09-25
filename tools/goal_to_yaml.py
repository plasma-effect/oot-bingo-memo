import json
from typing import Any, Dict, List
import click


def expand(data: Dict[str, List[dict]], filename: str):
    with open(filename, mode="w", encoding="utf_8") as f:

        def write(line: str):
            print(line, file=f)

        def write_item(key: Any, item: Any, depth: int = 1):
            if isinstance(item, dict):
                write(f"{'  ' * depth}{key}:")
                for ckey, citem in item.items():
                    write_item(ckey, citem, depth + 1)
            else:
                write(f"{'  ' * depth}{key}: {item}")

        for index in [str(i + 1) for i in range(25)]:
            for d in data[index]:
                write(f'{d["id"]}:')
                for key, item in d.items():
                    if key == "id":
                        continue
                    write_item(key, item)


@click.command()
@click.argument("input-file", type=str)
@click.option("--short", "-s", type=str, required=True)
@click.option("--normal", "-n", type=str, required=True)
def main(input_file: str, short: str, normal: str):
    with open(input_file, encoding="utf_8") as file:
        s = file.read()
        start = s.find("{")
        end = s.find(";")
        if end == -1:
            raw = json.loads(s[start:])
        else:
            raw = json.loads(s[start:end])
        expand(raw["short"], short)
        expand(raw["normal"], normal)


if __name__ == "__main__":
    main()
