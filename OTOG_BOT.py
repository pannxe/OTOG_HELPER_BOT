import discord
import requests
import json
from json import JSONEncoder
import time
import datetime
import os.path
import asyncio
from itertools import cycle
from random import randint
from urllib.request import Request, urlopen
import Pat1Grader

PATH = os.path.realpath(__file__)
while PATH[-1] != "\\":
	PATH = PATH[:-1]


INF = 999999999999999999999999

Bot_Namae = "OTOG - One Tambon One Grader"
DEB = "" #Before Command
if DEB != "":
	Bot_Namae = "น้อวงตัวน้อยยย"

VER = "B08"

IsStart = False

TOKEN = input("Tell me your TOKEN :) :")
if TOKEN == "":
	print("WTF MANN")
	exit(1)

def Count_All_Task():
	response = requests.get("https://otog.cf/api/countProblem")
	if response.status_code != 200:
		return "เว็ปบึ้มง่าาาาาา"
	Con = response.json()["allProblem"]

	return str(Con)

def Getname(Client,Id,Guild = None):
	if Guild== None:
		return Client.get_user(int(Id)).name
	else:
		Mininame = Guild.get_member(int(Id)).nick
		if Mininame != None:
			return Client.get_user(int(Id)).name+"(AKA. "+Mininame+")"
		return Client.get_user(int(Id)).name

def Count_Today_Task():
	return "??"

def Time_Convert(hour = 0,minn = 0,secc = 0):
	TI = (hour-7)*60*60+minn*60+secc
	if TI < 0:
		TI += 60*60*24
	return TI

User_Live_Count = -1

def Reload_User_Live_Count():
	global User_Live_Count
	response = requests.get("https://otog.cf/api/countProblem")
	if response.status_code != 200:
		User_Live_Count = -1
	else:
		User_Live_Count = response.json()["onlineUser"]

def Get_User_Ongoing():

	Reload_User_Live_Count()

	if (User_Live_Count == -1):
		return "เว็ปบึ้มง่าาาา"
	elif (User_Live_Count == 0):
		return "ไม่มีอะ เหงา Hereๆ"
	return "ฮั่นแน่...มีคนทำโจทย์อยู่ "+str(User_Live_Count)+"คน"

def Pick_One(LIST):
	return LIST[randint(0,len(LIST)-1)]

Contest_Time = INF
Contest_namae = "??"
Contest_End = INF
Contest_Id = -1

TimeTick = 0

def Reload_Incoming_Contest():
	global Contest_Time
	global Contest_namae
	global Contest_End
	global Contest_Id
	global TimeTick

	TimeTick = 0
	response = requests.get("https://otog.cf/api/contest")




	if response.status_code != 200:
		Contest_Time = INF
		Contest_namae = "??"
		Contest_End = INF
		Contest_Id = -1
		return
	Con = response.json()

	if len(Con) == 0:
		Contest_namae = "!!None!!"
		Contest_Time = INF
		Contest_End = INF
		Contest_Id = -1

	for cc in Con:
		if cc['time_start'] < Contest_Time:
			Contest_Time = cc['time_start']
			Contest_End = cc['time_end']
			Contest_Id = cc['idContest']
			Contest_namae = str(Contest_Id)+" : `" + cc['name'] + "`"

