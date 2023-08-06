def objects_summary_pipeline():
    return [
    {
        '$match': {
            'status': 'active', 
            'inventory': {
                '$gt': {}
            }
        }
    }, {
        '$addFields': {
            'items': {
                '$objectToArray': '$inventory'
            }
        }
    }, {
        '$group': {
            '_id': '$_id', 
            'item_array': {
                '$push': '$items.k'
            }
        }
    }, {
        '$unwind': {
            'path': '$item_array', 
            'includeArrayIndex': 'string', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$unwind': {
            'path': '$item_array', 
            'includeArrayIndex': 'string2', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$group': {
            '_id': '$item_array', 
            'count': {
                '$count': {}
            }
        }
    }, {
        '$lookup': {
            'from': 'items', 
            'localField': '_id', 
            'foreignField': '_id', 
            'as': 'category'
        }
    }, {
        '$unwind': {
            'path': '$category', 
            'includeArrayIndex': 'string', 
            'preserveNullAndEmptyArrays': False
        }
    }
]

def get_all_mastered_pipeline(player):
    return [
                {
                    '$lookup': {
                        'from': 'characters', 
                        'localField': 'master', 
                        'foreignField': '_id', 
                        'as': 'char'
                    }
                }, {
                    '$match': {
                        'char': {
                            '$elemMatch': {
                                'player': player
                            }
                        }
                    }
                }
            ]

def get_unlucky_player_pipeline():
    return [
                {
                    '$match': {
                        'status': 'dead'
                    }
                }, {
                    '$lookup': {
                        'from': 'players', 
                        'localField': 'player', 
                        'foreignField': '_id', 
                        'as': 'p'
                    }
                }, {
                    '$unwind': {
                        'path': '$p', 
                        'includeArrayIndex': 'string', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$project': {
                        '_id': '$p.name'
                    }
                }, {
                    '$group': {
                        '_id': '$_id', 
                        'count': {
                            '$count': {}
                        }
                    }
                }
            ]

def get_more_active_master_pipeline():
    return [
            {
                '$lookup': {
                    'from': 'characters', 
                    'localField': 'master', 
                    'foreignField': '_id', 
                    'as': 'p'
                }
            }, {
                '$unwind': {
                    'path': '$p', 
                    'includeArrayIndex': 'string', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$project': {
                    'player': '$p.player'
                }
            }, {
                '$group': {
                    '_id': '$player', 
                    'count': {
                        '$count': {}
                    }
                }
            }, {
                '$lookup': {
                    'from': 'players', 
                    'localField': '_id', 
                    'foreignField': '_id', 
                    'as': 'p'
                }
            }, {
                '$unwind': {
                    'path': '$p', 
                    'includeArrayIndex': 'string', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$project': {
                    'count': 1, 
                    'player': '$p.name'
                }
            }
        ]

def get_deadly_master_pipeline():
        return [
                {
                    '$project': {
                        'deaths': {
                            '$filter': {
                                'input': '$characters.isAlive', 
                                'as': 'el', 
                                'cond': {
                                    '$not': '$$el'
                                }
                            }
                        }, 
                        'master': 1
                    }
                }, {
                    '$project': {
                        'deaths': {
                            '$size': '$deaths'
                        }, 
                        'master': 1
                    }
                }, {
                    '$lookup': {
                        'from': 'characters', 
                        'localField': 'master', 
                        'foreignField': '_id', 
                        'as': 'char'
                    }
                }, {
                    '$unwind': {
                        'path': '$char', 
                        'includeArrayIndex': 'string', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$project': {
                        'deaths': 1, 
                        'master': '$char.player'
                    }
                }, {
                    '$group': {
                        '_id': '$master', 
                        'total_deaths': {
                            '$sum': '$deaths'
                        }
                    }
                }, {
                    '$lookup': {
                        'from': 'players', 
                        'localField': '_id', 
                        'foreignField': '_id', 
                        'as': 'player'
                    }
                }, {
                    '$unwind': {
                        'path': '$player', 
                        'includeArrayIndex': 'string', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$project': {
                        '_id': 1, 
                        'total_deaths': 1, 
                        'player': '$player.name'
                    }
                }
            ]

