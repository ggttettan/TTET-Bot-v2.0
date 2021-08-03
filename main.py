import discord
import os
import requests
import random
import json 
import asyncio
from replit import db
from keep_alive import keep_alive
from datetime import datetime
from discord.ext import commands

client = commands.Bot(command_prefix = 'ttet', help_command=None)

sad_words = ["depressed", " sad ", "sien", "unhappy", "buhaoxiao", "bhx", "die", "shangxin"]

angry_words = ["angry", "dajia", "nishishui", " lj", "fuck", "cibai", "fk ", "maderr", "mader", "cao", "cnm", "tulan", "puki"]

nickt = ["nickt"]

starter_encouragements = [
  "Cheer up!<:zhcheers:870912844034633769>",
  "Hang in there.",
  "You are a great person / bot!<a:ztnods:870910924238778378>",
  "Your problem loh<:fine:870912844663762984>",
  "Nishishui<:cringe:870912844986732555>"
]

angry_joke = [
  "lai tio la<:oklo:870912844479234048>",
  "do ttetjoke to hear my joke and chill sia",
  "mao angry lin, 小事nia<:mao:870912844663762974>",
  "scolding bad words is not good<:niyiwei:870912844076552283>"
]

if "sad_respond" not in db.keys():
  db["sad_respond"] = True

def get_joke():
  response = requests.get("https://official-joke-api.appspot.com/random_joke")
  json_data = json.loads(response.text)
  joke = json_data["setup"] + " -" + json_data["punchline"]
  return(joke)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]
    
def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + "TTET"
  return(quote)

def get_waifu():
  response = requests.get("https://api.waifu.pics/sfw/waifu")
  json_data = json.loads(response.text)
  waifu = json_data["url"]
  return(waifu)
  
def get_gif(input):
  response = requests.get("https://api.waifu.pics/sfw/" + input)
  json_data = json.loads(response.text)
  gif = json_data["url"].replace(' ', '%20')
  return(gif)

def get_nsfw(input):
  response = requests.get("https://api.waifu.pics/nsfw/" + input)
  json_data = json.loads(response.text)
  nsfw = json_data["url"].replace(' ', '%20')
  return(nsfw)



@client.event
async def on_ready():
    print("TTET Bot v2 is ready.")
    await client.change_presence(activity=discord.Game(name="with TTET"))

