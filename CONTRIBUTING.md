# Contributing to the github-admin-toolkit

Your contributions are absolutely welcome in this repository! This toolkit was created with outside contributions in mind, but it can certainly use your feedback and changes.

Please see the sections below for additional details if you wish to contribute back to the project.

## Adding scripts

To add scripts to the toolkit, it is recommended to add the shell script (which sets required parameters) and add the associated python module method.

1. Navigate to the scripts directory and add a script file, using the below guideline.
2. Open the `./scripts/modules/github-admin-toolkit.py` module and add a method.

## Enhancement Ideas

Possible ideas:

- Dockerized Hubot
    - Separate the logical modules into a scheduler (i.e. Jenkins) and make it possible for both the dockerized hubot and the local bash script to call the remote job.
    - Separate dependency on the scheduler by having the scheduler simply clone from source
