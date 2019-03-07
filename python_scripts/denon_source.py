## 2019-03-03 Added pattern to select "Blu-ray"

##This Python Script Service gets called by an automation triggered
##by a webhook ID from IFTTT recipe to change the source on the Denon Recvr.
##
##id: denon select source
##alias: Denon Select Source

## Possible source list:
##    AUX1,Apple TV,Blu-ray,Bluetooth,CHROME AUDIO,Chromecast,Favorites,
##    Flickr,HA,Internet Radio,Media Server,Online Music,Pandora,Phono,Roku,
##    SiriusXM,Sony TV,Spotify,Tuner,iPOD,iPod/USB

## Set defaults
entity_id = "media_player.denon_main"
source = "Roku"
zone = "main"

## data from automation, as passed from IFTTT
source = data.get('source')
source_command = (source.lower()).split()

## Set source based on how someone might ask for Denon source
if "roku" in source_command:
    source = "Roku"
elif "chrome" in source_command:
    source = "CHROME AUDIO"
elif "chromecast" in source_command:
    source = "Chromecast"
elif "tv" in source_command:
    source = "Sony TV"
elif "blu" in source_command:
    source = "Blu-ray"
else:
    source = "Roku"

## Now determine entity_id to use, based on whether Denon "Main" or "Remote"
if "main" in source_command:
    entity_id = "media_player.denon_main"
elif "remote" in source_command:
    entity_id = "media_player.denon_remote"
else:
    entity_id = "media_player.denon_main"

## then call the media_player.select_source service
service_data = {'entity_id': entity_id, 'source': source }
hass.services.call('media_player', 'select_source', service_data, False)

