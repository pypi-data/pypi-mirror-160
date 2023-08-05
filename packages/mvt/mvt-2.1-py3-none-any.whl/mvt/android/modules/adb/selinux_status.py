# Mobile Verification Toolkit (MVT)
# Copyright (c) 2021-2022 Claudio Guarnieri.
# Use of this software is governed by the MVT License 1.1 that can be found at
#   https://license.mvt.re/1.1/

import logging

from .base import AndroidExtraction

log = logging.getLogger(__name__)


class SELinuxStatus(AndroidExtraction):
    """This module checks if SELinux is being enforced."""

    slug = "selinux_status"

    def __init__(self, file_path: str = None, target_path: str = None,
                 results_path: str = None, fast_mode: bool = False,
                 log: logging.Logger = None, results: list = []) -> None:
        super().__init__(file_path=file_path, target_path=target_path,
                         results_path=results_path, fast_mode=fast_mode,
                         log=log, results=results)

        self.results = {} if not results else results

    def run(self) -> None:
        self._adb_connect()
        output = self._adb_command("getenforce")
        self._adb_disconnect()

        status = output.lower().strip()
        self.results["status"] = status

        if status == "enforcing":
            self.log.info("SELinux is being regularly enforced")
        else:
            self.log.warning("SELinux status is \"%s\"!", status)
