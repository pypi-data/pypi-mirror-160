import pymongo
import random
from typing import Dict, List, Tuple
from datetime import datetime as dt
from .exceptions import InsufficientFundsException, InsufficientItemsException, ItemNotFoundException, NoActiveCharacterException, PlayerNotFoundException
from .pipelines import *
from pymongo import MongoClient
from pymongo.client_session import ClientSession
from werkzeug.security import generate_password_hash, check_password_hash

class MSTable:

    def __init__(self):
        self.tier_table = [1]*20 + [2]*40 + [3]*85 + [4]*105 + [5]
        self.level_table = [1]*2 + [2]*4 + [3]*6 + [4]*8 + [5]*10 + [6]*10 + [7]*10 + [8]*10 + [9]*20 + \
                            [10]*20 + [11]*20 + [12]*25 + [13]*25 + [14]*25 + [15]*25 + [16]*30 + [17]*30 + [18]*30 + [19]*40 + [20]
        self.ms_level = [0, 2, 6, 12, 20, 30, 40, 50, 60, 80, 100, 120, 145, 170, 195, 220, 250, 280, 310]
        self.tier_ms_mod = [1.0, 0.8, 1.0, 1.2, 1.5]

    def __getitem__(self, key):
        key = int(key)
        if key <=250:
            return self.tier_table[key], self.level_table[key]
        elif key <=350:
            return self.tier_table[250], self.level_table[key]
        return self.tier_table[250], self.level_table[350]

    def get_ms_level(self, level):
        return self.ms_level[level-1]

    def get_tier_ms_mod(self, tier):
        return self.tier_ms_mod[tier-1]

class Calendar:

    def __init__(self):
        self.calendar = []
        self.starting_year = 104
        self.total_days = 305
        for i in range(1, 52):
            self.calendar.append(("Sieliah", "Inverno", i))
        for i in range(1, 52):
            self.calendar.append(("Maha", "Primavera", i))
        for i in range(1, 52):
            self.calendar.append(("Aniyah", "Estate", i))
        for i in range(1, 52):
            self.calendar.append(("Halyr", "Estate", i))
        for i in range(1, 52):
            self.calendar.append(("Hamyer", "Autunno", i))
        for i in range(1, 51):
            self.calendar.append(("Tariah", "Inverno", i))

    def __getitem__(self, key):
        current_year = self.starting_year + key//self.total_days
        current_day = self.calendar[key%self.total_days]
        return current_year, current_day[0], current_day[1], current_day[2]

