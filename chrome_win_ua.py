import random
import logging
import time
from functools import lru_cache

# === CONFIGURATION ===
CONFIG = {
    "BROWSER": "Chrome",
    "ALLOWED_OS": [
        "Windows NT 10.0; Win64; x64",              # Windows 10
        "Windows NT 10.0; Win64; x64 (Windows 11)"    # Windows 11 (custom note)
    ],
    "WEBKIT_VERSION": "537.36",
    "CHROME_VERSION_RANGE": {
        "major": (100, 120),
        "build": (4000, 5000),
        "patch": (100, 500)
    }
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
        Simulate a dynamic version update.
        In a real implementation, this method could query an external API or use a maintained library.
        """
        # Simulate network delay
        time.sleep(0.1)
        major = random.randint(*self.config["CHROME_VERSION_RANGE"]["major"])
        build = random.randint(*self.config["CHROME_VERSION_RANGE"]["build"])
        patch = random.randint(*self.config["CHROME_VERSION_RANGE"]["patch"])
        version = f"{major}.0.{build}.{patch}"
        logger.info(f"Dynamic Chrome version obtained: {version}")
        return version

    @lru_cache(maxsize=32)
    def generate_user_agent(self, custom_os=None):
        """
        Generate a user agent string forcing Chrome with allowed Windows OS options.
        Caches results for identical parameters.
        """
        try:
            os_choice = custom_os if custom_os is not None else random.choice(self.config["ALLOWED_OS"])
            if custom_os and custom_os not in self.config["ALLOWED_OS"]:
                error_msg = "Invalid OS specified: must be one of the allowed Windows options."
                logger.error(error_msg)
                raise ValueError(error_msg)

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
    
    # Generate and print a user agent
    ua = generator.generate_user_agent()
    print("Generated User Agent:")
    print(ua)
    
    # === Unit Testing ===
    def test_generate_user_agent():
        ua1 = generator.generate_user_agent()
        assert "Chrome/" in ua1, "User agent should contain Chrome"
        assert "Windows NT" in ua1, "User agent should contain a Windows OS identifier"
        
        # Test using a valid custom OS
        valid_os = CONFIG["ALLOWED_OS"][0]
        ua2 = generator.generate_user_agent(valid_os)
        assert valid_os in ua2, "User agent should use the custom OS provided"
        
        # Test that providing an invalid OS raises a ValueError
        try:
            generator.generate_user_agent("Invalid OS")
            assert False, "A ValueError should be raised for an invalid OS."
        except ValueError:
            pass  # Expected behavior
        
    test_generate_user_agent()
    logger.info("All tests passed!")
