# okta_apply_quarantine_group.py
# james.brodsky@okta.com
# 30JAN2022
#
# Leverages Okta's Policy API to apply a "deny all" quarantine group to a provided list of
# applications so that the "sign on policy" for the applications contains the logic for the 
# quarantine group. Without this type of script there's a lot of clicking in the admin interface!
#
# Needs Okta Python SDK (pip uinstall okta)
# Needs a group you will put users in, created in your Okta instance called "Quarantine" and supply the ID of this group
# (to find this group, query the API endpoint {{url}}/api/v1/groups and search for "Quarantine"
#
# Supports "list" "apply" and "single" options
# 
# list: retrieves a list of applications available in your Okta instance, writes those out to a file. You then need
# to edit the list and provide just the application IDs on single lines if you want to use this file to then apply
# the quarantine group to each application, using the "apply" function of this script.
#
# EXAMPLE of list usage:
#
# python okta_apply_quarantine_group.py --list output.txt
#
# apply: takes as filename input a list of application IDs. Applys the quarantine group to each one. You must either provide
# your existing "quarantine" group ID in the variables below OR you can supply on the command line as --quargroup.
#
# EXAMPLE of apply usage:
#
# python okta_apply_quarantine_group.py --apply output.txt --quargroup 00g2eb9ms9sy8l2EU1d7
#
# single: applies the "quarantine" group policy to a single application that you specify. Optionally you can supply the
# quarantine group ID.
#
# EXAMPLE of single usage:
#
# python okta_apply_quarantine_group.py --single rst281whwpl4MrBqt1d7 --quargroup 00g2eb9ms9sy8l2EU1d7

import asyncio
import argparse
import os
from okta.client import Client as OktaClient
import okta.models as models

# edit the two lines below to match your org
okta_orgurl = 'https://<your_okta_tenant_with_domain>'
okta_apitoken = '<your_api_token>'

# provide the ID of your quarantine group below
static_quargroup = "<the id value of your quarantine group>"

# connect up to Okta
config = {
    'orgUrl': okta_orgurl,
    'token': okta_apitoken
}

okta_client = OktaClient(config)

# process the command line args
parser = argparse.ArgumentParser()
parser.add_argument('--list', help='list help')
parser.add_argument('--apply', help='apply help')
parser.add_argument('--single', help='single help')
parser.add_argument('--quargroup', help='quargroup help')
parser.add_argument
args = parser.parse_args()
if args.list:
    print("LIST mode output to",args.list)
elif args.apply:
	print("APPLY mode consuming IDs from",args.apply)
elif args.single:
	print("SINGLE mode processing ID",args.single)
else:
	print("no mode chosen! exiting.")
	exit()

# the ID of your quarantine group if not provided
# 
if args.quargroup:
	quargroup = args.quargroup
	print("Quarantine group ID frpm CLI:",quargroup)
else:
	quargroup = static_quargroup
	print("Quarantine group ID hardcoded as:",quargroup)

# list policy logic
async def policylist():
	policies, resp, err = await okta_client.list_policies(policydict)
	fileout = open(filetowrite, "a")
	for policy in policies:
		print(policy.id,policy.name,policy.system)
		outputline=policy.id+","+policy.name
		fileout.write(outputline)
		fileout.write("\n")
	fileout.close()
	print("file written to:",filetowrite)
	print("Edit this file for proper input (just the application IDs, one each line) and then run this in apply mode.")
	print("Done.")
		
# policy options
policydict = {
	"type": "ACCESS_POLICY",
	"status": "ACTIVE",
	"expand": "RULES"
}

# create group model for a policy that simply denies all access
policy_model = models.Policy(
{
    "system": False,
    "type": "ACCESS_POLICY",
    "name": "Quarantine Added by Python SDK",
    "conditions": {
        "userType": {
            "include": [],
            "exclude": []
        },
        "network": {
            "connection": "ANYWHERE"
        },
        "riskScore": {
            "level": "ANY"
        },
        "people": {
            "users": {
                "exclude": [],
                "include": [
                  
                  
                ]
            },
            "groups": {
                "include": [ quargroup ],
                "exclude": []
            }
        },
        "platform": {
            "include": []
        },
        "elCondition": {}
    },
    "actions": {
        "appSignOn": {
            "access": "DENY",
            "verificationMethod": {
                "factorMode": "2FA",
                "reauthenticateIn": "PT2H",
                "constraints": [
                    {
                        "knowledge": {
                            "types": [
                                "password"
                            ]
                        }
                    }
                ],
                "type": "ASSURANCE"
            }
        }
    }
}
)

async def policyset():	
	policycount=0
	for id in policyids:
		policycount+= 1 
		print("PROCESSING APPLY MODE FROM LIST:",id)
		# Create Rule
		group, resp, err = await okta_client.create_policy_rule(id,policy_model)
	print("Total processed:",policycount)
	print("Done.")
		
async def policysetsingle():	
		print("PROCESSING SINGLE MODE:",id)
		group, resp, err = await okta_client.create_policy_rule(id,policy_model)
		print("Done.")
	
loop = asyncio.get_event_loop()
	
if args.list:
	filetowrite=args.list
	if os.path.exists(filetowrite):
		print("Removing the output file",filetowrite,"first...")
		os.remove(filetowrite)
	else:
		print("The file",filetowrite,"does not exist, continuing...")
	loop.run_until_complete(policylist())
	
if args.apply:
	filetoread=args.apply
	with open(filetoread) as p:
		policyids=p.readlines()
	loop.run_until_complete(policyset())
	
if args.single:
	id = args.single
	loop.run_until_complete(policysetsingle())
	