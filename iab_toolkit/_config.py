"""Configuration management for IAB toolkit."""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv, set_key, find_dotenv


class Config:
    """Configuration manager for IAB toolkit."""
    
    def __init__(self):
        self.config_dir = Path.home() / '.iab_toolkit'
        self.config_file = self.config_dir / 'config.json'
        self.env_file = self.config_dir / '.env'
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
        
        # Create .env file if it doesn't exist
        if not self.env_file.exists():
            self.env_file.touch()
        
        # Load environment variables from both system and local .env
        load_dotenv()  # Load system .env first
        load_dotenv(self.env_file)  # Then load user-specific .env
    
    def get_openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key from environment."""
        return os.getenv('OPENAI_API_KEY')
    
    def set_openai_api_key(self, api_key: str) -> None:
        """Set OpenAI API key in user .env file."""
        set_key(str(self.env_file), 'OPENAI_API_KEY', api_key)
        os.environ['OPENAI_API_KEY'] = api_key
    
    def get_config(self) -> Dict[str, Any]:
        """Load configuration from config file."""
        if not self.config_file.exists():
            return {
                'default_max_categories': 3,
                'default_min_score': 0.4,
                'batch_concurrency': 5,
                'output_format': 'text'
            }
        
        with open(self.config_file, 'r') as f:
            return json.load(f)
    
    def set_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to config file."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def update_config(self, **kwargs) -> None:
        """Update specific configuration values."""
        config = self.get_config()
        config.update(kwargs)
        self.set_config(config)


# Global config instance
config = Config()
