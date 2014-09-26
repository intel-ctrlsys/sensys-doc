####A.2.3.1 New Features

In general, the process for developing new features is as follows:

* Any new idea or feature should start with an RFC
* A review committee reserves the right to accept or refect the RFC
* RFCs should be sent at least 2 weeks prior to branching for a release to allow enough time for others to consider and review
* Once the RFC is accepted, its release timeline is defined (estimated)
* Once the code is ready, it should follow the normal development process for merging changes into mainline

On the GitHub ORCM project page, RFCs can be submitted as issues labeled as "RFC".

The following diagram shows the RFC process:

![RFC Process](Appendix/A.2-ORCM-Governance-Model/RFC-Process.png)
Source: https://svn.open-mpi.org/trac/ompi/attachment/wiki/DevProcess/OMPI%20RFC%20process.ppt

For more information, see: [OpenMPI Dev. Process](https://svn.open-mpi.org/trac/ompi/wiki/DevProcess)

####A.2.3.2 Development Procedure for a Release

The following diagram shows the development procedure for a release:

![Development Procedure for a Release](Appendix/A.2-ORCM-Governance-Model/Development-Procedure-for-Release.png)

####A.2.3.3 Code Reviews and Commit Procedures for ORCM

#####A.2.3.3.1 Legal

Before every release Intel will perform an IP (Intellectual Property) scan and developers will do a self-attestation.  After this, the IP plan and release BOM (Bill of Materials) will be reviewed with Intel Legal before the release.

#####A.2.3.3.2 Unit Tests

ORCM will have unit test suite, build-time tests and post-build tests.  Before a check-in, the tests should be run to ensure the quality of the code.  Intel will enable the infrastructure to run the unit tests automatically on the main trunk after every check-in.  If there are any test failures, the developer shall pull his changes from the trunk and fix the code.

#####A.2.3.3.3 New Tests

If developers develop new tests for new code (e.g. a new feature), they should check this code into the repository for inclusion in the appropriate automated test suites.

#####A.2.3.3.4 Moving R&D Code to Production

As part of moving code from "R&D status" to "production status" (in the main trunk), a design review is required.  The review committee should include at least two people not involved in the feature development.  Also, it should be announced at least one week in advance, giving anyone interested in participating in the review a chance to participate.  The intent of this review is to help establish requirements (functional and performance), if any, for inclusion in future release branches, and help identify impacts to other parts of the code as early as possible.

#####A.2.3.3.5 Code Review

For a release branch, it's required to have the code base section leader to review the code before committing.  The release manager can require a more rigorous code review process for particular commits based on severity, impact, cost and risk.  On the trunk, the gatekeeper makes sure that all code reviews have taken place before merging the code to the repo.

####A.2.3.5 Release Procedure

* Planning a release:
    * Generally planned in a developers' conference
    * Release criteria is defined
    * Features and quality requirements are defined
* A release manager is assigned
* Code is developed to meet the release goals
* Branch for the release
* The branch is tested until it meets the release criteria
* Release

####A.2.3.6 Changeset Move Requests

Since only gatekeepers have write permissions to release branches, developers must submit a Changeset Move Request (CMR) to get commits into a release branch.  On GitHub, these requests will be handled through Pull Requests.
