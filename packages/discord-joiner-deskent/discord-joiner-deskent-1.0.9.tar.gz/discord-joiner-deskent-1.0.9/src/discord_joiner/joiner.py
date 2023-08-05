import json
import random
import asyncio

from base64 import b64encode
import requests
from myloguru import get_logger
from urllib3 import disable_warnings

disable_warnings()


class DiscordJoiner:
    """
    Adds user token by invite link to discord server
    using proxy (optional)

        Attributes
        token: str
            Discord account token will be joined

        invite_link: str
            Invite link to channel

        log_level: int [Optional] = 20
            by default: 20 (INFO)

        proxy: dict [Optional] = None
             example: proxy = {
                "http": "http://user:pass@10.10.1.10:3128/",
                "https": "https://user:pass@10.10.1.10:3128/",

                }
        user_agent: str [Optional] =
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36
        (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36"

        delay: int [Optional] = 2
            Delay between requests, in seconds

        logger=None
            By default will be used my_loguru logger by Deskent

            (pip install myloguru-deskent)

    Methods
        join
            returns: bool
    """

    def __init__(
            self, token: str, invite_link: str, proxy: dict = None,
            delay: int = 2, user_agent: str = '', log_level: int = 20,
            logger=None
    ):
        self.__token: str = token
        self.__headers: dict = {}
        self.__invite_link: str = invite_link
        self.__user_agent = (
            user_agent
            if user_agent
            else ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36")
        )
        self.__session = None
        self.__locale: str = ''
        self.__invite_id: str = ''
        self.__discord_username: str = ""
        self.__proxy: dict = proxy if proxy else {}
        self.__xsuperproperties: bytes = b''
        self.__delay: int = delay
        self.__logger = logger if logger else get_logger(log_level)

    async def _update_proxy(self):
        if self.__proxy:
            self.__session.proxies.update(proxies=self.__proxy)
            self.__logger.debug("\n\tProxy updated: OK")

    async def __get_headers(self):
        self.__session.headers.update(
            {
                'user-agent': self.__user_agent, 'accept': '*/*',
                'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7',
                'content-type': 'application/json',
                'origin': 'https://discord.com', 'referer': self.__invite_link,
                'x-super-properties': self.__xsuperproperties
            }
        )
        self.__logger.debug("\n\tHeaders: OK")

    async def __get_finger_print(self) -> bool:
        params = {
            "url": "https://discord.com/api/v7/experiments",
            "verify": False
        }
        response: 'requests.Response' = await self.__send_request(params)
        if response and response.status_code == 200:
            fingerprint = json.loads(response.text)["fingerprint"]
            self.__session.headers.update({'X-Fingerprint': fingerprint,
                                           'x-discord-locale': self.__locale,
                                           'authorization': self.__token})
            self.__logger.debug(f'\n\tFingerPrints: OK')
            return True
        response_text = '' if not response else response.text
        self.__logger.debug(f'\n\tFingerPrints: ERROR: {response_text}')

    async def __authorization(self) -> bool:
        params = {
            "url": 'https://discordapp.com/api/v9/users/@me',
            "verify": False
        }
        response: 'requests.Response' = await self.__send_request(params)
        if response and 'username' in json.loads(response.text):
            self.__discord_username = json.loads(response.text)['username']
            self.__logger.debug(f'\n\tAuthorization: @{self.__discord_username}')
            self.__session.headers['__sdcfduid'] = response.cookies['__sdcfduid']
            return True
        self.__logger.debug(f'\n\tAuthorization: Error: Invalid_token')

    async def __update_invite_id(self) -> bool:
        self.__invite_id = self.__invite_link
        if self.__invite_link.startswith(('https://discord.com/invite/', 'https://discord.gg')):
            self.__invite_id = self.__invite_link.split('/')[-1]
            return True

    async def __get_xcontext_properties(self):
        params = {
            "url": f'https://discord.com/api/v7/invites/{self.__invite_id}',
        }
        response: 'requests.Response' = await self.__send_request(params)
        try:
            data = json.loads(response.text)
        except Exception as err:
            self.__logger.error(err)
            return False
        location_guild_id = data['guild']['id']
        location_channel_id = data['channel']['id']

        base64_encode_data = b64encode(bytes(
            '{"location":"Accept Invite Page","location_guild_id":"'
            + str(location_guild_id)
            + '","location_channel_id":"'
            + str(location_channel_id)
            + '","location_channel_type":0}', 'utf-8'
        )).decode('utf-8')

        self.__session.headers['x-context-properties'] = base64_encode_data
        self.__logger.debug("\n\tx-context-properties: OK")
        return True

    async def __join(self) -> bool:
        params = {
            "url": f'https://discord.com/api/v7/invites/{self.__invite_id}',
            "json": {},
            "verify": False
        }
        response: 'requests.Response' = await self.__send_request(params, request_type="post")
        if not response:
            self.__logger.debug(f'\n\tJoin: [@{self.__discord_username}] Ошибка No response')
            return False
        if response.status_code != 200:
            if json.loads(response.text)['code'] == 40007:
                self.__logger.debug(f'\n\tJoin: [@{self.__discord_username}] Ошибка при входе на канал, вы забанены на канале')
                return False
            self.__logger.debug(f'\n\tJoin: [@{self.__discord_username}] Ошибка при входе на канал, ответ: {response.text}')
            return False
        channel_name = json.loads(response.text)['guild']['name']
        channel_id = json.loads(response.text)['guild']['id']
        text = (
            f'\n\tJoin: @{self.__discord_username} успешно вступил в канал {channel_name}'
            f'\n\tServer id: {channel_id}')
        self.__logger.debug(text)
        return True

    async def __get_xsuperproperties(self) -> None:
        browser_version = str(self.__user_agent.split('Chrome/')[-1].split(' ')[0])
        self.__locale = random.choice(['za', 'et', 'ae', 'bh', 'dz', 'eg', 'iq', 'jo', 'kw', 'lb',
                                       'ly', 'ma',
                                       'cl', 'om', 'qa', 'sa', 'sd', 'sy', 'tn', 'ye', 'in', 'az',
                                       'ru', 'by',
                                       'bg', 'bd', 'in', 'cn', 'fr', 'es', 'fr', 'cz', 'gb', 'dk',
                                       'at', 'ch',
                                       'de', 'li', 'lu', 'de', 'mv', 'cy', 'gr', '029', 'au', 'bz',
                                       'ca', 'cb',
                                       'gb', 'ie', 'in', 'jm', 'mt', 'my', 'nz', 'ph', 'sg', 'tt',
                                       'us', 'za',
                                       'zw', 'ar', 'bo', 'cl', 'co', 'cr', 'do', 'ec', 'es', 'gt',
                                       'hn', 'mx',
                                       'ni', 'pa', 'pe', 'pr', 'py', 'sv', 'us', 'uy', 've', 'ee',
                                       'es', 'ir',
                                       'fi', 'ph', 'fo', 'be', 'ca', 'ch', 'fr', 'lu', 'mc', 'nl',
                                       'ie', 'gb',
                                       'ie', 'es', 'fr', 'in', 'il', 'in', 'ba', 'hr', 'de', 'hu',
                                       'am', 'id',
                                       'ng', 'cn', 'id', 'is', 'ch', 'it', 'il', 'jp', 'ge', 'kz',
                                       'gl', 'kh',
                                       'in', 'in', 'kr', 'kg', 'lu', 'la', 'lt', 'lv', 'nz', 'mk',
                                       'in', 'mn',
                                       'ca', 'in', 'bn', 'my', 'mt', 'no', 'np', 'be', 'nl', 'no',
                                       'no', 'za',
                                       'fr', 'in', 'in', 'pl', 'af', 'af', 'br', 'pt', 'gt', 'bo',
                                       'ec', 'pe',
                                       'ch', 'mo', 'ro', 'mo', 'ru', 'rw', 'ru', 'in', 'fi', 'no',
                                       'se', 'lk',
                                       'sk', 'si', 'no', 'se', 'no', 'se', 'fi', 'fi', 'al', 'ba',
                                       'cs', 'me',
                                       'rs', 'sp', 'fi', 'se', 'ke', 'sy', 'in', 'in', 'th', 'tm',
                                       'qs', 'za',
                                       'tr', 'ru', 'cn', 'ua', 'pk', 'uz', 'vn', 'sn', 'za', 'ng',
                                       'cn', 'hk',
                                       'mo', 'sg', 'tw', 'za'])
        xsuperproperties = ''.join((
            '{"os":"Windows","browser":"Chrome","device":"","system_locale":"',
            self.__locale,
            '","browser_user_agent":"',
            self.__user_agent,
            '","browser_version":"',
            browser_version,
            '","os_version":"',
            str(random.choice(['7', '10', 'xp', 'vista', '11'])),
            (
                '","referrer":"https://www.yandex.ru/clck/jsredir?from=yandex.ru;suggest;browser&text=",'
                '"referring_domain":"www.yandex.ru",'
                '"referrer_current":"https://www.yandex.ru/clck/jsredir?from=yandex.ru;suggest;browser&text=",'
                '"referring_domain_current":"www.yandex.ru","release_channel":"stable","client_build_number":'
            ),
            str(random.randint(100000, 199999)),
            ',"client_event_source":null}'
        ))
        self.__xsuperproperties: bytes = b64encode(str(xsuperproperties).encode('utf-8'))

    async def __send_request(self, params: dict, request_type: str = "get"):
        await asyncio.sleep(self.__delay)
        try:
            if request_type == "post":
                response = self.__session.post(**params)
            else:
                response = self.__session.get(**params)

            if 'retry_after' in response.text:
                sleep_time = float(json.loads(response.text)['retry_after'])
                self.__logger.debug(f'Cooldown, sleeping for {sleep_time} seconds.')
                await asyncio.sleep(sleep_time)
                return await self.__send_request(params, request_type)
            if response.status_code == 200:
                return response
            self.__logger.error(response.text)
        except Exception as err:
            self.__logger.error(err)

        return ''

    async def join(self) -> dict:
        """Add user with token to server by invite link

        :returns: dict {'success': True, 'token': token} if done
        else {'success': False, 'token': token, 'message': ...}
        """

        self.__logger.debug(f'TOKEN: {self.__token}:')
        result = {'success': False, 'token': self.__token}
        if not await self.__update_invite_id():
            result.update(message="Wrong invite link")
            return result
        self.__session = requests.Session()
        await self._update_proxy()
        await self.__get_xsuperproperties()
        await self.__get_headers()

        if not await self.__get_finger_print():
            result.update(message="Fingerprint error")
            return result
        if not await self.__authorization():
            result.update(message="Authorization error")
            return result
        if not await self.__get_xcontext_properties():
            result.update(message="X-content properties error")
            return result

        if not await self.__join():
            result.update(message="Joining error")
            return result

        result.update(success=True)
        return result
