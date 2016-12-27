# github-admin-toolkit

Administrative templates and tools for use with GitHub repositories.

One of the reasons teams choose GitHub is because they want visibility in how they and their team works, who is contributing and how their project is being consumed. They also want the ability to showcase their project to others for ~advertisement purposes~ or because they are looking for outside contributors to make their project better.

The **github-admin-toolkit** attempts to help bridge the gap between simple content hosting and analytics gathering to give GitHub stakeholders visibility into their projects.


The GitHub API provides a way to automate and gather data about the content you store. The github-admin-toolkit provides a framework built around the GitHub API to let you get these statistics quickly, across a variety of platforms.

Enterprise customers use a private instance to store sensitive company intellectual property, while they may also use the public github.com to open source content and contribute to public projects.

# Contributing to the github-admin-toolkit

This section to be moved to **CONTRIBUTING.md**.

## Adding scripts

To add scripts to the toolkit, it is recommended to add the shell script (which sets required parameters) and add the associated python module method.

1. Navigate to the scripts directory and add a script file, using the below guideline.
2. Open the `./scripts/modules/github-admin-toolkit.py` module and add a method.

## Enhancement Ideas

Possible ideas:

- Dockerized Hubot
    - Separate the logical modules into a scheduler (i.e. Jenkins) and make it possible for both the dockerized hubot and the local bash script to call the remote job.
    - Separate dependency on the scheduler by having the scheduler simply clone from source

# How to run the tool

There is currently one way to run this tool, but several in planning. As of now, you can only run this tool from the command line, but the following methods are planned:

- Run from a job engine (Jenkins, Electric Commander, etc)
- Called via hubot

To run this tool from a Linux-based command line:

1. (Optional) Set the web proxy if you are behind a company firewall:

    ```
    export http_proxy=http://proxy.company.com:8080
    export https_proxy=http://proxy.company.com:8080
    ```

2. Clone the **github-admin-toolkit** repository and `cd` into the directory:

    ```
    git clone https://github.com/colossus9/github-admin-toolkit.git
    cd github-admin-toolkit
    ```

3. To see the **help** page, run the following and available usage info will be displayed:

    ```
    ./github-admin-toolkit.sh --help
    ```

4. From the command line, this utility is intended to present one or more **scripts** to be executed and the subsequent output to be displayed. To see the list of available scripts, run the following:

    ```
    ./github-admin-toolkit.sh --list
    ```

5. To run a script from the command line, specify it as an argument to `github-admin-toolkit.sh`. Below is an example:

    ```
    ./github-admin-toolkit.sh --server github.com --owner git --repo git getContributors
    ```