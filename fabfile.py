#!/usr/bin/env /usr/local/bin/python3
import sys
import fabric
import sys
import time
from fabric.api import env, run, settings, task, run, roles, sudo, parallel, put
import datetime



env.user = "centos"
env.keys = "/Users/mvasupalli/patching/id_rsa_splunk"

# Setting up th inventory
env.roledefs = {

"test":[
"hosta",
"hostb"
],

"sauce_connect": [
"hosta",
"hostb"],

"ap_pdx":
["hosta",
"hostb"],

"splunk":
[
"hosta",
"hostb"
],

"cb_gcp":
["hosta",
"hostb"],

"cb_pdx":
["hosta",
"hostb"],

"cs_xcp":
["hosta",
"hostb"],

"p4":
["hosta",
"hostb"]
}

def restart_service(service_name):
	with settings(warn_only=True, parallel=True):
		time.sleep(10)
		run("sleep 3")
		restart = sudo("systemctl restart " + service_name)
		if restart.return_code == 0:
			time.sleep(2)
			status = sudo("systemctl status " + service_name)
			return status.return_code
		return 404

def change_permissons_on_remote(path, user, group, perms):
	with settings(warn_only=True, parallel=True):
		chperms = sudo("chmod 644 "+ path)
		time.sleep(2)
		chown = sudo ("chown "+ user + ":"  + group + " " + path )
		if chperms.return_code == 0 and chown.return_code == 0:
			return True
		return False

def backup_existing_certs(file_name):
	time.sleep(2)
	with settings(warn_only=True, parallel=True):
		dt = datetime.datetime.now()
		dt = "_" + str(dt).split()[0]
		backup = sudo("cp "+file_name+" "+ file_name + str(dt))
		if backup.return_code == 0:
			print(env.host + " - " + file_name + " has been backed up :"+ file_name+str(dt))
			return True
		else:
			print(env.host + " - Failed to back up " + file_name )
			return False


def replace_files(filea,fileb):
	time.sleep(2)
	with settings(warn_only=True, parallel=True):
		rf = sudo("yes| cp -rf "+ filea + " " + fileb)
		if rf.return_code == 0:
			return True
		return False

def apply_certs():
	user  = "zabbix"
	owner = "zabbix"
	perms = "0644"
	if "gcp" in env.host:
		certs_path = "/etc/zabbix/certs/"
		src = ["/tmp/gcp_certs/abshosts.gcp.eng.sfdc.net_20210220.privkey.pem", "/tmp/gcp_certs/abshosts.gcp.eng.sfdc.net.chain.pem"]
		dst = ["/etc/zabbix/certs/abshosts.gcp.eng.sfdc.net.privkey.pem", "/etc/zabbix/certs/abshosts.gcp.eng.sfdc.net.chain.pem"]
	elif "pdx" in env.host:
		certs_path = "/etc/zabbix/certs/"
		src = ["/tmp/pdx_certs/abshosts.pdx.eng.sfdc.net_20210220.privkey.pem", "/tmp/pdx_certs/abshosts.pdx.eng.sfdc.net.chain.pem"]
		dst = ["/etc/zabbix/certs/abshosts.pdx.eng.sfdc.net.privkey.pem", "/etc/zabbix/certs/abshosts.pdx.eng.sfdc.net.chain.pem"]
	elif "prd" in env.host or "dpxbot" in env.host:
		certs_path = "/etc/zabbix/certs/"
		src = ["/tmp/prd_certs/abshosts.prd.eng.sfdc.net_20210220.privkey.pem", "/tmp/prd_certs/abshosts.prd.eng.sfdc.net.chain.pem"]
		dst = ["/etc/zabbix/certs/abshosts.prd.eng.sfdc.net.privkey.pem", "/etc/zabbix/certs/abshosts.prd.eng.sfdc.net.chain.pem"]
	
	for i in range(0,len(src)):
		backup_existing_certs(dst[i])
		replace_certs = replace_files(src[i], dst[i])
		if replace_certs:
			chown = change_permissons_on_remote(dst[i], user, owner, perms)
			if chown:
				if "dpxbot" in env.host or "splunk" in env.host:
					service = "zabbix-agent"
				else:
					service = "zabbix"
				rs = restart_service(service)
				if rs == 0:
					print(env.host + " All Good")
				else: print(env.host + "- Restart failed. Please check")
			else:
				print(env.host + "- Failed to change the ownership. Please check")


		else:
			print(env.host + "- Failed to replace the files. Please check")
			
		

def copyfiles_2_remote(source, destination):
	with settings(warn_only=True, parallel=True):
		cp_cmd = put(source, destination)
		apply_certs()
 
def init_certs_copy():
	if "gcp" in env.host:
		copyfiles_2_remote("certs/gcp_certs", "/tmp")
	elif "pdx" in env.host:
		copyfiles_2_remote("certs/pdx_certs", "/tmp")
	elif "prd" in env.host or "dpxbot" in env.host:
		copyfiles_2_remote("certs/prd_certs", "/tmp")
	else:
		print("Unknown Category")

def verify_certs_status():
	with settings(warn_only=True, parallel=True):
		if "dpxbot" in env.host or "splunk" in env.host:
			service = "zabbix-agent"
		else:
			service = "zabbix"
		msg = "\n\n=================================================="
		certs_list = sudo("ls -lrt /etc/zabbix/certs")
		msg  += certs_list
		msg += "\n\n"
		certs_conf = sudo("cat /etc/zabbix/zabbix_agentd.conf")
		msg += "\n\n"
		sstatus = run("systemctl status "+service+"| head -4")
		msg += sstatus
		msg += "\n\n=================================================="
		print(msg)

def check_expiry():
	with settings(warn_only=True, parallel=False):
		expiry_date = run("ls")
		if expiry_date.return_code == 0:
			print(expiry_date)
			Year_exp = expiry_date.split()[-2]
		
			try:
				if int(Year_exp) <= 2021:
					init_certs_copy()
				else:
					print("Already upto date"+ env.host)
			except Exception as e:
				print(env.host + " - Encountered exception. Please check")
				print(e)
		else:
			print(env.host + " - Failed to fetch the expiry date. Please check")

@task
def starter():
	with settings(warn_only=True, parallel=False):
		# hosname = run("uname")
		# print(hosname)
		# check_expiry()
		
		verify_certs_status()
	# copyfiles_2_remote("./certs/gcp", "/tmp/")
