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

# Retrieve a user agent string for a iPhone
user_agent_iphone = generator.generate_user_agent(custom_os="iPhone")
print("iPhone User Agent:", user_agent_iphone)

# Retrieve a user agent string for a Android device
user_agent_android = generator.generate_user_agent(custom_os="Android")
print("Android User Agent:", user_agent_android)