##  This script accepts inputs from an automation named Denon Volume Select
##  (denon_volume.yaml).  Denon Volume Select is triggered by a webhook post
##  from one of three IFTTT recipes that capture various formats of Google
##  Assistant voice commands, and send them as json data to be parsed and
##  acted upon ... which is the job of this python script service.
##
##  All recipes post ...
##
##  {"volume_command": "{{TextField}}","direction": "increase/decrease/parse"}
##
##  ...  where "volume_command" is the voice command, and "direction" is a
##  value to indicate if we are turning the volume up, down, or if we must
##  parse the volume command for keywords to figure that out
## 2019-01-12 Added check keyword "remote" to direct command to Denon Remote
## =====================================================

def lower_list(command_wds,count = 0):
    """Changes all 'alpha' list members to lower case"""
    for i in command_wds:
        if i.isalpha():
            command_wds[count] = i.lower()
        count = count + 1

def vol_chg_direction(command_wds, up_cmds, down_cmds):
    """Return volume 'increase' or 'decrease' based keyword match."""
    direction = 'neither'
    up_down = False
    for i in command_wds:
        if i in up_cmds:
            up_down = True
            direction = 'increase'
        if i in down_cmds:
            if up_down:
                direction = 'both'
                #print(' ... both ... ')
                return direction
            else:
                direction = 'decrease'
    if direction == 'both': no_intent("direction = both")
    return direction

def find_chg_value(command_wds):
    """Return command change value if number is found, or '0' if not found"""
    cmd_value = '0'
    for i in command_wds:
        if i.isnumeric():
            cmd_value = i
    return cmd_value

def cmd_intent(command_wds, little_bump, cmd_value, direction, percent_cmds):
    """Return a list with intent of the command for direction, command value,
    increment or set, and % versus value change. """
    value_or_percent = 'value' ## set to 'value' unless % is found
    err_val = ''               ## init' empty error value
    if 'to' in command_wds: val_type = 'set'
    if 'by' in command_wds: val_type = 'increment'
    ## Having a DIRECTION only - without 'to' or 'by' -  means we bump volume
    ## ... so we set val_type to increment and choose a default bump
    ## further down in the script
    if ('to' not in command_wds and
        'by' not in command_wds and
         direction != 'neither'): val_type = 'increment'
    ## Having a VALUE only - without any other intent keywords - will
    ## be interpreted (further down the script) as a **possible** set
    ## if the value is greater than or equal to 15
    if ('to' not in command_wds and
        'by' not in command_wds and
         direction == 'neither'): val_type = 'set'

    for i in command_wds:
        if i in percent_cmds: value_or_percent = '%'

    ## AT THIS POINT WE HAVE DIRECTION, VALUE, INCREMENT/SET, and val/% ...
    ## which is everything we need to establish intent, or no_intent

    ## Exit for "no_intent" results

        ## "SET" without value is a failure to establish intent
    if val_type == 'set' and cmd_value == '0':
        err_val = ('Need a number. Try "Increase/Decrease TV volume by 5%."'+
                   '  Or "Set TV volume to" with a number [15 - 68')
       ## Only have a value ... above 15, assume SET, less than 15, assume error
    if (val_type == 'set' and cmd_value != '0' and direction == 'neither'
       and float(cmd_value) < 15):
        err_val = ('??? Try "Increase/Decrease TV volume by 5%."'+
                   '  Or "Set TV volume to" with a number [15 - 68')
        ## We HAVE INCREMENT WITH NO COMMAND VALUE or DIRECTION ...
    if val_type == 'increment' and cmd_value == '0' and direction == 'neither':
        err_val = ('How much? Try "Increase/Decrease TV volume by 5%."'+
                   '  Or "Set TV volume to" with a number [15 - 68')

    ## Evaluate special case of only direction, and determine size of bump
    ## CASE EXAMPLE cmd_wds = ['up'] or ['down'] or ['down', 'a', 'bit' ]
    if val_type == 'increment' and cmd_value == '0' and direction != 'neither':
        cmd_value = '5'          ## default increment value
        for i in command_wds:
            if i in little_bump: cmd_value = '2' ## ... for small increment

    ## We cannot handle SET values greater than 99
    #if (float(cmd_value) > 99 and vol_params[3] == 'value'):
    if float(cmd_value) > 99:
        err_val = ('Too high! Try "Increase/Decrease TV volume by 5%."'+
                   '  Or "Set TV volume to" with a number [15 - 68].')

    return direction, val_type, cmd_value, value_or_percent, err_val

