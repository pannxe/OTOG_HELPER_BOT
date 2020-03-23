import discord
from urllib.request import Request, urlopen
req = Request('https://otog.cf/main', headers={'User-Agent': 'Mozilla/5.0'})

def Get_Task():
	webpage = urlopen(req).read()
	webpage = str(webpage)
	i = webpage.find("nosub = ");
	i += 9;
	for j in range(0,10):
		if webpage[i+j] == '"':
			return webpage[i:i+j]
	return "??"

def Get_Today_Task():
	webpage = urlopen(req).read()
	webpage = str(webpage)
	#<h5 class="font_white cnt_msg">โจทย์วันนี้</h5>
	i = webpage.find('<div class="count_button blue select-none">');
	i += 272;
	for j in range(0,10):
		if webpage[i+j] == '<':
			return webpage[i:i+j]
	return "??"

def Get_User_Ongoing():
	webpage = urlopen(req).read()
	webpage = webpage.decode("utf-8")
	i = webpage.find('<!--<h6 class="font_gray text-center"> ');
	i += 39;
	#print(webpage[i:i+20])
	for j in range(0,1000):
		if webpage[i+j] == '<':

			e = webpage[i:i+j];
			return "ฮั่นแน่ มี "+e+" ที่ยังมีชีวิตอยู่"
	return "ไม่มีอะ"



class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		await client.change_presence(activity=discord.Game(name='รอทำคอนเทส'))

	async def on_message(self, message):
        # we do not want the bot to reply to itself
		if message.author.id == self.user.id:
			return


		if message.content.startswith('hello()'):
			await message.channel.send('สวัสดีไอ้หน้า {0.author.mention}'.format(message))
		if message.content.startswith('help()') or message.content.startswith('!help'):
			em = discord.Embed(title = "สิ่งที่น้อมทำได้",description = "มีแค่นี้แหละ")
			em.add_field(name = "help()",value = "ก็ที่ทำอยู่ตอนนี้แหละ")
			em.add_field(name = "hello()",value = "คำสั่งคนเหงา")
			em.add_field(name = "contest()",value = "คอนเทสที่กำลังจะมาถึง")
			em.add_field(name = "task()",value = "จำนวนโจทย์ตอนนี้")
			em.add_field(name = "today_task()",value = "โจทย์ใหม่วันนี้")

			await message.channel.send(content = None ,embed = em)

		if message.content.startswith('test()'):
			await message.channel.send('ยังมีชีวิตอยู่')

		if message.content.startswith('contest()'):
			await message.channel.send('อาจจะมีในอนาคต อิอิ')

		if message.content.startswith('task()'):
			await message.channel.send('มีอยู่ '+ Get_Task() +" ข้อ")
			await message.channel.send('ไปทำด้วย!!!')

		if message.content.startswith('today_task()'):
			await message.channel.send('มีอยู่ '+ Get_Today_Task() +" ข้อ")
			await message.channel.send('ไปทำด้วย!!!')

		if message.content.startswith('user_life()'):
			await message.channel.send(Get_User_Ongoing())


		for Mem in message.mentions:
			if "OTOG_Helper" == Mem.display_name:
				await message.channel.send('ไม่อ่าน ไม่ตอบ ไม่สน...')
				await message.channel.send('สนแค่คำสั่งที่ลงท้ายด้วย ()')
				await message.channel.send('ลอง help() จะช่วยให้ชีวิตดีขึ้น :)')
				break

	async def on_guild_join(guild):
		await guild.system_channel.send("กราบสวัสดีพ่อแม่พี่น้องครับ")

	async def on_member_join(self, member):
		guild = member.guild
		if guild.system_channel is not None:
			to_send = 'สวัสดีเจ้า {0.mention} สู่ {1.name}!'.format(member, guild)
			await guild.system_channel.send(to_send)

	async def on_member_remove(self, member):
		guild = member.guild
		if guild.system_channel is not None:
			to_send = 'ลาก่อย {0.mention}!'.format(member)
			await guild.system_channel.send(to_send)

	async def announcements(Con):
		channel = client.get_channel(691618323468779532)
		await channel.send(Con)



client = MyClient()
client.run('NjkxNTg0MjYxNjM0OTE2Mzk5.XniGYA.UkXoQidee__15AhNYsS65JaAoTY')
