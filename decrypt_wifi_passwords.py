# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 16:56:33 2021

@author: Yicong
"""

import subprocess
import csv

results = []
profiles = []
count=0

#(1) Find all wifi profiles
cmd_results = subprocess.check_output(['netsh','wlan','show','profiles']).decode('utf-8', errors ="backslashreplace")
cmd_results = cmd_results.split("\r\n")
profiles = [cmd_result.split(": ")[-1] for cmd_result in cmd_results if "All User Profile" in cmd_result]


if __name__ == '__main__':
    try:
        with open('decrypted_password.csv', mode='w', newline='') as decrypt_password_file:
            csv_writer = csv.writer(decrypt_password_file, delimiter=',')
            csv_writer.writerow(["index","wifi","password"])

            #(2) loop through all profiles and extract wifi password
            for index,profile in enumerate(profiles):
		
                cmd_results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors ="backslashreplace")
                password=[cmd_result.split(":")[1][1:] for cmd_result in cmd_results.split("\r\n") if "Key Content" in cmd_result]
                if len(password) == 1:

                    #(3) If available, save password into csv
                    print("Sequence: %d"%(count))
                    print("Wifi: %s \nPassword: %s"%(profile,password[0]))
                    print("*"*50)
                    csv_writer.writerow([count,profile,password[0]])
                    count=count+1
            
    except Exception as e:
        print("[ERR] "%str(e))