def calc_vol(vol_params, current_volume, min_max, cmd_value):
    """Given vol_params tuple, interpret intent values for direction,
    val_type, cmd_value, and value/percent, return volume_set"""
    volume_set = 0
    ##Set increment_direction multiple to -1 if direction is decrease
    if vol_params[0] == 'increase': increment_direction = 1
    else: increment_direction = -1
    if vol_params[3] == '%':
        if vol_params[1] == 'increment':
            volume_set = str((float(current_volume) +
            float(current_volume) *
            (float(vol_params[2])/100)*increment_direction)) + '000'
        else: volume_set = str(float(min_max[1])*float(vol_params[2])/100)+'000'
    if vol_params[3] == 'value':
        if vol_params[1] == 'increment':
            volume_set = str(float(current_volume) + float(vol_params[2])/100
            *increment_direction) + '000'
        if vol_params[1] == 'set':
            volume_set = str(float(cmd_value)/100) + "000"
    ##Convert string to required Denon format, ends in '0' or '5',
    ## and ensure set value within min_max values
    if float(volume_set[4]) <= 2: volume_set = volume_set[:4] + '0'
    elif float(volume_set[4]) <= 7: volume_set = volume_set[:4] + '5'
    else: volume_set = '0.' + str(int(volume_set[2:4]) + 1) + '0'
    if float(volume_set) < float(min_max[0]): volume_set = min_max[0]
    if float(volume_set) > float(min_max[1]): volume_set = min_max[1]
    return volume_set

#=============================================================================
#=============================================================================
## Program starts here

## keyword lists
up_cmds = ["up", "louder","increase"]
down_cmds = ["down", "softer", "quieter", "decrease"]
percent_cmds = ["%", "percent", "per", "cent"]
little_bump = ["little", "smidge", "tad", "bit", "hair", "small"]
## initialize values
new_volume = '0.225'    ##initialize some low default valume
cmd_value = '0 '        ##initialize increment value
val_type = ''           ##initialize value type as set or increment
up_down = False         ## init' flag for increase/decrease keyword found
value_or_percent = ''   ## init' indicator of value or percent command
min_max = ['0.050', '0.680'] ## first value is min, second is max

##Get the inputs
volume_command = data.get('volume_command')
direction = data.get('direction')

##PREPARE COMMAND WORDS LIST FOR EVALUATION
command_wds = volume_command.split()
lower_list(command_wds) ##makes all alpha members lower case

##DETERMINE ENTITY ID AND GET CURRENT VOLUME ... DEFAULTS TO denon_main
entity_id = 'media_player.denon_main'
if 'remote' in command_wds: entity_id = 'media_player.denon_remote'
states = hass.states.get(entity_id)
current_volume = states.attributes.get('volume_level') or '0.150'

##DETERMINE DIRECTION INTENT for INCREASE OR DECREASE
if direction == 'parse':
    direction = vol_chg_direction(command_wds, up_cmds, down_cmds)

## DETERMINE NUMERIC VALUE FOR VOLUME CHANGE (IF SPECIFIED ... COULD BE '0')
cmd_value = find_chg_value(command_wds)

## FINISH CONSTRUCTING INTENT TUPLE FOR CALCULATION
## FUNCTION WILL EXIT IF NO INTENT CAN BE ESTABLISHED, OR INVALID VALUE
vol_params = cmd_intent(command_wds, little_bump, cmd_value,
                        direction, percent_cmds)

## DO CALCULATION AND SET VOLUME
## But first check for err_val at vol_params[4]
if vol_params[4] != '':
    volume_set = "volume will not change"
    ## NEXT 2 LINES NO LONGER NEEDED ... LG TV NOT USED WITH THIS SCRIPT
    ## data = { "message" : vol_params[4] }
    ## hass.services.call('notify', 'lg_tv', data)
else:
    volume_set = calc_vol(vol_params, current_volume, min_max, cmd_value)
    data = { "entity_id" : entity_id, "volume_level" : volume_set }
    hass.services.call('media_player', 'volume_set', data)


##TEST/DEBUG
##
##logger.warning("Command: {3},  Entity: {0}, New Volume: {1}, Parameters: {2}"
##              .format(entity_id,volume_set, vol_params, volume_command))


##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
## Refactoring idea ... this will somewhat mitigate the namespace issue in hass
## 1.) create empyt list for vol_params, then append with each keyword evaluation
##     function, arriving at a finished "list"
##     The idea is that each keyword evaluation function only does it's piece,
##     and returns a new, or modified piece of intent information.
## 2.) Then modify the calculation function to operate on the list and return
##     volume_set based on that.
