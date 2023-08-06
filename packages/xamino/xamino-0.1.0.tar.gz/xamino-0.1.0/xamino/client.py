from .__init__ import *
from . import utilities as utils
class Client():
    def __init__(self, debug: bool = False, device_id: str = None, proxy_login: str = None, proxy_session: str = None, sleep_per_request: int = 0, rateLimit_: bool = False):
        self.api = "https://service.narvii.com"
        self.debug: bool = debug if debug is not None else False
        if self.debug is True:
            utils.printr("Debug Mode Enabled")
        self.sid: str = None
        self.auid: str = None
        self.secret: str = None
        self.device_id: str = device_id if device_id is not None else utils.generate_device_id()
        self._user_agent: str =  "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
        self.login_session = httpx(proxies = proxy_login) if proxy_login is not None else httpx()
        self.session = httpx(proxies = proxy_session) if proxy_session is not None else httpx()
        self.sleep_per_request: int = sleep_per_request if sleep_per_request != 0 else 0
        self._rateLimit_: bool = rateLimit_ if rateLimit_ is not None else False
        self._RateLimitFunctionCalled: int = 0
        self._headers = {
            "user-agent": self._user_agent,
            "accept-language": "en-US",
            "content-type": "application/json; charset = utf-8",
            "host": "service.narvii.com",
            "accept-encoding": "gzip",
            "connection": "Upgrade"
        }
    
    def _rateLimit(self):
        """
        Rate Limit Function
        """
        self._RateLimitFunctionCalled += 1
        if self._RateLimitFunctionCalled >= 10:
            self._RateLimitFunctionCalled = 0
            sleep(self.sleep_per_request)


    def _httpx(self, method: str, url: str, data: dict = None, type: str = None):
        """
        HTTPX - Request Function

            **Parameters**
            - `method`: str - HTTP Method
            - `url`: str - URL
            - `data`: dict - Data

            **Returns**
            - `response`: dict - Response

        """
        utils.printwr("{}: {}".format(method, url))
        headers = self._headers.copy()
        headers["ndcdeviceid"] = utils.generate_device_id()

        if self.sid is not None:
            headers["ndcauth"] = "sid={}".format(self.sid)
        if self.auid is not None:
            headers["auid"] = self.auid

        if data is not None:
            if type:
                headers["content-type"] = type
            elif type is None:
                data = dumps(data)
            headers["content-length"] = str(len(data))
            headers["ndc-msg-sig"] = utils.generate_signature(DATA = data)

        if self.debug is True:
            print(f"{data}")
            print(f"{headers}")

        if self._rateLimit_ is True:
            self._rateLimit()

        try:
            r = self.session.request(method, url, data = data, headers = headers)
        except httpxReadTimeout as error:
            utils.printwr("error: {}".format(error))

        utils.printr('\n{{"status_code": {}, "url": {}}}'.format(r.status_code, url))

        if r.status_code != 200:
            utils.printrb(loads(r.text))
            try:
                json_object = loads(r.text)
                if json_object["title"] == "Verify Account":
                    return json_object["url"]
            except KeyError:
                return None
        else:
            return loads(r.text)

    def storeSessions(self, session: dict):
        """
        Store Sessions
            
            **Parameters**
            - `session`: dict - Session
            
        """
        sessions = self.storedSessions()
        sessions.append(session)
        open("sessions.json", "w").write(dumps(sessions, indent = 4))

    def storedSessions(self) -> dict:
        """
        Stored Sessions
            
            **Returns**
            - `sessions`: dict - Stored Sessions

        """
        return loads(open("sessions.json", "r").read())
    
    def updateSession(self, email: str, sid: str):
        """
        Update sid in session
            
            **Parameters**
            - `session`: dict - Session
            
        """
        sessions = self.storedSessions()
        for session in sessions:
            if email == session["email"]:
                session["sid"] = sid
                open("sessions.json", "w").write(dumps(sessions, indent = 4))
                return
        return None

    def objects(self, data: dict, key: str) -> list:
        return utils._get_entities_(data, key)

    def object(self, data: dict, key: list):
        return utils._get_entity_(data, key)

    def returnSession(self, email) -> dict:
        """
        Return Session
            
            **Parameters**
            - `email`: str - Email
            
            **Returns**
            - `session`: dict - Session
            
        """
        sessions = self.storedSessions()
        for session in sessions:
            if email == session["email"]:
                return session
        return None

    def checkForSession(self, email: str) -> bool:
        """
        Check For Session

            **Parameters**
            - `email`: str - Email

            **Returns**
            - `accountInfo`: dict - Account Info

        """
        session = self.returnSession(email)

        if session is not None:
            self.sid = session["sid"]
            self.auid = session["auid"]
            self.secret = session["secret"]
            authenticated = self.authenticate()
            if authenticated is not None:
                utils.printwr({"status": 200, "message": "Successfully Authenticated"})
                return authenticated
            authenticated = self.login_secret(session["secret"])
            if authenticated is not None:
                utils.printwr({"status": 200, "message": "Successfully Authenticated"})
                self.updateSession(email, self.object(authenticated, "sid"))
                return authenticated
            else:
                utils.printr({"status": 401, "message": "Failed to Authenticate"})
                return False

    def login(self, email: str, password: str, device_id: str = None):
        """
        Login Function
            
            **Parameters**
            - `email`: str - Email
            - `password`: str - Password
            - `device_id`: str - Device ID
            
            **Returns**
            - `accountInfo`: dict - Account Info
        """
        url = "{}/api/v1/g/s/auth/login".format(self.api)

        session = self.checkForSession(email)

        if session is not None:
            return session

        else:

            data = {
                "email": email,
                "v": 2,
                "secret": "0 {}".format(password),
                "deviceID": device_id if device_id is not None else self.device_id,
                "clientType": 100,
                "action": "normal",
                "timestamp": int(time() * 1000)
            }
            self.accountInfo = self._httpx("POST", url, data)

            if (self.accountInfo is not None and isinstance(self.accountInfo, dict)):
                self.sid = self.object(self.accountInfo, "sid")
                self.secret = self.object(self.accountInfo, "secret")
                self.auid = self.object(self.accountInfo, "auid")

                self.storeSessions({
                    "email": email,
                    "password": password,
                    "device": device_id if device_id is not None else self.device_id,
                    "sid": self.sid,
                    "secret": self.secret,
                    "auid": self.auid
                })
                
                return self.accountInfo

    def authenticate(self):
        """
        Authenticate Session
            
            **Returns**
            - `accountInfo`: dict - Account Info

        """
        url = "{}/api/v1/g/s/account".format(self.api)
        accountInfo = self._httpx("GET", url)
        data = {
            "auid": self.auid,
            "sid": self.sid,
        }
        self.accountInfo = {**data, **accountInfo} if accountInfo is not None else None
        return self.accountInfo
    
    def login_secret(self, secret: str = None, device_id: str = None):
        """
        Login Using Secret
            
            **Parameters**
            - `secret`: str - Secret
            - `device_id`: str - Device ID

            **Returns**
            - `accountInfo`: dict - Account Info
        """

        url = "{}/api/v1/g/s/auth/login".format(self.api)

        data = {
            "secret": secret if secret is not None else self.secret,
            "deviceID": device_id if device_id is not None else self.device_id,
            "clientType": 100,
            "action": "normal",
            "timestamp": int(time() * 1000)
        }

        self.auth = self._httpx("POST", url, data)
        self.sid = self.object(self.auth, "sid")
        self.secret = secret if secret is not None else self.secret
        self.auid = self.object(self.auth, "auid")

        return self.auth

    def verifyLogin(self, email: str, password: str, device_id: str = None):
        """
        Verifies login 
            
            **Parameters**
            - `email`: str - Email
            - `password`: str - Password
            - `device_id`: str - Device ID
            
            **Returns**
            - `verifyInfoKey`: str - Verify Info Key
        """
        url = "{}/api/v1/g/s/auth/login".format(self.api)

        data = {
            "email": email,
            "v": 2,
            "secret": "0 {}".format(password),
            "deviceID": device_id if device_id is not None else self.device_id,
            "clientType": 100,
            "action": "normal",
            "timestamp": int(time() * 1000)
        }
        url = self._httpx("POST", url, data)
        if not isinstance(url, str): return None
        else: return url.split('k=')[1].split('&')[0]

    def getUserInfo(self, user_id: str, key: str = None):
        """
        Get User Info
            
            **Parameters**
            - `user_id`: str - User ID
            - `key`: str - Key
            
            **Returns**
            - `userInfo`: dict - User Info
            
        """
        url = "{}/api/v1/g/s/user-profile/{}".format(self.api, user_id)
        return self._httpx("GET", url) if key is None else self.object(self._httpx("GET", url), key)

    def joinCommunity(self, community_id: str):
        """
        Join Community
            
            **Parameters**
            - `community_id`: str - Community ID
            
            **Returns**
            - `communityUserInfo`: dict - Community User Info
            
        """
        url = "{}/api/v1/x{}/s/community/join".format(self.api, community_id)
        return self._httpx("POST", url)

    def leaveCommunity(self, community_id: str):
        """
        Leave Community
            
            **Parameters**
            - `community_id`: str - Community ID
            
            **Returns**
            - `api:message`  - API Message
            
        """
        url = "{}/api/v1/x{}/s/community/leave".format(self.api, community_id)
        return self._httpx("POST", url)
    
    def getCommunityInfo(self, community_id: str, key: str = None):
        """
        Get Community Info
            
            **Parameters**
            - `community_id`: str - Community ID
            - `key`: str - Key
            
            **Returns**
            - `communityInfo`: dict - Community Info

            - if key:
                **Returns**
                - `keyValue`: str - Key value from Community Info
            
        """
        url = "{}/api/v1/g/s-x{}/community/info".format(self.api, community_id)
        return self._httpx("GET", url) if key is None else self.object(self._httpx("GET", url), key)

    def joinedCommunities(self, key: str = None):
        """
        Get Info About Joined Communities

            **Parameters**
            - `key`: str - key

            **Returns**
            - if key:
                **Returns**
                - `keyValue`: str - Gets key value from all joined communities
        """
        url = "{}/api/v1/g/s/community/joined".format(self.api)
        return self._httpx("GET", url) if key is None else self.objects(self._httpx("GET", url), key)

    def joinChat(self, chat_id: str):
        """
        Join Chat
            
            **Parameters**
            - `chat_id`: str - Chat ID
            
            **Returns**
            - `api:message`  - API Message
            
        """
        url = "{}/api/v1/g/s/chat/thread/{}/member/{}".format(self.api, chat_id, self.auid)
        return self._httpx("POST", url)

    def leaveChat(self, chat_id: str):
        """
        Leave Chat
            
            **Parameters**
            - `chat_id`: str - Chat ID
            
            **Returns**
            - `api:message`  - API Message
            
        """
        url = "{}/api/v1/g/s/chat/thread/{}/member/{}".format(self.api, chat_id, self.auid)
        return self._httpx("DELETE", url)

    def getUserFollowers(self, user_id: str, start: int = 0, size: int = 25,  key: str = None):
        """
        Get User Followers
            
            **Parameters**
            - `user_id`: str - User ID
            - `start`: int - Start Index
            - `size`: int - Size of List
            - `key`: str - Key
            
            **Returns**
            - if key:
                **Returns**
                - `keyValue`: str - Gets key value from all followers
            
        """
        url = "{}/api/v1/g/s/user-profile/{}member?start={}&size={}".format(self.api, user_id, start, size)
        return self._httpx("GET", url) if key is None else self.objects(self._httpx("GET", url), key)

    def getUserFollowing(self, user_id: str, start: int = 0, size: int = 25,  key: str = None):
        """
        Get User Following
            
            **Parameters**
            - `user_id`: str - User ID
            - `start`: int - Start Index
            - `size`: int - Size of List
            - `key`: str - Key
            
            **Returns**
            - if key:
                **Returns**
                - `keyValue`: str - Gets key value from all following

        """
        url = "{}/api/v1/g/s/user-profile/{}joined?start={}&size={}".format(self.api, user_id, start, size)
        return self._httpx("GET", url) if key is None else self.objects(self._httpx("GET", url), key)

    def getGlobalChats(self, start: int = 0, size: int = 25,  key: str = None):
        """
        Get Global Chats
            
            **Parameters**
            - `start`: int - Start Index
            - `size`: int - Size of List
            - `key`: str - Key
            
            **Returns**
            - if key:
                **Returns**
                - `keyValue`: str - Gets key value from all global chats
            
        """
        url = "{}/api/v1/g/s/chat/thread/explore/categories?threadPreviewSize=20&language=en&start={}&size={}".format(self.api, start, size)
        return self._httpx("GET", url) if key is None else self.objects(self._httpx("GET", url), key)

    def searchForCommunity(self, query: str, key: str = None):
        """
        Search for Community
            
            **Parameters**
            - `query`: str - Query
            - `key`: str - Key
            
            **Returns**
            - if key:
                **Returns**
                - `keyValue`: str - Gets key value from all communities found

        """
        url = "{}/api/v1/g/s/community/search?q={}&language=en&completeKeyword=1&start=0&size=25".format(self.api, query)
        return self._httpx("GET", url) if key is None else self.objects(self._httpx("GET", url), key)
    
    def sendMessage(self, chat_id: str, message: str, messageType: int = 0):
        """
        Send Message
            
            **Parameters**
            - `chat_id`: str - Chat ID
            - `message`: str - Message
            
            **Returns**
            - `api:message`  - API Message
            
        """
        url = "{}/api/v1/g/s/chat/thread/{}/message".format(self.api, chat_id)
        data = {
            "type": messageType,
            "content": message,
            "timestamp": int(time() * 1000)
        }
        return self._httpx("POST", url, json=data)
    
    def deleteMessage(self, chat_id: str, message_id: str):
        """
        Delete Message
            
            **Parameters**
            - `chat_id`: str - Chat ID
            - `message_id`: str - Message ID
            
            **Returns**
            - `api:message`  - API Message
            
        """
        url = "{}/api/v1/g/s/chat/thread/{}/message/{}".format(self.api, chat_id, message_id)
        return self._httpx("DELETE", url)
    
    def verifyPassword(self, password: str):
        """
        Verify Password
            
            **Parameters**
            - `password`: str - Password
            
            **Returns**
            - `api:message`  - API Message
            
        """
        url = "{}/api/v1/g/s/auth/verify-password".format(self.api)
        data = {
            "deviceID": self.device_id,
            "secret": "0 {}".format(password),
            "timestamp": int(time() * 1000)
        }
        return self._httpx("POST", url, data=data)
    
    def requestSecurityValidation(self, email: str, device_id: str = None, resetPassword: bool = False, verifyInfoKey: str = None):
        """
        Request Security Validation
            
            **Parameters**
            - `email`: str - Email
            - `device_id`: str - Device ID

            **Returns**
            - `api:message`  - API Message

        """
        url = "{}/api/v1/g/s/auth/request-security-validation".format(self.api)
        data = {
            "type": 1,
            "identity": email,
            "deviceID": device_id if device_id else self.device_id,
            "timestamp": int(time() * 1000)
        }
        if resetPassword:
            data["level"] = 2
            data["purpose"] = "reset-password"
        
        if verifyInfoKey:
            data["verifyInfoKey"] = verifyInfoKey
            
        return self._httpx("POST", url, data=data)

    def checkSecurityValidation(self, email: str, code: str, device_id: str = None):
        """
        Check Security Validation
            
            **Parameters**
            - `email`: str - Email
            - `code`: str - Code
            - `device_id`: str - Device ID
                
                **Returns**
                - `api:message`  - API Message

        """
        url = "{}/api/v1/g/s/auth/check-security-validation".format(self.api)
        data = {
            "validationContext": {
                "type": 1,
                "identity": email,
                "data": {
                    "code": code
                }
            },
            "deviceID": device_id if device_id else self.device_id,
            "timestamp": int(time() * 1000)
        }
        return self._httpx("POST", url, data=data)

    def registerCheck(self, email: str, device_id: str = None):
        """
        Register Check
            
            **Parameters**
            - `email`: str - Email
            - `device_id`: str - Device ID
                
                **Returns**
                - `api:message`  - API Message

        """
        url = "{}/api/v1/g/s/auth/register-check".format(self.api)
        data = {
            "deviceID": device_id if device_id else self.device_id,
            "email": email,
            "timestamp": int(time() * 1000)
        }
        return self._httpx("POST", url, data=data)
    
    def updateEmail(self, email: str, password: str, new_code: str, device_id: str = None):
        """
        Update Email
                
                **Parameters**
                - `email`: str - Email
                - `password`: str - Password
                - `new_code`: str - New Code
                - `device_id`: str - Device ID
                    
                    **Returns**
                    - `api:message`  - API Message

        """
        url = "{}/api/v1/g/s/auth/update-email".format(self.api)
        data = {
            "deviceID": device_id if device_id else self.device_id,
            "secret": f"0 {password}",
            "newValidationContext": {
                "identity": email,
                "data": {
                    "code": new_code
                },
                "level": 1,
                "type": 1,
                "deviceID": device_id if device_id else self.device_id,
            },
            "timestamp": int(time() * 1000)
        }
        return self._httpx("POST", url, data=data)
    
    def getGlobalLink(self, user_id: str, key: str = None):
        """
        Get Global Link
            
            **Parameters**
            - `user_id`: str - User ID
            - `key`: str - Key
            
            **Returns**
            - `global link`: str - Global Link
            
        """
        aminoId = self.getUserInfo(user_id, key="aminoId")
        return "https://aminoapps.com/u/{}".format(aminoId)
    
    def getFromLink(self, link: str, key: str = None):
        """
        Get From Link
            
            **Parameters**
            - `link`: str - Link
            - `key`: str - example: "ndcId" or "objectId"
            
            **Returns**
            - `object id`: str - Object ID
            
        """
        if not link.startswith("https://aminoapps.com/"):
            raise ValueError("Invalid link")
        
        url = "{}/api/v1/g/s/link-resolution?q={}".format(self.api, link)
        return self._httpx("GET", url) if key is None else self.object(self._httpx("GET", url), key)
    
    def uploadMedia(self, file: str, fileType: str):
        """
        Upload Media
            
            **Parameters**
            - `file`: str - binary file
            - `fileType`: str - "audio" or "image"
            
            **Returns**
            - `media value`: str - Media Value
            
        """
        url = "{}/api/v1/g/s/media/upload".format(self.api)
        type = "audio" if fileType == "audio" else "image"

        return self.object(self._httpx("POST", url, data=file.read(), type=type), "mediaValue")

    def checkDeviceId(self, device_id: str):
        """
        Check Device ID
            
            **Parameters**
            - `device_id`: str - Device ID
            
            **Returns**
            - `api:message`  - API Message
            
        """
        url = "{}/api/v1/g/s/device".format(self.api)
        data = {
            "deviceID": device_id,
            "clientType": 100,
            "timezone": -timezone // 1000,
            "locale": localtime()[0],
            "timestamp": int(time() * 1000)
        }
        return self._httpx("POST", url, data=data)

    def registerAccount(self, nickname: str, email: str, password: str, device_id: str, code: str):
        """/
        Register Account
            
            **Parameters**
            - `nickname`: str - Nickname
            - `email`: str - Email
            - `password`: str - Password
            - `device_id`: str - Device ID
            - `code`: str - Code
            
            **Returns**
            - `api:message`  - API Message

        """
        url = "{}/api/v1/g/s/auth/register".format(self.api)
        data = {
        "secret": f"0 {password}",
        "deviceID": device_id,
        "email": email,
        "clientType": 100,
        "nickname": nickname,
        "validationContext": {
            "data": {
                "code": code
            },
            "type": 1,
            "identity": email
        },
        "type": 1,
        "identity": email,
        "timestamp": int(time() * 1000)
        }
        return self._httpx("POST", url, data=data)

    def totalCoins(self):
        """
        Total Coins
            
            **Returns**
            - `total coins`: int - Total Coins
            
        """
        url = "{}/api/v1/g/s/wallet".format(self.api)
        return self.object(self._httpx("GET", url), "totalCoins")

    def accountExistCheck(self, device_id: str, secret: str):
        """
        Account Exist Check
                
                **Parameters**
                - `device_id`: str - Device ID
                - `secret`: str - Secret
                
                **Returns**
                - `api:message`  - API Message

        """
        url = "{}/api/v1/g/s/auth/account-exist-check".format(self.api)
        data = {
            "deviceID": device_id,
            "secret": secret,
            "clientType": 100,
            "timestamp": int(time() * 1000)
        }
        return self._httpx("POST", url, data=data)

    def verifyAccount(self, verifyInfoKey: str, code:str, email: str, device_id: str):
        """
        Verify Account
                
                **Parameters**
                - `verifyInfoKey`: str - Verify Info Key
                - `code`: str - Code
                - `email`: str - Email
                - `device_id`: str - Device ID
                    
                    **Returns**
                    - `api:message`  - API Message
                        
            """
        url = "{}/api/v1/g/s/auth/verify-account".format(self.api)
        data = {
            "verifyInfoKey": verifyInfoKey,
            "validationContext": {
                "data": {
                    "code": code
                },
                "type": 1,
                "identity": email
            },
            "deviceID": device_id
        }
        return self._httpx("POST", url, data=data)
