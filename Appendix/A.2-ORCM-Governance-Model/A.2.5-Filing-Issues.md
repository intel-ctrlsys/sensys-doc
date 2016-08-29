To file an issue in the ORCM project, please use the [issues section](https://github.com/intel-ctrlsys/sensys/issues) on the [GitHub ORCM project page](https://github.com/intel-ctrlsys/sensys) (which can be found as a tab on the right-hand side).

For each issue, please apply the approriate labels for proper filing and processing.  The labels that may be used are as follows:

* **bug**: issue that is considered a bug (i.e. exception conditions that the program is not handling correctly or in general when the program is not behaving as expected or documented).
* **documentation**: issues that are related to the documentation.
* **architectural**: issues that are known to be limitations of the ORCM implementation, support library implementation, operating system design or hardware capabilities.
* **fixed**: used to mark a bug as fixed (but still waiting for validation and approval).  Once the fix has been verified, the bug will be closed.
* **RFC**: used to propose new features or enhancements in the project.
* **duplicate**: applied to issues that turn out to be a duplicate of a previously filed issue.
* **question**: applied to issues that require further clarification from the filer.
* **release blocker**: during the release process, this label is applied to issues that are critical enough to block the release (until it's fixed).
* **wontfix**: for issues that have been acknowledged but after further review it has been determined that it won't be fixed (e.g. because it falls out of current scope, it's not critical enough to fix, lack of resources, etc.).

In general, the process for processing bugs is as follows:

1. Bug is filed.  Please include:
    * Release used
    * Configuration details (options used when building and running)
    * Details about the hardware on which the program was run
    * Failure details: error messages, issue frequency, instructions to reproduce
2. Bug is acknowledged and assessed:
    * Does it require fixing (is it a valid bug)?
    * Further classification: apply appropriate labels
    * Determine the rightful owner
    * Determine target release
3. Bug is fixed and the code is submitted for review
4. Once the code is approved, it is checked into the appropriate branch
    * NOTE: by this point the fix has to be already verified by unit testing (i.e. all unit tests should be passing with the new changes)
5. Bug is marked as fixed
6. Bug is verified and closed