def Second_To_Good_Str(sec):
	if sec > 60*60*24:
		return str(sec//(60*60*24)) + " วัน "
	elif sec > 60*60:
		return str(sec//(60*60)) + " ชั่วโมง " + str((sec%(60*60))//60) + " นาที "
	elif sec > 60:
		return str(sec//60) + " นาทีกว่าๆ!"
	else:
		return "ไม่ถึงนาที!!"

def Get_Incoming_Contest():
	global Contest_Time
	global Contest_namae
	global Contest_End
	global Contest_Id
	global TimeTick
	Reload_Incoming_Contest()

	if Contest_namae == "!!None!!":
		return "ไม่มีการแข่งจ้าา วันนี้นอนได้\nอนาคตอาจจะมี"
	elif Contest_Time == INF:
		return "เว็ปบึ้มง่าาาาาา"

	Now_Time = int(time.time())
	Delta = Contest_Time - Now_Time

	if Delta > 0:
		Str_Time = "\n["+time.ctime(Contest_Time)+"]"

		Ap_Time = Second_To_Good_Str(Delta)
		if Ap_Time == "ไม่ถึงนาที!":
			Ap_Time += " เตรียมมือเตรียมแขนเตรียมหัวเตรียมขาให้พร้อม"

		return "จะมีคอนเทสที่" + Contest_Id + ":" + Contest_namae +"ในอีก `" + Ap_Time + "`" + Str_Time

	else:
		if Now_Time < Contest_End :
			return "{0.author.mention}" + " ไอ้นี่มันอู้การแข่งคร๊าาาาบ\nเขาแข่งกันแล้วววว"
		else:
			return "ไม่มีการแข่งจ้าา วันนี้นอนได้\nอนาคตอาจจะมี"
	return "????"

def Get_Top10_User():
	response = requests.get("https://otog.cf/api/user")
	Content = response.json()
	StrNum = [
	":one:",":two:",":three:",":four:",":five:",
	":six:",":seven:",":eight:",":nine:",":keycap_ten:",
	]
	if response.status_code != 200:
		return "เว็ปบึ้มง่าาาาาา"
	Rank_Str = ":100:10 อันดับท่านเทพมีดังนี้:100:\n"
	for i in range(0,10):
		Rank_Str += "อันดับที่ " + StrNum[i] +Content[i]["sname"]+" <"+str(Content[i]["rating"])+">\n"
	Rank_Str += "อันดับต่อไป **อาจ เป็น คุณ**"
	return Rank_Str


def Get_Problem_Name(id):
	response = requests.get("https://otog.cf/api/problem")
	Content = response.json()
	if response.status_code != 200:
		return "เว็ปบึ้มง่าาาาาา"

	noi,mak = 0,len(Content)-1
	ANS = -1

	while noi <= mak:
		mid = (noi+mak)//2

		if (id <= Content[mid]["id_Prob"]):
			noi = mid+1
			ANS = mid
		else:
			mak = mid-1

	if Contest_Id != -1 and Content[ANS]["id_Prob"] != id:

		Contest_api_new = requests.get("https://otog.cf/api/contest/"+str(Contest_Id))

		if Contest_api_new.status_code != 200:
			return "เว็ปบึ้มง่าาาาาา"

		Now_Time = int(time.time())
		if Now_Time <= Contest_api_new['timeEnd']:
			#print(type(id),id,Contest_api['problems'][0])
			X = Contest_api_new['problem']

			for iid in X:
				if id ==iid["id_Prob"]:
					#print("F")
					return iid["sname"]



		return "???????!??????"
	else:
		return Content[ANS]["name"]
Question_List = []
Question_User = {}
Verify_User = {}
Guess_Num = {}

def Is_Time_Passed_In_Range(Des,Now,Range):
	if Range == 0:
		return (Now>=Des)
	else:
		return (Now>=Des) and (Now<=Des+Range)

async def Set_Bot_Namae(Client,Namae):
	for GG in Client.guilds:
		await GG.me.edit(nick =Namae)

class MyClient(discord.Client):

	global Question_List
	global Question_User
	global Verify_User
	global Contest_Time
	global Contest_namae
	global Contest_End
	global Contest_Id
	global TimeTick
	global IsStart
	global User_Live_Count
	global VER
	global Guess_Num



	def sSave(self):
		ddata = {
			"Question_List":Question_List,
			"Question_User":Question_User,
			"Verify_User":Verify_User
		}
		try:
			os.makedirs("All_DATA")
		except:
			pass
		with open("All_DATA/Save_Data"+VER+".otog", 'w') as outfile:
			json.dump(ddata, outfile)

	def lLoad(self):
		global Question_User
		global Question_List
		global Verify_User
		if os.path.isfile("All_DATA/Save_Data"+VER+".otog"):
			with open("All_DATA/Save_Data"+VER+".otog") as json_file:
				ddata = json.load(json_file)
				Question_List = ddata["Question_List"]
				Question_User = ddata["Question_User"]
				Verify_User = ddata["Verify_User"]


	def Mes_To_ID(self,Mes):
		Mes_ID = Mes.id
		Cha_ID = Mes.channel.id
		return {"Mes_ID" : Mes_ID,"Cha_ID" : Cha_ID}

	async def ID_To_Mes(self,Ids):
		Mes_ID = Ids["Mes_ID"]
		Cha_ID = Ids["Cha_ID"]
		try:
			Cha = client.get_channel(Cha_ID)
		except:
			return None

		#get_channel
		try :
			Mes = await Cha.fetch_message(Mes_ID)
		except:
			return None

		return Mes


	async def Reload_Question(self):
		if len(Question_List) > 0:
			Q_ind = 1
			RRR = None
			for L in Question_List:
				L["Que_Ind"] = Q_ind

				ME_ADMIN = await self.ID_To_Mes(L["Message_Admin"])
				new_content = """:question:#{ind} : มีน้อง`{namae}`ถามมาว่า ในข้อ `{id}` ซึ่งถามมาว่า `{mes}`""".format(namae = L["Name_Sender" ],ind = L["Que_Ind"],id = L["Problem_Id"],mes = L["Que_Message"])

				await ME_ADMIN.edit(content = new_content)

				ME_ADMIN = await self.ID_To_Mes(L["Message"])

				if ME_ADMIN == None:
					RRR = Q_ind

				Q_ind+=1

			if RRR != None:
				Message_Sender = await self.ID_To_Mes(Question_List[RRR-1]["Message"])
				if Message_Sender != None:
					await Message_Sender.delete()

				Mes_Admin = await self.ID_To_Mes(Question_List[RRR-1]["Message_Admin"])
				if Mes_Admin != None:
					await Mes_Admin.delete()
				Question_User[Question_List[RRR-1]["Id_Sender"]].remove(Question_List[RRR-1]["Problem_Id"])
				Question_List.pop(RRR-1)
				await self.Reload_Question()
		self.sSave()

	async def Content_Announcement(self):

		global Contest_Time
		global Contest_namae
		global Contest_End
		global Contest_Id
		global TimeTick
		global User_Live_Count


		await self.wait_until_ready()
		Reload_Incoming_Contest()
		st = 0
		channel = client.get_channel(691575760674226217)
		while True:

			Now_Time = int(time.time())
			if TimeTick == 60*30:
				TimeTick = 0
				Reload_Incoming_Contest()


			if TimeTick %60 == 0 and (int(time.time())%(60*60*24) < Time_Convert(hour = 2,minn = 0) or int(time.time())%(60*60*24) > Time_Convert(hour = 5,minn = 0)):
				Reload_User_Live_Count()


			if Contest_Time != INF:
				if Now_Time > Contest_Time:
					if Contest_End != INF :
						if Now_Time < Contest_End:
							await Set_Bot_Namae(self,Contest_namae)
							await client.change_presence(activity=discord.Game(name='เหลือเวลา '+Second_To_Good_Str(Contest_End-Now_Time)+' help()'))
				else:
					await Set_Bot_Namae(self,Bot_Namae)
					await client.change_presence(activity = discord.Game(name='รอทำคอนเทส '+Contest_namae+' ในอีก '+Second_To_Good_Str(Contest_Time-Now_Time)+' help()'))

			else:
				await Set_Bot_Namae(self,Bot_Namae)

				#if int(time.time())%(60*60*24) >= Time_Convert(hour = 20,minn = 20):
				if(int(time.time())%(60*60*24) >= Time_Convert(hour = 2,minn = 0) and int(time.time())%(60*60*24) <= Time_Convert(hour = 5,minn = 0)):
					await client.change_presence(status=discord.Status.idle,activity=discord.Game(name='น้องนอนอยู่'))

				elif(User_Live_Count == -1):
					await client.change_presence(activity=discord.Game(name='นั่งทำโจทย์แบบเหงาๆ help() '))
				elif(User_Live_Count == 0):
					await client.change_presence(activity=discord.Game(name='นั่งทำโจทย์แบบเหงาๆจริงๆ help() '))
				else:
					await client.change_presence(activity=discord.Game(name='นั่งทำโจทย์กับอีก '+str(User_Live_Count)+' คน help() '))




			if st >= 7:
				st += 1
			if st == 12:
				Reload_Incoming_Contest()
				st = 0
			#print("Delta = "+ str(Contest_Time-Now_Time))
			if Is_Time_Passed_In_Range(Contest_Time,Now_Time,0):

				if Is_Time_Passed_In_Range(Contest_Time,Now_Time,60*5) and st < 6:
					st = 6
					await channel.send("Contest เริ่มแว้ววว ขอให้ทุกๆคนโชคดีครับ")

				elif Is_Time_Passed_In_Range(Contest_End,Now_Time,60*5) and st < 7:
					await channel.send("@everyone **TIME'S UP!!**\nหมดเวลาแล้วครับ\n"+Pick_One(["ยกมือขึ้นครับ!!!","ส่งอาหารได้แล้วครับ","มาดูผลกันครับ","ถือว่าทุกคนทำเต็มที่แล้วนะครับ เก่งมากๆครับ"]))
					st = 7


			elif Is_Time_Passed_In_Range(Contest_Time-60,Now_Time,60*5) and st < 5:
				st = 5
				await channel.send('@everyone\nอีกไม่ถึงนาทีจะมีคอนเทส '+Contest_namae+" ตั้งสติให้พร้อม")
			elif Is_Time_Passed_In_Range(Contest_Time-60*10,Now_Time,60*5) and st < 4:
				st = 4
				await channel.send('ทุกๆคนน\nอีก `10 นาที` จะมีคอนเทส '+Contest_namae+" "+Pick_One(["น้าาา เตรียมคีย์บอร์ดและ #include ให้พร้อม","はやい!","ปิดโปรแกรมให้หมด แต่ไม่ต้องปิดดิสน้าาา"]))
			elif Is_Time_Passed_In_Range(Contest_Time-60*60,Now_Time,60*5) and st < 3:
				st = 3
				await channel.send('@everyone\nใน `1 ชั่วโมง` จะมีคอนเทส '+Contest_namae+" "+Pick_One(["น้าาา เตรียมตัวให้พร้อม","เตรียมตัวเปิดตัว IDE คู่ใจได้เลย"]))
			elif Is_Time_Passed_In_Range(Contest_Time-60*60*24,Now_Time,60*60) and st < 2:
				st = 2
				await channel.send('ทุกๆคนน\nอีก `1 วัน` จะมีคอนเทส '+Contest_namae+" "+Pick_One(["น้าาานอนเล่นได้อีกไม่นานแว้วว","わくわく","..."]))
			elif Is_Time_Passed_In_Range(Contest_Time-60*60*24*2,Now_Time,60*5) and st < 1:
				st = 1

				await channel.send('@everyone\nอีก `2 วัน` จะมีคอนเทส '+Contest_namae+" "+Pick_One(["อีกน๊าน สบายได้","เตรียมตัวให้พร้อมมม","บอกก่อนเฉยๆ :)",":face_with_monocle:",":trophy:","やれやれ","ไม่ต้องรีบ เจนเคสยุอิอิ"]))

			if TimeTick < 0 :
				if Is_Time_Passed_In_Range(Contest_Time,Now_Time,0):
					if Is_Time_Passed_In_Range(Contest_Time,Now_Time,60*5) and st < 6:
						st = 6

					elif Is_Time_Passed_In_Range(Contest_End,Now_Time,60*5) and st < 7:
						st = 7

				elif Is_Time_Passed_In_Range(Contest_Time-60,Now_Time,0) and st < 5:
					st = 5
				elif Is_Time_Passed_In_Range(Contest_Time-60*10,Now_Time,0) and st < 4:
					st = 4
				elif Is_Time_Passed_In_Range(Contest_Time-60*60,Now_Time,0) and st < 3:
					st = 3
				elif Is_Time_Passed_In_Range(Contest_Time-60*60*24,Now_Time,0) and st < 2:
					st = 2
				elif Is_Time_Passed_In_Range(Contest_Time-60*60*24*2,Now_Time,0) and st < 1:
					st = 1

					await channel.send('@everyone\nอีก `2 วัน` จะมีคอนเทส '+Contest_namae+" อีกน๊าน สบายได้")
				TimeTick = 0
			TimeTick+= 1

			await asyncio.sleep(1)

	async def on_ready(self):
		global IsStart
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')


		#AllowMen = client.AllowedMentions(everyone = True)
		#print(type(AllowMen))//
		self.loop.create_task(self.Content_Announcement())
		if DEB =="" and not IsStart:
			IsStart = True
			channel = client.get_channel(691644349758308423)
			await channel.send('Bot is now online')


		self.lLoad()


	async def on_message(self, message):
		global Question_List
		global Question_User
		global Verify_User
		global TimeTick
		global VER
		global Guess_Num

        # we do not want the bot to reply to itself
		if message.author.id == self.user.id:
			return

		Is_Admin = False
		if hasattr(message.author, 'roles'):
			for r in message.author.roles:
				if str(r) == "Adminstator":
					Is_Admin = True

		Is_Channel_Admin = False
		if hasattr(message.channel, 'changed_roles'):
			for r in message.channel.changed_roles:
				if str(r) == "Adminstator":
					Is_Channel_Admin = True

		Is_Admin = Is_Admin and Is_Channel_Admin



		if message.content.lower().startswith(DEB+'hello()'):
			await message.channel.send((Pick_One(["สวัสดีเจ้า","สวัสดีจ้า","สวัสดีครับ","สวัสดีค่ะ","ສະບາຍດີ","Annyeonghaseyo","Kon'nichiwa","Hello","привет!","ว่าไง",";w;?","Meow Meooww?",":wave:","https://giphy.com/gifs/capoo-halloween-3ov9k0OmfNYeLdK4gg","Nǐ hǎo"])\
				+ " {0.author.mention}").format(message))


		if message.content.lower().startswith(DEB+'help()') or message.content.lower().startswith('!help'):
			em = discord.Embed(title = ":grey_question:สิ่งที่น้อมทำได้:grey_question:",description = "มีแค่นี้แหละ")
			em.add_field(name = ":grey_question:help()",value = "ก็ที่ทำอยู่ตอนนี้แหละ")
			em.add_field(name = ":trophy:contest()",value = "คอนเทสที่กำลังจะมาถึง")
			em.add_field(name = ":person_playing_handball:task()",value = "จำนวนโจทย์ตอนนี้")
			em.add_field(name = ":military_medal:ranking()",value = "คำสั่งไว้ขิงกัน")
			em.add_field(name = ":question:question(<ชื่อโจทย์>) <คำถาม>",value = "ถามคำถามเกี่ยวกับโจทย์ <ชื่อโจทย์>\nและ<คำถาม>ควรตอบเป็น Yes/No(ใช่/ไม่ใช่)")
			em.add_field(name = ":musical_note:[OtogRadio] <ชื่อเพลง>",value = "ขอเพลงได้ๆๆ")

			await message.channel.send(content = None ,embed = em)

			em = discord.Embed(title = ":speech_balloon:คำสั่งคนเหงา:speech_balloon:",description = "มีแค่นี้แหละ")
			em.add_field(name = ":speech_balloon:hello()",value = "คำสั่งคนเหงา")
			em.add_field(name = ":1234:guess_num()",value = "เล่นเกมทายเลข")

			await message.channel.send(content = None ,embed = em)

			if Is_Admin:
				em = discord.Embed(title = ":grey_question:สิ่งที่แอดมินทำได้:grey_question:",description = "แค่ในนี้เท่านั้น")
				em.add_field(name = ":orange_heart:user_life()",value = "ดูว่าใครมีชีวิตอยู่บ้าง")
				em.add_field(name = ":1234:Version()",value = "ตรวจสอบ Version")
				em.add_field(name = ":loudspeaker:ann() <Text>",value = "ประกาศๆๆๆๆ")
				em.add_field(name = ":loudspeaker:say(<Channel_ID>) <Text>",value = "ส่ง <Text> ไปยังห้อง <Channel_ID>")
				em.add_field(name = ":question:q_answer(<id>) <text>",value = "ตอบคำถามที่ <id> โดยคำถามจะหายด้วย")
				em.add_field(name = ":question:q_remove(<id>)",value = "ลบคำถามที่ <id>")
				em.add_field(name = ":question:q_clear()",value = "clear คำถามทั้งหมด(ต้องแน่ใจจริงๆว่าจะทำ)")
				em.add_field(name = ":exclamation:test()",value = "ดูว่าน้องยังมีชีวิตอยู่ไหม")
				em.add_field(name = ":exclamation:test_Verify()\\n<Code in C/C++>",value = "ทดสอบว่า Grader แมวๆยังใช้ได้ไหม")
				em.add_field(name = ":exclamation:check_Verify()",value = "ดูว่ามีใครมา Verify ไหม")
				em.add_field(name = ":exclamation:Watch_Code_Verify(<id>)",value = "ดู Code ของ <id>")
				em.add_field(name = ":exclamation:test_Verify_Delete()",value = "ลบ Code ของตัวเอง")
				em.add_field(name = ":exclamation:Force_Reload()",value = "บังคับให้รีโหลดฐานข้อมูลใหม่")
				em.add_field(name = ":sleeping_accommodation:shutdown()",value = "ชื่อก็บอกอยู่แล้ว")
				await message.channel.send(content = None ,embed = em)

		if message.content.lower().startswith(DEB+'guess_num()'):
			namae = str(message.author.id)
			
			GUILD = None
			try:
				GUILD = message.channel.guild
			except:
				pass

			if namae in Guess_Num:
				await message.channel.send("อย่าเล่นซ้ำเซ่ เจ้า"+Getname(self,namae,GUILD))
				await message.delete()
				return

			await message.channel.send(":crossed_swords:**โห๋ 1-1 ได้ครับเจ้า"+Getname(self,namae,GUILD)+"**:crossed_swords:\n" + \
				":1234:วิธีการเล่นคือ ข้าจะ**คิดเลขหนึ่งตัวตั้งแต่ 1 ถึง 100**\nเจ้าต้องทายเลขของค่าให้ถูก**ภายใน 7 ครั้ง**\nสามารถทายโดยการ `? <ตัวเลข>` เช่น `? 12`\n" + \
				":arrow_down:ถ้าเลขที่เจ้าตอบมัน**ต่ำกว่า** ข้าก็จะบอก**ต่ำไป** \n:arrow_up:แต่ถ้าเลขเจ้ามัน**สูงไป** ข้าก็จะบอก **สูงไป** \n:white_check_mark:แต่ถ้าถูก ข้าจะบอกว่าถูกเอง\n:x:ถ้าเจ้ากลัวที่จะแพ้ข้าก็สามารถออกได้โดยการ `? *` เอา หึๆๆๆ" \
				)
			
			NEW = {"Time" : 0,"Troll" : randint(0,2) == 0,"TrollSeq" : False,"ANS" : randint(1,100)}
			Guess_Num[namae] = dict(NEW)

		if message.content.lower().startswith(DEB+'? '):
			namae = str(message.author.id)

			GUILD = None
			try:
				GUILD = message.channel.guild
			except:
				pass

			if namae in Guess_Num:
				Mes_Str = message.content[len(DEB+'? '):]
				if Mes_Str.startswith('*'):
					await message.channel.send(":x:เจ้ายอมแพ้สินะ "+Getname(self,namae,GUILD))
					await message.delete()
					Guess_Num.pop(namae,None)
				else:
					LEK = 0
					try:
						LEK = int(Mes_Str)
					except:
						Guess_Num[namae]["Time"]+= 1
						if Guess_Num[namae]["Time"] == 7:
							await message.channel.send(":question:ข้าไม่รู้นะว่าเจ้าส่งอะไรมา("+Mes_Str+") แต่ตอนนี้เจ้าแพ้แล้ว... "+Getname(self,namae,GUILD)+"\nเฉลยคือ "+str(Guess_Num[namae]["ANS"]))
							await message.delete()
							Guess_Num.pop(namae,None)
						else:
							await message.channel.send(":question:ข้าไม่รู้นะว่าเจ้าส่งอะไรมา("+Mes_Str+") แต่เหลือ: **"+str(7-Guess_Num[namae]["Time"])+" ครั้ง**นะเจ้า "+Getname(self,namae,GUILD))
							await message.delete()
						return
					Guess_Num[namae]["Time"]+= 1
					if LEK > Guess_Num[namae]["ANS"]:
						if Guess_Num[namae]["Time"] == 7:
							if Guess_Num[namae]["Troll"] and Guess_Num[namae]["TrollSeq"]:
								await message.channel.send(":white_check_mark:ข้าล้อเล่นๆๆ จริงๆ"+str(Guess_Num[namae]["ANS"])+"มันถูกละ555 เจ้าชนะนะ "+Getname(self,namae,GUILD))
								await message.delete()
							else:
								await message.channel.send(":x:"+Mes_Str+"น่ะ**มันสูงเกิน**... เจ้าแพ้แล้ว "+Getname(self,namae,GUILD)+"\nเฉลยคือ "+str(Guess_Num[namae]["ANS"]))
								await message.delete()
							Guess_Num.pop(namae,None)
						else:
							await message.channel.send(":arrow_up:"+Mes_Str+"น่ะ**มันสูงเกิน**... เหลือ: **"+str(7-Guess_Num[namae]["Time"])+" ครั้ง**นะเจ้า "+Getname(self,namae,GUILD))
							await message.delete()
					elif LEK < Guess_Num[namae]["ANS"]:
						if Guess_Num[namae]["Time"] == 7:
							if Guess_Num[namae]["Troll"] and Guess_Num[namae]["TrollSeq"]:
								await message.channel.send(":white_check_mark:ข้าล้อเล่นๆๆ จริงๆ"+str(Guess_Num[namae]["ANS"])+"มันถูกละ555 เจ้าชนะนะ "+Getname(self,namae,GUILD))
								await message.delete()
							else:
								await message.channel.send(":x:"+Mes_Str+"ของเจ้าน่ะ**มันต่ำเกิน**... เจ้าแพ้แล้ว "+Getname(self,namae,GUILD)+"\nเฉลยคือ "+str(Guess_Num[namae]["ANS"]))
								await message.delete()
							Guess_Num.pop(namae,None)
						else:
							await message.channel.send(":arrow_down:"+Mes_Str+"ของเจ้าน่ะ**มันต่ำเกิน**... เหลือ: **"+str(7-Guess_Num[namae]["Time"])+" ครั้ง**นะเจ้า "+Getname(self,namae,GUILD))
							await message.delete()
					elif LEK == Guess_Num[namae]["ANS"]:
						if Guess_Num[namae]["Troll"]:
							if Guess_Num[namae]["Time"] == 7:
								await message.channel.send(":arrow_up:"+Mes_Str+"ของเจ้าน่ะ**มันสูงเกิน**... ข้าล้อเล่น \n:white_check_mark:**"+Mes_Str+"**น่ะถูกแล้วนะ... เจ้า "+Getname(self,namae,GUILD))
								await message.delete()
								Guess_Num.pop(namae,None)
							else:
								await message.channel.send(":arrow_up:"+Mes_Str+"ของเจ้าน่ะ**มันสูงเกิน**... เหลือ: **"+str(7-Guess_Num[namae]["Time"])+" ครั้ง**นะเจ้า "+Getname(self,namae,GUILD))
								await message.delete()
								Guess_Num[namae]["TrollSeq"] = True
						else:
							await message.channel.send(":white_check_mark:ถถถถถูกต้อง ตัวเลขข้าคือ "+Mes_Str+" เก่งไม่เบาเลยนะเจ้า "+Getname(self,namae,GUILD))
							await message.delete()
							Guess_Num.pop(namae,None)

					


		if message.content.lower().startswith(DEB+'[otogradio] '):
			Mes_Str = message.content[len(DEB+'[OtogRadio] '):]
			await message.channel.send(':microphone:กำลังเปิด `'+Mes_Str+"`")

		if message.content.lower().startswith(DEB+'verify()'):

			Is_RETURN0_Role = False
			if hasattr(message.author, 'roles'):
				for r in message.author.roles:
					Is_RETURN0_Role = Is_RETURN0_Role or (str(r) == "return 0;")
			else:
				return

			if not Is_RETURN0_Role:
				await message.delete()
				return

			MESS = message
			namae = str(message.author.id)

			if namae in Verify_User and Verify_User[namae] == 5:
				await MESS.author.send("ส่งมาก็ไม่ตรวจครับ หยิ่ง...\nลองติดต่อรุ่นพี่เอาครับ:)")
				return
			try:
				CODO = message.content[len(DEB+'Verify()')+1:]
			except:
				await message.delete()
				await MESS.author.send("**ส่ง Code มาด้วยเซ่**\nไม่ส่งแล้วจะตรวจยังไงงงง")
				return
			if CODO == "":
				await message.delete()
				await MESS.author.send("**ส่ง Code มาด้วยเซ่**\nไม่ส่งแล้วจะตรวจยังไงงงง")
				return
			n_FILE = open("VerifyCode\\"+namae+".cpp","w")
			n_FILE.write(CODO)
			n_FILE.close()

			await message.delete()
			await MESS.author.send("กำลังตรวจ...\n"+CODO)

			Verdict = Pat1Grader.Grading(namae)

			if Verdict.startswith("อ่อนหัด!!"):
				await MESS.author.send(Verdict)
			else:
				PERFECT = True
				for c in Verdict:
					if c == "T" or c == "-" or c == "X":
						PERFECT = False
						break
				if PERFECT:
					ALL_ROLE = MESS.guild.roles
					OTOGER = discord.utils.get(ALL_ROLE,name = "OTOGer")
					await MESS.author.send("ผลตรวจคือ : "+Verdict+"\nยินดีต้อนรับเข้าสู่เซิฟแห่งความฮา...OTOG")
					await message.author.edit(roles = [OTOGER])
					os.remove("VerifyCode\\"+namae+".cpp")
					os.remove("VerifyCode\\"+namae+"RUN.exe")
					Verify_User.pop(namae, None)

					return
				else:
					await MESS.author.send("ผลตรวจคือ : "+Verdict+"\nแต่ก็ยังไม่ผ่านอ่ะนะ ลองใหม่นะหึหึ")

			if namae in Verify_User:
				Verify_User[namae]+=1
			else:
				Verify_User[namae] = 1

			if Verify_User[namae] == 5:
				await MESS.author.send("เจ้าหมดโอกาสแล้ว...\nลองติดต่อรุ่นพี่เอาครับ")
			else:
				await MESS.author.send("ตอนนี้เหลือโอกาสเพียง **"+str(5-Verify_User[namae])+"** ครั้งเท่านั้น")
			self.sSave()



		if message.content.lower().startswith(DEB+'contest()'):
			await message.channel.send(Get_Incoming_Contest().format(message))

		if message.content.lower().startswith(DEB+'baka()'):
			await message.channel.send("<:baka:704310333120053248>")

		if message.content.lower().startswith(DEB+'task()'):
			await message.channel.send('มีอยู่ '+ Count_All_Task() +" ข้อ")
			await message.channel.send('ไปทำด้วย!!!')

		if message.content.lower().startswith(DEB+'today_task()'):
			await message.channel.send("อย่าถามเว้ย ไม่รุ")

		if message.content.lower().startswith(DEB+'ranking()'):
			await message.channel.send(Get_Top10_User())

		if message.content.lower().startswith(DEB+'question('):


			Message_Con = message
			if str(message.channel.type) != "private":
				await message.delete()


			Str_Content = Message_Con.content
			#question(<id>) <คำถาม>
			Id_Problem = Str_Content.find("(")

			Id_Sender = str(message.author.id)

			for i in range(1,500):
				if Str_Content[Id_Problem+i]==")":
					
					Id_Problem = Str_Content[Id_Problem+1:Id_Problem+i]
					if (Str_Content.find("("))+i+2 >= len(Str_Content):

						if (Id_Sender in Question_User) and (Id_Problem in Question_User[Id_Sender]):
							for QQ in Question_List:
								if QQ["Id_Sender"] == Id_Sender and QQ["Problem_Id"] == Id_Problem:
									BOI = await Message_Con.author.send(":axe:ลบคำถาม`"+Id_Problem+"`เรียบร้อยแล้ว")
									await BOI.delete(delay = 30)

									MESS = await self.ID_To_Mes(QQ["Message"])
									await MESS.delete()

									MESS = await self.ID_To_Mes(QQ["Message_Admin"])
									await MESS.delete()

									Question_List.remove(QQ)
									Question_User[Id_Sender].remove(Id_Problem)
									await self.Reload_Question()

									return


						await Message_Con.author.send("ไม่ใส่คำถามก็ไม่รู้จะตอบยังไงงง")
						return
					Question_Con =  Str_Content[(Str_Content.find("("))+i+2:]
					Question_Con.replace("`","'")
					
					break

			channel_Quation_All = client.get_channel(694444493570572288)


			Name_Sender = message.author.display_name
			

			#print("Id_Sender =",Id_Sender)
			#print("Question_User =",Question_User)
			#print(Id_Sender in Question_User)
			if Id_Sender in Question_User:
				if Id_Problem in Question_User[Id_Sender]:
					for QQ in Question_List:
						if QQ["Id_Sender"] == Id_Sender and QQ["Problem_Id"] == Id_Problem:
							
							#replace User Message
							Mess = await self.ID_To_Mes(QQ["Message"])
							Mess_Str = Mess.content
							i = Mess_Str.find("\n:regional_indicator_q: : `")
							i+=len("\n:regional_indicator_q: : `")

							Mess_Str = Mess_Str[:i]
							Mess_Str+=Question_Con + "`"
							await Mess.edit(content = Mess_Str)

							#replace Admin message
							Mess = await self.ID_To_Mes(QQ["Message_Admin"])
							Mess_Str = Mess.content
							i = Mess_Str.find("ซึ่งถามมาว่า `")
							i+=len("ซึ่งถามมาว่า `")

							Mess_Str = Mess_Str[:i]
							Mess_Str+=Question_Con + "`"

							await Mess.edit(content = Mess_Str)

							str_sen = ":tools:แก้คำถาม `{Pro_name}` เรียบร้อยแล้ว".format(Pro_name = Id_Problem)
							Nofi = await Message_Con.author.send(str_sen)
							await Nofi.delete(delay = 30)

							QQ["Que_Message"] = Question_Con

							return
				else:
					if len(Question_User[Id_Sender]) == 5:
						await Message_Con.author.send(":interrobang:รู้สึกว่าเจ้าจะถามเยอะไปแล้วน่ะ **นี่ปาไป 5 คำถามแว้วว**\nให้คนอื่นได้ถามบ้าง งิ")
						return
					else:
						Question_User[Id_Sender].append(Id_Problem)
			else:
				Question_User[Id_Sender] = [Id_Problem]




			Message_Sent = await Message_Con.author.send(":question:ในข้อ `{id}` \n:regional_indicator_q: : `{mes}`\n:regional_indicator_a: : รอไปก่อนแบบใจเย็นๆ...".format(id = Id_Problem,mes = Question_Con))

			Question_Ind = len(Question_List)+1
			Mes_Str = """:question:#{ind} : มีน้อง`{namae}`ถามมาว่า ในข้อ `{id}` ซึ่งถามมาว่า `{mes}`""".format(namae = Name_Sender,ind = Question_Ind,id = Id_Problem,mes = Question_Con)
			Message_Sent_G = await channel_Quation_All.send(Mes_Str)

			Question_List.append(\
			{"Name_Sender" : Name_Sender, \
			"Id_Sender" : Id_Sender, \
			"Que_Ind" : Question_Ind, \
			"Problem_Id" : Id_Problem, \
			"Que_Message" : Question_Con, \
			"Message" : self.Mes_To_ID(Message_Sent), \
			"Message_Admin" : self.Mes_To_ID(Message_Sent_G) \
			})
			self.sSave()




		for Mem in message.mentions:
			if self.user.name == Mem.display_name:
				WORDS = ["จงทำโจทย์ จงทำโจทย์ จงทำโจทย์",\
						"ทำโจทย์เถอะ ขอหล่ะ",\
						"ว่างมากนั้นก็ไปทำโจทย์สิ",\
						"ไม่อ่าน ไม่ตอบ ไม่สน...",\
						"แต่ว่า...ทำโจทย์ด้วยสิ...",\
						";w;","=A=!","- -*",\
						"แล้วไง?","https://giphy.com/gifs/sad-cry-capoo-3og0IG0skAiznZQLde","https://giphy.com/stickers/cat-pearl-capoo-TFUhSMPFJG7fPAiLpQ","https://giphy.com/gifs/happy-rainbow-capoo-XEgmzMLDhFQAga8umN","https://giphy.com/gifs/cat-color-capoo-dYZxsY7JIMSy2Afy6e","ระเบิดเวลา......**อ๊าาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาา**","โฮ่... แทนที่แกจะเข้าค่ายอื่น แกกลับเดินมาค่ายคอม อย่างนั้นนะเรอะ","เปล่าประโยชน์ เปล่าประโยชน์ เปล่าประโยชน์ เปล่าประโยชน์","**How Dare You!!??**","เคยฟังรึเปล่า... X ติดไซเรน (https://pastebin.com/6a7u1b85)","พี่รู้ว่ามันเศร้า แต่จงทำโจทย์ต่อไปครับ","ญิรดีร์ฏ้อณรับสูเก็ฒเฎอร์ฌาวไฑญ",":thinking:",":joy:",":poop:",":+1:",":eyes:",":P"]
				await message.channel.send(Pick_One(WORDS))



		##Admin Command
		if Is_Admin:

			if message.content.lower().startswith(DEB+'version()'):
				await message.channel.send('ตอนนี้ Version '+ VER + ' เด้อ!!')

			if message.content.lower().startswith(DEB+'test()'):
				await message.channel.send('ยังมีชีวิตอยู่เด้อ')

			if message.content.lower().startswith(DEB+'user_life()'):
				await message.channel.send(Get_User_Ongoing())

			if message.content.lower().startswith(DEB+'shutdown()'):
				channel = client.get_channel(691644349758308423)
				await channel.send('Bot is now shutting down')
				exit(0)

			if message.content.lower().startswith(DEB+'ann()'):

				channel = client.get_channel(691575760674226217)
				Mes_Str = message.content[len(DEB+'ann()')+1:]

						
				if len(message.attachments) > 0:
					F = []
					for A in message.attachments:
						NAMAE = A.filename
						await A.save(NAMAE)
						
						F.append(discord.File(fp = NAMAE,filename = NAMAE))
					await channel.send(content = ":loudspeaker:@everyone:loudspeaker:\n"+Mes_Str,files = F)

					try:
						os.remove(NAMAE)
					except:
						pass
						
				else:
					await channel.send(":loudspeaker:@everyone:loudspeaker:\n"+Mes_Str)
						
				await message.delete()


			if message.content.lower().startswith(DEB+'say('):
				Str_Content = message.content
				
				#Say(4412) ไอ้นี้มันอู้งานครับบ
				Id_channel = Str_Content.find("(")

				for i in range(1,40):
					if Str_Content[Id_channel+i]==")":
						channel = client.get_channel(int(Str_Content[Id_channel+1:Id_channel+i]))
						
						if len(message.attachments) > 0:
							F = []
							for A in message.attachments:
								NAMAE = A.filename
								await A.save(NAMAE)
								
								F.append(discord.File(fp = NAMAE,filename = NAMAE))
							await channel.send(content = Str_Content[Id_channel+i+2:],files = F)

							try:
								os.remove(NAMAE)
							except:
								pass
						
						else:
							await channel.send(Str_Content[Id_channel+i+2:])
						
						break
				await message.delete()

			if message.content.lower().startswith(DEB+'say_test('):
				Str_Content = message.content
				
				#Say(4412) ไอ้นี้มันอู้งานครับบ
				Id_channel = Str_Content.find("(")

				for i in range(1,40):
					if Str_Content[Id_channel+i]==")":
						channel = client.get_channel(int(Str_Content[Id_channel+1:Id_channel+i]))
						
						if len(message.attachments) > 0:
							F = []
							for A in message.attachments:
								NAMAE = A.filename
								await A.save(NAMAE)
								print("NAME file is",NAMAE)
								
								F.append(discord.File(fp = NAMAE,filename = NAMAE))
							await channel.send(content = Str_Content[Id_channel+i+2:],files = F)

							try:
								os.remove(NAMAE)
							except:
								print("Cant Delete file",NAMAE)
						
						else:
							print("Sending...",Str_Content[Id_channel+i+2:])
							await channel.send(Str_Content[Id_channel+i+2:])
						
						break
				await message.delete()

			if message.content.lower().startswith(DEB+'q_answer('):

				namae = str(message.author.id)
				GUILD = None
				try:
					GUILD = message.channel.guild
				except:
					pass
				namae = Getname(self,namae,GUILD)

				Str_Content = message.content
				Id_Problem = Str_Content.find("(")


				for i in range(1,40):
					if Str_Content[Id_Problem+i]==")":
						if Id_Problem+i+2 >= len(Str_Content):
							DEL = await message.channel.send(":interrobang:ไม่ใส่คำตอบก็ไม่รู้จะตอบยังไงงง")
							await DEL.delete(delay = 15)
							await message.delete()
							return

						Ans_Con =  Str_Content[Id_Problem+i+2:]
						Id_Question = Str_Content[Id_Problem+1:Id_Problem+i]
						break
				try:
					Id_Question = int(Id_Question)
				except ValueError:
					DEL = await message.channel.send(":interrobang:ไหว้ล่ะ ใส่ <id> เป็นจำนวนเต็มเถอะ\nเดวน้องบึ้ม>>>" + str(Id_Question))
					await DEL.delete(delay = 15)
					await message.delete()
					return


				if Id_Question > len(Question_List):
					DEL = await message.channel.send(":interrobang:อย่าตอบคำถามที่คำถามมันไม่มีจริงสิฟะ (ข้อที่"+str(Id_Question)+")")
					await DEL.delete(delay = 15)
					await message.delete()
					return

				Message_Sender = Question_List[Id_Question-1]["Message"]

				Message_Sender = await self.ID_To_Mes(Message_Sender)

				channel_Quation_All = client.get_channel(704547470591524884)#HISTORY

				if Message_Sender == None:
					DEL = await channel_Quation_All.send(":disappointed_relieved:น้องลบคำถามข้อที่ {ind} ไปแล้ว ;w;".format(ind = Id_Question))
					Question_User[Question_List[Id_Question-1]["Id_Sender"]].remove(Question_List[Id_Question-1]["Problem_Id"])
					Question_List.pop(Id_Question-1)
					await self.Reload_Question()
					await DEL.delete(delay = 15)
					await message.delete()
					return

				#Ans_Con

				await Message_Sender.channel.send((":white_check_mark:ในข้อ `{id}` \n:regional_indicator_q: : `{mes}`\n:regional_indicator_a: : `{ans}`").format(id = Question_List[Id_Question-1]["Problem_Id"],mes = Question_List[Id_Question-1]["Que_Message"],ans = Ans_Con))
				await Message_Sender.delete()

				Mes_Admin = await self.ID_To_Mes(Question_List[Id_Question-1]["Message_Admin"])

				if Mes_Admin != None:
					await Mes_Admin.delete()
				await message.delete()
				await channel_Quation_All.send(":white_check_mark:ตอบคำถามจากน้อง `{namae}` สำเร็จโดย `{admins}` ".format(admins = namae,ind = Id_Question,namae = Question_List[Id_Question-1]["Name_Sender"]))
				await channel_Quation_All.send(("ในข้อ `{id}` \n:regional_indicator_q: : `{mes}`\n:regional_indicator_a: : `{ans}`").format(id = Question_List[Id_Question-1]["Problem_Id"],mes = Question_List[Id_Question-1]["Que_Message"],ans = Ans_Con))

				Question_User[Question_List[Id_Question-1]["Id_Sender"]].remove(Question_List[Id_Question-1]["Problem_Id"])
				Question_List.pop(Id_Question-1)
				await self.Reload_Question()

			if message.content.lower().startswith(DEB+'q_remove('):
				
				namae = str(message.author.id)
				GUILD = None
				try:
					GUILD = message.channel.guild
				except:
					pass
				namae = Getname(self,namae,GUILD)

				Str_Content = message.content
				#question(<id>) <คำถาม>
				Id_Problem = Str_Content.find("(")


				for i in range(1,40):
					if Str_Content[Id_Problem+i]==")":
						Id_Question = Str_Content[Id_Problem+1:Id_Problem+i]
						break
				try:
					Id_Question = int(Id_Question)
				except ValueError:
					DEL = await message.channel.send(":interrobang:ไหว้ล่ะ ใส่ <id> เป็นจำนวนเต็มเถอะ\nเดวน้องบึ้ม>>>" + str(Id_Question))
					await DEL.delete(delay = 15)
					await message.delete()
					return


				if Id_Question > len(Question_List):
					DEL = await message.channel.send(":interrobang:อย่าลบคำถามที่คำถามมันไม่มีจริงสิฟะ (ข้อที่"+str(Id_Question)+")")
					await DEL.delete(delay = 15)
					await message.delete()
					return



				Message_Sender = await self.ID_To_Mes(Question_List[Id_Question-1]["Message"])
				if Message_Sender != None:
					await Message_Sender.delete()

				Mes_Admin = await self.ID_To_Mes(Question_List[Id_Question-1]["Message_Admin"])
				if Mes_Admin != None:
					await Mes_Admin.delete()

				channel_Quation_All = client.get_channel(704547470591524884)#HISTORY

				await channel_Quation_All.send(":axe:ลบคำถามสำเร็จโดย `{admins}`".format(admins = namae))

				Question_User[Question_List[Id_Question-1]["Id_Sender"]].remove(Question_List[Id_Question-1]["Problem_Id"])
				Question_List.pop(Id_Question-1)
				await self.Reload_Question()
				await message.delete()

			if message.content.lower().startswith(DEB+'q_clear()'):

				namae = str(message.author.id)
				GUILD = None
				try:
					GUILD = message.channel.guild
				except:
					pass
				namae = Getname(self,namae,GUILD)

				channel_Quation_All = client.get_channel(704547470591524884)#HISTORY
				await channel_Quation_All.send(":fire:ลาก่อย ซึ่งโดนเผาโดย `"+namae+"`")

				if len(Question_List) > 0:
					for q in Question_List:

						MES_A = await self.ID_To_Mes(q["Message"])
						if MES_A != None:
							await MES_A.delete()

						MES_A = await self.ID_To_Mes(q["Message_Admin"])
						if MES_A != None:
							await MES_A.delete()

				Question_List = []
				Question_User = {}
				self.sSave()
				await message.delete()

			if message.content.lower().startswith(DEB+'q_list()'):
				await message.channel.send("<:baka:704310333120053248>ไม่.... **ไม่ให้ใช้คำสั่งนี้แล้วเว้ย**")

			if message.content.lower().startswith(DEB+'test_verify()'):
				namae = str(message.author.id)
				CODO = message.content[len(DEB+'test_Verify()')+1:]
				n_FILE = open("VerifyCode\\"+namae+".cpp","w")
				n_FILE.write(CODO)
				n_FILE.close()
				await message.channel.send("รอแป๊ป...")

				Verdict = Pat1Grader.Grading(namae)

				if Verdict.startswith("อ่อนหัด!!"):
					await message.channel.send(Verdict)
				else:
					await message.channel.send(Verdict)

			if message.content.lower().startswith(DEB+'check_verify()'):
				if len(Verify_User.keys()) != 0:
					await message.channel.send("ตอนนี้มี `"+str(len(Verify_User.keys()))+"`ea ที่กำลังอยู่ในบททดสอบ")
					ALL_Verify = ""

					for USER in Verify_User.keys():#get_user
						ALL_Verify += "{ID}(`{NAME}`) ได้ลองไป `{times}` ครั้งแล้ว\n".format(ID = USER,NAME = Getname(self,USER,message.guild),times = Verify_User[USER])

					await message.channel.send(ALL_Verify)

				else:
					await message.channel.send("ไม่มีคนมา Verify งะ")

			if message.content.lower().startswith(DEB+'Watch_Code_Verify('):

				Watch_ID = len(DEB+'Watch_Code_Verify(')
				for i in range(1,100):
					if message.content[Watch_ID+i] == ")":
						Watch_ID = message.content[Watch_ID:Watch_ID+i]
						break

				try:
					F = open("VerifyCode\\"+Watch_ID+".cpp","r")
					CODO = F.read()
					F.close()
				except:
					await message.channel.send("หาของ `"+Getname(self,Watch_ID,message.guild)+"` ไม่เจองะ")
					return

				await message.channel.send(Getname(self,Watch_ID,message.guild)+"'s CODE\n`"+CODO+"`")

			if message.content.lower().startswith(DEB+'test_verify_delete()'):
				namae = str(message.author.id)
				try:
					os.remove("VerifyCode\\"+namae+".cpp")
					os.remove("VerifyCode\\"+namae+"RUN.exe")
				except:
					await message.channel.send("ไม่มีเว้ยย")
					return
				await message.channel.send("จัดการให้แล้ว")

			if message.content.lower().startswith(DEB+'force_reload()'):
				await message.channel.send("จัดการให้แล้ว!!")
				Reload_Incoming_Contest()
				TimeTick = -2




	async def on_guild_join(self,guild):
		await guild.system_channel.send("กราบสวัสดีพ่อแม่พี่น้องครับ")

	async def on_member_join(self, member):
		ALL_ROLE = member.guild.roles

		role = discord.utils.get(ALL_ROLE,name = "return 0;")
		await member.edit(roles = [role])

		guild = member.guild
		if guild.system_channel is not None:
			to_send = 'สวัสดีเจ้า {0.mention} สู่ {1.name}!'.format(member, guild)
			await guild.system_channel.send(to_send)

	async def on_member_remove(self, member):
		guild = member.guild
		if guild.system_channel is not None:
			to_send = 'ลาก่อย {0.mention}!'.format(member)
			await guild.system_channel.send(to_send)

	async def announcements(self,Con):
		channel = client.get_channel(691618323468779532)
		await channel.send(Con)


client = MyClient()
client.run(TOKEN)
