from randomuser import RandomUser
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

for user in RandomUser.generate_users(50):
    print(".init(givenName: \"{}\", familyName: \"{}\", emailAddress: \"{}\"),".format(user.get_first_name(), user.get_last_name(), user.get_email()))

