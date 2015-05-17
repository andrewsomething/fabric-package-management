# Functional Tests

These tests are run against a local Docker container that is treated like a
remote host. The Docker image is built from the Dockerfile in this directory
which simply provides a SSH server.

To run the tests, simply use:

    fab test