import json
import helheim
import cloudscraper
from bs4 import BeautifulSoup
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
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
webhooks = [
    'https://discord.com/api/webhooks/1000038962628403200/ZdHxaLSwBGCVmJTuEoHKE9IF7InjpWJgamtOCO6rn3fN7FFDdKxAElV0eQfH5ZwquhyL',
    'https://discord.com/api/webhooks/1000169276411494410/Ej_VnNPreaTKk0Hurx4BkSADAqO_7rJ__sClB3RWKzIQTbJoQCqadW_FrQqbX6aCj4MX'
]


def sendWebhooks(data):
    for webhook in webhooks:
        time.sleep(5)
        webhook = DiscordWebhook(url=webhook)

        embed = DiscordEmbed(title='**New PreMint Raffle**', color='248e97')

        embed.set_url('https://www.premint.xyz/{}/'.format(data['id']))
        embed.set_thumbnail(url=data['image'])
        embed.set_footer(
            text='@amnotifynft', icon_url='https://media.discordapp.net/attachments/776073568114704424/1000115103791861810/amnftv3.png')
        embed.add_embed_field(name='Raffle', value=data['name'], inline=True)
        embed.add_embed_field(name='Number of Winner',
                              value=data['winners'], inline=True)
        embed.add_embed_field(name='ETH Required',
                              value=data['eth'], inline=True)
        embed.set_timestamp()

        try:
            follow_list = ''
            for follow in data['twitter']['follows']:
                follow_list += f'[{follow}](https://twitter.com/{follow}) '
            embed.add_embed_field(
                name='Twitter', value=follow_list, inline=False)
        except KeyError:
            pass
        try:
            if data['twitter']['retweet'] or data['twitter']['like']:
                description = '['
                if data['twitter']['retweet']:
                    description += 'Retweet,'
                if data['twitter']['like']:
                    description += 'Like'
                description += ']('
                if data['twitter']['tweet']:
                    description += data['twitter']['tweet'].strip()
                    description += ')'
                embed.add_embed_field(name='Tweet', value=description)

            if data['discord']['join']:
                embed.add_embed_field(name='Discord', value='[Join Here]({})'.format(
                    data['discord']['join'], data['discord']['join']))
            if data['discord']['role']:
                embed.add_embed_field(
                    name='Discord Role', value='Get {} Role'.format(data['discord']['role']))
        except KeyError:
            pass

        webhook.add_embed(embed)
        webhook.execute()


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
    helheim.bifrost(session, './bifrost-0.0.7-linux.x86_64.so')
    session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    session.headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    return session


