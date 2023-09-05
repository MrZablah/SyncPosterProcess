<div align="center">

# SyncPosterProcess

This is a simple script that is meant to used with the provided Dockerfile or the docker container on the [Docker Hub](https://hub.docker.com/r/mrzablah/spp) or [GHCR](https://github.com/MrZablah/SyncPosterProcess/pkgs/container/spp).

</div>

---

# Special thanks to:

> This script was made possible thanks to the following projects:

- [MM2k-BORDER-REPLACER](https://github.com/listentofaze/mm2k-border-replacer/tree/main)
- [Drazzilb08 User Scripts](https://github.com/Drazzilb08/userScripts)
- [Stupifier Script provided in Discord](https://discord.com/channels/492590071455940612/1124032073557086258/1126226814629576858)
- [TCM](https://github.com/CollinHeist/TitleCardMaker)

Thanks for the great work you guys have done! it's really appreciated!

---

# What is this?

This is an all-in-one solution for the following scripts:
- [Stupifier Script provided in Discord](https://discord.com/channels/492590071455940612/1124032073557086258/1126226814629576858)
This is script will sync a directory with a Google Drive folder. 
- [Drazzilb08 User Scripts](https://github.com/Drazzilb08/userScripts)
This script will fix naming of the images base on the naming you have on arr apps.
- [MM2k-BORDER-REPLACER](https://github.com/listentofaze/mm2k-border-replacer/tree/main)
This script will replace or removed the borders of the images.

# How to use it?

The recommend use of the script is to use the docker container provided in the 
[Docker Hub](https://hub.docker.com/r/mrzablah/spp) or [GHCR](https://github.com/MrZablah/SyncPosterProcess/pkgs/container/spp)
and configure it as explain below, but you can also use the script directly.

# Docker
They are several ways to run the docker container, but the recommend way is to use the following command:
```bash
docker run -d \
    --name spp \
    -v /path/to/config:/config \
    -v /path/to/data:/data \
    -e TZ=America/Monterrey \
    mrzablah/spp:latest
```
Keep in mind that you need to change the TZ variable to your timezone so you can se the schedule correctly,
and the volumes to the path you want to use.

# Configuration file
The config file is where you will change all the settings for any of the scripts.

## Global
The first part to change is the global section:
```yaml
global:
  run_now: true # If true it will run the script immediately, if false it will wait until the schedule_hour
  schedule_hour: 4 # This is the hour of the day you want the script to run, it's based on a 24 hour clock and defaults to 4am
  log_level: info # log_level can be: debug, info, warning, error, critical
  radarr:
    # name is the name of the radarr instance, this is used to reference the instance in other scripts
    - name: radarr_1
      # api is the api key for the radarr instance
      api: abcdefghijlmnop
      # url is the url for the radarr instance
      url: http://localhost:7878
    - name: radarr_2
      api: abcdefghijklmnop
      url: http://localhost:1212
  sonarr:
    # name is the name of the sonarr instance, this is used to reference the instance in other scripts
    - name: sonarr_1
      # api is the api key for the sonarr instance
      api: abcdefghijlmnop
      # url is the url for the sonarr instance
      url: http://localhost:8989
    # name is the name of the second sonarr instance, this is used to reference the instance in other scripts, names must match
    - name: sonarr_2
      api: abcdefghijlmnop
      url: http://localhost:9090
  plex:
    # name is the name of the plex instance, this is used to reference the instance in other scripts
    - name: plex
      # api is the token key for the plex instance, if you don't know your token please see https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
      api: abcdefghijlmnop
      # url is the url for the plex instance
      url: http://localhost:32400
```

## Sync Google Drive
There are sections for each of script,
you can enable or disable any of the script with the `run` variable.

1. Get rclone client ID and Secret following these [instructions](https://rclone.org/drive/#making-your-own-client-id)
2. Then get a token following these [instructions](https://rclone.org/remote_setup/)

> Alternative use Google Cloud Service Account instead of token:
- Creating and using this option will make it, so you don't need to create the token manually but I will still strongly
  recommend to still add the Client ID and Client Secret and just change the token to SA, otherwise you might reach some limits.

> Instructions for creating a Google Cloud Service Account
1. To create a service account and obtain its credentials, go to the [Google Developer Console](https://console.developers.google.com/).
2. You must have a project - create one if you don't.
3. Then go to "IAM & admin" -> "Service Accounts".
4. Use the "Create Service Account" button. Fill in "Service account name" and "Service account ID" with something that identifies your client.
5. Select "Create And Continue". Step 2 and 3 are optional.
6. Once created you will need to go to the Actions of the SA -> Manage Keys and create a JSON key and saved it as a file.
7. These credentials are what rclone will use for authentication. If you ever need to remove access, press the "Delete service account key" button.

```yaml
sync_gdrive:
  run: true # If false it will skip this step
  client_id: asdasds.apps.googleusercontent.com # Client ID for rclone usually ends with .apps.googleusercontent.com
  client_secret: GOCSPX-asda123 # Client Secret for rclone, usually starts with GOCSPX-
  sync_location: /data/input # Where you want to sync the posters to
  gdrive_id: 1VeeQ_frBFpp6AZLimaJSSr0Qsrl6Tb7z # The ID of the folder you want to sync from
  token: # The token for rclone, this is the output of rclone config dump that needs to run manually, it's not needed if you have a service account
  # Token looks like this: { "access_token": "value", "token_type": "Bearer", "refresh_token": "value", "expiry": "value" }
  gdrive_sa_location: /config/rclone_sa.json # The location of your rclone service account file (JSON), id this is added token will be ignored
```

## Renamer
```yaml
renamer:
  run: true # If false it will skip this step
  # Options are 'true' or 'false'
  dry_run: true # dry_run can be true or false, if true it will not actually rename anything
  asset_folders: false
  # Options are 'copy' or 'move'
  action_type: copy
  print_only_renames: false # If print_only_renames is True, then we don't want to print files that don't need to be renamed
  # Library names are used to match collections posters to the collections listed w/in Plex. Typically Movie Libraries are used
  library_names:
    - Movies
    - TV Shows
    - Anime Movies
  # Where your ingest movies folder is (THe source and destination should not be the same directory)
  source_dir: /path/to/posters/ <--- Lowest priority
  # What posters you'd like to override the souce dir with. This dir will take priority for assets over source_dir
  # To not use any override, simply leave it blank or remove it from the config
  # Can be a single dir or a list of dirs
  source_overrides:
    - /path/to/posters/override/ <--- Middle priority
    - /path/to/posters/override2/ <--- Highest priority
  # Where your posters are going to go. In my usecase I use Plex-Meta-Manager. This is the /config/assets dir for PMM for me.
  destination_dir: /path/to/poster/destination
  # The thresholds are used to consider what is a "Match", As with any automation there is never a 100% guarantee of accuracy. There will be times the script will mess up.
  # If however you see it messing up more often on things you can restrict the threshold.
  # 0 = Anything goes, 100 = Must be exact match
  # The default numbers here are based upon what I've seen to be the most effective, I've had one-offs where I had to manually fix things.
  # Eg. Hanna vs Anna, One letter difference and in the case I had the years were the same too.
  movies_threshold: 96
  series_threshold: 96
  collection_threshold: 99
  # Decide which radarr instance you will be using for renamer, this is useful if you have for example: A Sonarr/Sonarr-Anime and/or Radarr/Radarr-Anime
  # If you however duplicate entries between a Radarr/Radarr4K for example. this won't help and will only double the work for the script for no gain.
  radarr:
    - name: radarr_1
  sonarr:
    - name: sonarr_1
    - name: sonarr_2
```

## Border Replacer
```yaml
fix_border:
  run: true # If false it will skip this step
  input_folder: /data/input # Where your posters are going to be coming from
  output_folder: /data/fix_posters # Where your posters are going to go
  border_color: none # This will remove the border of the image, but you can also add a color to change th border to any hex color, Ej: '#000000'
  overwrite_existing: true # If true it will overwrite the existing poster, if false it will skip the poster
  resize: false # If true it will resize the poster to 1000x1500, this requires border_color to be set to a 'none'
  bottom_only: false # If true it will only keep the bottom border, this requires border_color to be set to a color Ej: '#000000'
```


