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
"prod0ceo0-splunkidx1-2-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-3-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-4-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-6-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-7-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-8-gcp.dop.sfdc.net",
"prod0ceo0-splunkidxmaster1-1-gcp.dop.sfdc.net"
],

"dpx_bot":[
"dpxbot-instance-prod-0.eng.sfdc.net",
"dpxbot-instance-prod-1.eng.sfdc.net",
"dpxbot-instance-prod-2.eng.sfdc.net",
"dpxbot-instance-stg-0.eng.sfdc.net",
"dpxbot-instance-stg-1.eng.sfdc.net"
],

"sauce_connect": [
"sauceconnect01-gcp.prod.ci.sfdc.net",
"sauceconnect02-gcp.prod.ci.sfdc.net",
"sauceconnect03-gcp.prod.ci.sfdc.net",
"sauceconnect04-gcp.prod.ci.sfdc.net",
"sauceconnect05-gcp.prod.ci.sfdc.net",
"sauceconnect06-gcp.prod.ci.sfdc.net"
],

"ap_pdx":
["apiarysls-pdx-1.prod.ci.sfdc.net", 
"apiarysls-pdx-2.prod.ci.sfdc.net", 
"apiarysls-pdx-3.prod.ci.sfdc.net", 
"apiarysls-pdx-4.prod.ci.sfdc.net",
"apiarysls-pdx-5.prod.ci.sfdc.net",
"apiarysls-pdx-6.prod.ci.sfdc.net"],

"splunk":
[
"prod0ceo0-splunkhead2-1-gcp.dop.sfdc.net",
"prod0ceo0-splunkagent1-1-gcp.dop.sfdc.net",
"prod0ceo0-splunkhead2-2-gcp.dop.sfdc.net",
"prod0ceo0-splunkhead2-3-gcp.dop.sfdc.net",
"prod0ceo0-splunkhec1-1-gcp.dop.sfdc.net",
"prod0ceo0-splunkhec1-2-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-1-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-10-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-12-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-13-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-14-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-15-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-2-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-3-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-4-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-6-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-7-gcp.dop.sfdc.net",
"prod0ceo0-splunkidx1-8-gcp.dop.sfdc.net",
"prod0ceo0-splunkidxmaster1-1-gcp.dop.sfdc.net",

"tp0ceo0-app1-2-gcp.eng.sfdc.net",
"tp0ceo0-esearch1-10-gcp.eng.sfdc.net",
"tp0ceo0-esearch1-2-gcp.eng.sfdc.net",
"tp0ceo0-esearch1-3-gcp.eng.sfdc.net",
"tp0ceo0-esearch1-4-gcp.eng.sfdc.net",
"tp0ceo0-esearch1-6-gcp.eng.sfdc.net",
"tp0ceo0-esearch1-7-gcp.eng.sfdc.net",
"tp0ceo0-esearch1-8-gcp.eng.sfdc.net",
"tp0ceo0-esearch1-9-gcp.eng.sfdc.net"
],

"cb_gcp":
["cloudyboy-gcp-1.prod.ci.sfdc.net",
"cloudyboy-gcp-10.prod.ci.sfdc.net",
"cloudyboy-gcp-11.prod.ci.sfdc.net",
"cloudyboy-gcp-12.prod.ci.sfdc.net",
"cloudyboy-gcp-13.prod.ci.sfdc.net",
"cloudyboy-gcp-14.prod.ci.sfdc.net",
"cloudyboy-gcp-15.prod.ci.sfdc.net",
"cloudyboy-gcp-16.prod.ci.sfdc.net",
"cloudyboy-gcp-17.prod.ci.sfdc.net",
"cloudyboy-gcp-18.prod.ci.sfdc.net",
"cloudyboy-gcp-19.prod.ci.sfdc.net",
"cloudyboy-gcp-2.prod.ci.sfdc.net",
"cloudyboy-gcp-20.prod.ci.sfdc.net",
"cloudyboy-gcp-21.prod.ci.sfdc.net",
"cloudyboy-gcp-22.prod.ci.sfdc.net",
"cloudyboy-gcp-23.prod.ci.sfdc.net",
"cloudyboy-gcp-24.prod.ci.sfdc.net",
"cloudyboy-gcp-25.prod.ci.sfdc.net",
"cloudyboy-gcp-26.prod.ci.sfdc.net",
"cloudyboy-gcp-3.prod.ci.sfdc.net",
"cloudyboy-gcp-4.prod.ci.sfdc.net",
"cloudyboy-gcp-5.prod.ci.sfdc.net",
"cloudyboy-gcp-6.prod.ci.sfdc.net",
"cloudyboy-gcp-7.prod.ci.sfdc.net",
"cloudyboy-gcp-8.prod.ci.sfdc.net",
"cloudyboy-gcp-9.prod.ci.sfdc.net"],