def get_played_sessions_pipeline(character):
    return [
                {
                    '$unwind': {
                        'path': '$characters', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$match': {
                        'characters.character': character
                    }
                }, {
                    '$sort': {
                        'date': -1
                    }
                }
            ]

def get_session_info_pipeline(character):
    return [
            {
                '$match': {
                    'characters': {
                        '$elemMatch': {
                            'character': character
                        }
                    }
                }
            }, {
                '$project': {
                    'result': {
                        '$filter': {
                            'input': '$characters', 
                            'as': 'el', 
                            'cond': {
                                '$eq': [
                                    '$$el.character', character
                                ]
                            }
                        }
                    }
                }
            }, {
                '$unwind': {
                    'path': '$result', 
                    'includeArrayIndex': 'string', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$group': {
                    '_id': None, 
                    'ms': {
                        '$push': '$result.ms'
                    }
                }
            }
        ]

def get_deaths_pipeline(): 
    return [
            {
                '$project': {
                    'deaths': {
                        '$filter': {
                            'input': '$characters.isAlive', 
                            'as': 'el', 
                            'cond': {
                                '$not': '$$el'
                            }
                        }
                    }, 
                    'total': {
                        '$filter': {
                            'input': '$characters.isAlive', 
                            'as': 'el', 
                            'cond': True
                        }
                    }
                }
            }, {
                '$project': {
                    'n_deaths': {
                        '$size': '$deaths'
                    }, 
                    'n_tot': {
                        '$size': '$total'
                    }
                }
            }, {
                '$project': {
                    'death_p': {
                        '$divide': [
                            '$n_deaths', '$n_tot'
                        ]
                    }
                }
            }, {
                '$group': {
                    '_id': None, 
                    'deaths': {
                        '$push': '$death_p'
                    }
                }
            }
        ]

def get_transfer_master_activity_pipeline(player):
    return [
                {
                    '$match': {
                        'player': player
                    }
                }, {
                    '$group': {
                       '_id': '$player', 
                        'last': {
                            '$max': '$lastMastered'
                        }
                    }
                }
            ]

def get_characters_w_players_pipeline():
    return [
                {
                    '$match': {
                        'status': 'active'
                    }
                }, {
                    '$lookup': {
                        'from': 'players', 
                        'localField': 'player', 
                        'foreignField': '_id', 
                        'as': 'player'
                    }
                }
            ]

def get_played_sessions_count_pipeline(characters, start_date, end_date):
    return [
                {
                    '$match': {
                        'date': {
                            '$gte': start_date, 
                            '$lte': end_date
                        }
                    }
                }, {
                    '$unwind': {
                        'path': '$characters', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$replaceRoot': {
                        'newRoot': '$characters'
                    }
                }, {
                    '$group': {
                        '_id': '$character', 
                        'count': {
                            '$count': {}
                        }
                    }
                }, {
                    '$lookup': {
                        'from': 'characters', 
                        'localField': '_id', 
                        'foreignField': '_id', 
                        'as': 'charsInfo'
                    }
                }, {
                    '$unwind': {
                        'path': '$charsInfo', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$match': {
                        'charsInfo.status': 'active', 
                        'charsInfo.player': {
                            '$in': characters
                        }
                    }
                }, {
                    '$group': {
                        '_id': {
                            'player': '$charsInfo.player', 
                            'count': '$count'
                        }
                    }
                }
            ]

