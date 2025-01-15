import datetime
import os
import pathlib

import testing


tests = {
    "scheme":[
        pathlib.Path(".") / "test_files" / "pass.scm",
        pathlib.Path(".") / "test_files" / "fail-syntax.scm",
        ],
    "prolog":[
        pathlib.Path(".") / "test_files" / "pass.pl",
        pathlib.Path(".") / "test_files" / "fail-syntax.pl",
        ],
    }


for language, paths in tests.items():
    if os.getenv("TEST_HARNESS_LOCAL_IMAGES", default="false").lower() in ("true", "1", "t", "yes", "y"):
        image = testing.get_language_image(
            language=language,
            base_url="rando-ga-test-harness"
        )
    else:
        image = testing.get_language_image(
            language=language
        )
        image.pull()

    for path in paths:
        testing.run_test(image, path)