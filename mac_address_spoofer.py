#!/usr/bin/env python

import subprocess
import optparse
import re

#This function is to get the input given by the user
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Network Interface whose MAC adress is to be changed")
    parser.add_option("-n", "--new_mac", dest="new_mac", help="New mac address you want to use")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        #Code to handle error
        parser.error("[-] Please specify an interface, use --help for info")
    elif not options.new_mac:
        parser.error("[-] Please specify a new_mac address, use --help for info")
    return options     
    
#This function does the actual changing of the mac address
def spoof_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to "+ new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface , "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    subprocess.call(["ifconfig", interface])
 
#Miscelleneous function to optimize the code  
def get_current_mac(interface):
    results = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", results)
    if mac_address_search_result:
        return(mac_address_search_result.group(0))
    else:
        return("[-] No MAC address Available")
        


options = get_arguments()
present_mac_address = get_current_mac(options.interface)
print("Your Current MAC: " + present_mac_address)

spoof_mac(options.interface,options.new_mac)
present_mac_address = get_current_mac(options.interface)

if present_mac_address == options.new_mac:
    print("[+] MAC address change successfuly, new MAC: " + present_mac_address)
    
else:
    print("[-] No change in MAC address")



