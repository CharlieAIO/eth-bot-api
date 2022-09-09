import helheim
import cloudscraper
import time
import json
from discord_webhook import DiscordWebhook
from helheim.exceptions import (
    HelheimException,
    HelheimSolveError,
    HelheimRuntimeError,
    HelheimSaaSError,
    HelheimSaaSBalance,
    HelheimVersion,
    HelheimAuthError,
    HelheimBifrost
)

SERVER = 'http://178.62.79.103:8000'
API_KEY = '329eae77-9a91-4666-8a00-ce8a9de6147a'
WEBHOOK = 'https://discord.com/api/webhooks/1000169276411494410/Ej_VnNPreaTKk0Hurx4BkSADAqO_7rJ__sClB3RWKzIQTbJoQCqadW_FrQqbX6aCj4MX'


def injection(session, response):
    if helheim.isChallenge(session, response):
        # solve(session, response, max_tries=5)
        return helheim.solve(session, response)
    else:
        return response


def createSession():
    helheim.auth('b0b7987d-1a05-431e-b2c9-15bc7483f713')

    session = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'mobile': False,
            'platform': 'windows'
        },
        requestPostHook=injection,
        captcha={"provider": 'vanaheim'}
    )
    helheim.wokou(session)
    session.bifrost_clientHello = 'chrome'
    helheim.bifrost(session, './bifrost-0.0.8-linux.x86_64.so')
    session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    session.headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    return session


def sendHook(text):
    webhook = DiscordWebhook(url=WEBHOOK, content=text)
    webhook.execute()


def run_checker():
    session = createSession()
    while True:
        print("Checking for closed raffles...")
        raffles = getAll(session)
        deleted = 0
        for r in raffles:
            response = session.get('https://www.premint.xyz/'+r['id'], headers={
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "max-age=0",
                "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "Referer": "https://www.premint.xyz/",
                "Referrer-Policy": "same-origin",
            })
            if "You aren't registered." in response.text or "This list is no longer accepting entries" in response.text:
                print("Deleting {} from database".format(r['id']))
                delFromDB(session, r['id'])
                deleted += 1

            time.sleep(1)

        print("Deleted {} Raffles from DB".format(deleted))
        # sendHook("Deleted {} Raffles from DB".format(deleted))
        time.sleep(1 * 60 * 60 * 3)


def getAll(session):
    response = session.get(SERVER+'/raffles',
                           headers={'x-api-key': API_KEY})

    return json.loads(response.text)


def delFromDB(session, id):
    response = session.delete(SERVER+'/raffles/'+id,
                              headers={'x-api-key': API_KEY})
    return


run_checker()
