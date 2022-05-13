import getpass
from netmiko import ConnectHandler
import logging
import time
import os
import sys
import datetime
import logging

date = datetime.datetime.now()
date = datetime.datetime.now()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('macsearchV1DC.log')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)


#Add all switches in campus to the myswitch list. 
myswitch = []
#Add all of the MAC addresses that you want to search for in the macaddr list.
macaddr = []



#Main Function that will do the SSH process of creating an SSH session into the switch list. 



# *****************Before this is ran please update the VLAN entries below, ir it will not work. ************************
def ssh(username, password, myswitch):
    vlan_change = ['vlan xxxx','name xxxxxxxxxx']

    device_type = 'cisco_ios'
    net_connect = ConnectHandler(host=myswitch, username=username, password=password, device_type=device_type)
    logger.info(myswitch)
    print("Establishing an SSH session to switch :" +myswitch)
    time.sleep(.5)
    print("Checking for Vlan xxxx")
    time.sleep(1)
#This is going to check for a single vlan , and move on if it detects it, if not it will add it. 
    vlan_check = net_connect.send_command('show vlan | inc xxxx')
    logger.info(vlan_check)
    if vlan_check == "":
        print('Going to add Vlan to switch:' +myswitch)
        add_vlan = net_connect.send_config_set(vlan_change)
        print(add_vlan)
        logger.info(add_vlan)
        time.sleep(3)
        print('Moving on to switchport check.')
    print("Vlan detected, moving on to searching for the MAC's")
#Here is the process of moving through the different mac addresses through the different switches. 
    for i, f in enumerate(macaddr):
        print ("---------- Checking switch "+myswitch+" and mac: "+macaddr[i]+" ----------")
        time.sleep(2)
        command1 = net_connect.send_command('show mac address-table | inc '+macaddr[i])
        print (command1)
        logger.info(command1)
        if command1 !=  "": 
            command2 = net_connect.send_command("show interfaces trunk | inc "+ command1[37:])
            print (command2)
            logger.info(command2)
            if not "trunking" in command2:
                config_commands = ['interface '+ command1[37:], 'switchport access vlan xxxx']
                shut_no_shut = ['interface '+ command1[37:], 'shutdown','no shutdown']
                print("Going to change switchport on "+myswitch+" switchport: "+command1[37:])
                logger.info("Going to change switchport on "+myswitch+" switchport: "+command1[37:])
                time.sleep(5)
                chgint = net_connect.send_config_set(config_commands)
                print (chgint)
                logger.info(chgint)
                print("Going to now Shut/ No Shut port.")
                time.sleep(5)
                booter = net_connect.send_config_set(shut_no_shut)
                logger.info(shut_no_shut)
                time.sleep(2)
                print("Switchport Changed, moving to next Mac Address")
            else:
                print ('Trunk Port Detected on switch ' +myswitch+ ' port ' +command1[37:])
                logger.info('Trunk Port Detected on switch ' +myswitch+ ' port ' +command1[37:])
#Going to check to see if there is a trunk on that port, if not , going to change switchport to what is programmed. Then shut / no shut the port. 




#Credentials
username = input('Username: ')
password = getpass.getpass("Password: ")

#Enumerate though the different switches that are listed above. 
for i, d in enumerate(myswitch):
    ssh(username, password, d)


