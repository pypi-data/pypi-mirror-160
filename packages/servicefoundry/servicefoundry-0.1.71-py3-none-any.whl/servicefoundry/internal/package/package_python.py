import logging

import pkg_resources

from servicefoundry.internal.package.package_docker import PackageDocker
from servicefoundry.internal.util import (
    create_file_from_content,
    manage_file_diff,
    read_text_from_file,
)
from servicefoundry.io.output_callback import OutputCallBack
from servicefoundry.requirements.python_requirements import PythonRequirements

logger = logging.getLogger()

NEWLINE = "\n"
REQUIREMENTS_TXT = "requirements.txt"


class PackagePython(PackageDocker):
    def package(self, callback: OutputCallBack):
        super().package(callback)
        if self.build_pack.dependency.auto_update:
            source_lines = read_text_from_file(REQUIREMENTS_TXT)
            requirements = PythonRequirements(source_lines)
            installed_packages = {
                d.project_name.lower(): d.version for d in pkg_resources.working_set
            }
            requirements.update_requirements_txt(installed_packages)
            target_lines = requirements.get_requirements_txt()
            manage_file_diff(source_lines, target_lines, REQUIREMENTS_TXT, callback)
            create_file_from_content(REQUIREMENTS_TXT, NEWLINE.join(target_lines))
