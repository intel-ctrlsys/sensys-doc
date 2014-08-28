The Open Resilient Cluster Manager (ORCM) was originally developed as an open-source project (under the Open MPI license) by Cisco Systems, Inc to provide a resilient, 100% uptime run-time environment for enterprise-class routers. Based on the Open Run-Time Environment (ORTE) embedded in Open MPI, the system provided launch and execution support for processes executing within the router itself (e.g., computing routing tables), ensuring that a minimum number of copies of each program were always present. Failed processes were relocated based on the concept of fault groups - i.e., the grouping of nodes with common failure modes. Thus, ORCM attempted to avoid cascade failures by ensuring that processes were not relocated onto nodes with a high probability of failing in the immediate future.

The Cisco implementation naturally required a significant amount of monitoring, and included the notion of fault prediction as a means of taking pre-emptive action to relocate processes prior to their node failing. This was facilitated using an analytics framework that allowed users to chain various analysis modules in the data pipeline so as to perform in-flight data reduction.

Subsequently, ORCM was extended by Greenplum to serve as a scalable monitoring system for Hadoop clusters. While ORCM itself had run on quite a few "nodes" in the Cisco router, and its base ORTE platform has been used for years on very large clusters involving many thousands of nodes, this was the first time the ORCM/ORTE platform had been used solely as a system state-of-health monitor with no responsibility for process launch or monitoring. Instead, ORCM was asked to provide a resilient, scalable monitoring capability that tracked process resource utilization and node state-of-health, collecting all the data in a database for subsequent analysis. Sampling rates were low enough that in-flight data reduction was not required, nor was fault prediction considered to be of value in the Hadoop paradigm.

However, data flows did require introduction of an aggregator role. Aggregators absorb the data sent by other nodes and can either store the data in a database, analyze the data, or both. The objective of the aggregator is primarily to concentrate the database operations, thus minimizing the number of active connections to the database itself.

Throughout this time, ORCM has retained ORTE's ability to perform scalable launch and process monitoring, and ORTE's support for a variety of scheduling environments. We are now in the process of validating and extending ORCM to provide both monitoring and launch support for exascale environments.

### Core Features

* Plugin architecture based on Open MPI's Module Component Architecture (MCA)
  * Sophisticated auto-select algorithms based on system size, available resources
  * Binary proprietary plugin support
  * On-the-fly updates for maintenance*
  * Addition of new plugin capabilities/features without requiring system-wide restart if compatibility requirements are met

* Hardware discovery support
  * Automatic reporting of hardware inventory on startup
  * Automatic updating upon node removal and replacement

* Provisioning support
  * Images provisioned based on user directive prior to launch*

* Scalable overlay network
  * Supports multiple topologies, including both tree and mesh plugins
  * Automatic route failover and restoration, messages cached pending comm recovery
  * Both in-band and out-of-band transports with auto-failover between them

* Sensors
  * Both push and pull models supported
  * Read as a group at regular intervals according to a specified rate, or individual sensors can be read at their own regular interval, or individual readings of any combination of sensors can be polled upon request
  * Polling requests can return information directly to the caller, or can include the reading in the next database update, as specified by the caller
  * Data collected locally and sent to an aggregator for recording into a database at specified time intervals
  * Environment sensors
    * Processor temperature - on-board sensor for reading processor temperatures when coretemp kernel module loaded
    * Processor frequency - on-board sensor for reading processor frequencies. Requires read access to /sys/devices/system/cpu directory
    * IPMI readings of AC power, cabinet temperature, water and air temperatures, etc.
    * Processor power - reading processor power from on-board MSR. Only supported for Intel SandyBridge, IvyBridge, and Haswell processors
  * Resource utilization
    * Wide range of process and node-level resource utilization, including memory, cpu, network I/O, and disk I/O
  * Process failure
    * Monitors specified file(s) for programmatic access within specified time intervals and/or file size restrictions
    * Heartbeat monitoring

* Analytics*
  * Supports in-flight reduction of sensor data
  * User-defined workflows for data analysis using available plugins connected in user-defined chains
  * Analysis chain outputs can be included in database reporting or sent to requestor at user direction
  * Plugins can support event and alert generation
  * "Tap" plugin directs copied stream of selected data from specified point to remote requestor
  * Chains can be defined at any aggregation point in system

* Database
  * Both raw and processed data can be stored in one or more databases
  * Supports both SQL and non-SQL* databases
    * Multiple instances of either type can be used in parallel*
    * Target database for different data sources and/or types can be specified using MCA parameters during configure and startup, and can be altered by command during operation*
  * Cross-data correlation maintained
    * Relationship between job, sensor, and performance data tracked and linked for easy retrieval*

* Scalable launch
  * Distributed mapping system to minimize data transmission of launch commands*
  * Rapid MPI wireup
    * Endpoint management and support for static endpoints, enabling communication upon init
    * [PMIx](https://github.com/open-mpi/pmix/wiki) wireup support for unmanaged environments*
    * Automatic pre-positioning of dynamic libraries*
    * Pre-loading of libraries and data by user directive*

* Fault Tolerance
  * Self-healing communication system (see above)
  * Non-heartbeat detection of node failures
  * Automatic state recovery based on retrieval of state information from peers*
  * Support for time-based checkpoint of applications*
  * Burst buffer management for rapid checkpoint/restart*

*indicates areas of development

### Documentation
Detailed documentation on the design of ORCM itself is under development on the [ORCM developer page](https://github.com/open-mpi/orcm/wiki/Developer).

### Getting and using ORCM

There are no ORCM releases at this time. The GIT repository is accessible for online browsing or checkout.

### Questions and bugs
Questions, comments, and bugs should be sent to [ORCM mailing lists](http://www.open-mpi.org/community/lists/orcm.php). Passing --enable-debug to ./configure also enables a lot of helpful debugging information.

Also be sure to see the [ORCM wiki](https://github.com/open-mpi/orcm/wiki) and bug tracking system. 