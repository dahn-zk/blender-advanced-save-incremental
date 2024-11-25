from advanced_save_incremental.core import build_version_str
from advanced_save_incremental.core import file_name_get
from advanced_save_incremental.core import version_increment
from advanced_save_incremental.core import Template
from advanced_save_incremental.core import VersionTemplate

def test_file_name_get():
    file_name = f"John Doe - Project Foobar v03.00.12.blend"
    template = Template(
        prefix = "John Doe - ",
        suffix = " v",
        version = VersionTemplate(
            separator = ".",
            count = 3,
            width = 2,
        )
    )
    version_parts = [3, 0, 12]
    assert file_name_get(template, "Project Foobar", version_parts) == file_name

def test_version_increment():
    assert version_increment([3, 0, 12], idx = 0) == [4, 0, 0]
    assert version_increment([3, 0, 12], idx = 1) == [3, 1, 0]
    assert version_increment([3, 0, 12], idx = 2) == [3, 0, 13]
    assert version_increment([3, 0, 12], idx = 3) == [3, 0, 12, 1]
    assert version_increment([3, 0, 12]) == [3, 0, 13]
    assert version_increment([3], idx = 0, count = 3) == [4, 0, 0]

def test_build_version_str():
    assert build_version_str(VersionTemplate(".", 3, 1), [3, 0, 12]) == "3.0.12"
    assert build_version_str(VersionTemplate(".", 3, 2), [3, 0, 12]) == "03.00.12"
    assert build_version_str(VersionTemplate(".", 3, 3), [3, 0, 12]) == "003.000.012"
    assert build_version_str(VersionTemplate(".", 1, 1), [3, 0, 12]) == "3"
    assert build_version_str(VersionTemplate(".", 1, 2), [3, 0, 12]) == "03"
    assert build_version_str(VersionTemplate(".", 1, 3), [3, 0, 12]) == "003"
