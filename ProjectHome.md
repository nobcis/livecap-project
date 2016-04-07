# Livecap #
The Livecap project is a forensic framework intended to simplify the task of forensic live capture. All that
the user needs to do is specify the source of the tools that will be used in addition to a few configuration
details and Livecap does the rest. Livecap adheres to standard forensic practices such as not doing
anything that can tamper with forensic evidence on the victim workstation from which information
is being captured. Through the use of a client/server architecture Livecap transfers all its data from the
victim workstation to the forensic workstation via a TCP/IP connection. Where this approach is not
feasible the framework also supports other storage means including mounted remote drive and attached USB
storage. It is, however, recommended the client/server TCP/IP connection be used with the client being
run from a CD ROM on the victim workstation. This guarantees the least interference with forensic
evidence. Current version only works on Windows.

[Download](http://code.google.com/p/livecap-project/downloads/list)

[Project documentation](http://code.google.com/p/livecap-project/w/list)

### Developers ###
Francis Mensah, BYU

Kellie Kercher, BYU
