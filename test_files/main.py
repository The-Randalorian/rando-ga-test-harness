import datetime
import os
import pathlib

import testing


tests = {
    "scheme":[
        (pathlib.Path(".") / "test_files" / "pass.scm", ""),
        (pathlib.Path(".") / "test_files" / "fail-syntax.scm", ""),
        (pathlib.Path(".") / "test_files" / "eval.scm", "(begin (newline) (newline) (display (compare 1 6)) (newline) (display (compare 3 6)) (display (sum1toN 10)) (newline) (newline) (newline) (exit))")
        ],
    "prolog":[
        (pathlib.Path(".") / "test_files" / "pass.pl", ""),
        (pathlib.Path(".") / "test_files" / "fail-syntax.pl", ""),
        ],
    }


# If you really need speed, do some multiprocessing instead of a basic loop like this. That being said, with a 60 second
# limit (plenty of time for code to run) and ~100 students, this should still take less than 2 hours. If I have to get
# some dinner while it runs, I'll enjoy the break (or just start grading them while more are processing).
for language, tests in tests.items():
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

    for path, evaluator in tests:
        testing.run_test(image, path, evaluator=evaluator)