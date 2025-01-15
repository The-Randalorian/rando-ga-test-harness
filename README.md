# The Randalorian's Grading Test Harness
This is a set of test containers for running student assignments. Each student's code is run in a fresh docker container to both help protect my machine and ensure each student has the same environment for their code. I'm publishing this code so that students can use it to test their own code in the same environment I'll be using.

This is less of a test program, and more of a test program platform. It's supposed to make it easier to create grading programs that check the actual output text. This system greatly simplifies the process of creating containers, running code, and tearing everything down for the next student.

For my students: This is not the only criteria I use to grade your code. Just because your code fails a test here doesn't mean it's going to lose points. I always check the output to verify there aren't minor formatting issues. If your code fails to run though, that's always going to at least lose several points.

## Installation

Clone the repository. Docker images and other necessary components are downloaded as needed.

## Usage
WIP, for now, just run `test_files/main.py` to see how it works.