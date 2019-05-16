Log of items changed since last commit:

- added second IFTTT key for Kathy ... and duplicated Wyze notifications for her account
- added automation to turn off Wyze notifications when wind speed > 10 mph
- improved comments in "groups.yaml" for the "group.not_home_on" and "group.not_home_random" groups
- added "card-modder.js" custom card from Thomas Love
- added new "epsonworkforce" sensor platform
	- created low ink template sensor ... if any color < 50%, sensor.low_ink state is "on"
	- created conditional card to display ink levels if low_ink sensor is on
- created custom card to display EPSON ink levels in front end
	- created a combination vertical/horizontal stack
	- has a meter that changes color as ink gets low
	- title shows the water drop icon with custom color to match ink

BASEMENT DEHUMIDIFIER ENHANCENTS
- commented dehumidifer (switch.merry_and_bright) out of not_home_on and not_home_random
- created separate input_booleans for ... 
  dehumidifier_active: ... means the dehumidifier switch should be enabled as a dehumidifier
  dehumidifier_scheduling: ... means the switch should turn on/off by a schedule
- updated automations for scheduling and on/off to reference the new booleans
- updated the front end cards with conditions to display cards and schedule controls, 
  depending on whether or not the booleans are on.


CREATED A PRESENCE AUTOMATION DESIGN WHERE ONE AUTOMATION FIRES WHEN THE HOUSE BECOMES EMPTY, AND 
ANOTHER FIRES WHEN IT GOES FROM EMPTY TO OCCUPIED.  ANY CONDITIONS TO BE 
CHECKED "LIVE WITH" THE ACTIONS THAT SHOULD BE DONE (I.E. IN THE SCRIPTS THAT THESE AUTOMATIONS CALL).
- renamed "aws_notify.yaml" automation to "home_all_gone.yaml", 
	- created new "all_gone_scipts.yaml"to make it easier to find scripts that fire when we leave
	- "all_gone_scipts.yaml" now has all the actions to trigger when state changes to nobody home
	- created new action "script.dehumidify_while_gone" within "all_gone_scipts.yaml"
- refactored and renamed "someone_arrived_after_dark.yaml" automation to "home_someone_returns.yaml
	- it is now the automation that calls various scripts to take action upon someone's return 
	  when house was empty 
	- removed the condition to check for after dark (conditions are in script with actions)
	- created someone_returns_scripts to store the return action scripts:
		- return_home_lighting
		- stop_dehumidifying_on_return