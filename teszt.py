import serial, msvcrt

# PORT kiosztás
COM_RS232_1 = "COM1"
COM_RS232_2 = ""
COM_RS485_1 = "COM3"
COM_RS485_2 = "COM4"
COM_MOXA_P1 = "COM29"	# RS485
COM_MOXA_P2 = "COM30"	# RS232

# Más cuccok
Msg = b'swag,yolo!'
msg_db = 100

ser_RS485_1 = serial.Serial(port=COM_RS485_1, baudrate=115200, timeout=0.1)  		# open serial port
ser_RS485_2 = serial.Serial(port=COM_RS485_2, baudrate=115200, timeout=0.1)  	# open serial port
i=0
msg_ok_to1 = 0
msg_ko_to1 = 0
msg_ok_to2 = 0
msg_ko_to2 = 0

while(True):
    ser_RS485_1.write(Msg)     # write a string
    read = ser_RS485_2.read_until(Msg)
    if(read == Msg):
        #print("OK, msg:", Msg)
        msg_ok_to2 += 1
    else:
        #print(str(db) + "ERROR, msg: " + read)
        msg_ko_to2 += 1
    
    ser_RS485_2.write(Msg)     # write a string
    read = ser_RS485_1.read_until(Msg)
    if(read == Msg):
        #print("OK, msg:", Msg)
        msg_ok_to1 += 1
    else:
        #print(str(db) + "ERROR, msg: " + read)
        msg_ko_to1 += 1
    
    i+=1
    
    if(msvcrt.kbhit()):
        kb = int.from_bytes(msvcrt.getch(),'big')
        print(kb)
        if kb == 27:
            break

print("Number of Msg: " + str(i))
print("Number of OK Msg (p1->p2, p1<-p2): " + str(msg_ok_to2) + ', ' + str(msg_ok_to1))
print("Number of KO Msg (p1->p2, p1<-p2): " + str(msg_ko_to2) + ', ' + str(msg_ko_to1))        
ser_RS485_1.close() # close port
ser_RS485_2.close()	# close port