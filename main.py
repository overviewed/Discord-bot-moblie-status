import ast, inspect, re, discord
from discord.ext import commands

def source(o):
    s = inspect.getsource(o).split("\n")
    indent = len(s[0]) - len(s[0].lstrip())
    return "\n".join(i[indent:] for i in s)

source_ = source(discord.gateway.DiscordWebSocket.identify)
patched = re.sub(
    r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])', 
    r"\1Discord Android\2",  
    source_
)

loc = {}
exec(compile(ast.parse(patched), "<string>", "exec"), discord.gateway.__dict__, loc)
discord.gateway.DiscordWebSocket.identify = loc["identify"]

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name="a game"))

client.run("token_here")