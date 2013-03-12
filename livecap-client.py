"""Developed by Francis Mensah, BYU, Provo and Kellie Kercher, BYU, Provo. Email: fn.mensah$byu.edu """

import subprocess, sys, os, getopt, atexit
from livecap import * # livecap is a module that contains functions and classes for the correct operation of the application

try:

	date = sanitize_date(subprocess.check_output("date /t",shell=True)[:-2])	
	
	#create a Livecap instance
	lc = Livecap() 
		
	os.system("cls")
	
	draw_splash()
	
	#parse options and arguments 
	try:
		options, args = getopt.gnu_getopt(sys.argv[1:],'Ac:fh:k:M:P:p:t:')
	except Exception as ex:
		print "\nERROR (Invalid arguments or options): ", ex,"\n"
		sys.exit(1)
		
	get_tool = False
	
	for opt,arg in options:
		if opt == "-A":
			auto = True
		elif opt == "-h":
			lc.remote_host = arg
			lc.storage_mode = "remote_server"
		elif opt == "-p":
			lc.remote_port = arg
			lc.storage_mode = "remote_server"
		elif opt == "-M":
			lc.remote_path = arg
			lc.storage_mode = "remote_drive"
		elif opt == "-P":
			lc.attached_path = arg
			lc.storage_mode == "attached_drive"
		elif opt == "-t":
			lc.tools_path = arg			
		elif opt == "-c":
			lc.config_file = arg
		elif opt == "-k":
			lc.commands_file = arg
		elif opt == "-f":
			get_tool = True
				
	if options == []: #start in interactive mode if no arguments or options are provided
		print "Starting in interactive mode..."
		interactive_mode = "config"
		auto = False		
				
	if get_tool == True: #copy tools from system folder to tools folder
		print "Copying tools, please wait..."
		returnstatus = get_tools(lc)
		if returnstatus > 0:
			print str(returnstatus) + " Tools copied"
			sys.exit(0)
		else:
			print "There was an error"
			sys.exit(1)
	
	if auto == True: #run in automatic mode
		print "Starting in automatic mode..."
		
		if lc.read_config() == 1: 
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
			
	elif auto == False:
		while True:
			if interactive_mode == "config":
				keybd = raw_input("\nlivecap~config> ").lower().strip()
				if keybd == "set run":
					interactive_mode = "run"
					continue
				elif keybd == "set config":
					interactive_mode = "config"
					continue
				elif keybd == "show config":
					lc.show_config()
					continue
				elif keybd[0:3] == "set":
					try:
						command = keybd[3:].strip().split("=")
						param = command[0].strip()
						value = command[1].strip()
						if param!="" and value!="":
							lc.set_config(param,value)
						else:
							print "\nInvalid command format"
						if param == "remote_path":
							lc.prompt = True
						continue
					except:
						print "Bad command"
						continue
				elif keybd == "read config":
					lc.read_config()
					continue
				elif keybd == "get tools":
					returnstatus = get_tools(lc)
					if returnstatus > 0:
						print "\n" + str(returnstatus) + " Tools copied"
						continue
					else:
						print "\nThere was an error. Could not copy tools"						
					
				elif keybd == "cls":
					os.system("cls")
					continue
				elif keybd == "exit":
					sys.exit(0)
				else:
					print "\nBad command"
					continue
					
			elif interactive_mode == "run":
				keybd = raw_input("\nlivecap~run> ").strip()
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
						print command_output

except KeyboardInterrupt:
	pass