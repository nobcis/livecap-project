"""Developed by Francis Mensah, BYU, Provo and Kellie Kercher, BYU, Provo. Email: fn.mensah$byu.edu """

import subprocess, sys, os, hashlib, subprocess, socket, shutil, platform, datetime

call_count = 0

def build_data(field,data,data_append):
	"""Constructs the data to be sent over the network by adding fields"""
	return data + field + ":" + data_append + "\n"

def time_signature():
	t = datetime.datetime.now()
	h = t.hour
	m = t.minute
	s = t.second
	return str(h) + "_" + str(m) + "_" + str(s) 
	
def getTimestamp():
	"""Returns time and date on local system"""
	date = subprocess.check_output("date /t",shell=True)[:-2]
	time = subprocess.check_output("time /t",shell=True)[:-2]
	return date + "" + time

def md5sum(data):
	"""Returns md5 hash of data passed to it"""
	m = hashlib.md5()
	m.update(data)
	return m.hexdigest()
	
def fmd5sum(filePath):
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()
	
def save(filename,data,path,command):
	"""Saves data to remote drive or attached storage"""
	try:
		outputfile = open(path + filename,"w")				
		print ("Saving: " + command).ljust(50),
		outputfile.write(data)			
		outputfile.close()
		print "...... Success"
		return 0
	except Exception as ex:
		print "...... Error", ex
		return 1
		
def run_command(command):
	"""Runs command and returns results and error status"""
	command_run = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out, error = command_run.communicate()
	if error==None or error == "" or out==None:
		if (error==None or error == "") and out!=None:
			return (out,0)
		elif out==None and (error!=None or error!=""):
			return (error,1)
		else:
			return ("1",1)
	else:
		command_out = error + out
		return (command_out,1)
		
visited = []
		
def copy_file(src, dest, file):	
	
	for path, dirs, files in os.walk(src, topdown=True):		
		if path not in visited:			
			for di in dirs:				
				copy_file(os.path.join(path, di), os.path.join(dest, di), file)
			for fi in files:
				
				if fi.lower().startswith(file.lower()):					
					if not os.path.exists(dest):
						os.makedirs(dest)					
					shutil.copy(os.path.join(path, fi), dest)
			visited.append(path)
		
def get_tools(lc):
	"""Fetches tools from the system folder into the specified tools folder"""
	global call_count
	call_count = 0
	try:		
		if not os.path.exists(lc.tools_path):
			os.makedirs(lc.tools_path)
		toolslistfile = open("toolslist.txt","r")
		toolslist = toolslistfile.readlines()
		toolslistfile.close()		
		count = 0
		for tool in toolslist:
			try:				
				tool = tool[:-1]				
				if tool != "":
					copy_file("C:\\Windows\\System32\\",lc.tools_path,tool)
					count = count + 1
					del visited[:]
			except Exception as ex:
				print ex
				continue
		return count
	except Exception as ex:
		print ex
		return -1
		
def is_internal_cmd(command):	
	try:
		internalcommandsfile = open("internalcommands.txt","r")
		internalcommands = [c.lower().strip() for c in internalcommandsfile.readlines()]
		internalcommandsfile.close()
		return command in internalcommands
	except:
		return False
		
def sanitize_date(date):
	"""Converts the date or time to a format that can be used in a file or directory name"""
	sanitized_date = date.replace("/","-").strip()
	sanitized_date = sanitized_date.replace(":","-").strip()
	return sanitized_date.replace(" ","_")
	
def sanitize_path(path):
	"""Removes backslash from path"""
	last_char = path[-1]
	if last_char == "\\":
		return path[:-1]
	else:
		return path	
		
def draw_splash():
	for i in range(80):
		sys.stdout.write("=")
	print "\n\t\t\t\tLIVECAP v1.0 \n"
	for i in range(80):
		sys.stdout.write("=")
	print ""
	
def send(data, lc, command):
	try:
		size  = 8
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((lc.remote_host,int(lc.remote_port)))
		s.send(data)
		reply = s.recv(size)
		s.close()
		return reply
	except Exception as ex:
		return ex
		
