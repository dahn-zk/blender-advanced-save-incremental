from advanced_save_incremental.core import Template
from advanced_save_incremental.core import VersionTemplate

default_templates_example = [
    Template(
        name = "1st Template",
        prefix = "foo_",
        suffix = "_v",
        version = VersionTemplate(
            separator = "_",
            count = 2,
            width = 2,
        ),
    ),
    Template(
        name = "Unnamed Template",
        suffix = "-",
    ),
    Template(),
]
