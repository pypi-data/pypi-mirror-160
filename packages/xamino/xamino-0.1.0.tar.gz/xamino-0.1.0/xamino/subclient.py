from .__init__ import *
from . import client

class SubClient(client.Client):
    def __init__(self, ndcId, accountInfo):
        super().__init__(ndcId, accountInfo)
        self._ndcId: str = ndcId
        self.sid = accountInfo["sid"]
        self.auid = accountInfo["auid"]

    def edit_profile(self, nickname: str = None, content: str = None, icon: str = None):
        """
        Edits community profile.
            
            **Parameters**
            - `nickname`: str - username
            - `content`: str - bio

            **Returns**
            - `response`: dict - response from api
        """
        url = "{}/api/v1/x{}/s/user-profile/{}".format(self.api, self._ndcId, self.auid)
        data = {
            "timestamp": int(time() * 1000)
        }
        if nickname is not None:    data["nickname"] = nickname
        if content is not None:     data["content"] = content
        if icon is not None:        data["icon"] = self.uploadMedia(icon, "image")

        return self._httpx("POST", url, data)
    
    def checkIn(self, timezone: int = -300):
        """
        Checks in to community.
            
            **Parameters**
            - `timezone`: int - timezone offset in minutes
                
                **Returns**
                - `response`: dict - response from api
        """
        url = "{}/api/v1/x{}/s/check-in".format(self.api, self._ndcId)
        data = {
            "timestamp": int(time() * 1000),
            "timezone": timezone
        }
        return self._httpx("POST", url, data)
    
    def playLottery(self, timezone: int = -300):
        """
        Plays lottery.
            
            **Parameters**
            - `timezone`: int - timezone offset in minutes
                
                **Returns**
                - `response`: dict - response from api
        """
        url = "{}/api/v1/x{}/s/check-in/lottery".format(self.api, self._ndcId)
        data = {
            "timestamp": int(time() * 1000),
            "timezone": timezone
        }
        return self._httpx("POST", url, data)

    def liveLayerChats(self, start: int = 0, size: int = 25, key: str = None):
        """
        Gets live layer chats.
            
            **Parameters**
            - `start`: int - start index
            - `size`: int - size of the list
                
                **Returns**
                - `response`: dict - response from api
        """
        url = "{}/api/v1/x{}/s/live-layer/public-live-chats?start={}}&size={}".format(self.api, self._ndcId, start, size)
        return self._httpx("GET", url) if key is None else self.objects(self._httpx("GET", url), key)
    
    def getNotifications(self, size: int = 25, key: str = None):
        """
        Gets notifications.
            
            **Parameters**
            - `size`: int - size of the list
                    
                **Returns**
                - `response`: dict - response from api
        """
        url = "{}/api/v1/x{}/s/notification?pagingType=t&size={}".format(self.api, self._ndcId, size)
        return self._httpx("GET", url) if key is None else self.objects(self._httpx("GET", url), key)

    def getLatestBlogs(self, size: int = 25, key: str = None):
        """
        Gets latest blogs.
            
            **Parameters**
            - `size`: int - size of the list
                
                **Returns**
                - `response`: dict - response from api
        """
        url = "{}/api/v1/x{}/s/feed/blog-all?pagingType=t&size={}".format(self.api, self._ndcId, size)
        return self._httpx("GET", url) if key is None else self.objects(self._httpx("GET", url), key)

    def postBlog(self, title: str, content: str, image: str = None):
        """
        Posts blog.
            
            **Parameters**  
            - `title`: str - title
            - `content`: str - content
            - `image`: image 
                    
                **Returns**
                - `response`: dict - response from api
        """
        url = "{}/api/v1/x{}/s/blog".format(self.api, self._ndcId)
        data = {
            "title": title,
            "content": content,
            "timestamp": int(time() * 1000),
            "mediaList": [self.uploadMedia(image, "image")] if image is not None else []
        }
        return self._httpx("POST", url, data)

    def deleteBlog(self, blogId: str):
        """
        Deletes blog.
            
            **Parameters**
            - `blogId`: str - blog id
                    
                **Returns**
                - `response`: dict - response from api
        """
        url = "{}/api/v1/x{}/s/blog/{}".format(self.api, self._ndcId, blogId)
        return self._httpx("DELETE", url)
    
    def postWiki(self, title: str, content: str, image: str = None, keyword: str = None):
        """
        Posts wiki.
            
            **Parameters**
            - `title`: str - title
            - `content`: str - content
            - `image`: image 
            - `keywords`: str - keywords
                        
                **Returns**
                - `response`: dict - response from api
        """
        url = "{}/api/v1/x{}/s/item".format(self.api, self._ndcId)
        data = {
            "label": title,
            "content": content,
            "icon": self.uploadMedia(image, "image") if image is not None else "",
            "keywords": keyword,
            "timestamp": int(time() * 1000),
            "mediaList": [self.uploadMedia(image, "image")] if image is not None else [],
            "props": [{
                "title": "My Rating",
                "value": "5",
                "type": "levelStar"
            }]
        }
        return self._httpx("POST", url, data)

    def deleteWiki(self, wikiId: str):
        """
        Deletes wiki.
            
            **Parameters**
            - `wikiId`: str - wiki id
                    
                **Returns**
                - `response`: dict - response from api
        """
        url = "{}/api/v1/x{}/s/item/{}".format(self.api, self._ndcId, wikiId)
        return self._httpx("DELETE", url)

    def commentOnRecentBlogs(self, comments: list, size: int = 25, sleep_per_comment: int = 3):
        """
        Comments on recent blogs.
            
            **Parameters**
            - `comments`: list - comments
            - `size`: int - size of the list
                        
                **Returns**
                - `response`: dict - response from api
        """
        latest_blogs = self.getLatestBlogs(size=size, key="blogId")
        for blog in latest_blogs:
            url = "{}/api/v1/x{}/s/blog/{}/comment".format(self.api, self._ndcId, blog)
            sleep(sleep_per_comment)
            data = {
                "content": choice(comments),
                "mediaList": [],
                "type": 0,
                "eventSource": "FeedList",
                "timestamp": int(time() * 1000)
            }
            return self._httpx("POST", url, data)

    def commentOnBlog(self, blogId: str):
        """
        Comments on blog.
            
            **Parameters**
            - `blogId`: str - blog id
                    
                **Returns**
                - `response`: dict - response from api
        """
        url = "{}/api/v1/x{}/s/blog/{}/comment".format(self.api, self._ndcId, blogId)
        data = {
            "content": "This is a comment",
            "mediaList": [],
            "type": 0,
            "eventSource": "FeedList",
            "timestamp": int(time() * 1000)
        }
        return self._httpx("POST", url, data)

    def deleteCommentOnBlog(self, blogId: str, commentId: str):
        """
        Deletes comment on blog.
            
            **Parameters**
            - `blogId`: str - blog id
            - `commentId`: str - comment id
                    
                **Returns**
                - `response`: dict - response from api
        """
        url = "{}/api/v1/x{}/s/blog/{}/comment/{}".format(self.api, self._ndcId, blogId, commentId)
        return self._httpx("DELETE", url)

    def likeRecentBlogs(self, size: int = 25):
        """
        Likes recent blogs.
        
            **Parameters**
            - `size`: int - size of the list
            
                **Returns**
                - `response`: dict - response from api
                        
        """
        latest_blogs = self.getLatestBlogs(size=size, key="blogId")
        for blog in latest_blogs:
            url = "{}/api/v1/x{}/s/blog/{}/vote".format(self.api, self._ndcId, blog)
            data = {
                "value": 4,
                "eventSource": "FeedList",
                "timestamp": int(time() * 1000)
            }
            return self._httpx("POST", url, data)
    
    def unlikeRecentBlogs(self, size: int = 25):
        """
        Unlikes recent blogs.
        
            **Parameters**
            - `size`: int - size of the list
            
                **Returns**
                - `response`: dict - response from api
                        
        """
        latest_blogs = self.getLatestBlogs(size=size, key="blogId")
        for blog in latest_blogs:
            url = "{}/api/v1/x{}/s/blog/{}/vote".format(self.api, self._ndcId, blog)
            return self._httpx("DELETE", url)

    def likeBlog(self, blogId: str):
        """
        Likes blog.
        
            **Parameters**
            - `blogId`: str - blog id
            
                **Returns**
                - `response`: dict - response from api
                        
        """
        url = "{}/api/v1/x{}/s/blog/{}/vote".format(self.api, self._ndcId, blogId)
        data = {
            "value": 4,
            "eventSource": "FeedList",
            "timestamp": int(time() * 1000)
        }
        return self._httpx("POST", url, data)

    def unlikeBlog(self, blogId: str):
        """
        Unlikes blog.
        
            **Parameters**
            - `blogId`: str - blog id
            
                **Returns**
                - `response`: dict - response from api
                        
        """
        url = "{}/api/v1/x{}/s/blog/{}/vote".format(self.api, self._ndcId, blogId)
        return self._httpx("DELETE", url)
    
    def generateInviteCode(self):
        """
        Generates invite code.
        
            **Returns**
            - `inviteCode`: str - invite code
        """
        url = "{}/api/v1/g/s-x{}/community/invitation".format(self.api, self._ndcId)
        data = {
            "duration": 0,
            "force": "true",
            "timestamp": int(time() * 1000)
        }
        return self.objects(self._httpx("POST", url, data), "inviteCode")

    def getAllUsers(self, type: str = "recent", start: int = 0, size: int = 25, key: str = None):
        """
        Gets all users.
        
            **Parameters**
            - `type`: str - "curators", "leaders", "recent", "all"
            - `start`: int - start index
            - `size`: int - size of the list
            - `key`: list - returns data based on key 
                
                **Returns**
                - `response`: dict or list - json response or list of users[key]
        """
        url = "{}/api/v1/x{}/s/user-profile?type={}&start={}&size={}"
        urls = []
        data = []

        if key is None:
            return self._httpx("GET", url.format(self.api, self._ndcId, type, start, size))

        if type == "all":
            urls.append(url.format(self.api, self._ndcId, "curators", start, size))
            urls.append(url.format(self.api, self._ndcId, "leaders", start, size))
            urls.append(url.format(self.api, self._ndcId, "recent", start, size))

        else:
            urls.append(url.format(self.api, self._ndcId, type, start, size))

        for url in urls:
            data.append(self.objects(self._httpx("GET", url), key))

        return [item for sublist in data for item in sublist]
    
    def getPublicChats(self, type: str = "recommended", start: int = 0, size: int = 25, key: str = None):
        """
        Gets public chat threads
        
            **Parameters**
            - `type`: str - "recommended", "latest", "popular"
            - `start`: int - start index
            - `size`: int - size of the list
            - `key`: list - returns data based on key 
                
                **Returns**
                - `response`: dict or list - json response or list of chat threads[key]
        """
        url = "{}/api/v1/x{}/s/chat/thread?type=public-all&filterType={}&start={}&size={}".format(self.api, self._ndcId, type, start, size)
        if key is None: return self._httpx("GET", url)
        return self.objects(self._httpx("GET", url), key)

    def getLeaderboardUsers(self, type: int = 1, start: int = 0, size: int = 25, key: str = None):
        """
        Gets leaderboard users.
        
            **Parameters**
            - `type`: int -
            1 - active 24 hrs,
            2 - active 7 days,
            3 - hall of fame,
            4 - highest check-in,
            5 - highest quiz scores
            - `start`: int - start index
            - `size`: int - size of the list
            - `key`: list - returns data based on key 
                
                **Returns**
                - `response`: dict or list - json response or list of users[key]
        """
        url = "{}/api/v1/g/s-x{}/community/leaderboard?rankingType={}&start={}&size={}".format(self.api, self._ndcId, type, start, size)
        if key is None: return self._httpx("GET", url)
        return self.objects(self._httpx("GET", url), key)

    def inviteToChat(self, chatId: str, auid: str or list):
        """
        || Invite a user to chat ||

        **Parameters**
        - `chatId`: str - chat id
        -   auid: str or list
        """
        url = "{}/api/v1/x{}/s/chat/thread/{}/member/invite".format(self.api, self._ndcId, chatId)
        if type(auid) == str:
            auid = [auid]
        data = {
            "type": 0,
            "inviteeUids": auid,
            "timestamp": int(time() * 1000)
        }
        return self._httpx("POST", url, data)
    
    def follow(self, userId: str or list):
        """
        Follows user.
        
            **Parameters**
            - `userId`: str or list - user id
            
                **Returns**
                - `response`: dict - response from api
                        
        """
        if isinstance(userId, str):
            url = "{}/api/v1/x{}/s/user-profile/{}/member"

        elif isinstance(userId, list):
            data = {
                "targetUidList": userId,
                "timestamp": int(time() * 1000)
            }
            url = "{}/api/v1/x{}/s/user-profile/{}/joined".format(self.api, self._ndcId, self.auid)
            return self._httpx("POST", url, data)

        return self._httpx("POST", url.format(self.api, self._ndcId, userId))

    def unfollow(self, userId: str):
        """
        Unfollows user.
        
            **Parameters**
            - `userId`: str - user id
            
                **Returns**
                - `response`: dict - response from api
                        
        """
        url = "{}/api/v1/x{}/s/user-profile/{}/member".format(self.api, self._ndcId, userId)
        return self._httpx("DELETE", url)

    def block(self, userId: str):
        url = "{}/api/v1/x{}/s/block/{}".format(self.api, self._ndcId, userId)
        return self._httpx("POST", url)

    def unblock(self, userId: str):
        url = "{}/api/v1/x{}/s/block/{}".format(self.api, self._ndcId, userId)
        return self._httpx("DELETE", url)

    def deleteMessage(self, chatId: str, messageId: str, asModerator: bool = False, reason: str = None):
        data = {
            "adminOpName": 102,
            "timestamp": int(time() * 1000),
        }
        if asModerator: data["adminOpNote"] = {"content": reason}

        if not asModerator:  url = "{}/api/v1/x{}/s/chat/thread/{}/message/{}".format(self.api, self._ndcId, chatId, messageId)
        else: url = "{}/api/v1/x{}/s/chat/thread/{}/message/{}/admin".format(self.api, self._ndcId, chatId, messageId)

        return self._httpx("DELETE", url, data)

    def joinChat(self, chatId: str):
        url = "{}/api/v1/x{}/s/chat/thread/{}/member".format(self.api, self._ndcId, chatId)
        return self._httpx("POST", url)

    def leaveChat(self, chatId: str):
        url = "{}/api/v1/x{}/s/chat/thread/{}/member".format(self.api, self._ndcId, chatId)
        return self._httpx("DELETE", url)

    def deleteChat(self, chatId: str):
        url = "{}/api/v1/x{}/s/chat/thread/{}".format(self.api, self._ndcId, chatId)
        return self._httpx("DELETE", url)
        
    def subscribe(self, userId: str, autoRenew: str = False, transactionId: str = None):
        if transactionId is None: transactionId = str(UUID(hexlify(urandom(16)).decode('ascii')))

        url = "{}/api/v1/x{}/s/influencer/{}/subscribe".format(self.api, self._ndcId, userId)
        data = {
            "paymentContext": {
                "transactionId": transactionId,
                "isAutoRenew": autoRenew
            },
            "timestamp": int(time() * 1000)
        }
        return self._httpx("POST", url, data)

    def getUserFollowing(self, userId: str, start: int = 0, size: int = 25, key: list = None):
        url = "{}/api/v1/x{}/s/user-profile/{}/joined?start={}&size={}".format(self.api, self._ndcId, userId, start, size)
        if key is None: return self._httpx("GET", url)
        return self.objects(self._httpx("GET", url), key)

    def getUserFollowers(self, userId: str, start: int = 0, size: int = 25, key: list = None):
        url = "{}/api/v1/x{}/s/user-profile/{}/member?start={}&size={}".format(self.api, self._ndcId, userId, start, size)
        if key is None: return self._httpx("GET", url)
        return self.objects(self._httpx("GET", url), key)