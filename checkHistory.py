# This function is called by winFunc and will check/edit checkHistory.txt
cmd = ["o","c"];
usr_cmd = "o";
#try: I was attempting to create the file if it does not exist
#    p = 0;
#    f = open("check_History.txt","r+"); #
#    p = 2;
f = open("check_History",'r+')
pre = f.read();
if pre == "":
    # return usr_cmd as the direction_input
    f.write(usr_cmd);
    f.close();
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
            # return current as the direction output
    else:
        current = usr_cmd;
        f.close();
        f = open("check_History","w+");
        f.write(current);
        f.close();
        #retun current as the direction output
#except:
#    if p < 1:
#        with open("check_History.txt","w") as f: #
#            f.write(usr_cmd)
