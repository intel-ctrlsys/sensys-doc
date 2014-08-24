### Theory of Operation

ORCM's model for in-flight analytics is loosely based on the [EVPath](http://www.cc.gatech.edu/systems/projects/EVPath/doxygen/evpath.html#evpath-intro) concept of a data flow graph (DFG) implemented as a state machine. Users can write an ORCM ''workflow'' that collects and passes data thru a specified graph, each node in that graph being executed as a distinct event-driven state. Use "stone" terminology for consistency.

NOTE: the workflow is an independent program written by the user and executed on an appropriate node. The analytics framework provides some commonly used algorithms that may be of use - however, the user is free to implement any algorithm of their choosing. Similarly, the analytics framework components can be tasked with pre-processing data prior to sending it to the workflow, or to send it to the workflow when specified conditions are met (alert-driven data transmission).

Analytics framework components can be "chained", passing data from the output of one to the input of the next upon completion of that analytic step.

Point to the overview of how ORCM uses libevent elsewhere on the wiki. Workflows automatically generate their own event base with its independent progress thread to avoid interfering with other program operations. This includes creation of a separate thread to execute any requested analytics framework operations. Important to recognize that each workflow represents an impact on computational load on the node where it is executing, planning required to avoid overtaxing the resource. Accordingly, workflows are not permitted on compute nodes, and daemons on compute nodes will not support the analytics framework. Note also that although multiple analytics components in the DFG may be specified in the workflow, each component will be processed in series as only one event state can be active at a time. Helps manage resource consumption.

Walk thru an example workflow. Workflows operate by:

  * initializing the system
  * "connecting" to data sources. Support both "push" and "pull" data collection methods - user can specify either one. Sources can include ORCM sensors and/or other processes in the SCON. Also includes ability to request pre-processing of data. 
  * analyzing received data

### Data Type Support

ORCM's data type support utilizes OPAL's Datatype Support System (DSS) for the packing and unpacking of data being sent between processes. Users can define their own structured data types, register them with DSS by including pack/unpack functions, etc.


