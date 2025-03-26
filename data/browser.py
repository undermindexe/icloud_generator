import asyncio
import aiohttp
import ssl
import certifi


class Browser:
    base_url_v1 = "https://p154-maildomainws.icloud.com/v1/hme"
    base_url_v2 = "https://p154-maildomainws.icloud.com/v2/hme"
    info_url = "https://setup.icloud.com/setup/ws/1/validate"
    params = {
        "clientBuildNumber": "2511Project37",
        "clientMasteringNumber": "2511B20",
        "clientId": "",
        "dsid": "",
    }

    def __init__(self, label: str = ".", cookies: str = "", proxy: str = ""):
        self.label = label
        self.cookies = cookies
        self.proxy = proxy
        headers={
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Content-Type": "text/plain",
            "Accept": "*/*",
            "Sec-GPC": "1",
            "Origin": "https://www.icloud.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.icloud.com/",
            "Accept-Language": "en-US,en-GB;q=0.9,en;q=0.8,cs;q=0.7",
            "Cookie": self.cookies
        }

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(ssl_context=ssl.create_default_context(cafile=certifi.where())) 
        self.s = aiohttp.ClientSession(
            headers={
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                "Content-Type": "text/plain",
                "Accept": "*/*",
                "Sec-GPC": "1",
                "Origin": "https://www.icloud.com",
                "Sec-Fetch-Site": "same-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://www.icloud.com/",
                "Accept-Language": "en-US,en-GB;q=0.9,en;q=0.8,cs;q=0.7",
                "Cookie": self.cookies
            },
            timeout=aiohttp.ClientTimeout(total=10),
            connector=connector
        )

        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        await self.s.close()

    async def base_info(self):
        try:
            async with self.s.get(f"{self.info_url}", params=self.params, proxy = f"http://{self.proxy}") as resp:
                res = await resp.json()
                return res
        except asyncio.TimeoutError:
            return {"error": 1, "reason": "Request timed out"}
        except Exception as e:
            return {"error": 1, "reason": str(e)}

    async def generate_email(self) -> dict:
        try:
            async with self.s.post(
                f"{self.base_url_v1}/generate", params=self.params,  proxy = f"http://{self.proxy}"
            ) as resp:
                res = await resp.json()
                return res
        except asyncio.TimeoutError:
            return {"error": 1, "reason": "Request timed out"}
        except Exception as e:
            return {"error": 1, "reason": str(e)}

    async def reserve_email(self, email: str) -> dict:
        """Reserves an email and registers it for forwarding"""
        try:
            payload = {
                "hme": email,
                "label": self.label,
                "note": "I Love Expanse Crypto",
            }
            async with self.s.post(
                f"{self.base_url_v1}/reserve", params=self.params, json=payload,  proxy = f"http://{self.proxy}"
            ) as resp:
                res = await resp.json()
            return res
        except asyncio.TimeoutError:
            return {"error": 1, "reason": "Request timed out"}
        except Exception as e:
            return {"error": 1, "reason": str(e)}

    async def list_email(self) -> dict:
        try:
            async with self.s.get(f"{self.base_url_v2}/list", params=self.params, proxy = f"http://{self.proxy}") as resp:
                res = await resp.json()
                return res
        except asyncio.TimeoutError:
            return {"error": 1, "reason": "Request timed out"}
        except Exception as e:
            return {"error": 1, "reason": str(e)}