import serial, msvcrt, time, os, sys, datetime

class Connection:
	_counter = 0
	def __init__( self, Port_A="", Port_B="", BR=9600, Msg="a", Con_Name=""):
		Connection._counter += 1
		self.id = Connection._counter
		self.Msg = Msg
		self.Port_A = Port_A
		self.Port_B = Port_B
		self.BR = BR
		self.Con_Name = Con_Name
		self.COM_Port_A = serial.Serial(port=self.Port_A, baudrate=self.BR, timeout=0.1)
		self.COM_Port_B = serial.Serial(port=self.Port_B, baudrate=self.BR, timeout=0.1)
		self.msg_ok_toP1 = 0
		self.msg_ok_toP2 = 0
		self.msg_ko_toP1 = 0
		self.msg_ko_toP2 = 0

	def PortA_to_PortB(self):
		# SEND MSG from A to B
		self.COM_Port_A.write(self.Msg)     # write a string
		read = self.COM_Port_B.read_until(self.Msg)
		if(read == self.Msg):
			self.msg_ok_toP2 += 1
		else:
			#print(str(db) + "ERROR, msg: " + read)
			self.msg_ko_toP2 += 1

	def PortB_to_PortA(self):
		# SEND MSG from B to A
		self.COM_Port_B.write(self.Msg)     # write a string
		read = self.COM_Port_A.read_until(self.Msg)
		if(read == self.Msg):
			self.msg_ok_toP1 += 1
		else:
			#print(str(db) + "ERROR, msg: " + read)
			self.msg_ko_toP1 += 1

	def Print_Number_of_Msg(self, i):
		text = "Number of Msg " + self.Con_Name + ": " + str(i) + "\n" + \
		"Number of OK " + self.Con_Name + " Msg (A -> B, A <- B): " + \
		str(self.msg_ok_toP2) + ", " + str(self.msg_ok_toP1) + "\n" + \
		"Number of KO " + self.Con_Name + " Msg (A -> B, A <- B): " + \
		str(self.msg_ko_toP2) + ", " + str(self.msg_ko_toP1) + "\n"
		sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (3 + (self.id-1)*4, 1, text))
		sys.stdout.flush()

	def Close_Ports(self):
		self.COM_Port_A.close()
		self.COM_Port_B.close()

# PORT kiosztás
COM_RS232_1 = "COM5"
COM_RS232_2 = "COM6"
COM_RS485_1 = "COM1"
COM_RS485_2 = "COM4"
COM_MOXA_P1 = "COM29"	# RS485
COM_MOXA_P2 = "COM30"	# RS232

# Connection létrehozása
RS485 = Connection(COM_RS485_1, COM_RS485_2, 9600, b'swag, yolo!', "HW RS232")
Emulated_RS232 = Connection(COM_RS232_1, COM_RS232_2, 9600, b'swag, yolo!', "Emulated RS232")

# Init
os.system('cls' if os.name=='nt' else 'clear')
start = time.time()
start_datetime = datetime.datetime.now()
i=0
end_row=Connection._counter*5
print("Communication started (" + str(start_datetime) + ")")

while(True):	
	RS485.PortA_to_PortB()
	RS485.PortB_to_PortA()

	Emulated_RS232.PortA_to_PortB()
	Emulated_RS232.PortB_to_PortA()

	i+=1

	if(time.time() - start > 0.5):
		RS485.Print_Number_of_Msg(i)
		Emulated_RS232.Print_Number_of_Msg(i)

		start = time.time()
	
	if(msvcrt.kbhit()):
		kb = int.from_bytes(msvcrt.getch(),'big')
		text = "\n"*end_row + "Communication stopped by User (" + str(datetime.datetime.now()) + ")\n"
		text += "Test duration: " + str(datetime.datetime.now() - start_datetime)
		sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (1, 1, text))
		sys.stdout.flush()
		print("\n"*end_row)
		if kb == 27:
			break

RS485.Close_Ports()
Emulated_RS232.Close_Ports()
