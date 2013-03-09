"""Developed by Francis Mensah, BYU, Provo and Kellie Kercher, BYU, Provo. Email: fn.mensah$byu.edu """

from twisted.internet import reactor,protocol,endpoints
import os, sys, re
from livecap import fmd5sum, md5sum

class LivecapServerProtocol(protocol.Protocol):
	def connectionMade(self):
		pass
		
	def connectionLost(self, reason):
		pass		
		
	def dataReceived(self, data):
	
		try:
			try:
				command_output = data.split('data:')
				command_output = command_output[1]
				chksum = md5sum(command_output).strip()
				
				data = data.replace("\r\n","\n")
				
				self.transport.write("OK")
				self.transport.loseConnection()
				
				#Report Creation
				dir = data.split('directory:') #Get the directory name from input data
				dir = dir[1].split('\nfilename')
				dir = dir[0]
				config_file=open('serverconfig.txt','r').readlines() #Get the directory location from Server_Config.txt file to store results
				config = []
				for line in config_file:
					entry=line.split('=')
					config.append(entry[1].strip())
				directory = config[0] + dir
			except Exception as ex:
				print "Server error: data received may be of invalid format.", ex
			if not os.path.exists(directory): #Check if directory already exisits
				os.makedirs(directory) #create the evidence directory and start the html file
				f = open(directory+'/forensiclog.html','w')
				report_css = "<STYLE>\nbody{background-color:#EEEEEE;}#main{margin:0px auto; width: 90%; background-color: #FFFFFF; font-size:15px; border-color: #666666; border-width:2px; border-style:solid; -webkit-border-radius: 10px; border-radius: 10px; color: #666666; padding: 5px;}\n.subject_head{width: 97.5%; font-size:20px; background-color:#332266; border-color: #666666; border-width:2px; border-style:solid; -webkit-border-radius: 10px; border-radius: 10px; color: #FFFFFF; padding: 5px;}#copyright{text-align:center; width: 97.5%; font-size:9px; color:#999999;}</STYLE>"
				report_js = """<SCRIPT type='text/javascript'> function toggle_show(id, link) { var e = document.getElementById(id); if (e.style.display == '') {  e.style.display = 'none';  link.innerHTML = 'Show command output';  } else { e.style.display = '';  link.innerHTML = 'Hide command output'; } } </SCRIPT>"""
				report_header="<HTML>\n<HEAD>\n<TITLE>Livecap Project v1.0</TITLE>\n"+report_css+"\n"+report_js+"\n</HEAD>\n\n<BODY>\n\n"
				report_content="<div id='main'><H1>"+dir+" Report</H1>\n"
				f.write(report_header+report_content)
			else: #delete last line that clases the div and adds copyright to the log
				readFile = open(directory+'/forensiclog.html','r')
				lines = readFile.readlines()
				readFile.close()
				w = open(directory+"/forensiclog.html",'w')
				w.writelines([item for item in lines[:-1]])
				w.close()
			
			f = open(directory+'/forensiclog.html','a') #append to the file
			data_full = data.split('command:') #Create a list with each block containing the entire record for a command
			data_commands = [] #create a list of commands performed on the client
			temp_data = data.split('command:')
			for temp in temp_data:
				temp = temp.split('\ndirectory:')
				data_commands.append(temp[0])
			data_timestamps = [] #create a list of command timestamps
			temp_data = data.split('timestamp:')
			for temp in temp_data:
				temp = temp.split('\ndatachksum:')
				data_timestamps.append(temp[0])
			data_checksums = [] #create a list of data checksums
			temp_data = data.split('datachksum:')			
			for temp in temp_data:
				temp = temp.split('\ntoolchksum:')
				data_checksums.append(temp[0].strip())				
			data_toolchecksums = [] #create a list of tool checksums
			temp_data = data.split('toolchksum:')
			for temp in temp_data:
				temp = temp.split('\ndata:')
				data_toolchecksums.append(temp[0])
			data_data = [] #create a list containing the output of commands performed on the client
			temp_data = data.split('data:')
			for temp in temp_data:
				temp = temp.split('\ncommand:')
				data_data.append(temp[0])
			data_filenames = [] #create a list containing the output filenames of commands performed on the client
			temp_data = data.split('filename:')
			for temp in temp_data:
				temp = temp.split('\ntimestamp:')
				data_filenames.append(temp[0])
			data_integrity = True
			count=0
			del data_commands[0] #delete blank cells in list
			del data_data[0]
			del data_filenames[0]
			del data_full[0]
			del data_timestamps[0]
			del data_checksums[0]
			del data_toolchecksums[0]
			report_inside=""
			for command in data_commands: #output the results in the html report formatted
				side_report = open(directory+'/'+data_filenames[count]+'.txt','w')
				side_report.write("command:"+data_data[count])
				side_report.close()				
				
				if data_checksums[count] == chksum:					
					data_integrity = False
				
				file_checksum = fmd5sum(directory+'/'+data_filenames[count]+".txt")
				report_inside+="<div class='subject_head'>"+command+" : "+data_timestamps[count] \
								+"</div><pre>" \
								+"Filename: ".ljust(40)+data_filenames[count]+".txt<br>" \
								+"File checksum (md5): ".ljust(40)+file_checksum+"<br>" \
								+"Data corrupted in transit: ".ljust(40)+ str(data_integrity)+"<br>" \
								+"Tool Checksum: ".ljust(40)+data_toolchecksums[count]+"<br>" \
								+"<a href = \"#\" onclick=\"toggle_show('"+data_filenames[count]+"',this); return false\">Show command output</a>" \
								+"<div id='"+data_filenames[count]+"' style='display:none'>"+data_data[count]+"</div>" \
								+"</pre><br><br>\n"			
				count = count + 1
			report_footer="<div id='copyright'>&#169;Livecap Project 2013</div></div></BODY></HTML>" #add a footer to the document
			f.write(report_inside+report_footer) #write out everything.
			f.close()
		except Exception as ex:
			print "Server error: ",ex
		
class NewFactory(protocol.ServerFactory):
	def __init__(self):
		try:
			self.protocol = LivecapServerProtocol
			self.count = 0
		except Exception as ex:
			print "There was an error", ex
port = ""
#read configuration file
configfile = open("serverconfig.txt","r")
config = configfile.readlines()
configfile.close()

for conf in config:
	param = conf.split("=")
	if param[0] == "port":
		port = param[1].strip()

endpoints.serverFromString(reactor,"tcp:"+port).listen(NewFactory())
print "Server started...\r\n"
reactor.run()

