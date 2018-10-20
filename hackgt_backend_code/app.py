from chalice import Chalice
from __future__ import print_function
import uuid
import sys
import elasticache_auto_discovery
from pymemcache.client.hash import HashClient
import json

app = Chalice(app_name='hackgt_backend_code')

ELASTICACHE_CONFIG_ENDPOINT = "your-elasticache-cluster-endpoint:port"

@app.route('/test')
def index():
    return {'hello': 'world'}

@app.route('/push_game_info/{group_id}/{game_info}', methods=['POST']):
def push_game_info(group_id, game_info):
    """
    Push the game info for a group.

    :param group_id: ID for the group
    :type group_id: String
    :param game_info: JSON information regarding the game status
    """
    nodes = elasticache_auto_discovery.discover(ELASTICACHE_CONFIG_ENDPOINT)
    nodes = map(lambda x: (x[1], int(x[2])), nodes)
    memcache_client = HashClient(nodes)

    #Create a random UUID... this will the sample element we add to the cache.
    uuid_inserted = uuid.uuid4().hex
    #Put the UUID to the cache.
    memcache_client.set('uuid', uuid_inserted)
    #Get item (UUID) from the cache.
    uuid_obtained = memcache_client.get('uuid')
    if uuid_obtained.decode("utf-8") == uuid_inserted:
        # this print should go to the CloudWatch Logs and Lambda console.
        print ("Success: Fetched value %s from memcache" %(uuid_inserted))
    else:
        raise Exception("Value is not the same as we put :(. Expected %s got %s" %(uuid_inserted, uuid_obtained))

    return "Fetched value from memcache: " + uuid_obtained.decode("utf-8")
