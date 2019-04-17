Log of items changed since last commit:

- updated Lambda configuration per the lates HASS release;
  repleaced notify platform with new AWS component and nested lambda notifier
- added Kathy Night Stand to upstairs light group
- improved WAZE ETA flow ... eliminated Lambda posting back to HASS, which sent to IFTTT;
  now Lambda sends the SMS directly using the AWS SNS service.
- modified configuration.yaml to use !include sensors.yaml
- re-purposed switch.merry_and_bright to operate dehumidifiers on a schedule
	- created input_datetime selectors to change on and off times in the front end
	- created an automation to turn on and off, based on input_datetimes'
	- created an automation to validate that "off" time is at least 10 minutes
	  in the future; if not, the automation pushes out the "off" time
	- created input boolean to enable/disable the schedule
	- added a Basement Dehumidifier card to manipulate all of the above in the 
	  front end. 
- added time/date sensors to configuration in sensors.yaml	  
