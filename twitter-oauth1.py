from requests_oauthlib import OAuth1Session
import secrets

client_key = secrets.client_key
client_secret = secrets.client_secret

# get a request token
request_token_url = 'https://api.twitter.com/oauth/request_token'
oauth = OAuth1Session(client_key, client_secret=client_secret)
fetch_response = oauth.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')


# get authorization from user 
base_authorization_url = 'https://api.twitter.com/oauth/authorize'
# authorize_url = base_authorization_url + '?oauth_token='
# authorize_url = authorize_url + resource_owner_key
# print ('Please go here and authorize,', authorize_url)
# verifier = input('Please input the verifier')

authorization_url = oauth.authorization_url(base_authorization_url)
print ('Please go here and authorize,', authorization_url)
verifier = input('Paste the verification code here: ')

access_token_url = 'https://api.twitter.com/oauth/access_token'
oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
oauth_tokens = oauth.fetch_access_token(access_token_url)

resource_owner_key = oauth_tokens.get('oauth_token')
resource_owner_secret = oauth_tokens.get('oauth_token_secret')

print(resource_owner_key, resource_owner_secret)
protected_url = 'https://api.twitter.com/1.1/account/settings.json'

oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret)
r = oauth.get(protected_url)
print (r.text)

protected_url = 'https://api.twitter.com/1.1/search/tweets.json'
params = {'q':'food'}
r = oauth.get(protected_url, params=params)
print (r.text)