class WaghamDB:
    
    def __init__(self, config, tier_rewards):     
        self.client: MongoClient = MongoClient("mongodb://{}:{}@{}:{}/wagham".format(config["DATABASE"]["user"],
                                                        config["DATABASE"]["pwd"],
                                                        config["DATABASE"]["ip"],
                                                        config["DATABASE"]["port"]))
        self.ptx = self.client.get_database()
        self.calendar = Calendar()
        self.mstable = MSTable()
        self.tier_rewards = tier_rewards

    def get_db(self):
        '''
        This funtion returns the pointer to the database
        '''
        return self.ptx

    def set_master_ms(self, only_active=True):
        '''
        Calculates the MS for each master based on the sessions in the database
        '''
        if only_active:
            filter = {"status": "active"}
        else:
            filter = {}
        cursor = self.ptx.characters.find(filter, {'_id': 1})
        # For each character
        for doc in cursor:  
            # Find the session it mastered
            sessions = self.ptx.sessions.count_documents({"master": doc['_id']})
            # Update the document
            self.ptx.characters.update_one({'_id': doc['_id']}, 
                                            {'$set': {'masterMS': sessions}})

    def set_session_ms(self, only_active=True):
        '''
        Calculates the MS gained in the sessions/PBV for all the characters
        '''
        if only_active:
            filter = {"status": "active"}
        else:
            filter = {}
        cursor = self.ptx.characters.find(filter, {'_id': 1})
        # For each character in the collection
        for doc in cursor:
            # Sum the MS gained in the sessions
            res = list(self.ptx.sessions.aggregate(pipeline=get_sum_pipeline(doc['_id'])))
            # len(res) is 0 if there are no sessions
            if len(res) == 0:
                total_ms = 0
            else:
                total_ms = res[0]["sum"]
            # Update the document
            self.ptx.characters.update_one({'_id': doc['_id']}, 
                                            {'$set': {'sessionMS': total_ms}})

    def set_pbc_ms(self, only_active=True):
        '''
        Calculates the MS gained in the PBCs for all the characters
        '''
        if only_active:
            filter = {"status": "active"}
        else:
            filter = {}
        cursor = self.ptx.characters.find(filter, {'_id': 1})
        # For each character in the collection
        for doc in cursor:
            # Sum the MS gained in the PBCs
            res = list(self.ptx.PBX.aggregate(pipeline=get_sum_pipeline(doc['_id'])))
            # len(res) is 0 if there are no PBCs
            if len(res) == 0:
                total_ms = 0
            else:
                total_ms = res[0]["sum"]
            # Update the document
            self.ptx.characters.update_one({'_id': doc['_id']}, 
                                            {'$set': {'PBCMS': total_ms}})

    def set_errata_ms(self, only_active=True):
        '''
        Calculates the MS adjustments for all the characters
        '''
        if only_active:
            filter = {"status": "active"}
        else:
            filter = {}
        cursor = self.ptx.characters.find(filter, {'_id': 1, 'errata': 1})
        # For each character in the collection
        for doc in cursor:
            total_ms = 0
            # Sums the MS adjustements in the errata
            for e in doc["errata"]:
                total_ms += e["ms"]
            # Update the document
            self.ptx.characters.update_one({'_id': doc['_id']}, 
                                {'$set': {'errataMS': total_ms}})

    def set_reputation(self, only_active=True):
        '''
        Updates the reputation of all the characters
        '''
        if only_active:
            filter = {"status": "active"}
        else:
            filter = {}
        cursor = self.ptx.characters.find(filter, {'_id': 1, 'errata': 1, 'territory': 1})
        # For each character in the collection
        for doc in cursor:
            if doc["territory"] is None:
                reputation = self.ptx.reputation.find_one({"_id": "reputation"})["unknown"]
            else:
                reputation = self.ptx.reputation.find_one({"_id": "reputation"})[doc["territory"]]
            # Sum all the reputation adjustments in the errata
            for e in doc["errata"]:
                for race, rep_adj in e["reputationAdjustment"].items():
                    reputation[race] += rep_adj
            # Sums all the reputation adjustments in the sessions' results
            res = self.ptx.sessions.aggregate(pipeline=get_reputation_pipeline(doc['_id']))
            for session in res:
                for race, rep_adj in session["characters"][0]["reputationAdjustment"].items():
                    reputation[race] += rep_adj
            # Sums all the reputation adjustments in the PBC/PBV results
            res = self.ptx.PBX.aggregate(pipeline=get_reputation_pipeline(doc['_id']))
            for session in res:
                for race, rep_adj in session["characters"][0]["reputationAdjustment"].items():
                    reputation[race] += rep_adj
            # Update the document
            self.ptx.characters.update_one({'_id': doc['_id']}, 
                                        {'$set': {'reputation': reputation}})
    
    def set_last_activity(self, only_active=True):
        '''
        Update the last master/player activity for all the characters
        '''
        if only_active:
            filter = {"status": "active"}
        else:
            filter = {}
        cursor = self.ptx.characters.find(filter, {'_id': 1})
        # For each character in the collection
        for doc in cursor:
            # Get the last session mastered
            last_master = list(self.ptx.sessions.aggregate(pipeline=get_last_mastered_pipeline(doc['_id'])))
            # len(last_master) is 0 if the character mastered no session
            if len(last_master) == 0:
                ret_master = None
            else:
                ret_master = last_master[0]["lastDate"]
            # Gets the last session played
            last_played_session = list(self.ptx.sessions.aggregate(pipeline=get_last_played_pipeline(doc['_id'])))
            # Gets the last PBC/PBV played
            last_played_pbx = list(self.ptx.sessions.aggregate(pipeline=get_last_played_pipeline(doc['_id'])))
            # len(last_played) is 0 if the character played no session
            if len(last_played_session) == 0 and len(last_played_pbx) == 0:
                ret_player = None
            elif len(last_played_session) == 0:
                ret_player = last_played_pbx[0]["lastDate"]
            elif len(last_played_pbx) == 0:
                ret_player = last_played_session[0]["lastDate"]
            else:
                ret_player = max(last_played_session[0]["lastDate"], last_played_pbx[0]["lastDate"])
            # Update the document
            self.ptx.characters.update_one({'_id': doc['_id']}, 
                                    {'$set': {'lastPlayed': ret_player, 'lastMastered': ret_master}})         

    def get_total_days(self, starting_date=dt(2020, 4, 27)):
        '''
        Returns the total number of in-game days, from a starting_date to today
        :param starting_date: the starting date (default 27/4/2020, beginning of the server)
        '''
        pipe_results = list(self.ptx.sessions.aggregate(pipeline=get_days_pipeline(starting_date)))
        if len(pipe_results) == 0:
            raw_days = 0
        else:
            raw_days = pipe_results[0]["days"]
        return int(raw_days + (dt.today() - starting_date).days - 1)

    def get_inactivity_days(self, character=None, player=None):
        '''
        Calculates the inactivity days of a character as master and player
        :param character: the character name
        :param player: the player id
        '''
        if character is not None:
            res = self.ptx.characters.find_one({'_id': character})
        elif player is not None:
            res = self.ptx.characters.find_one({'player': player, 'status': 'active'})
        else:
            return None, None, None

        if res is None:
            return None, None, None

        if res['lastMastered'] is None:
            ret_master = None
        else:
            ret_master = (dt.today() - res['lastMastered']).days

        if res['lastPlayed'] is not None:
            ret_player = (dt.today() - res['lastPlayed']).days
        elif res['created'] is not None:
            ret_player = (dt.today() - res['created']).days
        else:
            ret_player = None

        return ret_master, ret_player, res['_id']

    def get_weekly_tbadge(self, start_date, end_date):
        '''
        Calculates the number of Tbadge earned in a certain interval
        :start_date: the starting day of the interval, datetime object
        :end_date: the ending day of the interval, datetime object
        '''
        return int(list(self.ptx.sessions.aggregate(pipeline=get_tbadge_pipeline(start_date, end_date)))[0]["tbadge"] + (end_date - start_date).days + 1)

    def get_master_rewards(self, start_date, end_date):
        '''
        Calculates the master rewards earned in a certain interval
        :start_date: the starting day of the interval, datetime object
        :end_date: the ending day of the interval, datetime object
        '''
        rewards = dict()
        # Gets the number of sessions for each master
        res = self.ptx.sessions.aggregate(pipeline=get_session_count_pipeline(start_date, end_date))
        for doc in res:
            # Gets the tier of the master to calculate the results
            character = list(self.ptx.characters.aggregate(pipeline=get_total_ms_pipeline(doc['_id'])))[0]
            tier, _ = self.mstable[character['ms']]
            rewards[character['_id']] = self.tier_rewards[tier]*doc['sessCount']*2
        return rewards

    def get_website_tables(self):
        '''
        Returns the info of all the active players to be put in the website table
        '''
        ms_table = []
        rep_table = []
        res = self.ptx.characters.aggregate(pipeline=get_characters_w_players_pipeline())
        # For each active player
        for doc in res:
            if doc['lastMastered'] is None:
                in_master = "Mai"
            else:
                in_master = (dt.today() - doc['lastMastered']).days

            if doc['lastPlayed'] is not None:
                in_player = (dt.today() - doc['lastPlayed']).days
            elif doc['created'] is not None:
                in_player = (dt.today() - doc['created']).days
            else:
                in_player = "Nuovo"

            total_ms = sum([doc['masterMS'], doc['sessionMS'], doc['PBCMS'], doc['errataMS']])
            tier, level = self.mstable[total_ms]
            # Create a row in a table for all the info
            ms_table.append([
                doc['player'][0]["name"],
                doc['_id'],
                doc['race'],
                doc['territory'],
                doc['class'],
                total_ms,
                level,
                tier,
                in_player, 
                in_master
            ])
            # Create a row in a table for the rep
            row = []
            for _, v in doc['reputation'].items():
                row.append(v)
            rep_table.append(row)
        return ms_table, rep_table

    def get_ms(self, player):
        '''
        Gets MS, level and tier info relative to one player
        :param player: the discord ID of the player
        '''
        doc = self.ptx.characters.find_one({'player': str(player), "status": "active"}, {'_id':1, 'class':1, 'masterMS':1, 'sessionMS':1, 'PBCMS':1, 'errataMS':1})
        if doc is None:
            return None, None, None, None, None
        total_ms = sum([doc['masterMS'], doc['sessionMS'], doc['PBCMS'], doc['errataMS']])
        tier, level = self.mstable[total_ms]      
        return doc['_id'], doc['class'], round(total_ms, 1), tier, level

    def get_reputation(self, player):
        '''
        Gets the reputation info relative to one player
        :param player: the discord ID of the player
        '''
        doc = self.ptx.characters.find_one({'player': str(player), "status": "active"}, {'_id':1, 'reputation':1})
        if doc is None:
            return None, None
        return doc['_id'], doc['reputation']

    def get_session_info(self, player):
        '''
        Returns all the sessions mastered by a player
        :param player: the discord ID of the player
        '''
        return list(self.ptx.sessions.aggregate(pipeline=get_mastered_sessions_pipeline(player)))

    def get_game_date(self, past_date=None):
        if past_date is None:
            return self.calendar[self.get_total_days()]
        else:
            return self.calendar[self.get_total_days()-self.get_total_days(past_date)]

    def add_user(self, user, password):
        self.ptx.web_users.insert_one({
            '_id': user,
            'pwd': generate_password_hash(password),
            'isActive': True,
            'isAuthenticated': False,
            'isAnonymous': False
        })

    def get_user(self, user):
        '''
        Returns if a web user is authenticated
        '''
        return self.ptx.web_users.find_one({'_id': user}, {'_id':1, 'isAuthenticated': 1})

    def check_user(self, user, password):
        '''
        Checks if a user exists and if the password match.
        '''
        u = self.ptx.web_users.find_one({'_id': user})
        return (u is not None) and (check_password_hash(u['pwd'], password))

    def authenticate_user(self, user): 
        '''
        Authenticate a user
        '''
        self.ptx.web_users.update_one({'_id': user}, 
                                {'$set': {'isAuthenticated': True}})

    def insert_player(self, username, discord_id, joined):
        '''
        Creates a new player
        '''
        self.ptx.players.insert_one({
            '_id': discord_id,
            'name': username,
            'dateJoined': joined,
            'isTraitor': False
        })

    def get_players_list(self):
        '''
        Gets all the players' names
        '''
        players = list(self.ptx.players.aggregate(pipeline=[{'$group':{'_id':None,'names':{'$push':'$name'}}}]))
        return players[0]["names"]

    def get_character_list(self):
        '''
        Gets all the characters' names
        '''
        characters = list(self.ptx.characters.aggregate(pipeline=[{'$group':{'_id':None,'names':{'$push':'$_id'}}}]))
        return characters[0]["names"]

    def get_all_characters(self, only_active=True, has_buildings=False):
        '''
        Returns an iterable with all the characters' info
        :param only_active: returns only the active 
        '''
        active_filter = {}
        if only_active:
            active_filter = {'status': 'active'}
        if has_buildings:
            active_filter["buildings"] = {"$gt": {}}
        return self.ptx.characters.find(active_filter)

    def player_exists(self, player):
        '''
        Checks if a player exists
        '''
        return self.ptx.players.find_one({'name': player}) is not None

    def insert_character(self, player_name, character, starting_level, race, territory, char_class, char_age, joined):
        '''
        Creates a new character
        '''
        discord_id = self.ptx.players.find_one({'name': player_name}, {'_id': 1})['_id']
        reputation = self.ptx.reputation.find_one({"_id": "reputation"})[territory]
        self.ptx.characters.insert_one({
            '_id': character,
            'player': discord_id,
            'race': race,
            'territory': territory,
            'class': char_class,
            'age': char_age,
            'status': "active",
            'masterMS': 0,
            'sessionMS': 0,
            'PBCMS': 0,
            'errataMS': 0,
            'errata': [],
            'created': joined,
            'lastPlayed': None,
            'lastMastered': None,
            'reputation': reputation,
            'inventory': {},
            'money': 0.0,
            'proficiencies': [],
            'languages': []
        })
        if starting_level > 1:
            self.insert_errata(character, "Nuovo personaggio, parte da livello {}".format(starting_level), joined, self.mstable.get_ms_level(starting_level), None, {})
        self.update_master_activity(discord_id)

    def character_exists(self, character):
        '''
        Checks if a character exists
        '''
        return self.ptx.characters.find_one({'_id': character}) is not None

    def insert_session(self, master, title, date, duration, characters):
        players_doc = []
        cursor = self.ptx.sessions.find().sort("uid", pymongo.DESCENDING)
        uid = next(cursor)["uid"] + 1
        for c in characters:
            if c['is_dead']:
                self.insert_errata(c["player"], "Morto nella sessione {}".format(title), date, 0, "dead", {})
            char = self.ptx.characters.find_one({'_id': c["player"]})
            total_ms = sum([char['masterMS'], char['sessionMS'], char['PBCMS'], char['errataMS']])
            tier_ms_mod = self.mstable.get_tier_ms_mod(self.mstable[total_ms][0])
            players_doc.append({
                "character": c["player"],
                "ms": int(c["ms"])*tier_ms_mod,
                "isAlive": not c["is_dead"],
                "reputationAdjustment": {k: int(v) for k, v in c["rep_adj"].items()}
            })
        self.ptx.sessions.insert_one({
            "master": master,
            "date": date,
            "title": title, 
            "uid": uid,
            "duration": int(duration),
            "characters": players_doc
        })
        self.set_session_ms()
        self.set_master_ms()
        self.set_reputation()
        self.set_last_activity()

    def insert_pbc(self, date, characters):
        players_doc = []
        for c in characters:
            players_doc.append({
                "character": c["player"],
                "ms": int(c["ms"]),
                "isAlive": True,
                "reputationAdjustment": {}
            })
        self.ptx.PBX.insert_one({
            "date": date,
            "title": "",
            "type": "pbc",
            "characters": players_doc
        })
        self.set_pbc_ms()
        self.set_last_activity()

    def insert_pbv(self, master, title, date, characters):
        players_doc = [{
                "character": master,
                "ms": 1,
                "isAlive": True,
                "reputationAdjustment": {}
            }]
        for c in characters:
            players_doc.append({
                "character": c["player"],
                "ms": 1,
                "isAlive": True,
                "reputationAdjustment": {k: int(v) for k, v in c["rep_adj"].items()}
            })
        self.ptx.PBX.insert_one({
            "date": date,
            "title": title, 
            "type": "pbv",
            "characters": players_doc
        })
        self.set_pbc_ms()
        self.set_reputation()
        self.set_last_activity()

    def insert_errata(self, character, description, date, ms, status, rep_adj):
        edit = {}
        if status is not None:
            edit["$set"] = {"status": status}
            player_discord = self.ptx.characters.find_one({'_id': character}, {'player': 1})["player"]
            if status == "traitor":
                self.ptx.players.update_one({'_id': player_discord}, {"$set": {"isTraitor": True}})
            if status != "active":
                self.remove_all_proficiencies(int(player_discord))
        edit["$push"] = {"errata": 
                        {
                            "ms": ms,
                            "description": description,
                            "reputationAdjustment": {k: int(v) for k, v in rep_adj.items()},
                            "date": date,
                            "statusChange": status
                        }}
        self.ptx.characters.update_one({'_id': character}, edit)
        self.set_errata_ms()
        self.set_reputation()

    def update_player_discord_id(self, old_id, new_id):
        old_player = self.ptx.players.find_one({'_id': old_id})
        old_player['_id'] = new_id
        self.ptx.players.insert_one(old_player)
        self.ptx.players.delete_one({'_id': old_id})
        self.ptx.characters.update_many({'player': old_id}, {'$set': {'player': new_id}})

    def get_played_sessions(self, characters, start_date, end_date):
        '''
        Returns the number of sessions played by a list of characters in a time interval
        :param characters: the characters list
        :param start_date: the starting date
        :param end_date: the ending date
        :return: a dictionary
        '''
        data = self.ptx.sessions.aggregate(pipeline=get_played_sessions_count_pipeline(characters, start_date, end_date))
        ret = {}
        for el in data:
            ret[el['_id']['player']] = el['_id']['count']
        return ret

    def _compute_tier_summary(self):
        '''
        Returns a dict containing the number of active player for each tier
        '''
        doc = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
        for c in self.ptx.characters.find({"status": "active"}, {'masterMS':1, 'sessionMS':1, 'PBCMS':1, 'errataMS':1}):
            total_ms = sum([c['masterMS'], c['sessionMS'], c['PBCMS'], c['errataMS']])
            tier, _ = self.mstable[total_ms]    
            doc[str(tier)] += 1
        return doc

    def tier_summary(self):
        '''
        Saves the active players tier summary into the db
        '''
        doc = self._compute_tier_summary()
        d = dt.today()
        doc['_id'] = dt(d.year, d.month, d.day)
        doc["type"] = "tier"
        self.ptx.stats.insert_one(doc)

    def get_items(self):
        return list(self.ptx.items.find())

    def get_spells(self):
        return list(self.ptx.spells.find())

    def get_classes(self):
        return list(self.ptx.classes.find())

    def get_feats(self):
        return list(self.ptx.feats.find())

    def get_backgrounds(self):
        return list(self.ptx.backgrounds.find())

    def get_building_recipes(self):
        return list(self.ptx.buildingrecipes.find())

    def get_inactive_players(self):
        act_master = dict()
        act_player = list()
        no_info_player = list()

        for doc in self.ptx.characters.aggregate(pipeline=get_characters_w_players_pipeline()):
            if doc['lastMastered'] is not None:
                act_master[doc['player'][0]["_id"]] = (dt.today() - doc['lastMastered']).days

            tier, _ = self.mstable[sum([doc['masterMS'], doc['sessionMS'], doc['PBCMS'], doc['errataMS']])]

            if doc['lastPlayed'] is not None:
                act_player.append((doc['player'][0]["_id"], doc["_id"], (dt.today() - doc['lastPlayed']).days, tier))
            elif doc['created'] is not None:
                act_player.append((doc['player'][0]["_id"], doc["_id"], (dt.today() - doc['created']).days, tier))
            elif doc["player"][0]["dateJoined"] is not None:
                act_player.append((doc['player'][0]["_id"], doc["_id"], (dt.today() - doc["player"][0]["dateJoined"]).days, tier))
            else:
                no_info_player.append((doc['player'][0]["_id"], doc["_id"]))

        return act_master, act_player, no_info_player

    def update_master_activity(self, player):
        '''
        When a master changes character, updates the last mastered session
        '''
        # Get the date of the last session mastered
        data = list(self.ptx.characters.aggregate(pipeline=get_transfer_master_activity_pipeline(player)))
        if len(data) > 0 and data[0]["last"] is not None:
            self.ptx.characters.update_one({"player": player, "status": "active"}, {"$set": {"lastMastered": data[0]["last"]}})
            return data[0]["last"]

    def server_stats(self):
        session_count = {"days": [], "count": []}
        for doc in self.ptx.sessions.aggregate(pipeline=[{'$group': {'_id': '$date','count': {'$count': {}}}}]):
            session_count["days"].append(doc["_id"])
            session_count["count"].append(doc["count"])

        player_stats = {}
        for doc in self.ptx.characters.aggregate(pipeline=[{'$group': {'_id': '$status','count': {'$count': {}}}}]):
            player_stats[doc["_id"]] = doc["count"]

        tier_summary = self._compute_tier_summary()

        death_rate = list(self.ptx.sessions.aggregate(pipeline=get_deaths_pipeline()))[0]["deaths"]

        deadly_masters = list(self.ptx.sessions.aggregate(pipeline=get_deadly_master_pipeline()))
        active_masters = list(self.ptx.sessions.aggregate(pipeline=get_more_active_master_pipeline()))
        unlucky_players = list(self.ptx.characters.aggregate(pipeline=get_unlucky_player_pipeline()))

        return {
            "sessions": session_count,
            "players": player_stats,
            "tier": tier_summary,
            "deaths": death_rate,
            "deadly_masters": deadly_masters,
            "active_masters": active_masters,
            "unlucky_players": unlucky_players
        }

    def get_active_character(self, player: str) -> Dict:
        return self.ptx.characters.find_one({"player": player, "status": "active"})

    def get_ms_list(self, character):
        res = list(self.ptx.sessions.aggregate(pipeline=get_session_info_pipeline(character)))
        if len(res) == 0:
            return []
        return res[0]["ms"]

    def get_sessions_list(self, player):
        ret = list()
        for doc in self.ptx.sessions.aggregate(pipeline=get_all_mastered_pipeline(player)):
            ret.append(
                {
                    "title": doc["title"],
                    "character": doc["char"][0]["_id"],
                    "real_date": doc["date"].strftime("%d-%m-%Y"),
                    "game_date": self.get_game_date(doc["date"])
                }
            )
        return ret

    def insert_war(self, name, populations, started):
        doc = {
            '_id': name,
            'populations': {p:0 for p in populations},
            'status': 'active',
            'started': started,
            'updates': []
        }
        self.ptx.wars.insert_one(doc)

    def add_war_result(self, name, population, result, session):
        self.ptx.wars.update_one(
            {"_id": name},
            {"$push": {"updates": {
                "population": population,
                "result": result,
                "session": session
            }}}
        )

    def end_war(self, name, ended_date):
        self.ptx.wars.update_one(
            {"_id": name},
            {"$set": {
                "status": "ended",
                "ended": ended_date
            }}
        )
    
    def get_wars(self, active=True):
        query = {"status": "active"} if active else dict()
        return list(self.ptx.wars.find(query))

    def get_recent_sessions(self, limit=7):
        return self.ptx.sessions.find().sort("date", pymongo.DESCENDING).limit(limit)

    def add_proficiency(self, player_id, proficiency):
        self.ptx.market.update_one({'_id': proficiency}, {"$addToSet": {"users": player_id}}, upsert=True)

    def get_market(self):
        return {doc["_id"]:doc["users"] for doc in self.ptx.market.find()}

    def remove_all_proficiencies(self, player_id):
        self.ptx.market.update_many({}, {"$pull": {"users": player_id}})

    def remove_proficiency(self, player_id, proficiency):
        self.ptx.market.update_one({'_id': proficiency}, {"$pull": {"users": player_id}})

    def get_all_sessions(self, player_id): 
        ret = list()
        active_character = self.ptx.characters.find_one({"player": str(player_id), "status": "active"})
        
        if active_character is not None:
            for doc in self.ptx.sessions.aggregate(get_played_sessions_pipeline(active_character["_id"])):
                ret.append({
                    "title": doc["title"],
                    "date": doc["date"],
                    "master": doc["master"],
                    "ms": doc["characters"]["ms"]
                })

        name = active_character["_id"] if active_character is not None else None
        return ret, name

    def insert_building(self, character: str, b_type: str, title: str, description: str, zone: str, db_session: ClientSession=None) -> int:
        ret = self.ptx.characters.update_one(
            {'_id': character},
            {
                "$push": {
                    f"buildings.{b_type}": {
                        "name": title,
                        "description": description,
                        "zone": zone,
                        "status": "active"
                    }
                }
            },
            session = db_session
        )
        return ret.modified_count

    def get_item(self, item: str) -> dict:
        ret_item = self.ptx.items.find_one({"_id": item})
        if ret_item is None:
            raise ItemNotFoundException(item=item)
        return ret_item

    def get_character(self, player: str) -> dict:
        character = self.ptx.characters.find_one({"player": str(player), "status": "active"})
        if character is None:
            p = self.ptx.players.find_one({"_id": str(player)})
            if p is not None:
                raise NoActiveCharacterException(player=p["name"])
            else:
                raise PlayerNotFoundException(player=player)
        return character

    def add_money(self, player: str, qty: float, db_session: ClientSession=None) -> int:
        character = self.get_character(player)
        ret = self.ptx.characters.update_one(
            {
                "_id": character["_id"]
            }, {
                "$set": {
                    "money": character["money"] + qty
                }
            },
            session = db_session
        )
        return ret.modified_count

    def subtract_money(self, player: str, qty: float, db_session: ClientSession=None) -> int:
        character = self.get_character(player)
        if qty > character["money"]:
            raise InsufficientFundsException(character=character["_id"])
        ret = self.ptx.characters.update_one(
            {
                "_id": character["_id"]
            }, {
                "$set": {
                    "money": character["money"] - qty
                }
            },
            session = db_session
        )
        return ret.modified_count

    def give_item(self, player: str, item: str, qty: int, db_session: ClientSession=None) -> int:
        self.get_item(item)
        character = self.get_character(player)

        new_qty = 0
        if item in character["inventory"]:
            new_qty = character["inventory"][item] + qty
        else:
            new_qty = qty
        ret = self.ptx.characters.update_one(
            {
                "_id": character["_id"]
            }, {
                "$set": {
                    f"inventory.{item}": new_qty
                }
            },
            session = db_session
        )
        return ret.modified_count

    def remove_item(self, player: str, item: str, qty: int, db_session: ClientSession=None) -> int:
        self.get_item(item)
        character = self.get_character(player)
        if item not in character["inventory"] or character["inventory"][item] < qty:
            raise InsufficientItemsException(character["_id"], item)

        new_qty = character["inventory"][item] - qty
        if new_qty > 0:
            update_query = {
                    "$set": {
                        f"inventory.{item}": new_qty
                    }
                }
        else:
            update_query = {
                    "$unset": {
                        f"inventory.{item}": 1
                    }
                }
        ret = self.ptx.characters.update_one(
            {
                "_id": character["_id"]
            }, update_query, session = db_session
        )
        return ret.modified_count

    def get_inventory(self, player: str) -> Tuple[str, dict]:
        character = self.get_character(player)
        return character["_id"], character["inventory"]

    def get_money(self, player: str) -> Tuple[str, float]:
        character = self.get_character(player)
        return character["_id"], character["money"]

    def add_proficiencies(self, player: str, proficiencies: List[str], db_session: ClientSession=None) -> int:
        character = self.get_character(player)
        ret = self.ptx.characters.update_one(
            {
                "_id": character["_id"]
            }, {
                "$addToSet": {
                    "proficiencies": {
                        "$each": proficiencies
                    }
                }
            }, session=db_session
        )
        return ret.modified_count

    def add_languages(self, player: str, languages: List[str], db_session: ClientSession=None) -> int:
        character = self.get_character(player)
        ret = self.ptx.characters.update_one(
            {
                "_id": character["_id"]
            }, {
                "$addToSet": {
                    "languages": {
                        "$each": languages
                    }
                }
            }, session=db_session
        )
        return ret.modified_count

    def add_schedule(self, player: str, item: str, qty: int, date: dt) -> None:
        self.ptx.schedule.insert_one(
            {
                "player": player,
                "item": item,
                "qty": qty,
                "date": date
            }
        )

    def get_player(self, player_id: str) -> Dict[str, any]:
        return self.ptx.players.find_one({"_id": str(player_id)})

    def remove_schedule(self, player: str, date: dt) -> None:
        self.ptx.schedule.delete_one(
            {
                "player": player,
                "date": date
            }
        )
    
    def get_schedule(self) -> pymongo.cursor.Cursor:
        return self.ptx.schedule.find()

    def rename_item(self, old_item: str, new_item: str) -> None:
        with self.client.start_session() as session:
            with session.start_transaction():
                item = self.get_item(old_item)
                self.ptx.characters.update_many({}, 
                    {"$rename": {f"inventory.{old_item}": f"inventory.{new_item}"}},
                    session=session)
                self.ptx.items.delete_one({"_id": old_item}, session=session)
                item["_id"] = new_item
                self.ptx.items.insert_one(item, session=session)

    def get_object_report(self):
        return list(self.ptx.characters.aggregate(pipeline=objects_summary_pipeline()))

    def count_flame(self):
        d = dt(dt.today().year, dt.today().month, dt.today().day)
        today_flame = self.ptx.flamecount.find_one({"_id": d})
        if today_flame is None:
            self.ptx.flamecount.insert_one({
                "_id": d,
                "count": 1
            })
        else:
            self.ptx.flamecount.update_one(
                {"_id": d},
                {"$set": {"count": today_flame["count"] + 1}}
            )

    def add_good_flame(self, flame: str) -> None:
        self.ptx.flame.update_one({
            "_id": "flame"
        },
        {
            "$addToSet": {"flame": flame}
        })

    def get_random_flame(self) -> str:
        flame = self.ptx.flame.find_one({"_id": "flame"})["flame"]
        return random.choice(flame)