def get_mastered_sessions_pipeline(player_id):
    return [
                {
                    '$lookup': {
                        'from': 'characters', 
                        'localField': 'master', 
                        'foreignField': '_id', 
                        'as': 'character'
                    }
                }, {
                    '$unwind': {
                        'path': '$character', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$lookup': {
                        'from': 'players', 
                        'localField': 'character.player', 
                        'foreignField': '_id', 
                        'as': 'player'
                    }
                }, {
                    '$unwind': {
                        'path': '$player', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$match': {
                        'player._id': str(player_id)
                    }
                }, {
                    '$project': {
                        'master': 1, 
                        'date': 1, 
                        'title': 1,
                        'player': 1
                    }
                }, {
                    '$sort': {
                        'date': -1
                    }
                }
            ]

def get_total_ms_pipeline(character):
    return [
                {
                    '$match': {
                        '_id': character
                    }
                }, {
                    '$group': {
                        '_id': '$player', 
                        'ms': {
                            '$sum': {
                                '$add': [
                                    '$masterMS', '$sessionMS', '$errataMS', '$PBCMS'
                                ]
                            }
                        }
                    }
                }
            ]

def get_session_count_pipeline(start_date, end_date):
    return [
                {
                    '$match': {
                        'date': {
                            '$gte': start_date, 
                            '$lte': end_date
                        }
                    }
                }, {
                    '$group': {
                        '_id': '$master', 
                        'sessCount': {
                            '$count': {}
                        }
                    }
                }
            ]

def get_tbadge_pipeline(start_date, end_date):
    return [
                {
                    '$match': {
                        'date': {
                            '$gte': start_date, 
                            '$lte': end_date
                        }
                    }
                }, {
                    '$group': {
                        '_id': {
                            'date': '$date'
                        }, 
                        'maxdays': {
                            '$max': '$duration'
                        }
                    }
                }, {
                    '$group': {
                        '_id': None, 
                        'tbadge': {
                            '$sum': '$maxdays'
                        }
                    }
                }
            ]

def get_last_played_pipeline(character):
    return [
                {
                    '$match': {
                        'characters': {
                            '$elemMatch': {
                                'character': character
                            }
                        }
                    }
                }, {
                    '$group': {
                        '_id': None, 
                        'lastDate': {
                            '$max': '$date'
                        }
                    }
                }
            ]

def get_last_mastered_pipeline(character):
    return [
                {
                    '$match': {
                        'master': character
                    }
                }, {
                    '$group': {
                        '_id': None, 
                        'lastDate': {
                            '$max': '$date'
                        }
                    }
                }
            ]

def get_days_pipeline(starting_date):
    return [
                {
                    '$match': {
                        'date': {
                            '$gte': starting_date
                        }
                    }
                },
                {
                    '$group': {
                        '_id': {
                            'date': '$date'
                        }, 
                        'maxdays': {
                            '$max': '$duration'
                        }
                    }
                }, {
                    '$group': {
                        '_id': None, 
                        'days': {
                            '$sum': '$maxdays'
                        }
                    }
                }
            ]

def get_sum_pipeline(character):
    return [
            {
                '$match': {
                    'characters': {
                        '$elemMatch': {
                            'character': character
                        }
                    }
                }
            }, 
            {
                '$unwind': {
                    'path': '$characters', 
                    'includeArrayIndex': 'string', 
                    'preserveNullAndEmptyArrays': False
                }
            }, 
            {
                '$match': {
                    'characters.character': character
                }
            }, 
            {
                '$group': {
                    '_id': None, 
                    'sum': {
                        '$sum': '$characters.ms'
                    }
                    }
            }
            ]

def get_reputation_pipeline(character):
    return [
                {
                    '$match': {
                        'characters': {
                            '$elemMatch': {
                                'character': character
                            }
                        }
                    }
                }, {
                    '$project': {
                        'characters': {
                            '$filter': {
                                'input': '$characters', 
                                'as': 'c', 
                                'cond': {
                                    '$eq': [
                                        '$$c.character', character
                                    ]
                                }
                            }
                        }
                    }
                }
            ]
