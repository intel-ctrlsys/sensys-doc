# Roles and Responsabilities
#### Gatekeepers

Two gatekeepers are designated for each release series and have write permissions to the corresponding release branch.  Preferably, the gatekeepers should not be from the same organization.

After the branch, only the gatekeepers are allowed to write to the release branch.  Gatekeepers ensure that all changes to the release branches have been reviewed and should provide some level of sanity checking before committing (e.g. ensuring it compiles, running some tests, etc.).

#### Release Managers

Two release managers should govern the release process regarding the decisions made when the release is planned.  Just as for the gatekeepers, it's preferable that the release managers are not from the same organization.

The release managers take care of many of the details to make the release happen:

* They document and publish the entire process
* They delegate certain duties if necessary
* On a weekely basis, they track the status towards the release (e.g. they track bugs and performance issues) and publish the information where the team has access to it
* They come up with the schedule for the release (e.g. backward planning from the release date)
* They enforce the release schedule (e.g. by arbitrating the severity, impact, cost and risk of each issue)

#### Administrative Steering Committee

The administrative steering committee shall consist of one representative from each member organization.  The committee shall perform the following functions:

* Define the purpose of the project organization
* Plan release timelines based on available resources, target features and target goals of the member organizations
* Vote on all issues requiring group consensus (one vote per member organization)
* Assemble technical steering committees
* Nominate and approve the appointment of individuals to fill the roles of release manager, gatekeeper and meeting organizer (per release)

Note: the administrative committee is more important at the beginning of the project.  Once the team is solidified, the process requires less formality as consensus is reached more easily.  However, it's always important to have a committee as sometimes there are issues where reaching consensus is difficult.

#### General Voting Rules

1. The philosophy and goal of the Open MPI community is to reach consensus on most, if not all, issues.  In the event that full consensus cannot be reached, the administrative steering committee will apply the following rules.
2. On all issues requiring group consensus, all active community members eligible to vote (see rule 3 below) will receive one vote.  All votes are required to pass with 2/3 majority.  A quorum of members must vote (i.e. >50%).  Abstentions will not be counted in the total votes when calculating whether there is a 2/3 majority.
3. In order to participate in a vote a member must have attended two of the last three quarterly administrative meetings.
4. A member may send a proxy vote, but each phisical person can only cast one vote.  This prevents a member for voting on behalf of its own entity and acting as a proxy.
5. A periodic administrative voting cycle will be held quarterly.  The purpose of this voting cycle is to approve new members to the group as well as to vote on any additional administrative issues.  A voting agenda should be distributed to all current members of the group in advance.
6. In the event a consensus cannot be reached by the voting members with 2/3 majority, a special vote must be taken by a small governing body.
7. Urgent voting issues will be given a reasonable amount of time for voting to allow all members unable to attend the voting session to submit a vote not to exceed a week after the in-person voting session.  The amount of time will be set based on the urgency of the issue.  Voting will be allowed at the physical meeting, via email or via phone.

#### Committee Regular Meetings

There shall be a biweekly developers' meeting to discuss:

* Features
* Bugs
* Performance goals
* Release milestones

#### Reference

For more information regarding roles and responsibilities and the administrative steering committee, please see:

* [Open MPI Technical Guidelines](https://svn.open-mpi.org/trac/ompi/wiki/TechnicalGuidelines)
* [Open MPI Administrative Rules](https://svn.open-mpi.org/trac/ompi/wiki/Admistrative%20rules)