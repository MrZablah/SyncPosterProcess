import pathlib
import yaml
import os

base_dir = pathlib.Path(__file__).parent.parent
config_path = os.getenv('SPP_CONFIG', f'{base_dir}/config.yml')


class Config:

    def __init__(self, script_name):
        self.config_path = config_path
        self.script_name = script_name
        self.load_config()

    def load_config(self):
        # Read config from the YAML file
        with open(self.config_path, "r") as file:
            config = yaml.safe_load(file)

        # Load config into instance variables
        self.global_data = config['global']
        self.script_data = config.get(f'{self.script_name}', {})
        self.run_now = self.global_data.get('run_now', False)  # Use False as default value for run_now if not provided
        self.schedule_hour = self.global_data.get('schedule_hour', 5)  # Use '5' as default schedule_hour if not provided
        self.log_level = self.global_data.get('log_level', 'info').lower()  # Use 'info' as default log level if not provided

        # Global variables
        self.plex_data = self.global_data.get('plex', {})  # Use empty dict if plex data is not found
        self.radarr_data = self.global_data.get('radarr', {})  # Use empty dict if radarr data is not found
        self.sonarr_data = self.global_data.get('sonarr', {})  # Use empty dict if sonarr data is not found
        self.run = self.script_data.get('run', True)  # By default, run the script if not specified

        # Typical variables
        self.dry_run = self.script_data.get('dry_run', False)  # Use False as default value for dry_run if not provided
        self.asset_folders = self.script_data.get('asset_folders', [])  # Use empty list as default value for asset_folders if not provided
        self.radarr = self.script_data.get('radarr', False)  # Use False as default value for radarr if not provided')
        self.sonarr = self.script_data.get('sonarr', False)  # Use False as default value for sonarr if not provided')

        # Plex variables
        self.library_names = self.script_data.get('library_names', [])  # Use empty list as default value for library_names if not provided
        self.ignore_collections = self.script_data.get('ignore_collections', [])  # Use empty list as default value for ignore_collections if not provided

        # Renamer variables
        self.use_plex = self.script_data.get('use_plex', False)  # Use False as default value for use_plex if not provided
        self.source_dir = self.script_data.get('source_dir', '')  # Use empty string as default value for source_dir if not provided
        self.source_overrides = self.script_data.get('source_overrides', [])  # Use empty list as default value for source_override if not provided
        self.destination_dir = self.script_data.get('destination_dir', '')  # Use empty string as default value for destination_dir if not provided
        self.movies_threshold = self.script_data.get('movies_threshold', 0)  # Use 0 as default value for movies_threshold if not provided
        self.series_threshold = self.script_data.get('series_threshold', 0)  # Use 0 as default value for series_threshold if not provided
        self.collection_threshold = self.script_data.get('collection_threshold', 0)  # Use 0 as default value for collection_threshold if not provided
        self.action_type = self.script_data.get('action_type', 'move')  # Use 'move' as default value for action_type if not provided
        self.print_only_renames = self.script_data.get('print_only_renames', False)  # Use False as default value for print_only_renames if not provided

        # sync_gdrive variables
        self.client_id = self.script_data.get('client_id', '')  # Use empty string as default value for client_id if not provided
        self.client_secret = self.script_data.get('client_secret', '')  # Use empty string as default value for client_secret if not provided
        self.sync_location = self.script_data.get('sync_location', '')  # Use empty string as default value for sync_location if not provided
        self.gdrive_id = self.script_data.get('gdrive_id', '1VeeQ_frBFpp6AZLimaJSSr0Qsrl6Tb7z')  # Use empty string as default value for gdrive_id if not provided
        self.token = self.script_data.get('token', {})  # Use empty dict if token data is not found

        # fix_border variables
        self.input_folder = self.script_data.get('input_folder', '')  # Use empty string as default value for input_folder if not provided
        self.output_folder = self.script_data.get('output_folder', '')  # Use empty string as default value for output_folder if not provided
        self.border_color = self.script_data.get('border_color', '#000000')  # Use #000000 as default value for border_color if not provided
        self.resize = self.script_data.get('resize', False)  # Use False as default value for resize if not provided
