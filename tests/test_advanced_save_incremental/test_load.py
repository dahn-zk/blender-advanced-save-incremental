import pathlib

from advanced_save_incremental.core.persistence import templates_export
from advanced_save_incremental.core.persistence import templates_import
from test_advanced_save_incremental.fixtures import default_templates_example

dir_path = pathlib.Path(__file__).absolute().parent

def test_import():
    file_path = dir_path / "fixtures/default-templates-example.toml"
    assert templates_import(file_path) == default_templates_example

def test_export():
    file_path = dir_path / "output/exported-templates-example.toml"
    templates_export(file_path, default_templates_example)
    assert default_templates_example == templates_import(file_path)
