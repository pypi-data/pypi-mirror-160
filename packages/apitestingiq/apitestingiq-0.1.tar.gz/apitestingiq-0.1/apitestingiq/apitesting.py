import requests



def get_asset_node_red(asset_name,api_url):
    req_json = {"Asset_Name" :asset_name}
    res = requests.post(api_url, json = req_json)
    return res

