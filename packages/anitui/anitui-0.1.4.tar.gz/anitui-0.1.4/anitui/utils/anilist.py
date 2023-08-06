import requests


def get_data(query, variables):
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})
    return response.json()


def query_watch_list(username):
    query = """
    query ($page: Int, $perPage: Int, $userName: String) {
      Page (page: $page, perPage: $perPage) {
        mediaList (userName: $userName, status: CURRENT, type: ANIME) {
          mediaId
          media {
            title {
              english
            }
          }
          progress
        }
      }
    }
    """
    variables = {
        "page": 1,
        "perPage": 20,
        "userName": username,
    }
    res = get_data(query, variables)
    return res["data"]["Page"]["mediaList"]
