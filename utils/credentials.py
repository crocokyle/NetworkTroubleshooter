from abc import ABC

class Credential(ABC):
    def __init__(self, **kwargs):
        self.user = kwargs.get('user', "")
        self.password = kwargs.get('password', "")
        self.api_key = kwargs.get('api_key', "")
        self.mfa_token = kwargs.get('mfa_token', "")

        self.masked = kwargs.get('masked', True)

        if not ((self.user and self.password) or self.api_key or self.mfa_token):
            raise AttributeError(f'Invalid credential kwargs')

    def __str__(self):
        pw = '*'*len(self.password) if self.masked else self.password
        api_key  = '*'*len(self.api_key) if self.masked else self.api_key
        return f"User: {self.user}\nPassword: {pw}\nAPI Key: {api_key}\nMFA Token: {self.mfa_token}"

if __name__ == '__main__':
    test_creds = Credential(user='Kyle', password='Pass123!')
    print(test_creds)

    test_api_key = Credential(api_key='pqi4jr-q2d3qd-dq3ddqd-3dqd3', mfa_token='553426')
    test_api_key.masked = False
    print(test_api_key)
