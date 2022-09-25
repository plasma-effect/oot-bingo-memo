from io import TextIOWrapper
import sys
import click
import yaml


def get_diff_elem(before_elem: dict, after_elem: dict) -> dict:
    ret = {}
    for key in before_elem:
        if key == "weight":
            continue
        if key in after_elem:
            if isinstance(before_elem[key], dict):
                diff = get_diff_elem(before_elem[key], after_elem[key])
                if diff:
                    if "changed" not in ret:
                        ret["changed"] = {}
                    ret["changed"][key] = diff
            elif before_elem[key] != after_elem[key]:
                if "changed" not in ret:
                    ret["changed"] = {}
                ret["changed"][key] = {
                    "before": before_elem[key],
                    "after": after_elem[key],
                }
        else:
            if "removed" not in ret:
                ret["removed"] = [key]
            else:
                ret["removed"].append(key)
    for key in after_elem:
        if key not in before_elem:
            if "new" not in ret:
                ret["new"] = [key]
            else:
                ret["new"].append(key)
    return ret


@click.command()
@click.argument("before", type=click.File(encoding="utf_8"))
@click.argument("after", type=click.File(encoding="utf_8"))
@click.option("--output", "-o", default="-")
def main(before: TextIOWrapper, after: TextIOWrapper, output: str):
    before_data = yaml.safe_load(before)
    after_data = yaml.safe_load(after)
    diff_data = {"changed": {}, "new": {}, "removed": {}}
    for key in before_data:
        if key in after_data:
            diff_elem = get_diff_elem(before_data[key], after_data[key])
            if diff_elem:
                diff_data["changed"][key] = {
                    "name": before_data[key]["name"],
                    "jp": before_data[key]["jp"],
                    "diff": diff_elem,
                }
        else:
            diff_data["removed"][key] = {
                "name": before_data[key]["name"],
                "jp": before_data[key]["jp"],
            }
    for key in after_data:
        if key not in before_data:
            diff_data["new"][key] = {
                "name": after_data[key]["name"],
                "jp": after_data[key]["jp"],
            }
    if output == "-":
        yaml.safe_dump(diff_data, sys.stdout.buffer, allow_unicode=True)
    else:
        with open(output, mode="w", encoding="utf_8") as f:
            yaml.safe_dump(diff_data, f, allow_unicode=True)


if __name__ == "__main__":
    main()
