##This Python Script Service gets called by an automation triggered
##by a webhook ID ...
##
##    id: aws wrkg_days
##    alias: AWS Workign Days Update

### Get data
wrkg_days  = data.get('wrkg_days') + " days"
commute_miles = ('{:,}'.format(round(float(data.get('commute_miles'))))
                + ' miles')
next_vacation  = data.get('next_vacation')
update_time  = data.get('update_time')


## Update states
hass.states.set('retirement_countdown.working_days', wrkg_days)
hass.states.set('retirement_countdown.commute_miles', commute_miles)
hass.states.set('retirement_countdown.next_vacation', next_vacation)
hass.states.set('retirement_countdown.update_time', update_time)
