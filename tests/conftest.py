import pathlib
import sys

src_dir = pathlib.Path(__file__).parents[1].absolute() / "src"
sys.path.append(src_dir.as_posix())
