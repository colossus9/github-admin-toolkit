# How to contribute

:+1::tada: Thanks for taking the time to contribute! :tada::+1:

Your contributions are absolutely welcome in this repository! This toolkit was created with outside contributions in mind, but it can certainly use your feedback and changes. Feel free to propose your changes in a [Pull Request](https://help.github.com/articles/about-pull-requests/).

Please see the sections below for additional details if you wish to contribute back to the project.

## Using the Issues list

The [Issues list](https://github.com/colossus9/github-admin-toolkit/issues) is the best way to provide feedback or propose ideas. Take a look at **Open/Closed** Issues for reference.

## Adding scripts

The most common way to contribute is to add scripts into the toolkit, which is the base logic that gets the data you need. You may also contribute to the overall toolkit framework if you wish.

Use the below guide to add scripts to the toolkit:

1. [Fork](https://help.github.com/articles/fork-a-repo/) the repository
2. Add a script to the `/scripts` directory. Use existing scripts as a guide. These are used for:
    - Enable/Disable in the `--list` output
    - Ensure required vars are set
    - This script will **call** the associated method in the [Python module](https://github.com/colossus9/github-admin-toolkit/blob/master/scripts/modules/github-admin-toolkit.py)
3. Create a new method or Update the existing method of the same name in the [Python module](https://github.com/colossus9/github-admin-toolkit/blob/master/scripts/modules/github-admin-toolkit.py)
    - For example, if your script is called `scripts/getNeededData`, then the associated Python module method should be named `getNeededData()`

**To see a previous simple fully working change, see [this Pull Request](https://github.com/colossus9/github-admin-toolkit/pull/11).**

Please use existing code as a guide! It is well documented and formatted with comments.
