from twitchio.ext import commands
from twitchio.client import Client

ACESS_TOKEN = 'vt1jghwh3mhsmzkgaehk2mwkywrxeo'
REFRESH_TOKEN = 'biyphp8d651yowj78ba2ibqhdtjswkaixgs66t4uyz1vzcvw6l'
CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'
CHANNEL = 'kaeric_'


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=ACESS_TOKEN,
                         prefix='!', initial_channels=['kaeric_'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')


bot = Bot()
bot.run()
