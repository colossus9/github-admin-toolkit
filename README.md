## Welcome to the github-admin-toolkit

Administrative templates and tools for use with GitHub repositories. :+1:

This toolkit provides a simple interface to interact with frequently used GitHub API endpoints. 

- **GitHub API Documentation:** https://developer.github.com/v3
- **GitHub API Status:** [![Build Status](https://travis-ci.org/colossus9/github-api-status.svg?branch=master)](https://travis-ci.org/colossus9/github-api-status)

:warning: Be sure to check out the [Issues List](https://github.com/colossus9/github-admin-toolkit/issues) for questions, enhancements, feedback, etc regarding this project.

# Description

Teams choose GitHub is because they want visibility in how their team works, including who is contributing and how their project is being consumed. GitHub doesn't just host project collateral, it is a Social Coding and Open/Inner Source platform that serves as the foundation for helping individuals, teams and companies ship and showcase great content.

The **github-admin-toolkit** attempts to help bridge the gap between simple content hosting and analytics gathering to give GitHub stakeholders visibility into their projects.

The GitHub API provides a mechanism to automate and gather data about the content you store. The github-admin-toolkit provides a framework built around the GitHub API to let you get these statistics quickly, across a variety of platforms.

Enterprise customers use a private instance to store sensitive company intellectual property, while they may also use the public github.com to open source content and contribute to public projects.

**Common uses** include: :thought_balloon:

 - Fine tune output to understand GitHub usage
 - Easily use commonly used API calls in specific formats
 - Customize output for business reports

:warning: Be sure to check out the [Issues List](https://github.com/colossus9/github-admin-toolkit/issues) for questions, enhancements, feedback, etc regarding this project.

# How to run the toolkit

Currently in planning there are several methods to run the tool, for example:

- Command line _(available today)_
- Run from a job engine (Jenkins, Electric Commander, etc)
- Called via hubot

As of today this tool is executed from a unix-based command line. 

![Command Line Animation](https://raw.githubusercontent.com/colossus9/github-admin-toolkit/master/media/github-admin-toolkit.gif)

To run this tool:

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

5. Identify and provide options for the scripts you wish to run. Each script will provide specific output according to their descriptions. The **github-admin-toolkit** is capable of running against the public **github.com** or a **GitHub Enterprise** server (specified with the `[-s|--server]` option), but some of the _preview_ API endpoints available on **github.com** are not yet available on **GitHub Enterprise**.

# See Also

Please check out the [wiki](https://github.com/colossus9/github-admin-toolkit/wiki) for additional details on implemented scripts.

