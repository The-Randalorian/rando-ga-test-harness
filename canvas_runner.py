import os
import pathlib
from pprint import pprint

# Import the Canvas class
from canvasapi import Canvas

# Import the custom testing code
import testing

# Canvas API URL
API_URL = os.getenv("RANDOGRADER_URL")
# Canvas API key
API_KEY = os.getenv("RANDOGRADER_TOKEN")
USER_ID = int(os.getenv("RANDOGRADER_UID"))
ROOT_DIR = pathlib.Path(__file__).parent / "grading"
ROOT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

user = canvas.get_user(USER_ID)

courses = [canvas.get_course(x) for x in (8884, 8878)]
for i, course in enumerate(courses):
    print(f"{i}. {course}")
course = courses[int(input("Select a course:"))]
course_dir = ROOT_DIR / str(course.name)
course_dir.mkdir(parents=True, exist_ok=True)

assignments = course.get_assignments()
for i, assignment in enumerate(assignments):
    print(f"{i}. {assignment.name}")
assignment = assignments[int(input("Select a assignment:"))]
assignment_dir = course_dir / str(assignment.name)
assignment_dir.mkdir(parents=True, exist_ok=True)

file_count = int(input("Select the number of files to run per student:"))
languages = ["scheme", "prolog", "clips"]
for i, language in enumerate(languages):
    print(f"{i}. {language}")
language = languages[int(input("Select a language:"))]

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

users = course.get_users(enrollment_type=['student'])
user_lookup = {}
for user in users:
    user_lookup[user.id] = user

'''
(begin (newline) (newline) (display "no=") (display (compare 1 6)) (newline) (display "yes=") (display (compare 3 6)) (newline) (newline) (display "3=") (display (sum1toN 2)) (newline) (display "55=") (display (sum1toN 10)) (newline) (newline) (display "4=") (display (len '(1 2 3 4))) (newline) (display "6=") (display (len '(a b c d e f))) (newline) (newline) (exit))
'''
evaluator = input("Enter an evaluation script: ")

upload_details = True

submissions = assignment.get_submissions(include=["submission_comments"])
for i, submission in enumerate(submissions):
    #pprint(submission.__dict__)
    submission_url = f"/api/v1/courses/{submission.course_id}/assignments/{submission.assignment_id}/submissions/{submission.user_id}"
    #print(submission_url)
    #exit()

    try:
        user = user_lookup[submission.user_id]
    except KeyError:
        continue

    print(f"Downloading and running submission {i}...")

    submission_dir = assignment_dir / user.name
    submission_dir.mkdir(parents=True, exist_ok=True)
    files = []
    for attachment in submission.attachments:
        file = submission_dir / attachment.filename
        if not file.exists():
            attachment.download(file)
        files.append(file)
    success = testing.run_test(submission_dir / user.name, image, files, testing.MAX_TIME, file_count, evaluator)

    if upload_details:
        if success:
            submission.edit(comment={'text_comment':'''-Automated Testing Report-
Your program ran successfully.
This does not mean a passing or failing grade. It only means your code ran.
Programs that do not run to completion will still be checked manually.
See .result file for details.'''})
        else:
            submission.edit(comment={'text_comment':'''Automated Testing Report:
Your program did not run successfully in the automated system.
This does not mean a passing or failing grade. It only means your code ran.
Programs that do not run to completion will still be checked manually.
See .result file for details.'''})

        f_path = submission_dir / (user.name + ".result")
        if f_path.stat().st_size > 0:
            submission.upload_comment(f_path)
        else:
            submission.edit(comment={'text_comment':".result file is empty, this is an error. The grader will handle this."})

        f_path = submission_dir / (user.name + ".stdout")
        if f_path.stat().st_size > 0:
            submission.upload_comment(f_path)
        else:
            submission.edit(comment={'text_comment':".stdout file is empty, your program did not generate output."})

        f_path = submission_dir / (user.name + ".stderr")
        if f_path.stat().st_size > 0:
            submission.upload_comment(f_path)
        else:
            pass # no errors, don't send an empty stderr

