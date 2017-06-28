# Aggregator node and multi-node execution

Sensys has a daemon called `orcmd` that runs at root level. This daemon is able to perform two different types of roles: the aggregator and the compute node.

![Aggregator](Getting-started/aggregator.png)

Sensys architecture allows you to connect multiple nodes to a single aggregator.

## Aggregator

An aggregator is an interface that receives all the telemetry collected by a single or multiple nodes in a cluster. This role's responsbility is to provide a data analytics for the incoming telemetry to dispatch data to a database.

![Aggregator-capabilities](Getting-started/agg-capabilities.png)

The aggregator and the compute node roles are given by the user. Those are specified on the configuration file named `orcm-site.xml`. The example below is the most basic configuration having an aggregator node `agg01` and a compute node `cn02`.

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<configuration>
    <version>3.1</version>
    <role>RECORD</role>
    <junction>
        <type>cluster</type>
        <name>My_cluster</name>
        <junction>
            <type>row</type>
            <name>My_row</name>
            <junction>
                <type>rack</type>
                <name>agg01</name>
                <controller>
                     <host>agg01</host>
                     <port>55805</port>
                     <aggregator>yes</aggregator>
                </controller>
                <junction>
                     <type>node</type>
                     <name>cn01</name>
                </junction>
            </junction>
        </junction>
    </junction>

    <scheduler>
        <shost>SMS</shost>
        <port>55820</port>
    </scheduler>
<configuration>
```

## Scheduler

The `orcmshed` is another Sensys daemon run at root level. The main purpose of the daemon is to keep the status of each of the `orcmd` it also acts as a communication gateway between them. For further details please take a look at our wiki section [3.3 orcmsched](3.3-orcmsched)

## Sensys configuration

The previous configuration file shown has a hierarchy-based cluster architecture which presents the interconnection between aggregator node and compute node. Sensys allows multiple aggregator and compute node configuration by simply adding junction type `rack` to describe the aggregator-node connectivity, ie:

```XML
<junction>
    <type>rack</type>
    <name>agg02</name>
    <controller>
         <host>agg02</host>
         <port>55805</port>
         <aggregator>yes</aggregator>
    </controller>
    <junction>
        <type>node</type>
        <name>cn[2:00-49]</name>
        <controller>
            <host>@</host>
            <port>55805</port>
            <aggregator>no</aggregator>
        </controller>
    </junction>
</junction>

```
Above configuration specifies the connection between an aggregator called `agg02` and fifty compute nodes name as cnXX starting from `cn00` to `cn49`. The configuration file makes use of regular expressions to configure multiple compute nodes with a single junction node description. The special character `@` parameter in the `host` tag is used to indicate that the `name` tag value of the parent junction will be used to replace the character.

As mentioned on the previous section, `orcmd` can be configured using mca parameters. As the `orcmd` parameter list increases it also becomes difficult to handle it on a one-liner command. Therefore Sensys offers two solutions:

1. Include a mca parameter list on the orcm-site.xml configuration file as follows:

```XML
<mca-params>sensor_sample_rate=10,sensor_base_verbose=100</mca-params>
```
This options is recommended when you want to have a dedicated configuration for certain nodes or aggregators. This tag can be used inside the `scheduler` and `controller` tags.

2. Use an specific configuration file located and named as `<sensys_installation_path>/etc/openmpi-mca-params.conf`

```
sensor_sample_rate=10
sensor_base_verbose=100
```
This option is recommended to create a default configuration that applies to all the nodes in the system.

# Advanced features
## Data analytics

The data analytics is a framework that provides data processing through plug-ins that performs different data analysis like: data filtering, average, threshold among others. This service can be requested and configured using workflows. For specific details of the available plug-ins, scope and usage please refer to our wiki section [3.9 Data Smoothing Algorithms Analytics](3.9-Data-Smoothing-Algorithms-Analytics).

## Notification events

The notification event provides information for system events or errors. Sensys provides two notification mechanisms through plug-ins: smtp and syslog. Notification events are requested using workflows. For further details please visit section [3.10 ErrorManager Notification](3.10-ErrorManager-Notification).

The example below shows a threshold data analytics with a notification event using syslog:

```XML
<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<workflows>
    <aggregator>aggregator1</aggregator>
    <workflow name = "wf1">
         <step name = "filter">
             <hostname>c[2:00-10]</hostname>
             <data_group>coretemp</data_group>
             <core>core0</core>
             <notifier_action>syslog</notifier_action>
        </step>
    </workflow>
</workflows>
```
