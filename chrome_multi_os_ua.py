import random
import time
import requests
from functools import lru_cache

# === CONFIGURATION ===
CONFIG = {
    "BROWSER": "Chrome",
    "OS_OPTIONS": {
        "windows": [
            "Windows NT 10.0; Win64; x64",              # Windows 10
            "Windows NT 10.0; Win64; x64 (Windows 11)"  # Windows 11
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
    "CHROME_VERSION_API": "https://versionhistory.googleapis.com/v1/chrome/platforms/win/channels/stable/versions"
}

class UserAgentGenerator:
    def __init__(self, config=None):
        self.config = config or CONFIG
        self._cached_chrome_version = None

    def get_dynamic_chrome_version(self):
        """
        Fetch the latest stable Chrome version from the Google API.
        If the API call fails, generate a fallback version.
        """
        if self._cached_chrome_version:
            return self._cached_chrome_version  # ✅ Use cached version

        try:
            response = requests.get(self.config["CHROME_VERSION_API"], timeout=10)
            response.raise_for_status()
            data = response.json()
            if "versions" in data and len(data["versions"]) > 0:
                self._cached_chrome_version = data["versions"][0]["version"]
                return self._cached_chrome_version
        except:
            pass  # Ignore errors and use fallback

        # Fallback random version
        major = random.randint(100, 120)
        build = random.randint(4000, 5000)
        patch = random.randint(100, 500)
        return f"{major}.0.{build}.{patch}"

    @lru_cache(maxsize=32)
    def generate_user_agent(self, os_type="windows", custom_os=None):
        """
        Generate a Chrome user agent string for a given OS.

        Parameters:
          os_type (str): OS type (e.g., 'windows', 'mac', 'linux', 'android', 'ios'). Default is 'windows'.
          custom_os (str): Custom OS string to override the predefined options.

        Returns:
          str: A user agent string.
        """
        os_choice = custom_os if custom_os else random.choice(self.config["OS_OPTIONS"].get(os_type, ["Windows NT 10.0; Win64; x64"]))
        chrome_version = self.get_dynamic_chrome_version()
        webkit_version = self.config["WEBKIT_VERSION"]

        return (
            f"Mozilla/5.0 ({os_choice}) AppleWebKit/{webkit_version} "
            f"(KHTML, like Gecko) Chrome/{chrome_version} Safari/{webkit_version}"
        )

# === DEMO USAGE ===
if __name__ == "__main__":
    generator = UserAgentGenerator()

    print(generator.generate_user_agent(os_type="windows"))  # Windows User Agent
    print(generator.generate_user_agent(os_type="mac"))      # macOS User Agent
    print(generator.generate_user_agent(os_type="linux"))    # Linux User Agent
    print(generator.generate_user_agent(os_type="ios"))      # iPhone User Agent
    print(generator.generate_user_agent(os_type="android"))  # Android User Agent
