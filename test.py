from chrome_win_ua import UserAgentGenerator

# Create an instance of the generator
generator = UserAgentGenerator()

# Retrieve a user agent string
user_agent = generator.generate_user_agent()
print("Generated User Agent:")
print(user_agent)
