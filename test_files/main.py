import datetime
import pathlib

import testing

paths = [
    pathlib.Path(".") / "test_files" / "pass.scm",
    pathlib.Path(".") / "test_files" / "fail-syntax.scm",
]

scheme_image = testing.get_language_image(
    language="scheme",
    #base_url="rando-ga-test-harness"
)
scheme_image.pull()

for path in paths:
    testing.run_test(scheme_image, path)