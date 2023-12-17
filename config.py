# env = 'dev'
# env = 'docker'
env = 'test'

if env == 'dev':
    config_audio_path = "/Users/andysun/Library/CloudStorage/OneDrive-Personal/Code/Python/ai-coustics/storage"
    config_temp_path = "/Users/andysun/Library/CloudStorage/OneDrive-Personal/Code/Python/ai-coustics/temp"
    config_log_path = "/Users/andysun/Library/CloudStorage/OneDrive-Personal/Code/Python/ai-coustics/logs"
    config_db_engine = "sqlite"
    config_db_connection = {
        "database_url": "sqlite:///audio.db"
    }
elif env == 'docker':
    config_audio_path = "/backend/storage"
    config_temp_path = "/backend/temp"
    config_log_path = "/backend/logs"
    config_db_engine = "sqlite"
    config_db_connection = {
        "database_url": "sqlite:////backend/audio.db"
    }
elif env == 'test':
    config_audio_path = "/Users/andysun/Library/CloudStorage/OneDrive-Personal/Code/Python/ai-coustics/storage"
    config_temp_path = "/Users/andysun/Library/CloudStorage/OneDrive-Personal/Code/Python/ai-coustics/temp"
    config_log_path = "/Users/andysun/Library/CloudStorage/OneDrive-Personal/Code/Python/ai-coustics/logs"
    config_db_engine = "sqlite"
    config_db_connection = {
        "database_url": "sqlite://///Users/andysun/Library/CloudStorage/OneDrive-Personal/Code/Python/ai-coustics/test/test.db"
    }
else:
    config_audio_path = "./storage"
    config_temp_path = "./temp"
    config_log_path = "./logs"
    config_db_engine = "sqlite"
    config_db_connection = {
        "database_url": "sqlite:///./audio.db"
    }

config_token_valid_time = 60 * 12
