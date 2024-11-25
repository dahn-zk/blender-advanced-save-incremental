from advanced_save_incremental.core import parse_stem
from advanced_save_incremental.core import StemParts
from advanced_save_incremental.core import Template
from advanced_save_incremental.core import Version
from advanced_save_incremental.core import VersionTemplate

def test_parse():
    stem = "John Doe - Project Foobar v3.0.12"
    version_template = VersionTemplate(
        separator = ".",
        count = 3,
        width = 1,
    )
    template = Template(
        prefix = "John Doe - ",
        suffix = " v",
        version = version_template
    )
    expected_stem_parts = StemParts(
        prefix = "John Doe - ",
        root = "Project Foobar",
        suffix = " v",
        version = Version(
            parts = [3, 0, 12],
            template = version_template,
        )
    )
    assert parse_stem(stem, template) == expected_stem_parts
