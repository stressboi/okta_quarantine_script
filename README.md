# okta_quarantine_script
A script using Okta's Python SDK to manipulate application sign-on policy for quarantine group membership.

What's the use case? This provides the ability to create a sign-on policy rule, per application, in Okta
in a scripted fashion. Say for example you want to be able to block the ability for a user to log into 
ALL applications in a temporary fashion because you suspect they, or their device, has become compromised.

In order to do this you have to create a sign-on policy, per application, so that when the user is a member
of the "Quarantine" group they are locked out of logging into the app. Therefore, you have to create a 
rule PER APP and that is tedious to do in the Admin GUI. This makes it easy. Simply run it in "list" mode
and get a list of all apps. Then edit that list down to include JUST the apps you want to "block" while a 
user is in quarantine. Then run the script again in "apply" mode supplying the edited list.

Suggest that you block all groups you have created EXCEPT for perhaps your IT Helpdesk group - e.g. still
allow a user to log a ticket in ServiceNow or whatever you use.

Thanks go to kelbys@splunk.com for suggesting this.

james.brodsky@okta.com
30JAN2022
