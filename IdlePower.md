Saving power when nodes are not being used is a big deal in most installations - having a cluster sit there burning full power while idle, especially when it was set to performance mode, represents a significant cost in places where usage is “on demand” as opposed to constant. Administrators therefore value a system that can be directed via policy to automatically put nodes in a reduced power mode when idle for more than a specified time, and then bring them back online when needed. Sys admins also need to take nodes offline (leaving them powered up), and order nodes to power down, for maintenance purposes, and would like to track those as distinct from a node failing as the implications in terms of specified policies could be different.

Sensys's approach to such requirements is to provide mechanisms by which users can control the system's behavior, and then allow those users to establish policies indicating when an dhow those controls are to be used. In this case, Sensys provides two mechanisms for minimizing the amount of lost energy while in idle mode:

* powering the node ''off'' - this represents the minimum energy impact, but requires that the node effectively reboot prior to becoming available for the next session; and

* setting the node to ''idle'' - i.e., the minimum frequency or power state. This allows the node to remain active and able to rapidly respond to the next session request, including ramping its frequency and/or power state to maximum, but does continue to consume some idle power.

Sensys supports the following policy definitions:

* time a node remains unallocated before placing it in ''standby'' mode

* power setting for nodes declared ''standby'' by the scheduler. Nodes set to ''idle'' power will be declared on ''active standby'', while those set to ''off'' will be marked as in ''cold standby'' to indicate that a longer recovery time is required.

* minimum number of nodes on ''active standby'' - i.e., the number of nodes which must be available at ''idle'' power when no sessions are currently active. This represents a pool of nodes immediately available for allocation without delays for power-on reboot. If the default power setting for nodes declared on ''standby'' by the scheduler is defined as ''off'', then the scheduler will ensure that at least this many nodes in the standby pool are retained at ''idle'' power.

* default power setting between sessions. Nodes are declared "deallocated" and returned to the general pool for reassignment upon completion of a session. This policy defines the power state into which the local daemon will set the node upon reporting the session as complete. For example, the system admin may choose to have nodes set to ''idle'' power upon completion of a session, but set to ''off'' by the scheduler if unallocated for a long period of time.

* default power setting between executions - during the course of a session, users may execute jobs on all or some portion of the allocation at any given time. Nodes within an allocation that are not currently being used can be set to ''idle'' power until needed, and restored to the default or specified power setting for the job upon next execution.

The typical power-up procedure is to issue a "power-up" command to nodes that are being allocated, but not to issue the allocation until the nodes are completely up again. A timeout is required in the procedure so a node can be marked as “ordered-to-power-up-but-didn’t-show”, thereby allowing the scheduler to allocate a different node. Obviously, systems that use this policy must accept the longer time required to complete an allocation from a power-down state.

The additional "ordered-to-power-up-but-didn’t-show” state is required because the system can’t necessarily mark the node as “failed-to-power-up” and report it to the sys admin for repair. For example, after N reboots (which the OS declares upon re-power), many file systems will force a complete consistency check which takes a lot of time. So the timeout may well trigger, yet the node eventually does successfully report. Hence, the scheduler needs to mark the node as not showing up in time, but not mark it as “failed-to-power-up” until a much longer time has elapsed. At that point, the scheduler would notify the sys admin that someone needs to look and see why the node failed to return.

Implementing these policies and mechanisms requires the following features in Sensys:

* track the idle time of a node - i.e., the time since it was last used in an allocation.
 
* set a timer to periodically check node idle times. For now, we can specify the idle timeout policy via an MCA param. If the policy is to switch nodes to ''off'', then nodes that have been idle for at least the specified time will have a power-down command issued to them, and node state will be marked as “powered down for idle”. This state will leave them marked as “online” and available for scheduling, but will serve to indicate to the scheduler that they need to be powered up prior to use. We also need to add a command by which the scheduler can order a node to power back up.
 
* commands to power down/up should flow to an identified control point. For compute nodes, that would be their rack controller/aggregator so it can use IPMI to order the power down, if supported. If the control point cannot execute the power change, then the command shall be passed along to the compute node daemon itself which will set the local frequency to the lowest value for power down, and to the default value on power up. I do not anticipate idling non-compute nodes at this time.
 
* add node states for offline-powered-up, offline-powered-down, powered-down-for-idle, ordered-to-power-up, ordered-to-power-up-but-didn’t-show - we already have states to indicate unexpected failure
 
* add commands to our console program for taking a node offline-power-up, offline-power-down, power-up, declare-idle, declare-nonidle