"cb_pdx":
["cloudyboy-pdx-1.prod.ci.sfdc.net",
"cloudyboy-pdx-10.prod.ci.sfdc.net",
"cloudyboy-pdx-11.prod.ci.sfdc.net",
"cloudyboy-pdx-12.prod.ci.sfdc.net",
"cloudyboy-pdx-13.prod.ci.sfdc.net",
"cloudyboy-pdx-14.prod.ci.sfdc.net",
"cloudyboy-pdx-15.prod.ci.sfdc.net",
"cloudyboy-pdx-16.prod.ci.sfdc.net",
"cloudyboy-pdx-17.prod.ci.sfdc.net",
"cloudyboy-pdx-18.prod.ci.sfdc.net",
"cloudyboy-pdx-19.prod.ci.sfdc.net",
"cloudyboy-pdx-2.prod.ci.sfdc.net",
"cloudyboy-pdx-20.prod.ci.sfdc.net",
"cloudyboy-pdx-21.prod.ci.sfdc.net",
"cloudyboy-pdx-3.prod.ci.sfdc.net",
"cloudyboy-pdx-4.prod.ci.sfdc.net",
"cloudyboy-pdx-5.prod.ci.sfdc.net",
"cloudyboy-pdx-6.prod.ci.sfdc.net",
"cloudyboy-pdx-7.prod.ci.sfdc.net",
"cloudyboy-pdx-8.prod.ci.sfdc.net",
"cloudyboy-pdx-9.prod.ci.sfdc.net"],

"cs_xcp":
["credstore-gcp-0.prod.ci.sfdc.net",
"credstore-gcp-1.prod.ci.sfdc.net",
"credstore-gcp-2.prod.ci.sfdc.net",
"credstore-gcp-3.prod.ci.sfdc.net",
"credstore-gcp-4.prod.ci.sfdc.net",
"credstore-gcp-5.prod.ci.sfdc.net",
"credstore-pdx-1.prod.ci.sfdc.net",
"credstore-pdx-2.prod.ci.sfdc.net",
"credstore-pdx-3.prod.ci.sfdc.net"],

"dpx_bot":
["dpxbot-instance-prod-0.eng.sfdc.net",
"dpxbot-instance-prod-1.eng.sfdc.net",
"dpxbot-instance-prod-2.eng.sfdc.net",
"dpxbot-instance-stg-0.eng.sfdc.net",
"dpxbot-instance-stg-1.eng.sfdc.net"],

