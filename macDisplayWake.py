import datetime, sys, subprocess

"""
Simple script to grep two mac logs for indications of what caused the mac display to
turn on (probably in the middle of the night).

Execute like this:

   python3 macDisplayWake.py 8 | less
   
The argument (8 here) indicates how many hours to look back in the log. For example,
I would run first thing in the morning to check for what happened overnight - i.e. about
the last 8 hours.

For me, it turned out to be an old USB headset, probably with a bad driver.

"""

# These are the grep strings for pmset and syslog and can be edited. Note
# that when adding another string, preface it with '\|' which is a logical 'or'
grep_pmset  = r"UserIsActive\|'to FullWake'\|'Display is turned on'"
grep_syslog = r"'Local user activity reported'\|'Lets turn it on'\|'full wake'"

hours    = sys.argv[1]

now            = datetime.datetime.today()
now_str        = now.strftime("%Y-%m-%d %H")
delta          = datetime.timedelta(hours=int(hours))  # create a delta time of 'hours'
new_time       = now - delta                           # get time value of 'hours' ago
time_str       = new_time.strftime("%Y-%m-%d %H")      # format a string of the new_time value

# These are the two commands to fetch the logs. Since pmset doesn't accept the '--last' argument
# I pipe the pmset log through another python script (printAfter.py) so that only the messages
# after a certain time (i.e. time_str) are displayed
cmd_pmset      = f"pmset -g log"
cmd_syslog     = f"log show --style syslog --last {hours}h"


full_cmd_list  = [f'{cmd_pmset} | python3 printAfter.py --search "{time_str}" | egrep {grep_pmset}',
 		  f'{cmd_syslog} | egrep {grep_syslog}']

comment_list   = [ f"\n\n#################################### {cmd_pmset}",
                   f"\n\n#################################### {cmd_syslog}" ]

print(f"Note: Looking back {hours} hours, from now ({now_str}) back to {time_str}")
print("This can take a few minutes...")

for i, comment in enumerate(comment_list):
    print(comment)
    cmd = full_cmd_list[i]
    print(subprocess.getoutput(cmd))
