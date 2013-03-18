"""Developed by Francis Mensah, BYU, Provo and Kellie Kercher, BYU, Provo. Email: fn.mensah$byu.edu """

import subprocess, sys, os, getopt, atexit, itertools
from livecap import * # livecap is a module that contains functions and classes for the correct operation of the application

try:

	date = sanitize_date(subprocess.check_output("date /t",shell=True)[:-2])	
	
	#create a Livecap instance
	lc = Livecap() 
		
	os.system("cls")
	
	draw_splash()
	
	print "Command entered: livecap-client", " ".join(sys.argv[1:]),"\n"
	
	#parse options and arguments 
	try:
		options, args = getopt.gnu_getopt(sys.argv[1:],'Ac:e:fh:k:p:r:t:',['help'])
	except Exception as ex:
		print "\nERROR (Invalid arguments or options): ", ex
		sys.exit(1)
	
	for opt in options:
		if "--help" in opt:
			show_help()
			sys.exit(0)
	if "?" in args:		
		show_help()
		sys.exit(0)
	
	for opt in options:
		if "-f" in opt and len(options)>1:
			print "Option '-f' should be used as the only option\n"
			sys.exit(0)
		elif "-f" in opt:
			print "Copying tools, please wait..."
			returnstatus = get_tools(lc)
			if returnstatus >= 0:
				print str(returnstatus) + " Tool(s) copied"
				sys.exit(0)
			else:
				print "There was an error"
				sys.exit(1)
				
	opt_comb = ["-e","-h","-r"] # these three options should not be specified together
	opt_combinations = list(itertools.combinations(opt_comb,2))
	for combination in opt_combinations:
		opt_list = []
		for opt,arg in options:
			opt_list.append(opt)
		if combination[0] in opt_list and combination[1] in opt_list:
			print "\nTwo data storage modes have been specified: '{0}','{1}'. The first that occured in the command will be used".format(combination[0],combination[1])
			raw_input("\nPress any key to continue...\n")
			break
			
	for opt,arg in options:
		if opt == "-A":
			lc.auto = True
		elif opt == "-h":
			lc.remote_host = arg
			if lc.storage_mode == "":
				lc.storage_mode = "remote_server"
		elif opt == "-p":
			lc.remote_port = arg			
		elif opt == "-r":
			lc.remote_path = arg
			if lc.storage_mode == "":
				lc.storage_mode = "remote_drive"
		elif opt == "-e":
			lc.attached_path = arg
			if lc.storage_mode == "":				
				lc.storage_mode = "attached_storage"				
		elif opt == "-t":
			lc.tools_path = arg			
		elif opt == "-c":
			lc.config_file = arg
		elif opt == "-k":
			lc.commands_file = arg		
				
	if options == []: #start in interactive mode if no arguments or options are provided
		#print "Working in interactive mode..."
		os.system("cls")	
		draw_splash()
		interactive_mode = "config"
		auto = False				
	
	if lc.auto == True: #run in automatic mode
		#print "Working in automatic mode..."
		
		if lc.read_config() == 1:
			#print "Exiting"
			sys.exit(1)			
		
		if lc.storage_mode == "remote_drive" or lc.storage_mode == "attached_storage":
			if lc.storage_mode == "remote_drive":		
				print "\nData will be stored on remote drive"
			elif lc.storage_mode == "attached_storage":
				print "\nData will be stored on locally attached storage"
				
			if lc.remote_path == "" and lc.attached_path == "":
				print "\nERROR: Remote drive path or attached storage path not provided in config file"
				sys.exit(1)
															
			if lc.create_storage_directory() == 1:
				sys.exit(1)
				
			commands = lc.read_commands()
			
			if commands == 1: 
				sys.exit(1)
				
			print "\n"
				
			if lc.run_command_list(commands) == 1:
				sys.exit(1)
				
		elif lc.storage_mode == "remote_server":
			print "\nData transfer via remote_server connection selected\n"
			if lc.remote_host == "" or lc.remote_port == "":
				print "\nERROR (Remote host or remote port not provided in config file)"
				sys.exit(1)
			
			commands = lc.read_commands()
			
			if commands == 1: 
				sys.exit()
				
			if lc.run_command_list(commands)==1:
				sys.exit(1)

		else:
			print "\nNo storage mode specified"
			sys.exit(0)
			
	elif lc.auto == False:
		while True:
			if interactive_mode == "config":
			
				available_commands = ["set run", "set config", "set", "read config", "show config", "cls", "exit", "get tools", "help"]
				parameters = [("storage_mode","remote_server|remote_drive|attached_storage"), ("config_file","filename"), ("remote_host","hostname|IP address"), 
								("remote_port","port_number"), ("attached_path","directory_path"), ("remote_path","network_path"), ("tools_path","directory_path"), 
								("hostname","string"), ("commands_file","filename"), ("show_output","yes|no")]
				
				keybd = raw_input("\nlivecap~config> ").lower().strip()
				
				for cmd in available_commands:					
					if cmd.startswith(keybd.strip()):
						keybd = cmd						
						break
						
				if keybd == "set run":
					interactive_mode = "run"
					continue
				elif keybd == "set config":
					interactive_mode = "config"
					continue
				elif keybd[0:4] == ("show"):					
					if keybd[-1] == "?":
						print "\n show config"
						continue
					elif keybd == "show config":
						lc.show_config()
						continue
					else:
						print "Bad command"
				elif keybd[0:3] == "set":
					if keybd[-1] == "?":						
						if keybd[:-1].strip() == "set":
							print "\n set run\n set config\n set <parameter>=<value>"
							print "\n Paramter list: \n"
							for p in parameters:
								print "\t" + p[0] + "=" + p[1]
							continue
						else:
							parameter_found = False
							command = keybd[:-1].split(" ")
							print "\n"
							for cmd in parameters:								
								if cmd[0].startswith(command[1]):
									print " set " + cmd[0] + "=" + cmd[1]
									parameter_found = True																
							if not parameter_found:
								print "\n Parameter not found"
							continue
					try:
						command = keybd[3:].strip().split("=")
						param = command[0].strip()
						value = command[1].strip()
						if param!="" and value!="":
							lc.set_config(param,value)
						else:
							print "\n Invalid command format"
						if param == "remote_path":
							lc.prompt = True
						continue
					except:
						print "\nBad command"
						continue
				elif keybd[0:4] == "read":
					if keybd[-1] == "?":
						print "\n read config"
						continue
					elif keybd == "read config":
						lc.read_config()
						continue
					else:
						print "Bad command"						
				elif keybd == "cls":
					os.system("cls")
					continue		
				elif keybd == "?" or keybd == "help":
					show_help("config")
					continue
				elif keybd == "exit":
					sys.exit(0)
				else:
					print "\nBad command"
					continue
					
			elif interactive_mode == "run":
				available_commands = ["set config", "set run", "run auto", "cls", "exit", "help"]
				keybd = raw_input("\nlivecap~run> ").strip()
				
				for cmd in available_commands:					
					if cmd.startswith(keybd.strip()):
						keybd = cmd						
						break
				
				if keybd == "exit":
					sys.exit(0)
				elif keybd == "set config":
					interactive_mode = "config"
					continue
				elif keybd == "set run":
					interactive_mode = "run"
					continue
				elif keybd == "cls":
					os.system("cls")
					continue
				elif keybd == "?" or keybd == "help":
					show_help("run")
					continue
				else:					
					if lc.storage_mode == "remote_drive" or lc.storage_mode == "attached_storage":
						if lc.storage_mode == "remote_drive":		
							print "\nData will be stored on remote drive"
						elif lc.storage_mode == "attached_storage":
							print "\nData will be stored on locally attached storage"
						if lc.remote_path == "" and lc.remote_path == "":
							print "\nERROR: Remote drive path or attached storage path not provided\n"
							continue
											
						if lc.create_storage_directory() == 1:
							continue						
												
						if keybd == "run auto":
							commands = lc.read_commands()						
						else:					
							commands = [keybd]
									
						if commands == 1: 
							continue
						
						print "\n"
						
						if lc.run_command_list(commands)==1:
							continue						
						
					elif lc.storage_mode == "remote_server":
						print "\nData transfer via remote_server connection selected\n"
						if lc.remote_host == "" or lc.remote_port == "":
							print "\nERROR (Remote host or remote port not provided)\n"
							continue
						
						if keybd == "run auto":
							commands = lc.read_commands()						
						else:					
							commands = [keybd]
						
						if commands == 1:
							#print "\nInvalid command or command file could not be read"
							continue
							
						if lc.run_command_list(commands)==1:
							continue
							
					else:
						command = keybd
						command_output = run_command(command)[0]
						print "\nNo storage method has been specified. Command output will not be saved\n"
						raw_input("Press any key to continue...\n")
						print command_output

except KeyboardInterrupt:
	pass