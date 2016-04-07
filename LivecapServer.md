# Introduction #
The livecap-server runs on the Forensic workstation and listens on a specified TCP port and an IP address. Once a connection is received from a Livecap client the server processes the data received and generate report files.

# Details #

When data is received from a client the following tasks are performed:
  * A hash is computed of the main part of the data (output of command ran on the victim) that was received and compared with the original hash of the data before it was sent over the network (the original hash is sent with the data over the network).
  * The main part of the data (the output of a command ran on the victim machine) is saved in specified folder with a filename that include the time at which the command was run.
  * A checksum (md5) is computed on the saved data file.
  * An entry is appended to a report file. If the report file does not exist a new one is created. The entry consists the following information about the command:
    * Full command as was run (including all arguments an options)
    * Time of execution (as recorded on the victim machine)
    * State of command execution (whether it executed successfully or with errors)
    * Hash of the command output before the network transfer
    * Hash of the command output after it was received
    * Result of comparing the two hashes
    * Absolute path of command output file
  * The server takes its initial parameters from a server configuration file (serverconfig.txt). The parameters specified in this file are the directory to save the reports and the port to listen on.