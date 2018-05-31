import flickr_api

a = flickr_api.auth.AuthHandler()
perms = 'write'
url = a.get_authorization_url(perms)
print('Open in a browser: ' + url)
verifier = input('Oauth verifier >> ')
a.set_verifier(verifier)
a.save('auth_handler.key')
