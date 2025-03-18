# ChromeMultiOSUA

ChromeMultiOSUA is a flexible Python module designed to generate realistic Google Chrome user agent strings for multiple operating systems, including Windows, macOS, Linux, Android, and iOS. The module retrieves the latest stable Chrome version from the official Google Version History API. It features configurable settings, robust logging and error handling, caching, and basic unit tests—all encapsulated in a modular, easy-to-integrate class.

## Features

- **Cross-Platform Support:**  
  Generate Chrome user agents for various operating systems:
  - **Windows:** Windows 10 & Windows 11
  - **macOS**
  - **Linux**
  - **Android**
  - **iOS**

- **Latest Chrome Version Retrieval:**  
  Queries the official Google Version History API to get the latest stable Chrome version. Falls back to a randomly generated version if the API call fails.

- **Configurable Settings:**  
  Easily adjust allowed OS options, version ranges, and other settings through a centralized configuration dictionary.

- **Robust Logging & Error Handling:**  
  Utilizes Python's built-in logging module to capture key events and errors.

- **Caching:**  
  Caches user agents for repeated requests using Python's LRU cache decorator.

- **Modular & Extensible:**  
  Encapsulated in a single class (`UserAgentGenerator`) for easy import and extension in other projects.

- **Basic Unit Testing:**  
  Includes simple unit tests to ensure the generator produces valid user agent strings.

## Installation

Clone this repository or download the module files:

```bash
git clone https://github.com/Sheekovic/ChromeMultiOSUA.git
```

Then, navigate into the directory:

```bash
cd chrome-multi-os-ua
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

*Note:* This module requires Python 3.6 or later.

## Usage

Integrate the module into your project as follows:

```python
from chrome_multi_os_ua import UserAgentGenerator

# Create an instance of the generator
generator = UserAgentGenerator()

# Retrieve a user agent string for Windows (default)
user_agent_windows = generator.generate_user_agent()
print("Windows User Agent:", user_agent_windows)

# Retrieve a user agent string for macOS
user_agent_mac = generator.generate_user_agent(os_type="mac")
print("macOS User Agent:", user_agent_mac)

# Retrieve a user agent string for Linux
user_agent_linux = generator.generate_user_agent(os_type="linux")
print("Linux User Agent:", user_agent_linux)
```

For custom OS strings, provide a custom OS string directly:

```python
custom_os = "Custom OS String"
user_agent_custom = generator.generate_user_agent(custom_os=custom_os)
print("Custom OS User Agent:", user_agent_custom)
```

## Configuration

The module's configuration is defined in the `CONFIG` dictionary, including:

- **OS_OPTIONS:**  
  A dictionary mapping OS types (`windows`, `mac`, `linux`, `android`, `ios`) to lists of allowed OS strings.

- **WEBKIT_VERSION:**  
  The fixed WebKit version used in the user agent string.

- **CHROME_VERSION_RANGE:**  
  Defines the range for Chrome version components (major, build, and patch numbers). This is used only as a fallback if the API call fails.

- **CHROME_VERSION_API:**  
  The URL used to query the latest stable Chrome version.

Feel free to modify these settings to suit your needs.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for any bugs, feature requests, or enhancements.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## Acknowledgements

This module was inspired by the need for realistic user agent generation in web scraping and automation projects and is built to be flexible and easily integrated into various applications.

With this update, your module now actively fetches the latest stable Chrome version from the Google Version History API. This provides more accurate and current user agent strings for your applications.