def requestRafflePage(session, link):
    response = session.get('https://www.premint.xyz'+link, headers={
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
        "Referer": "https://www.premint.xyz/collectors/explore/",
        "Referrer-Policy": "same-origin",
    })
    parsed_html = BeautifulSoup(response.text, "html.parser")
    twitterStep = parsed_html.find('div', {"id": "step-twitter"})
    discordStep = parsed_html.find('div', {"id": "step-discord"})
    balanceStep = parsed_html.find('div', {"id": "step-balance"})
    customStep = parsed_html.find('div', {"id": "step-custom"})

    twitter_steps = {}
    discord_steps = {}
    extra_steps = {}
    eth = 0

    if(twitterStep):
        users_to_follow = []

        twitterStep = twitterStep.find('div', {"class": "col-12"})
        twitterStep = twitterStep.find_all(
            'div', {"class": "mb-2 border bg-muted p-2 rounded text-md"})

        if len(twitterStep) > 0:
            if 'Follow' in twitterStep[0].text:
                for f in twitterStep[0].find_all('a'):
                    users_to_follow.append(f.attrs['href'].split('.com/')[1])
            else:
                twitter_steps['retweet'] = 'Retweet' in twitterStep[0].text
                twitter_steps['like'] = 'Like' in twitterStep[0].text
                twitter_steps['tweet'] = twitterStep[0].a.href

            if len(twitterStep) > 1:
                if 'Follow' in twitterStep[1].text:
                    for f in twitterStep[1].find_all('a'):
                        users_to_follow.append(
                            f.attrs['href'].split('.com/')[1])
                else:
                    twitter_steps['retweet'] = 'Retweet' in twitterStep[1].text
                    twitter_steps['like'] = 'Like' in twitterStep[1].text
                    twitter_steps['tweet'] = twitterStep[1].a.attrs['href']

        twitter_steps['follows'] = users_to_follow

    if(discordStep):
        discordStep = discordStep.find('div', {"class": "col-12"})
        discordStep = discordStep.find_all(
            'div', {"class": "mb-2 border bg-muted p-2 rounded text-md"})

        if len(discordStep) > 0:
            discord_steps['join'] = discordStep[0].find(
                'a', {'class': 'c-base-1 strong-700 text-underline'}).attrs['href']

            if 'role' in discordStep[0].text.strip():
                discord_steps['role'] = discordStep[0].find(
                    'span', {"class": "c-base-1 strong-700"}).text

    if(balanceStep):
        balanceStep = balanceStep.find('div', {"class": "col-12"})
        if(balanceStep):
            eth = balanceStep.find('span', {'class': 'strong c-dark'})
            if(eth):
                eth = eth.text.split(' ')[0]

    if(customStep):
        customStep = customStep.find('div', {"class": "col-12"})
        if(customStep):
            custom = customStep.find('div', {'class': 'strong mb-1 text-md'})
            if(custom):
                extra_steps['custom_field'] = custom.text

    return twitter_steps, discord_steps, extra_steps, eth


def addToDB(session, data):
    print(data)
    response = session.post(SERVER+'/raffles', json=data,
                            headers={'x-api-key': API_KEY})
    print(response)
    print(response.text)


def getAll(session):
    response = session.get(SERVER+'/raffles',
                           headers={'x-api-key': API_KEY})

    return json.loads(response.text)


def requestPage(session, csrf, sessionId):
    response = session.get('https://www.premint.xyz/collectors/explore/new/', headers={
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
        "Referer": "https://www.premint.xyz/collectors/explore/",
        "Referrer-Policy": "same-origin",
        "Cookie": f'csrftoken=${csrf}; session_id={sessionId};',
    })
    parsed_html = BeautifulSoup(response.text, "html.parser")
    all_ = parsed_html.find_all('div', {"class": "row text-lg-right strong"})

    all_raffles = []
    for raffle in all_:
        try:
            img = raffle.find('div', {"class": "block-icon"}).img.attrs['src']
        except Exception as e:
            img = ''

        try:
            name = raffle.find('div', {"class": "block-content"}).a.text
        except Exception as e:
            name = ''

        try:
            link = raffle.find('div', {"class": "block-content"}).a['href']
        except Exception as e:
            link = ''

        try:
            supply = raffle.find(
                'div', {"class": "block-content"}).div.text.strip()
        except Exception as e:
            supply = ''

        twitter, discord, extra_steps, eth = requestRafflePage(session, link)

        data = {
            "name": name,
            "image": img,
            "id": link.replace('/', ''),
            "winners": supply,
            "twitter": twitter,
            "discord": discord,
            "extra": extra_steps,
            "eth": eth,
            "date": ""
        }
        print(data)
        sendWebhooks(data)
        all_raffles.append(data)
        with open('raffles.json', 'r+') as f:
            d = json.load(f)
            d.append(data)
            f.seek(0)
            json.dump(d, f)

    addToDB(session, all_raffles)
    # print(all_raffles)


def monitor():
    session = createSession()
    run = True
    csrf = 'pYhhPIPm4beqe5xt9K4WYbA6uqE8UEjZwUum3C7xFE73YgJm4pPBWkmDD1oUbYvJ'
    sessionId = 'f3zv7qat5aoya7b0f3mwq1a6vqzwl2dk'

    while(run):
        print(str(time.time()) + " |GETTING RAFFLES...")
        requestPage(session, csrf, sessionId)
        time.sleep(60 * 30)


monitor()
