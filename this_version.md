Log of items changed since last commit:

- added delay to onset of family room sunset lights, in 15 minute increments for every
  20% less cloud coverage, starting at 01:30:00 before sunset for 100% cloud cover.
- converted sunset.yaml and sunrise.yaml automations to work on solar angle
- tweaks to DarkSky sensors
- added Skip Commercial script to Garmin groups
- tweaks to switches that switch Roku apps'
- removed 1 second delay from night stand lights automation
- refactored Random Lights completely
	 ... now using an automation to launch two scripts
	 ... those scripts turn a light one with a random delay to turn off,
	     followed by turning on one of two other lights, randomly selected
	 ... sequence ends at 11, when another automation turns the lights out
	 ... alternately, if someone arrives home the sequence ends (as before)