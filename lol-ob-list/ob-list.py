# eocoding:utf-8

from request import Request
from req_exception import ReqException
import os
import json
import datetime


def welcome_info():
    # text-art: http://patorjk.com/software/taag
    print("""
           __  ____       __    __  ____  ____
          /  \(  _ \ ___ (  )  (  )/ ___)(_  _)
         (  O )) _ ((___)/ (_/\ )( \___ \  )(
          \__/(____/     \____/(__)(____/ (__)
          
          """)


def print_with_frame(info, padding=10):
    info = '| ' + info + ' |'
    frame = '-' * (len(info) + padding)
    info = frame + '\n' + info + '\n' + frame
    print(info)


def run_list():
    dict_path = './name-list.json'
    save_smr_path = './active-summoner.txt'
    api_key = 'RGAPI-0f59d20e-4663-40ba-9ea8-484cecd5d35e'
    update_smr_info = False

    with open(dict_path, 'r', encoding='utf-8') as fh:
        name_dict = json.load(fh)
    os.remove(save_smr_path)
    welcome_info()
    for region in name_dict.keys():

        # region host: https://developer.riotgames.com/regional-endpoints.html
        req = Request(api_key, region)
        player_list = sorted(name_dict[region].keys())
        for i, player_name in enumerate(player_list):
            for j, smr_name in enumerate(name_dict[region][player_name]):

                # In python3, all string is unicode object, str don't have decode attribute
                # using ``encode()`` method, str object change to bytes
                # using ``decode()`` method, bytes object turn to str
                # smr_name = smr_name.encode('gb18030').decode('utf-8')
                smr_name_info = '\n=== {0}-{1} --- {2}: {3}'.format(i, j, player_name, smr_name)
                print(smr_name_info, end='')
                try:
                    smr_info = req.req_by_name(smr_name, update_smr_info)
                    if not smr_info:
                        continue
                    account_id = smr_info['accountId']
                    summoner_id = smr_info['id']
                    position_info = req.req_position_by_id(summoner_id)
                    if not position_info:
                        continue
                    position_info = position_info[0]
                    pos_out_info = ' --- {0} {1}: {2}==='.format(
                        position_info['tier'], position_info['rank'], position_info['leaguePoints'])
                    print(pos_out_info)
                    active_game_info = req.req_active_game_by_id(summoner_id)
                    if not active_game_info:
                        match_list = req.req_match_by_account(account_id)
                        last_match_info = match_list['matches'][0]
                        game_time = datetime.datetime.fromtimestamp(int(last_match_info['timestamp']/1000))
                        game_lane = last_match_info['lane']
                        champion_id = last_match_info['champion']
                        champion_info = req.req_champion_by_id(champion_id)
                        out_info = 'Last game: {0}, {1}: {2}'.format(game_time, game_lane, champion_info)
                        print(out_info)
                    else:
                        champion_id = 0
                        for player in active_game_info['participants']:
                            if player['summonerId'] == summoner_id:
                                champion_id = player['championId']
                                break
                        # game_time
                        # game_length = active_game_info['gameLength']
                        # m, s = divmod(game_length, 60)
                        # h, m = divmod(m, 60)
                        # game_time = '%d:%02d:%02d' % (h, m, s)

                        game_time = datetime.datetime.fromtimestamp(int(active_game_info['gameStartTime']/1000))
                        game_time = datetime.datetime.now().replace(microsecond=0) - game_time
                        if game_time.total_seconds() > 3600 * 24:
                            game_time = datetime.timedelta(seconds=0)

                        champion_info = req.req_champion_by_id(champion_id)
                        out_info = 'Live game: {0} champion: {1}'.format(game_time, champion_info)
                        print_with_frame(out_info)
                        with open(save_smr_path, 'a', encoding='utf-8') as fh:
                            fh.write(smr_name_info + pos_out_info + '\n' + out_info + '\n')
                except ReqException as e:
                    print(e.message)


run_list()