#summon the holy embed HELP
@client.command(0)
async def help(ctx):
  embed = discord.Embed(title="Hey, welcome to TTET's Bot!", description="There are a few ways you can play with me :D", colour=0xD84A5A, timestamp=datetime.utcnow())
  embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/32pqExk8GSCWC-b7Ivx3o7ZjMrBumBVTM7Nn6Sp6W1Q/https/media.discordapp.net/attachments/870658163953762336/870959883095265320/DRu-71FVAAA9zbd.jpg")
  embed.set_image(url="https://media.discordapp.net/attachments/848113319382482954/870965318367997992/wallhaven-e79om8_1920x1080.png?width=1197&height=674")
  embed.set_author(name="ggttettan", icon_url="https://cdn.discordapp.com/avatars/387250841116999694/deda47a19b9b322025e341e0b50425df.webp?size=256")
  embed.add_field(name="ttetinspire", value="I will send you TTET's quotes!", inline=False)
  embed.add_field(name="ttetjoke", value="I will help you to make the channel less awkward!", inline=False)
  embed.add_field(name="ttetquiz", value="I will give you a question and you have to answer me (true/false).", inline=False)
  #embed.add_field(name="ttetwaifu", value="I will send your waifu pictures.", inline=False)
  embed.add_field(name="ttetwaifuhelp", value="Branch command includes: ttetgif, ttetnsfw", inline=False)
  embed.set_footer(text="I will come out occasionally to encourage people and stop people from saying bad words too!", icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png")
  await ctx.send(embed=embed)

#Check ping.
@client.command(0)
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

#This code is used to enable capitals and XXXspaces.
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  message.content = message.content.lower()#.replace(' ', '')
  msg = message.content
  await client.process_commands(message)

  #send encouragment when detect sadness
  if db["sad_respond"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      #options.extend(db["encouragements"])
      options = options + db["encouragements"][:]
      #options = options + list(db["encouragements"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  #calm ppl down when detect anger
  if any(word in msg for word in angry_words):
    await message.channel.send(random.choice(angry_joke))

  #send nickt emote when detect nickt
  if any(word in msg for word in nickt):
    await message.channel.send("<:nickt:826447573505671218>")

#8ball (use aliases, multiple command same code)
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

#purge msg
@client.command(aliases= ['purge', 'delete'])
#@has_permissions(manage_messages = True)
async def clear(ctx , amount=1):
  await ctx.channel.purge(limit=amount + 1)
  await ctx.send(f'{ctx.message.author.mention} cleared {amount} messages', delete_after=3)

#send joke
@client.command()
async def joke(ctx):
  joke = get_joke()
  await ctx.send(joke)

#send inspire
@client.command()
async def inspire(ctx):
  quote = get_quote()
  await ctx.send(quote)

#quiz3.0
@client.command()
async def quiz(ctx):
  response = requests.get("https://opentdb.com/api.php?amount=1")
  json_data = json.loads(response.text)
  embed = discord.Embed(title="Question", description=json_data["results"][0]["question"].replace('&quot;', '"').replace("&#039;","'").replace("&eacute","é").replace("&ouml;","ö"), colour=0xD84A5A, timestamp=datetime.utcnow())
  embed.set_thumbnail(url="https://d1ymz67w5raq8g.cloudfront.net/Pictures/480xany/6/5/5/509655_shutterstock_1506580442_769367.jpg")
  embed.add_field(name="Category", value=json_data["results"][0]["category"], inline=False)
  embed.add_field(name="Difficulty", value=json_data["results"][0]["difficulty"], inline=False)
  embed.set_footer(text="加油！", icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png")
  crt_ans = json_data["results"][0]["correct_answer"]
  incrt_ans = json_data["results"][0]["incorrect_answers"]
  opt = incrt_ans
  opt.append(crt_ans)
  random.choice(opt)

  if json_data["results"][0]["type"] == "multiple":
    embed.add_field(name="Answer", value=f"```A) {opt[0]}\nB) {opt[1]}\nC) {opt[2]}\nD) {opt[3]}```", inline=False)
    mcq = ["\U0001F1E6", "\U0001F1E7", "\U0001F1E8", "\U0001F1E9"]
    #o2e = dict(zip(opt, mcq))

  if json_data["results"][0]["type"] == "boolean":
    embed.add_field(name="Answer", value=f"```1) True\n2) False```", inline=False)
    mcq = ["\U0001F1F9", "\U0001F1EB"]
    #o2e = {"True": mcq[0], "False": mcq[1]}
  o2e = dict(zip(opt, mcq))
  mess = await ctx.send(embed=embed)

  for emoji in mcq:
    await mess.add_reaction(emoji)

  def check_answer(reaction, user):
    return user == ctx.author

  while True:
    try:
      reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check_answer)
      em = str(reaction.emoji)
      if reaction.emoji in mcq:
        print(mcq.index(reaction.emoji) + 1)
        if em == o2e[crt_ans]:
          await ctx.send(f"Aiyooo, {ctx.author.name} so pandai one ah")
        else:
          await ctx.send('不能啦你')
        break
      else:
        print("Unknown reaction")
    except asyncio.TimeoutError:
      await ctx.send(content="```Time's up ⌚!```")
      break
  await ctx.send(content=f"```Correct answer was {crt_ans}```")

#waifuhelp
@client.command()
async def waifuhelp(ctx):
  waifuhelp = "Put these behind `ttetgif`, example:`ttetgif cry`, try it yourself!:\n[waifu, neko, shinobu, megumin, bully, cuddle, cry, hug, awoo, kiss, lick, pat, smug, bonk, yeet, blush, smile, wave, highfive, handhold, nom, bite, glomp, slap, kill, kick, happy, wink, poke, dance, cringe]\n||For nsfw:\n[waifu, neko, trap, blowjob]||"
  await ctx.send(waifuhelp)

#ttetgif
@client.command()
async def gif(ctx, *,input):
  gif = get_gif(input)
  await ctx.send(gif)

#ttetnsfw
@client.command()
async def nsfw(ctx, *,input):
  nsfw = get_nsfw(input)
  await ctx.send(nsfw)

#send karuta dating sheet
@client.command()
async def kvi(ctx):
  sheet = "Hey, this is the documentation for `kvi` `talk` \nhttps://docs.google.com/spreadsheets/d/1ZaovZoC5WiGAYA2Th37GqtxnDG-YL7UYyewGzSyRcEw/edit?usp=sharing"
  await ctx.send(sheet)

#user add new reply for encouragemnts
#user and default reply does not mix tgt, user cannot delete bot reply
@client.command()
async def new(ctx, *,encouraging_message):
  update_encouragements(encouraging_message)
  await ctx.send("New encouraging_message added.")

#user del user reply for encouragemnts
@client.command(aliases=['del'])
async def _del(ctx, *,delete_message):
  encouragements = []
  if "encouragements" in db.keys():
    delete_message = int(delete_message)
    delete_encouragement(delete_message)
    encouragements = db["encouragements"]
  await ctx.send(encouragements)

#send the list for user input encouragements
@client.command()
async def list(ctx):
  encouragements = []
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
  await ctx.send(encouragements)

#send the list for user input encouragements
@client.command()
async def sadres(ctx, *, value):
  if value == "true":
    db["sad_respond"] = True
    await ctx.send("Sad responding is on.")
  else:
    db["sad_respond"] = False
    await ctx.send("Sad responding is off.")

keep_alive()
client.run(os.environ['TOKEN'])
