# Introduction #
The client runs from a CD ROM on the victim workstation. All forensic tools must be included in the tools folder before burning Livecap onto a CD-ROM. The client normally connects to the server on a specified port and IP address to transfer data. Other data storage mechanisms are also available. The client process works in conjunction with a couple of other files as mentioned in the details section.

# Details #
## Supporting Files and Folders ##
  * Client Configuration file (clientconfig.txt): This file contains settings for parameters that the client uses during runtime. The format for specifying parameter values in the configuration file is parameter=value, note that there is no space on either half of the equal sign. Some of the parameters that may be configured include:
    * Remote\_host
    * Remote\_port
    * Remote\_path (eg \\remote\_drive\_path)
    * Attached\_path (eg G:\path\_to\_attached\_storage)
    * Storage\_mode (accepted values are   remote\_server’,’remote\_drive’,’attached\_drive’)
    * Commands\_file
    * Tools\_path (path to the tools folder. Can specify a path relative to the livecap-client)
  * Commands file: This file contains a list of all the commands that the user wishes to run on the victim workstation. Each command should be on a separate line
  * Tools folder: This folder contains the actual forensic tools that are to be used to run the commands in the commands file. Because the compromised machine cannot be trusted it is recommended that forencic tools that are included in the Windows operating system are copied from a trusted machine and stored in this folder. To make it easy for you run the command ‘livecap-client.exe  -f’. The ‘-f’ option tells Livecap to copy tools from the Windows system folder to your tools folder. The tools that will be copied are specified in the ‘toolslist.txt’ file. Other tools (for example the sysinternals suite) can be downloaded and placed in this folder as well.
  * Tools list file: This file contains the list of Windows operating system tools that should be copied from the system folder to the tools folder.
  * Internal commands file: This file contains a list of commands that are internal to the Windows command shell.

## Operating modes ##
The client can run in either command line mode or in interactive mode.
  * Command Line Mode: In command line mode all options are specified in a single command. The most important option in command line mode is -A. This option tells Livecap to read the various configuration files and run any commands it finds according to the settings specified in the config files. The other options are optional for as long as the configuration files have the relevant values for the necessary parameters. Any option specified on the command line will override whatever is in the configuration file. Command line options include the following:
    * -A: Automatic mode
    * -c: Name and path of configuration file
    * -e: Attached storage path
    * -f: Copy tools from system folder to tools folder
    * -h: Hostname or IP address of remote server
    * --help: Help
    * ?: Help
    * -k: Name and path of commands file
    * -r: Remote drive path to mount
    * -p: Port number of remote server
    * -t: Tools paths
  * Interactive Mode: In interactive mode the user is presented with a shell within which commands can be entered. The least it takes to enter the interactive mode is the start the client with no options or arguments or by double clicking the client executable. The client shell runs in two modes namely ‘run mode’ and ‘config mode’. The shell starts in ‘config mode’. To switch between modes use the commands: ‘set config’ and ‘set run’ accordingly.
    * Config Mode: in the config mode the user is allowed to set configuration parameters to relevant values. The following commands can be used on config mode:
      * set run: changes to run mode
      * show config: displays the current values of the configuration parameters
      * read config: reads the specified configuration file and uses the values specified therein for the configuration parameters
      * set config: Allows the user to set a particular configuration parameter to a specified value. The syntax is ‘set config parameter\_name=value’. Use the same parameter names as shown in the output of ‘show config’ command.
      * get tools: copies tools specified in toolslist.txt from the system folder to the tools folder
      * cls: Clear screen
      * help: Show available commands in the current context
      * ?: Shows available commands in the current context. When you type a command followed a space and '?' (eg set ?), it gives you available options for that command. This feature only works in config mode for now.
      * exit: Exit the client shell
    * Run Mode: In the run mode the user can run commands using the various tools in the tools directory. Internal operating system commands can also be run in this mode. The user can run single commands at a time or run the commands specified in the commands folder all at once. The success of commands run in this mode depends on the completeness of the configuration parameters so it must be ensured that all the relevant parameters have been set. For example if the storage mode is specified as ‘remote\_server’ and no port number has been specified the command will not be successful. The following commands can be run in ‘run mode’:
      * set config: changes to config mode
      * run auto: run all commands in commands file
      * Command: whatever command you wish to run provided it is understood by the operating system or it is present in the tools directory. Run only one command at a time.
      * cls: Clear screen
      * help: Show available commands in the current context
      * ?: Show available commands in the current context
      * exit: Exit the shell
    * You can run commands in run mode even when a storage mode has not been specified. The results will, however, be only displayed and not stored.