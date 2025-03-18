import random
import logging
import time
from functools import lru_cache
import requests  # Make sure requests is installed

# === CONFIGURATION ===
CONFIG = {
    "BROWSER": "Chrome",
    "OS_OPTIONS": {
        "windows": [
            "Windows NT 10.0; Win64; x64",              # Windows 10
            "Windows NT 10.0; Win64; x64 (Windows 11)"    # Windows 11
        ],
        "mac": [
            "Macintosh; Intel Mac OS X 10_15_7",
            "Macintosh; Intel Mac OS X 11_0",
            "Macintosh; Intel Mac OS X 12_0"
        ],
        "linux": [
            "X11; Linux x86_64"
        ],
        "android": [
            "Linux; Android 13; Pixel 7"
        ],
        "ios": [
            "iPhone; CPU iPhone OS 17_0 like Mac OS X"
        ]
    },
    "WEBKIT_VERSION": "537.36",
    "CHROME_VERSION_RANGE": {
        "major": (100, 120),
        "build": (4000, 5000),
        "patch": (100, 500)
    },
    # API endpoint for the latest stable Chrome versions
    "CHROME_VERSION_API": "https://versionhistory.googleapis.com/v1/chrome/platforms/all/channels/stable/versions"
}

# === LOGGING CONFIGURATION ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === USER AGENT GENERATOR MODULE ===
class UserAgentGenerator:
    def __init__(self, config=None):
        self.config = config or CONFIG

    def get_dynamic_chrome_version(self):
        """
        Retrieve the latest stable Chrome version by querying the Google Version History API.
        If the API call fails or returns no version, fall back to a random version.
        """
        url = self.config["CHROME_VERSION_API"]
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if "versions" in data and len(data["versions"]) > 0:
                latest_version = data["versions"][0]["version"]
                logger.info(f"Latest Chrome version obtained from API: {latest_version}")
                return latest_version
            else:
                logger.warning("No versions found in API response, using fallback random version.")
        except Exception as e:
            logger.error(f"Error fetching latest Chrome version from API: {e}")

        # Fallback: generate a random version
        major = random.randint(*self.config["CHROME_VERSION_RANGE"]["major"])
        build = random.randint(*self.config["CHROME_VERSION_RANGE"]["build"])
        patch = random.randint(*self.config["CHROME_VERSION_RANGE"]["patch"])
        fallback_version = f"{major}.0.{build}.{patch}"
        logger.info(f"Using fallback Chrome version: {fallback_version}")
        return fallback_version

    @lru_cache(maxsize=32)
    def generate_user_agent(self, os_type="windows", custom_os=None):
        """
        Generate a Chrome user agent string for the specified OS type.

        Parameters:
          os_type (str): One of the keys in OS_OPTIONS (e.g., 'windows', 'mac', 'linux', 'android', 'ios'). Default is 'windows'.
          custom_os (str): If provided, this custom OS string will be used instead of one randomly chosen from the allowed list.

        Returns:
          str: A user agent string.
        """
        try:
            if custom_os is not None:
                os_choice = custom_os
            else:
                if os_type not in self.config["OS_OPTIONS"]:
                    error_msg = f"Invalid OS type specified: {os_type}. Allowed types: {list(self.config['OS_OPTIONS'].keys())}"
                    logger.error(error_msg)
                    raise ValueError(error_msg)
                os_list = self.config["OS_OPTIONS"][os_type]
                os_choice = random.choice(os_list)

            chrome_version = self.get_dynamic_chrome_version()
            webkit_version = self.config["WEBKIT_VERSION"]

            user_agent = (
                f"Mozilla/5.0 ({os_choice}) AppleWebKit/{webkit_version} "
                f"(KHTML, like Gecko) Chrome/{chrome_version} Safari/{webkit_version}"
            )
            logger.info(f"Generated user agent: {user_agent}")
            return user_agent
        except Exception as e:
            logger.exception("Error generating user agent")
            raise e

# === DEMO USAGE & BASIC UNIT TESTS ===
if __name__ == "__main__":
    generator = UserAgentGenerator()
    
    # Generate and print a user agent for the default OS (Windows)
    ua_windows = generator.generate_user_agent()
    print("Generated User Agent (Windows):")
    print(ua_windows)
    
    # Generate and print a user agent for macOS
    ua_mac = generator.generate_user_agent(os_type="mac")
    print("\nGenerated User Agent (macOS):")
    print(ua_mac)
    
    # Generate and print a user agent for Linux
    ua_linux = generator.generate_user_agent(os_type="linux")
    print("\nGenerated User Agent (Linux):")
    print(ua_linux)
    
    # === Unit Testing ===
    def test_generate_user_agent():
        ua1 = generator.generate_user_agent()
        assert "Chrome/" in ua1, "User agent should contain Chrome"
        assert any(x in ua1 for x in CONFIG["OS_OPTIONS"]["windows"]), "User agent should contain a Windows OS identifier"
        
        ua2 = generator.generate_user_agent(os_type="mac")
        assert any(x in ua2 for x in CONFIG["OS_OPTIONS"]["mac"]), "User agent should contain a macOS identifier"
        
        try:
            generator.generate_user_agent(os_type="invalid_os")
            assert False, "A ValueError should be raised for an invalid OS type."
        except ValueError:
            pass  # Expected behavior
        
    test_generate_user_agent()
    logger.info("All tests passed!")
