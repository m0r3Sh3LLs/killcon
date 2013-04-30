#       AUTO KILL FOREIGN CONNECTIONS
#       Copyrighted:  Chris & m0r3Sh3LLs
#       Version: 1.0
#       Tested on Windows XP
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.



from time import gmtime, strftime
import subprocess
import re
import string
import hashlib
import os
import sys

# TASKKILL FORCE BY PID FUNCTION
# The variable passed to killPid is the integer of the pid number
def killPid(pid):
  command="cmd /C taskkill /F /PID " + str(pid)
	os.system(command)
	
# Kill connection using currports
def killConnection(ip):
	command = "currports.exe /close * * " + ip + " *"
	os.system(command)



# SHOW NETSTAT -ANO AND PARSE THE RESULTS FUNCTION
# The variable passed to whiteList is an array of ip addresses
def netstat(whiteList):

	whiteList = whiteList.split(',')
	# setup the blank event variables
	event = ''
	netstat = False
	netstatOutput = []
	netstat_hash = ''
	tempPorts = []
	tempPort = ''

	event = strftime('%b %d %Y %H:%M:%S') + ' '

	# perform a try and catch to display errors, if no error get the output of the netstat command
	try:
		netstat = subprocess.Popen(['netstat', '-nao'], stdout=subprocess.PIPE)
	
	except:
			pass

	#IF NETSTAT CHECKS IF THERE IS DATA IN THE NETSTAT VARIABLE, IF ITS NOT NULL OR EMPTY THE PROGRAM WILL CONTINUE
	if netstat:
	
		# PARSE THE NETSTAT COMMAND INTO netstatOutput VARIABLE
		# run chkconfig command and split the output into a list
		netstatOutput = netstat.communicate()[0]
		netstatOutput = netstatOutput.split('\n')
		# remove header
		netstatOutput = netstatOutput[1:len(netstatOutput)]
		
		#REGULAR EXPRESSION TO CHECK IF THE CONNECTION IS ESTABLISHED
		validRE = re.compile('ESTABLISHED', re.I)
		#validRE = re.compile('ESTABLISHED|UDP', re.I)
		hostRE = re.compile('(.*)\:(\d+)')
	
		#FOR EACH LINE IN VARIABLE netstatOuput DO THE FOLLOWING
		for line in netstatOutput:
	
			#CREATE YOUR EVENT VARIABLES TO STORE DATA
			tempEvent = event
			tempPort = ''
			
			#THIS CHECKS IF THE NETSTAT LINE MATCHES ESTABLISHED
			validMatch = validRE.search(line)
	
			#IF YOUR CHECK COMES OUT TRUE DO THE FOLLOWING
			if validMatch:
				#split
				line = line.strip()
				line = line.split()
			
				# trim port array for lines with (ESTABLISHED)
	
				#THIS CODE WILL PARSE OUT YOUR NETSTAT COMMAND TO FORMAT AND DISPLAY IT NICELY
				# line[1] is the local addrss,  line[2] is the foreign address
				
				hostMatch = hostRE.match(line[2])
				tempEvent += ' transport=' + line[0].strip()
				tempPort += line[1].strip()
	
				if hostMatch:
					tempEvent += ' dest_ip=' + hostMatch.group(1).strip()	
					dest_ip=hostMatch.group(1).strip()
									
					tempPort += hostMatch.group(1).strip()
					tempEvent += ' dest_port=' + hostMatch.group(2).strip()
					tempPort += hostMatch.group(2).strip()
	
	
					if len(line) == 5:
						tempEvent += ' pid=' + line[4]
						pid = line[4]
					elif len(line) == 4:
						tempEvent += ' pid=' + line[3]
						pid = line[3]
	
					
					tempPorts.append(tempPort)
					
					#THIS IS YOUR WHITELIST DATA, IF THE NETSTAT LINE MATCHS A WHITELIST, DO NOTHING, IF IT DOES MATCH KILL THE CONNECTION
					isIpWhitelisted = False
					for ip in whiteList:
						if ip == dest_ip:
							#print "Good IP: "+str(dest_ip)
							isIpWhitelisted = True
							break
					

					if isIpWhitelisted == False:
						print tempEvent
						print "Bad IP: "+str(dest_ip)
						#kill the connection with currports
						killConnection(dest_ip)
						
						#uncomment the next two lines if you want to kill the process too... not recommended
						#killPid(pid)
						#print "Bad "+str(pid)
					
	
	if tempPorts:
		netstat = string.join(tempPorts, '')
		

# START THE MAIN APPLICATION		
if __name__ == '__main__':

	#Declare whiteList string
	whiteList = ''

	#Print banner
	print "\n\n\n\n-----------------------------------"
	print "Auto disconnect v1.0 by m0r3Sh3LLs"
	print "-----------------------------------\n\n\n\n"

    #SPECIFY WHITELIST OF IPS COMMA DELIMITED, passed in arguments
	if len(sys.argv) <= 1:
		print "ERROR: You must supply a whitelist comma delimited \n"
		print "example: "+ (sys.argv[0]) +" 127.0.0.1,0.0.0.0,192.168.1.1 \n"
		sys.exit()
	
	else:
		 whiteList = str(sys.argv[1])
	

	#INFINITE LOOP
	while True:
		#PASS YOUR WHITELIST OF IPS TO THE NETSTAT FUNCTION
		netstat(whiteList)
