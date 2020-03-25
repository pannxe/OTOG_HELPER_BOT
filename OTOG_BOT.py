import discord
import requests
import json
import time
from random import randint
from urllib.request import Request, urlopen
req = Request('https://otog.cf/main', headers={'User-Agent': 'Mozilla/5.0'})

TOKEN = input("Tell me your TOKEN :) :")
if TOKEN == "":
	print("WTF MANN")
	exit(1)

def Count_All_Task():
	webpage = urlopen(req).read()
	webpage = str(webpage)
	i = webpage.find("nosub = ");
	i += 9;
	for j in range(0,10):
		if webpage[i+j] == '"':
			return webpage[i:i+j]
	return "??"

def Count_Today_Task():
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

def Get_Random_Text_forMention():

    Words = ["จงทำโจทย์ จงทำโจทย์ จงทำโจทย์","ทำโจทย์เถอะ ขอหล่ะ","ว่างมากนั้นก็ไปทำโจทย์สิ","ไม่อ่าน ไม่ตอบ ไม่สน...","แต่ว่า...ทำโจทย์ด้วยสิ...",";w;","=A=!","- -*","แล้วไง?","https://giphy.com/gifs/sad-cry-capoo-3og0IG0skAiznZQLde","https://giphy.com/stickers/cat-pearl-capoo-TFUhSMPFJG7fPAiLpQ","https://giphy.com/gifs/happy-rainbow-capoo-XEgmzMLDhFQAga8umN","https://giphy.com/gifs/cat-color-capoo-dYZxsY7JIMSy2Afy6e","ระเบิดเวลา......**อ๊าาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาา**","โฮ่... แทนที่แกจะเข้าค่ายอื่น แกกลับเดินมาค่ายคอม อย่างนั้นนะเรอะ","เปล่าประโยชน์ เปล่าประโยชน์ เปล่าประโยชน์ เปล่าประโยชน์","**How Dare You!!??**","เคยฟังรึเปล่า... X ติดไซเรน (https://pastebin.com/6a7u1b85)","พี่รู้ว่ามันเศร้า แต่จงทำโจทย์ต่อไปครับ","ญิรดีร์ฏ้อณรับสูเก็ฒเฎอร์ฌาวไฑญ",":thinking:",":joy:",":poop:",":+1:",":eyes:",":P"]
    return Words[randint(0,len(Words)-1)]

def Get_Random_Text_forHello():
    Words = ["สวัสดีเจ้า","สวัสดีจ้า","สวัสดีครับ","สวัสดีค่ะ","ສະບາຍດີ","Annyeonghaseyo","Kon'nichiwa","Hello","привет!","ว่าไง",";w;?","Meow Meooww?",":wave:","https://giphy.com/gifs/capoo-halloween-3ov9k0OmfNYeLdK4gg","Nǐ hǎo"]
    return Words[randint(0,len(Words)-1)] + " {0.author.mention}"


def Get_Incoming_Contest():
	response = requests.get("https://otog.cf/api/contest")
	if response.status_code != 200:
		return "เว็ปบึ้มง่าาาาาา"
	Con = response.json()[-1]
	Contest_Time = Con['time_start']
	Now_Time = int(time.time())
	Delta = Contest_Time - Now_Time

	if Delta > 0:
		Str_Time = "\n["+time.ctime(Contest_Time)+"]"

		if Delta > 60*60*24 :
			return 'จะมีคอนเทส "'+Con['name']+'" ในอีก '+str(Delta//(60*60*24)) \
			+"วัน " \
			+Str_Time
		elif Delta > 60*60 :
			return 'จะมีคอนเทส "'+Con['name']+'" ในอีก '+str(Delta//(60*60)) \
			+" ชั่วโมง " + str((Delta%(60*60))//60)+" นาที " \
			+Str_Time
		elif Delta > 60:
			return 'จะมีคอนเทส "'+Con['name']+'" ในอีก ' \
			+str(Delta//60)+" นาที " \
			+Str_Time
		else:
			return 'ไม่ต้องถามแล้ว อีกไม่ถึงนาทีจะมี "'+Con['name']+'" เตรียมมือเตรียมแขนเตรียมหัวเตรียมขาให้พร้อม!!!'

	else:
		if Now_Time < Con['time_end'] :
			return "ยัง... ยังจะถามอีก เขาแข่งกันแล้วโว้ย!!!"
		else:
			return "ไม่มีการแข่งจ้าา วันนี้นอนได้\nอนาคตอาจจะมี"
	return "????"


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
			await message.channel.send(Get_Random_Text_forHello().format(message))
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
			await message.channel.send(Get_Incoming_Contest())

		if message.content.startswith('task()'):
			await message.channel.send('มีอยู่ '+ Count_All_Task() +" ข้อ")
			await message.channel.send('ไปทำด้วย!!!')

		if message.content.startswith('today_task()'):
			await message.channel.send('มีโจทย์ใหม่ '+ Count_Today_Task() +" ข้อ")
			await message.channel.send('ไปทำด้วย!!!')

		if message.content.startswith('user_life()'):
			await message.channel.send(Get_User_Ongoing())


		for Mem in message.mentions:
			if self.user.name == Mem.display_name:
				await message.channel.send(Get_Random_Text_forMention())
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
client.run(TOKEN)