"p4":
["scm-pfourbroker1-2-prd.eng.sfdc.net",
"scm-pfourbroker1-3-prd.eng.sfdc.net",
"scm-pfourbroker1-4-prd.eng.sfdc.net",
"scm-pfourbroker1-5-prd.eng.sfdc.net",
"scm-pfourbroker2-1-prd.eng.sfdc.net",
"scm-pfourbroker2-2-prd.eng.sfdc.net",
"scm-pfourbroker2-3-prd.eng.sfdc.net",
"scm-pfourbroker2-4-prd.eng.sfdc.net",
"scm-pfourbroker2-5-prd.eng.sfdc.net",
"scm-pfourbroker3-3-prd.eng.sfdc.net",
"scm-pfourbroker3-4-prd.eng.sfdc.net",
"scm-pfourbrorep1-1-prd.eng.sfdc.net",
"scm-pfourbrorep1-2-prd.eng.sfdc.net",
"scm-pfourbrorep1-3-prd.eng.sfdc.net",
"scm-pfourbrorep1-4-prd.eng.sfdc.net",
"scm-pfourbrorep2-1-prd.eng.sfdc.net",
"scm-pfourbrorep2-2-prd.eng.sfdc.net",
"scm-pfourbrorep2-3-prd.eng.sfdc.net",
"scm-pfourbrorep2-4-prd.eng.sfdc.net",
"scm-pfourbrorep3-1-prd.eng.sfdc.net",
"scm-pfourbrorep3-2-prd.eng.sfdc.net",
"scm-pfourbrorep3-3-prd.eng.sfdc.net",
"scm-pfourbrorep3-4-prd.eng.sfdc.net",
"scm-pfourbrorep4-1-prd.eng.sfdc.net",
"scm-pfourbrorep4-2-prd.eng.sfdc.net",
"scm-pfourbrorep4-3-prd.eng.sfdc.net",
"scm-pfourbrorep5-1-prd.eng.sfdc.net",
"scm-pfourbrorep5-2-prd.eng.sfdc.net",
"scm-pfourbrorep5-3-prd.eng.sfdc.net",
"scm-pfourbrorep5-4-prd.eng.sfdc.net",
"scm-pfourbrorep6-1-prd.eng.sfdc.net",
"scm-pfourbrorep6-3-prd.eng.sfdc.net",
"scm-pfourbrorep6-5-prd.eng.sfdc.net",
"scm-pfourbrorep6-6-prd.eng.sfdc.net",
"scm-pfourbrorep7-1-prd.eng.sfdc.net",
"scm-pfourbrorep7-2-prd.eng.sfdc.net",
"scm-pfourbrorep7-3-prd.eng.sfdc.net",
"scm-pfourbrorep7-4-prd.eng.sfdc.net",
"scm-pfourbrorep8-1-prd.eng.sfdc.net",
"scm-pfourbrorep8-2-prd.eng.sfdc.net",
"scm-pfourbrorep8-3-prd.eng.sfdc.net",
"scm-pfourbrorep8-4-prd.eng.sfdc.net",
"scm-pfourcommit1-3-prd.eng.sfdc.net",
"scm-pfourcommit1-4-prd.eng.sfdc.net",
"scm-pfouredge1-2-prd.eng.sfdc.net",
"scm-pfouredge1-3-prd.eng.sfdc.net",
"scm-pfouredge1-4-prd.eng.sfdc.net",
"scm-pfouredge1-5-prd.eng.sfdc.net ",
"scm-pfouredge1-6-prd.eng.sfdc.net",
"scm-pfouredge1-7-prd.eng.sfdc.net ",
"scm-pfouredge1-8-prd.eng.sfdc.net ",
"scm-pfouredge2-2-prd.eng.sfdc.net",
"scm-pfouredge2-3-prd.eng.sfdc.net",
"scm-pfouredge2-4-prd.eng.sfdc.net",
"scm-pfourproxy1-10-prd.eng.sfdc.net",
"scm-pfourproxy1-11-prd.eng.sfdc.net",
"scm-pfourproxy1-13-prd.eng.sfdc.net",
"scm-pfourproxy1-14-prd.eng.sfdc.net",
"scm-pfourproxy1-4-prd.eng.sfdc.net",
"scm-pfourproxy1-5-prd.eng.sfdc.net",
"scm-pfourproxy1-7-prd.eng.sfdc.net",
"scm-pfourproxy1-8-prd.eng.sfdc.net",
"scm-pfourproxy1-9-prd.eng.sfdc.net",
"scm-pfourproxy2-10-prd.eng.sfdc.net",
"scm-pfourproxy2-11-prd.eng.sfdc.net",
"scm-pfourproxy2-13-prd.eng.sfdc.net",
"scm-pfourproxy2-14-prd.eng.sfdc.net",
"scm-pfourproxy2-4-prd.eng.sfdc.net",
"scm-pfourproxy2-5-prd.eng.sfdc.net",
"scm-pfourproxy2-8-prd.eng.sfdc.net",
"scm-pfourproxy2-9-prd.eng.sfdc.net",
"scm-pfourproxy3-10-prd.eng.sfdc.net",
"scm-pfourproxy3-11-prd.eng.sfdc.net",
"scm-pfourproxy3-12-prd.eng.sfdc.net",
"scm-pfourproxy3-13-prd.eng.sfdc.net",
"scm-pfourproxy3-14-prd.eng.sfdc.net",
"scm-pfourproxy3-4-prd.eng.sfdc.net",
"scm-pfourproxy3-5-prd.eng.sfdc.net",
"scm-pfourproxy3-7-prd.eng.sfdc.net",
"scm-pfourproxy3-8-prd.eng.sfdc.net",
"scm-pfourproxy3-9-prd.eng.sfdc.net",
"scm-pfourproxy4-10-prd.eng.sfdc.net",
"scm-pfourproxy4-11-prd.eng.sfdc.net",
"scm-pfourproxy4-12-prd.eng.sfdc.net",
"scm-pfourproxy4-13-prd.eng.sfdc.net",
"scm-pfourproxy4-8-prd.eng.sfdc.net",
"scm-pfourproxy4-9-prd.eng.sfdc.net"]
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
		check_expiry()
		
		# verify_certs_status()
	# copyfiles_2_remote("./certs/gcp", "/tmp/")
