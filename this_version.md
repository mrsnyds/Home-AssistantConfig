Log of items changed since last commit:

- added HTML5 notify component; using it instead of SMS text in WAZE ETA
- refactored and consolidate at_work.yaml, at_church... etc as one automation each, using template to
  alter the action based on state
- refactored garage open reminders to only fire when we are not home, or if it is after dark, 
  because we may have forgotten and need a reminder before going to bed.
- various tweaks to WyzeSense sensor implementation
- various tweaks to Zwave config
- added a ZOOZ 4-in-1 sensor
- updated all_gone scripts to just turn stuff off,
  instead of notify 

