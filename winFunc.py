#!/usr/bin/ env python
# file: winFunc.py
# desc: modified rfcomm-server.py by Albert Huang. 


from bluetooth import *
import RPi.GPIO as GPIO, time

# servo motor settings start
GPIO.setmode(GPIO.BOARD)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
p = GPIO.PWM(16, 500)

def SpinMotor(direction, steps):
	GPIO.output(18, direction)
	GPIO.output(2, TRUE)
	while steps > 0:
		p.start(1)
		time.sleep(0.01)
		steps -= 1
	p.stop()
	GPIO.cleanup()
	return True
# servo motor settings end

# check function starts
def checkHistory(usr_cmd):
        cmd = ["o","c"];
        f = open("check_History",'r+')
        pre = f.read();
        if pre == []:
                # return usr_cmd as the direction_input
                f.write(usr_cmd);
                f.close();
                return usr_cmd
        else:
                if pre == usr_cmd:
                        # previous command and new command are the same
                        if usr_cmd == cmd[0]:
                                current = cmd[1];
                                f.close();
                                f = open("check_History","w+");
                                f.write(current);
                                f.close();
                        elif usr_cmd == cmd[1]:
                                current = cmd[0];
                                f.close();
                                f = open("check_History","w+");
                                f.write(current);
                                f.close();
                        return current
                else:
                        current = usr_cmd;
                        f.close();
                        f = open("check_History","w+");
                        f.write(current);
                        f.close();
                        return current
# check function ends

# bluetooth 
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        steps = 200 # the deafult number of steps. Depends on window
        direction_input = client_sock.recv(1024)
        if len(direction_input) == 0: break

        #
        direction = checkHistory(direction_input);
        #
        if direction == 'o':
            SpinMotor(False, steps); break
        elif direction == 'c':
                SpinMotor(True, steps); break
        else:
            break
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
