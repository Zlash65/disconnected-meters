# Disconnected Meters

There are some IOT nodes (which we will refer to as meters) deployed in the field.
These nodes connect to the server using a GSM network.
Whenever a Connection to server is established, the meter records the time of Connection in its system log.
Similarly, whenever a meter disconnects from the server, it records the time of Disconnection in its system log.
Disconnection and connection can happen at any point in time - that is to say that there is no minimum guarantee of duration of connection or disconnection.
A meter can remain connected or disconnected for a duration as small as 1 second to a duration as large as a few weeks.

The problem data-set consists of system logs of a series of meters deployed in the field captured as csv files.
The relevant fields in the csv are Meter-ID, Sequence ID, Timestamp, and Connection status.
The sequence id orders the events received. Connection status can be either connected or disconnected.
Timestamp is the time when the connection to server was established or the meter was disconnected.

### Task
For each meter, we need the list of days on which the meter did not communicate with the server at all.

### Example
1. If the meter reported Connected on 10th June 5.30pm and then reported Disconnected on 13th June 3 am,
we will count 10th, 11th, 12th and 13th June as connected days.
2. If the meter reported Disconnected on 13th June 3 am and indicates connected on 15th June 4pm,
we will indicate that the meter did not communicate with server on 14th June.
