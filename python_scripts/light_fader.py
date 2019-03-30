
## INPUTS
entity_id  = data.get('entity_id')
states = hass.states.get(entity_id)
current_level = states.attributes.get('brightness') or 0
current_level_pct = current_level/2.55 or 0     # start_level_pct is optional
start_level_pct = int(data.get('start_level_pct', current_level_pct ))
end_level_pct = int(data.get('end_level_pct'))
transition = data.get('transition')

## CALCULATE PARAMETERS FOR LOOP, BASED ON TRANSITION TIME FOR FADE
transition_secs = (int(transition[:2])*3600 + int(transition[3:5])*60
                   + int(transition[-2:]))    # convert string to total secs'


# We change brightness 1% every 'sleep_delay' seconds
step_pct  = 1
sleep_delay = abs(transition_secs/(end_level_pct - start_level_pct))

# If fading out the step_pct will be negative (decrement each iteration)
if end_level_pct < start_level_pct: step_pct = step_pct * -1


## DOES THE WORK ...

# Since we check for equality of new_level_pct and current_level_pct
# in each loop -  and break if !=, we must initialize new_level_pct
# to equal start_level_pct, and then set actual light brightness_pct
# (a.k.a. current_level_pct) to equal start_level_pct.
new_level_pct = start_level_pct
data = { "entity_id" : entity_id, "brightness_pct" : round(start_level_pct) }
hass.services.call('light', 'turn_on', data)
time.sleep(1)  # without delay,'hass.states.get' would not get the new value

while round(new_level_pct) != end_level_pct :     ## until we get to new level
    states = hass.states.get(entity_id)           ##  acquire status of entity
    current_level = states.attributes.get('brightness') or 0
    current_level_pct = current_level/2.55 or 0
    if (round(current_level_pct) != round(new_level_pct)):
        logger.info('Exiting Fade In')                ## this indicates manual
        break;                                        ## intervention, so exit
    else :
        new_level_pct = new_level_pct + step_pct
        logger.info('Setting brightness of ' + str(entity_id) + ' from '
          + str(current_level_pct) + ' to ' + str(new_level_pct))
        data = { "entity_id" : entity_id,
                "brightness_pct" : round(new_level_pct) }
        hass.services.call('light', 'turn_on', data)
        time.sleep(sleep_delay)


##  Some test json input for Services in Developer tools
##{
##  "entity_id": "light.living_room_pepe",
##  "start_level_pct": "0",
##  "end_level_pct": "100",
##  "transition": "00:00:19"
##}


