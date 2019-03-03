import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'retirement_countdown'
DEPENDENCIES = []

CONF_WRKG_DAYS = 'wrkg_days'
CONF_COMMUTE_MILES = 'commute_miles'
CONF_NEXT_VACATION = 'next_vacation'
CONF_UPDATE_TIME = 'update_time'
DEFAULT_TEXT = 'No text!'

def setup(hass, config):
    """Set up the Hello State component. """
    # Get the text from the configuration. Use DEFAULT_TEXT if no name is provided.
    wrkg_days = config[DOMAIN].get(CONF_WRKG_DAYS, DEFAULT_TEXT)
    commute_miles = config[DOMAIN].get(CONF_COMMUTE_MILES, DEFAULT_TEXT)
    next_vacation = config[DOMAIN].get(CONF_NEXT_VACATION, DEFAULT_TEXT)
    update_time = config[DOMAIN].get(CONF_UPDATE_TIME, DEFAULT_TEXT)

    # States are in the format DOMAIN.OBJECT_ID
    hass.states.set('retirement_countdown.Working_Days', wrkg_days)
    hass.states.set('retirement_countdown.Commute_Miles', commute_miles)
    hass.states.set('retirement_countdown.Next_Vacation', next_vacation)
    hass.states.set('retirement_countdown.Update_Time', update_time)

    return True