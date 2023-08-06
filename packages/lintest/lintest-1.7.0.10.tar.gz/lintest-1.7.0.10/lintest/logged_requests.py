import requests
import settings


def generate_curl(request):
    command = "curl --compressed -X {method} -H {headers} -d '{data}' '{uri}'"

    method = request.method

    headers = ['"{0}: {1}"'.format(k, v) for k, v in request.headers.items()]
    headers = " -H ".join(headers)

    data = request.body
    uri = request.url

    return command.format(method=method, headers=headers, data=data, uri=uri)


def log_curl(func):
    def wrapper(*args, **kw):
        self = None
        from . import base_testcase

        for item in args:
            if isinstance(item, base_testcase.BaseTestCase):
                self = item
                break

        res = func(*args, **kw)

        if self:
            self.logger.info("================================ cURL Start ==========================\n")
            self.logger.info(generate_curl(res.request))
            self.logger.info("================================ cURL End ============================\n")
        else:
            # todo
            print("原生requests调用。。。 此处直接讲cURL输出到控制台 ?")
            print("================================ cURL Start ==========================\n")
            print(generate_curl(res.request))
            print("================================ cURL End ============================\n")
        return res

    return wrapper


class LoggedRequests:
    """
    封装 requests module 的常用方法，自动log 每次 request 的参数 & response 内容
    @author: Wang Lin
    """

    @staticmethod
    @log_curl
    def get(self=None, url=None, params=None, **kwargs):
        '''
        self， 如果为None, 则此方法 等价于 开源 requests.get()方法， 否则 会自动写入 此请求的参数 & 响应值
        '''

        if type(self) == str:
            url = self

            # 直接调用 开源 requests
            # call requests.get()
            response = requests.get(url, params, **kwargs)
            return response

        if self is None:
            # call requests.get()
            response = requests.get(url, params, **kwargs)
            return response

        # 增加此判断逻辑，解释参见 post 方法
        if hasattr(settings, "auto_log_request") and settings.auto_log_request is False:
            # 直接调用 开源 requests
            return requests.get(url, params, **kwargs)

        self.logger.info("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Requests GET Start:")
        self.logger.info("---------------- URL: " + url)

        if params is not None:
            self.logger.info("-------------- params:")
            self.logger.info(self.pformat(params))

        if len(kwargs.keys()) > 0:
            self.logger.info("-------------- kwargs:")
            self.logger.info(self.pformat(kwargs))

        # call requests.get()
        response = requests.get(url, params, **kwargs)

        self.logger.info("\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Response:")
        self.logger.info(response)

        # todo
        if response.status_code == 200:
            try:
                self.logger.info(self.pformat(response.json()))
            except BaseException:
                return response

        self.logger.info("\n\n")

        return response

    @staticmethod
    @log_curl
    def post(self=None, url=None, data=None, json=None, **kwargs):
        '''
        self， 如果为None, 则此方法 等价于 开源 requests.post()方法， 否则 会自动写入 此请求的参数 & 响应值
        '''

        if type(self) == str:
            url = self

            # 直接调用 开源 requests
            response = requests.post(url, data, json, **kwargs)

            return response

        if self is None:
            response = requests.post(url, data, json, **kwargs)
            return response

        # 如果调用方式为  self.requests.post(
        #                   self,
        #                   "%s/login" % settings.SERVER_URL,
        #                   data=json.dumps(post_data),
        #                   headers=headers)
        # 并且 此时 很有可能 该调用方法之前 已经明确的 手工调用了 self.logger.info("xxxx..."), 只有传入的 self is not None，
        # 代码逻辑 才会执行到 此处！
        # eg:
        #     self.logger.info("social_login headers: ")
        #     self.logger.info(self.pformat(headers))
        #     self.logger.info("social_login post_data: ")
        #     self.logger.info(self.pformat(post_data))
        #     self.logger.info("social_login api: xxx/login")
        #  为了 不重复记录 log,则 增加如下判断， 如果 settings.auto_log_request = False, 则不需要框架自动记录log!
        if hasattr(settings, "auto_log_request") and settings.auto_log_request is False:
            # 直接调用 开源 requests
            return requests.post(url, data, json, **kwargs)

        self.logger.info("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Requests POST Start:")
        self.logger.info("------------ URL: " + url)

        if data is not None:
            self.logger.info("------------ data:")
            self.logger.info(self.pformat(data))

        if json is not None:
            self.logger.info("------------ json:")
            self.logger.info(self.pformat(json))

        if len(kwargs.keys()) > 0:
            self.logger.info(self.pformat(kwargs))

        # call requests.post()
        response = requests.post(url, data, json, **kwargs)

        self.logger.info("\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Response:")
        self.logger.info(response)

        # todo
        if response.status_code == 200:
            self.logger.info(response)
            # todo:
            try:
                self.logger.info(self.pformat(response.json()))
            except BaseException:
                self.logger.info(response.__dict__)

                # todo
                # self.logger.info("================================ cURL Start ==========================\n")
                # self.logger.info(generate_curl(response.request))
                # self.logger.info("================================ cURL End ============================\n")
                return response

        self.logger.info("\n\n")

        # print(generate_curl(response.request))
        # self.logger.info("================================ cURL Start ==========================\n")
        # self.logger.info(generate_curl(response.request))
        # self.logger.info("================================ cURL End ============================\n")

        return response

    @staticmethod
    @log_curl
    def put(self=None, url=None, data=None, **kwargs):
        '''
        self， 如果为None, 则此方法 等价于 开源 requests.put()方法， 否则 会自动写入 此请求的参数 & 响应值
        '''

        if type(self) == str:
            url = self

            # 直接调用 开源 requests
            response = requests.put(url, data, **kwargs)
            return response

        if self is None:
            response = requests.put(url, data, **kwargs)
            return response

        # 增加此判断逻辑，解释参见 post 方法
        if hasattr(settings, "auto_log_request") and settings.auto_log_request is False:
            # 直接调用 开源 requests
            return requests.put(url, data, **kwargs)

        self.logger.info("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Requests PUT Start:")
        self.logger.info("-------------- URL: " + url)

        if data is not None:
            self.logger.info("------------ data:")
            self.logger.info(self.pformat(data))

        if len(kwargs.keys()) > 0:
            self.logger.info(self.pformat(kwargs))

        # call requests.put()
        response = requests.put(url, data, **kwargs)

        self.logger.info("\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Response:")
        self.logger.info(response)

        # todo
        if response.status_code == 200:
            try:
                self.logger.info(self.pformat(response.json()))
            except BaseException:
                return response

        self.logger.info("\n\n")

        return response

    @staticmethod
    @log_curl
    def delete(self=None, url=None, **kwargs):
        '''
        self， 如果为None, 则此方法 等价于 开源 requests.delete()方法， 否则 会自动写入 此请求的参数 & 响应值
        '''

        if type(self) == str:
            url = self

            # 直接调用 开源 requests
            response = requests.delete(url, **kwargs)
            return response

        if self is None:
            response = requests.delete(url, **kwargs)
            return response

        # 增加此判断逻辑，解释参见 post 方法
        if hasattr(settings, "auto_log_request") and settings.auto_log_request is False:
            # 直接调用 开源 requests
            return requests.delete(url, **kwargs)

        self.logger.info("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Requests DELETE Start:")
        self.logger.info("--------------- URL: " + url)

        if len(kwargs.keys()) > 0:
            self.logger.info(self.pformat(kwargs))

        # call requests.delete()
        response = requests.delete(url, **kwargs)

        self.logger.info("\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Response:")
        self.logger.info(response)

        # todo
        if response.status_code == 200:
            try:
                self.logger.info(self.pformat(response.json()))
            except BaseException:
                return response

        self.logger.info("\n\n")

        return response
