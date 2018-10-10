import urllib3
import certifi
import datetime
import json


class Req(object):
    def __init__(self, api_key, region='kr'):
        self.api_key = api_key
        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                        ca_certs=certifi.where())
        self.region = region

    @staticmethod
    def check_name(name):
        return True

    def api_url(self):
        return 'https://' + self.region + '.api.riotgames.com/'

    def req_get(self, url, **kwargs):
        fields = {'api_key': self.api_key}
        fields.update(kwargs)

        r = self.http.request(
            'GET',
            url=url,
            fields=fields)

        r = json.loads(r.data.decode())
        return r

    def req_by_name(self, name):
        url = self.api_url() + 'lol/summoner/v3/summoners/by-name/' + name
        r = self.req_get(url)
        return r

    def req_by_account(self, account):
        url = self.api_url() + 'lol/summoner/v3/summoners/by-account/' + str(account)
        r = self.req_get(url)
        return r

    def req_match_by_account(self, account, **kwargs):
        url = self.api_url() + 'lol/match/v3/matchlists/by-account/' + str(account)
        r = self.req_get(url, **kwargs)
        return r

    def req_match_by_match_id(self, match_id):
        url = self.api_url() + '/lol/match/v3/matches/' + str(match_id)
        r = self.req_get(url)
        return r

    def req_match_by_name(self, name):
        account_id = self.req_by_name(name)['accountId']
        match_list = self.req_match_by_account(account_id)
        match_id = match_list['matches'][0]['gameId']
        game_info = self.req_match_by_match_id(match_id)

        return game_info

    def req_active_game_by_id(self, summoner_id):
        url = self.api_url() + '/lol/spectator/v3/active-games/by-summoner/' + str(summoner_id)
        r = self.req_get(url)
        return r

    def req_active_game_by_name(self, name):
        summoner_id = self.req_by_name(name)['id']
        game_info = self.req_active_game_by_id(summoner_id)

        return game_info

api_key = 'RGAPI-48a09528-4422-435a-8aa4-723f964e004b'
req = Req(api_key, 'kr')
print(req.req_active_game_by_name('chaser'))
