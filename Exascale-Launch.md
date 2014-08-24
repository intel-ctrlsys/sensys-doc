### Theory of Operation

Start from point of allocation. Broadcast is sent to all daemons involved in the allocation via the overlay network. Daemons on nodes involved in the allocation fork/exec a session daemon, with one designated as the shepherd for the job and the others in the lamb role. Explain role of shepherd vs lamb daemon: shepherd is responsible for coordinating the application, including executing any error management strategies if problems arise and reporting resource usage by the application at the end of the job. Each session daemon is given a static endpoint that other daemons in the session can use to connect into the overlay network topology.

Emphasize that no communication is allowed between session and root daemons. Root daemon creates shared memory segment and "drops" the application info into it, passing address and ownership to each session daemon upon launch. This includes allocation of endpoint resources for all procs on the local node, and for all procs on remote nodes. Typically, this is homogeneous by design, but can be heterogeneous if required. If endpoints cannot be allocated (or were not allocated for ORCM's use), then the PMIx wireup system will be used.

Each session daemon parses the application information to determine the number of processes in the job and any other details. The daemon then begins mapping the job to determine which procs are local to it. As each process is mapped, local procs are transferred to the ODLS for immediate launch while the mapper continues to process the application. This optimizes the parallel launch of processes.

As the mapper computes proc locations, it populates a shared memory database on the node with all known information about each process. This includes the location of the process, any pre-assigned endpoints, its binding locality, node and local rank. This requires homogeneous nodes, which is typical for large-scale systems.

