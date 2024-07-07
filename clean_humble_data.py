import argparse
import json
from pathlib import Path


def clear_humble_data_notebook(fp, activate_magic: bool = False, encoding: str = 'utf-8'):
    """
    This function changes all notebooks.

    It removes the solutions and restores the "# %load" magic

    optionally it uncomments it for quick testing of the notebook

    """
    nb = Path(fp)
    nb_content = json.loads(nb.read_text(encoding=encoding))

    for c in nb_content['cells']:
        if c.get('cell_type') == 'code':
            if c.get('execution_count') is not None:
                c['outputs'] = []
                c['execution_count'] = None
            try:
                if c['source'][0].startswith("# %load .."):
                    c['source'] = [c['source'][0]]
                elif c['source'][0].startswith("%load .."):
                    c['source'] = ["# " + c['source'][0]]

                if activate_magic:
                    if c['source'][0].startswith("# %load .."):
                        c['source'] = [c['source'][0][2:]]

            except IndexError:
                pass

    count_bytes = nb.write_text(
        json.dumps(nb_content), encoding=encoding
    )

    print(f"Saved {count_bytes} bytes in '{fp}'.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Clear humble data notebooks.")
    parser.add_argument('--path', default="notebooks", help="Path to the directory containing the notebooks.")
    parser.add_argument('--activate_magic', '-a', action='store_true', help="Activate magic functions in the notebook.")

    args = parser.parse_args()

    for fp in Path(args.path).glob("*.ipynb"):
        clear_humble_data_notebook(fp, args.activate_magic)