class Livecap():
	def __init__(self):
		#initialize class fields
		self.storage_mode = ""
		self.remote_host = ""
		self.remote_port = ""
		self.remote_path = ""
		self.attached_path = ""
		self.drive_letter = ""
		self.auto = False
		self.interactive_mode = ""
		self.config_file = "clientconfig.txt"
		self.sysplatform = platform.system() + " " + platform.release()		 
		self.tools_path = "Tools" + "\\" + self.sysplatform
		self.commands_file = ""
		self.show_output = "no"
		self.prompt = True
		self.computername = os.environ["computername"]
		self.date = sanitize_date(subprocess.check_output("date /t",shell=True)[:-2])
		self.time = sanitize_date(subprocess.check_output("time /t",shell=True)[:-2])
		
	def read_config(self):
		"""Reads settings in configuration file into the program environment"""
		try:
			config = open(self.config_file,"r")
			params = config.readlines()
			config.close()		
		except Exception as ex:
			print "\nFILE ERROR (Configuration file not found): ", ex
			return 1
			
		print "\nReading configuration file ..."
		
		for p in params:
			param = p.split("=")[0].strip()
			if param == "remote_host" and (self.remote_host == "" or not self.auto):
				self.remote_host = p.split("=")[1].strip()
			elif param == "remote_port" and (self.remote_port == "" or not self.auto):
				self.remote_port = p.split("=")[1].strip()
			elif param == "remote_path" and (self.remote_path == "" or not self.auto):
				self.remote_path = p.split("=")[1].strip()
			elif param == "attached_path" and (self.attached_path == "" or not self.auto):
				self.attached_path = p.split("=")[1].strip()
			elif param == "storage_mode" and (self.storage_mode == "" or not self.auto):
				self.storage_mode = p.split("=")[1].strip()
			elif param == "commands_file" and (self.commands_file == "" or not self.auto):
				self.commands_file = p.split("=")[1].strip()
			elif param == "tools_file" and (self.tools_path == "" or not self.auto):
				self.tools_path = p.split("=")[1].strip()
		print "Done"
		return 0
		
	def show_config(self):
		"""Displays current configuration on screen"""
		#draw_line()
		print "\nCurrent Configuration\n"
		#draw_line()
		print "Config_file: " + self.config_file
		print "Commands_file: " + self.commands_file
		print "Storage_mode: " + self.storage_mode
		print "Remote_host: " + self.remote_host
		print "Remote_port: " + self.remote_port
		print "Remote_path: " + self.remote_path
		print "Attached_path: " + self.attached_path
		print "Tools_path: " + self.tools_path
		print "Auto_mode: " + str(self.auto)
		print "Show_output: " + self.show_output
		print "Hostname: " + self.computername
		print "Date: " + self.date
		print ""
		
	def set_config(self,param, value):
		"""Sets configuration parameters to specified values"""
		if param == "storage_mode":
			self.storage_mode = value
		elif param == "config_file":
			self.config_file = value
		elif param == "remote_host":
			self.remote_host = value		
		elif param == "remote_port":
			self.remote_port = value
		elif param == "remote_path":
			self.remote_path = value
		elif param == "attached_path":
			self.attached_path = value
		elif param == "tools_path":
			self.tools_path = value
		elif param == "hostname":
			self.computername = value
		elif param == "commands_file":
			self.commands_file = value
		elif param == "show_output":
			self.show_output = value
		print "\nDone"
		
	def read_commands(self):
		"""Read commands from commands file. Returns a list of commands or 1 if there is an error"""
		try:
			commandsfile = open(self.commands_file,"r")
			commands = [c.lower().strip() for c in commandsfile.readlines()]
			commandsfile.close()
			commandslist = []
			
			for command in commands:
				commandname = command.split(" ")[0].strip()
				if is_internal_cmd(commandname):					
					commandslist.append(command.strip())					
				elif os.path.exists(self.tools_path+"\\"+commandname):
					commandslist.append(command.strip())					
				else:
					print commandname + " not found in " + self.tools_path
			return commandslist
		except Exception as ex:
			print "ERROR (Could not read the commands file): ",ex
			return 1
			
	def remote_drive_init(self,prompt_existing=True):
		"""Mounts remote drive. Return values: -1: Drive was mounted successfully, 0: Existing drive will be used
		1: There was an error"""
		try:					
			self.remote_path = sanitize_path(self.remote_path)
			remote_path = self.remote_path.split(":")
			self.drive_letter = remote_path[0]		
			if not os.path.exists(self.drive_letter+":\\"):
				drive_path = "\\" + remote_path[1]
				cmd_out = subprocess.call("net use " + self.drive_letter + ": " + drive_path, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
				if cmd_out == 0:
					self.remote_path = self.drive_letter + ":\\"
					print "Remote drive was successfully mounted"
					return -1
				else:
					print "Remote drive could not be mounted"
					return 1										
			else:
				if prompt_existing: 
					use_existing = raw_input("The drive letter you specified is already mounted. Do you want to go ahead and use it? (y/n): ")
				else:
					use_existing = "y"
				if use_existing=="y": 
					remote_path = sanitize_path(self.remote_path)
					remote_path = self.remote_path.split(":")
					self.drive_letter = remote_path[0]
					self.remote_path = self.drive_letter + ":\\"
					return 0
				else: 
					return 1
		except Exception as ex:
			print "ERROR (Could not mount remote drive): ",ex
			return 1
			
	def attached_storage_init(self):
		"""Set attached storage drive"""
		self.remote_path = sanitize_path(self.attached_path) + "\\"
		return 0
		
	def create_working_directory(self):
		"""Create working directory for the storage of output files"""
		try:
			remote_dir = self.computername + "_" + self.date
			if not (os.path.exists(self.remote_path + remote_dir)): 
				os.mkdir(self.remote_path + remote_dir)
			return 0
		except Exception as ex:
			print "\nERROR (Working directory could not be created): ", ex
			return 1
			
	def run_command_list(self,commands):
		"""Run list of commands. Returns 0 if completed successfully or 1 if with errors"""
		date = sanitize_date(subprocess.check_output("date /t",shell=True)[:-2])
		if self.storage_mode == "remote_storage" or self.storage_mode == "attached_storage":
			try:
				for c in commands:			
					command = c.strip()						
					commandname = command.split(" ")[0]
					commandargs = command.split(" ")[1:]
					if is_internal_cmd (commandname):
						toolchksum = "Windows Internal Command"
					else:
						command = os.path.join(self.tools_path,commandname)
						command = "\"" + command + "\" " + " ".join(commandargs).strip()
						toolchksum = fmd5sum(os.path.join(self.tools_path,commandname))
					time = time_signature()
					command_output,error = run_command(command)
					print ("Executing: " + command).ljust(50),
					if error == 0:
						print "...... Success"
					else:
						print "...... Command returned with errors"
					filename = self.computername+"_"+date+"\\"+commandname+"_"+time+".txt"			
					save(filename,command_output,self.remote_path,command)
				print "\nDone"
				return 0
			except Exception as ex:
				print "\nThere was an error in running list of commands:",ex
				return 1
				
		elif self.storage_mode == "remote_server":
			try:
				data = ""			
				for c in commands:
					command = c.strip()
					print command
					commandname = command.split(" ")[0]
					commandargs = command.split(" ")[1:]
					toolchksum = ""
					if is_internal_cmd (commandname):
						toolchksum = "Windows Internal Command"
					else:
						command = os.path.join(self.tools_path,commandname)
						command = "\"" + command + "\" " + " ".join(commandargs).strip()
						toolchksum = fmd5sum(os.path.join(self.tools_path,commandname))
					time = time_signature()					
					data = build_data("command",data,command)	#add preamble field						
					data = build_data("directory",data,self.computername+"_"+date)	#add directory name field						
					data = build_data("filename",data,commandname+"_"+time)  #add filename field					
					data = build_data("timestamp",data,getTimestamp())  #add timestamp field
					command_out,error = run_command(command)
					print ("Executing " + command).ljust(50),
					if error == 0:
						print "...... Success"
					else:
						print "...... Command returned with errors: ", command_out						
					
					data = build_data("datachksum",data,md5sum(command_out+"\n"))	#add data checksum field
					data = build_data("toolchksum",data,toolchksum)    #add tool checksum field
					data = build_data("data",data,command_out)	#add data field

					print ("Sending " + command).ljust(50),											
					response = send(data,self,command)  #send data
					if response == "OK":
						print "...... Success"
					else:
						print "...... Error: ",response
					data = ""
				print "\nDone"
				return 0
			except Exception as ex:
				print "\nThere was an error in running list of commands (network error):",ex
				return 1
		
		else:
			print "\nStorage mode not speficied"
			return 1