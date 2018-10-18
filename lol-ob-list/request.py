# encoding:utf-8
import urllib3
from urllib.parse import urlencode, quote
import certifi
import os
import datetime
import json
from req_exception import ReqException


class Request(object):
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

        try:
            r = self.http.request(
                'GET',
                url=url,
                fields=fields)
            r = json.loads(r.data.decode())
        except urllib3.exceptions.NewConnectionError:
            print('Connection failed.')
            exit()
        except json.decoder.JSONDecodeError:
            raise ReqException('Not message from server.')

        if isinstance(r, dict):
            status = r.get('status')
            if status:
                status_msg = "-- {0} -- , {1}".format(status['status_code'], status['message'])
                raise ReqException(status_msg)
        elif not r:
            raise ReqException('Not message from server.')

        return r

    def req_by_name(self, name, update_info=False):
        """
        :param name: summoner name
        :param update_info: if True, update summoner info json even summoner name in ``info.json``; If False, only
            update info when summoner name not in ``info.json``
        :return: summoner info
        """

        smr_info_path = './database/smr_info.json'
        smr_info_dict = dict()
        if os.path.exists(smr_info_path):
            with open(smr_info_path, 'r', encoding='utf-8') as fh:
                smr_info_dict = json.load(fh)
        smr_info = smr_info_dict.get(name)
        if smr_info and not update_info:
            return smr_info
        else:
            url = self.api_url() + 'lol/summoner/v3/summoners/by-name/' + quote(name)
            try:
                r = self.req_get(url)
                smr_info_dict.update({name: r})
                if os.path.exists(smr_info_path):
                    with open(smr_info_path, 'w', encoding='utf-8') as fh:
                        json.dump(smr_info_dict, fh, indent=4)
                return r
            except ReqException as e:
                print('\nSummoner name: ', e.message)
                return None

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

    def req_active_game_by_id(self, summoner_id):
        try:
            url = self.api_url() + '/lol/spectator/v3/active-games/by-summoner/' + str(summoner_id)
            r = self.req_get(url)
            return r
        except ReqException as e:
            print('Active game: ', e.message)
            return None

    def req_position_by_id(self, summoner_id):
        try:
            url = self.api_url() + '/lol/league/v3/positions/by-summoner/' + str(summoner_id)
            r = self.req_get(url)
            return r
        except ReqException as e:
            print('\nPosition info: ', e.message)
            return None

    @staticmethod
    def req_champion_by_id(champion_id):

        # https://developer.riotgames.com/static-data.html
        # http://ddragon.leagueoflegends.com/cdn/8.19.1/data/zh_CN/champion.json
        champion_path = './database/champion.json'
        champion_info = 'Unkown'

        if os.path.exists(champion_path):
            with open(champion_path, encoding='utf-8', mode='r') as fh:
                champion_dict = json.load(fh)

            for champion_name in champion_dict['data'].keys():
                name_dict = champion_dict['data'][champion_name]
                if int(name_dict['key']) == champion_id:
                    champion_info = '{0}-{1}'.format(name_dict['name'], name_dict['title'])

            return champion_info
        else:
            return champion_info
