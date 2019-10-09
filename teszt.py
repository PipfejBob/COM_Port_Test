import serial, msvcrt, time, os, colorama, sys, datetime

class Connection:
	def __init__( self, Port_A="", Port_B="", Msg="a"):
		self.Msg = Msg
		self.Port_A = Port_A
		self.Port_B = Port_B
		self.COM_Port_A = serial.Serial(port=self.Port_A, baudrate=115200, timeout=0.1)
		self.COM_Port_B = serial.Serial(port=self.Port_B, baudrate=115200, timeout=0.1)
		self.msg_ok_toP1 = 0
		self.msg_ok_toP2 = 0
		self.msg_ko_toP1 = 0
		self.msg_ko_toP2 = 0

	def PortA_to_PortB(self):
		# SEND MSG from RS485_P1 to RS485_P2
		self.COM_Port_A.write(self.Msg)     # write a string
		read = self.COM_Port_B.read_until(self.Msg)
		if(read == self.Msg):
			#print("OK, msg:", Msg)
			self.msg_ok_toP2 += 1
		else:
			#print(str(db) + "ERROR, msg: " + read)
			self.msg_ko_toP2 += 1

	def PortB_to_PortA(self):
		# SEND MSG from RS485_P1 to RS485_P2
		self.COM_Port_B.write(self.Msg)     # write a string
		read = self.COM_Port_A.read_until(self.Msg)
		if(read == self.Msg):
			#print("OK, msg:", Msg)
			self.msg_ok_toP1 += 1
		else:
			#print(str(db) + "ERROR, msg: " + read)
			self.msg_ko_toP1 += 1

# PORT kiosztás
COM_RS232_1 = "COM1"
COM_RS232_2 = ""
COM_RS485_1 = "COM1"
COM_RS485_2 = "COM2"
COM_MOXA_P1 = "COM29"	# RS485
COM_MOXA_P2 = "COM30"	# RS232

# Más cuccok
RS485 = Connection(COM_RS485_1, COM_RS485_2, b'swag, yolo!')
colorama.init()
os.system('cls' if os.name=='nt' else 'clear')
i=0
sajt = 0
start = time.time()
start_datetime = datetime.datetime.now()
print("Communication started (" + str(start_datetime) + ")" + "\n"*7)

while(True):	
	
	# SEND MSG from RS485_P1 to RS485_P2
	RS485.PortA_to_PortB()

	# SEND MSG from RS485_P2 to RS485_P1
	RS485.PortB_to_PortA()

	i+=1

	if(time.time() - start > 0.5):
		text = "Number of Msg: " + str(i) + "\n" + \
		"Number of OK RS485 Msg (p1->p2, p1<-p2): (" + \
		str(RS485.msg_ok_toP2) + " ," + str(RS485.msg_ok_toP1) + ")\n" + \
		"Number of KO RS485 Msg (p1->p2, p1<-p2): (" + \
		str(RS485.msg_ko_toP2) + " ," + str(RS485.msg_ko_toP1) + ")\n"
		sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (3, 1, text))
		sys.stdout.flush()
		start = time.time()
		sajt += 1
	
	if(msvcrt.kbhit()):
		kb = int.from_bytes(msvcrt.getch(),'big')
		text = "Communication stopped by User (" + str(datetime.datetime.now()) + ")\n"
		text += "Test duration: " + str(datetime.datetime.now() - start_datetime)
		sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (7, 1, text))
		sys.stdout.flush()
		#print('\bCommunication stopped by User')
		if kb == 27:
			break
	
RS485.COM_Port_A.close()	# close port
RS485.COM_Port_B.close()	# close port