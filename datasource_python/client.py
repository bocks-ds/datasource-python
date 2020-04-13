import requests

from .errors import DSQueryError, DSTargetError


URLS = {
    "starfinder": "https://sfdatasource.com",
    "pathfinder": "https://pfdatasource.com",
}

class Client():
    def __init__(self, api_name):
        self.url = self.get_url(api_name)

    def __getattribute__(self, name):
        """ Create & return attribute as Query object if it doesn't already exist

        :param name: Name of table/field to query. `Client.xyz` will be transformed into `{ query { xyz {...} }`
        """
        try:
            return object.__getattribute__(self, name)
        except:
            object.__setattr__(self, name, Type(name, self.url))
            return object.__getattribute__(self, name)

    def get_url(self, api_name):
        if api_name in URLS:
            return URLS[api_name]
        else:
            raise DSTargetError(f"The target '{api_name}' provided in Client initialization is not in available target names:\n {list(URLS.keys())}")

class Type():
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.args = []
    
    def get(self, fields):
        """ Get entries for the specified type, limited by arguments if set

        :param fields: Fields to include from the returned objects. `Client.xyz.get(['name'])` will be transformed into `{ query { xyz { name } } }`. Required field. 
        :param type: list
        :raises DSQueryError: This error is raised if any errors are returned by GraphQL.
        :return: Response object returned by requests.post
        :rtype: dict
        """
        if self.args:
            self.args = " ".join([
                (key + ":" + f'"{value}"') if type(value) is str else f"{key}:{value}"
                for key, value in self.args.items()
            ])
        self.table = self.name + f"({self.args})" if self.args else self.name
        query = "{" + self.table + "{" + ' '.join(fields) + "} }"
        response = requests.post(self.url, json={'query': query})
        self.args = []
        if "errors" in response.json():
            raise DSQueryError(response)
        return response

    def set_arguments(self, arguments):
        """ Prepare upcoming 'get' call to use these arguments

        :param arguments: Key-value pairs to use in refining a query.
        :param type: dict
        :return: Specifies whether arguments were provided, for use in debugging
        :rtype: bool
        """
        self.args = arguments
        return True if self.args else False
