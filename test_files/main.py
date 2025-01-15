import datetime
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
    image = testing.get_language_image(
        language=language,
        base_url="rando-ga-test-harness"
    )
    #image.pull()

    print(image.url)

    for path in paths:
        testing.run_test(image, path)