import discord, asyncio, requests, re, time, os, sys, json;from re import search;from discord.ext import commands;from discord.ext.commands import has_permissions, MissingPermissions

apikey = ""
secret = ""
aid = ""
version1 = ""
random1 = ""
auth = ''

try:
    setup = json.load(open('config.json'))
except FileNotFoundError:
    print('File does not exist / cannot be accesed.')
    time.sleep(2)
    input(sys.exit())
except:
    print('Error found, try again later, thanks for your patience.')
    input(sys.exit())

bot = commands.Bot(command_prefix=setup['prefix'])

@bot.event
async def on_ready():
    os.system('title Bot running.')
    print('Bot started / Running.')

"""@bot.event
async def on_member_join(member):
    channel = bot.get_channel(Welcome Channel)
    await channel.send('Welcome, enjoy your stay {}.'.format(member))"""

@bot.command()
@commands.has_role("panel")
async def hwid(ctx, username: str=None):
    if username is None:
        await ctx.send('Username is None, please re-try.')
    else:
        try:
            response = requests.get('https://developers.auth.gg/HWID/?type=reset&authorization={}&user={}'.format(auth, username))
            if response.status_code == 200:
                await ctx.send('Hwid reseted.')
            else:
                await ctx.send('Error.')
        except Exception as e:
            await ctx.send('Thread error.')

@hwid.error
async def hwid_error(error, ctx):
    if isinstance(error, MissingPermissions):
        await ctx.send('You don\'t have PANEL access.')

@bot.command()
@commands.has_role("panel")
async def license(ctx, days: int=None):
    if days is None:
        days = 9998
    try:
        response = requests.get('https://developers.auth.gg/LICENSES/?type=generate&days={}&amount=1&level=1&authorization={}'.format(str(days), auth))
        if response.status_code == 200:
            await ctx.send('License created: `{}`'.format(response.json()['0']))
        else:
            await ctx.send('Error.')
    except Exception as e:
        await ctx.send('Error: {}'.format(e))  

@license.error
async def license_error(error, ctx):
    if isinstance(error, MissingPermissions):
        await ctx.send('You don\'t have PANEL access.')   

@bot.command()
@commands.has_role("panel")
async def delete_user(ctx, username: str=None):
    if username is None:
        await ctx.send('Username cannot be none.')
    else:
        try:
            response = requests.get('https://developers.auth.gg/USERS/?type=delete&authorization={}&user={}'.format(auth, username))
            if response.status_code == 200:
                await ctx.send('User deleted.')
            else:
                await ctx.send('Error.')
        except Exception as e:
            await ctx.send('Error: {}'.format(e))  

@delete_user.error
async def delete_user_error(error, ctx):
    if isinstance(error, MissingPermissions):
        await ctx.send('You don\'t have PANEL access.')   

@bot.command()
@commands.has_role("panel")
async def password(ctx, username: str=None, password: str=None):
    if username is None:
        await ctx.send('Username cannot be none.')
    else:
        if password is None:
            await ctx.send('What\'s the new password?')
        else:
            try:
                response = requests.get('https://developers.auth.gg/USERS/?type=changepw&authorization={}&user={}&password={}t'.format(auth, username, password))
                if response.status_code == 200:
                    await ctx.send('Password changed.')
                else:
                    await ctx.send('Error.')
            except Exception as e:
                await ctx.send('Error: {}'.format(e))  

@password.error
async def password_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('You don\'t have PANEL access.')   

@bot.command()
@commands.has_role("panel")
async def users(ctx):
    try:
        response = requests.get('https://developers.auth.gg/USERS/?type=count&authorization={}'.format(auth))
        if response.status_code == 200:
            await ctx.send('Users in database: {}'.format(response.json()['success']))
        else:
            await ctx.send('Error.')
    except Exception as e:
        await ctx.send('Error: {}'.format(e))  

@users.error
async def users_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('You don\'t have PANEL access.')   

@bot.command()
@commands.has_role("panel")
async def info(ctx, username: str=None):
    if username is None:
        await ctx.send('Please select someone.')
    else:
        try:
            response = requests.get('https://developers.auth.gg/USERS/?type=fetch&authorization={}&user={}'.format(auth, username))
            if response.status_code == 200:
                await ctx.send('User Information: \nUsername: {}\nEmail: {}\nRank: {}\nhwid: {}\nLast IP: {}\nExpiry: {}'.format(response.json()['username'], response.json()['email'], response.json()['rank'], response.json()['hwid'], response.json()['lastip'], response.json()['expiry']))
            else:
                await ctx.send('Error.')
        except Exception as e:
            await ctx.send('Error: {}'.format(e))  

@info.error
async def info_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('You don\'t have PANEL access.')     

try:
    bot.run(setup['token'])
except:
    print('Error', input())
