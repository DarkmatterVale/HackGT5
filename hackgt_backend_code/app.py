from chalice import Chalice
import elasticache_auto_discovery
from pymemcache.client.hash import HashClient
import os

app = Chalice(app_name='hackgt_backend_code')

@app.route('/v1/game/POST/info/{group_id}/{game_info}', methods=['POST'])
def push_game_info(group_id, game_info):
    """
    Push the game info for a group.

    :param group_id: ID for the group
    :type group_id: String
    :param game_info: JSON information regarding the game status (serialized into String format)
    :type game_info: String
    """
    nodes = elasticache_auto_discovery.discover('hackgt5mem.gy46cz.cfg.use1.cache.amazonaws.com:11211')
    nodes = map(lambda x: (x[1], int(x[2])), nodes)
    memcache_client = HashClient(nodes)

    memcache_client.set(str(group_id), str(game_info))

    return {
        "group_id" : group_id,
        "game_info" : game_info,
        "status" : "success"
    }

@app.route('/v1/game/GET/info/{group_id}', methods=['GET'])
def get_game_info(group_id):
    """
    Get the game info for a group.

    :param group_id: ID for the group
    :type group_id: String
    :return: String representation of group information
    """
    nodes = elasticache_auto_discovery.discover('hackgt5mem.gy46cz.cfg.use1.cache.amazonaws.com:11211')
    nodes = map(lambda x: (x[1], int(x[2])), nodes)
    memcache_client = HashClient(nodes)

    return {
        "game_info" : memcache_client.get(str(group_id)).decode("utf-8"),
        "status" : "success"
    }
