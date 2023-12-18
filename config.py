# env = 'dev'
# env = 'docker'
env = 'test'

if env == 'dev':
    base_path = "/Users/***/Library/**/ai-coustics"
elif env == 'docker':
    base_path = "/backend"
elif env == 'test':
    base_path = "/Users/***/Library/**/ai-coustics"
else:
    base_path = "."

config_audio_path = f"{base_path}/storage"
config_temp_path = f"{base_path}/temp"
config_log_path = f"{base_path}/logs"
config_db_engine = "sqlite"
config_db_connection = {
    "database_url": f"sqlite:///{base_path}/test/test.db"
}

config_token_valid_time = 60 * 12
