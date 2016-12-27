# github-admin-toolkit

Administrative templates and tools for use with GitHub repositories.

This toolkit provides a simple interface to interact with frequently used GitHub API endpoints. 

- **GitHub API Documentation:** https://developer.github.com/v3
- **GitHub API Status:** [![Build Status](https://travis-ci.org/colossus9/github-api-status.svg?branch=master)](https://travis-ci.org/colossus9/github-api-status)

# Why use this toolkit?

One of the reasons teams choose GitHub is because they want visibility in how they and their team works, who is contributing and how their project is being consumed. They also want the ability to showcase their project to others for ~advertisement purposes~ or because they are looking for outside contributors to make their project better.

The **github-admin-toolkit** attempts to help bridge the gap between simple content hosting and analytics gathering to give GitHub stakeholders visibility into their projects.

The GitHub API provides a way to automate and gather data about the content you store. The github-admin-toolkit provides a framework built around the GitHub API to let you get these statistics quickly, across a variety of platforms.

Enterprise customers use a private instance to store sensitive company intellectual property, while they may also use the public github.com to open source content and contribute to public projects.

# How to run the toolkit

There is currently one way to run this tool, but several in planning. As of now, you can only run this tool from the command line, but the following methods are planned:

- Run from a job engine (Jenkins, Electric Commander, etc)
- Called via hubot

To run this tool from a Linux-based command line:

1. **(Optional)** Set the web proxy if you are behind a company firewall:

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

5. Identify and provide options for the scripts you wish to run. Each script will provide specific output according to their descriptions. The **github-admin-toolkit** is capable of running against the public **github.com** or a **GitHub Enterprise** server (specified with the `[-s|--server]` option).

The following sections will describe a few script examples in detail.

## getContributors

The **getContributors** script will get a list of contributors for the specified **organization** or **repository**. If you only specify an **organization**, then the output will iterate over each public repository and provide contributors for each, as well as a summary at the end. If you specify both an **organization** and **repository**, contributor details will be displayed from only that repository. An HTTP 404 (Not Found) error may be thrown if you attempt to get data from a private repository.

To run **getContributors**:

1. Navigate to the directory where the repository is cloned.

2. To get a contributor summary for a GitHub **organization**, use the following sample command as a guide:

    ```
    ./github-admin-toolkit.sh --server github.com --owner git getContributors
    ```

3. To get a contributor list for a GitHub **organization/repository**, specify both as options using the following sample command as a guide:

    ```
    ./github-admin-toolkit.sh --server github.com --owner git --repo git getContributors
    ```

Remember to use the **help** option with `-h|--help` for a list of additional options you may wish to try, including **proxy** `-p|--proxy` and **debug** `-d|--debug` modes.

## getLatestRelease

TBD
