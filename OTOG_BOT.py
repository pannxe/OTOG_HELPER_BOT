import discord
import requests
import json
from json import JSONEncoder
import time
import os.path
import asyncio
from itertools import cycle
from random import randint
from urllib.request import Request, urlopen
req = Request('https://otog.cf/main', headers={'User-Agent': 'Mozilla/5.0'})

INF = 999999999999999999999999

DEB = ""#Before Command
VER = "B04"

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

def Count_Today_Task():
	return "??"

def Get_User_Ongoing():
	response = requests.get("https://otog.cf/api/countProblem")
	if response.status_code != 200:
		return "เว็ปบึ้มง่าาาาาา"
	Con = response.json()["onlineUser"]
	if (Con == 0):
		return "ไม่มีอะ เหงา Hereๆ"
	return "ฮั่นแน่...มีคนทำโจทย์อยู่ "+str(Con)+"คน *แต่ไม่บอกหรอกว่าคือใคร*"

def Get_Random_Text_forMention():

    Words = ["จงทำโจทย์ จงทำโจทย์ จงทำโจทย์","ทำโจทย์เถอะ ขอหล่ะ","ว่างมากนั้นก็ไปทำโจทย์สิ","ไม่อ่าน ไม่ตอบ ไม่สน...","แต่ว่า...ทำโจทย์ด้วยสิ...",";w;","=A=!","- -*","แล้วไง?","https://giphy.com/gifs/sad-cry-capoo-3og0IG0skAiznZQLde","https://giphy.com/stickers/cat-pearl-capoo-TFUhSMPFJG7fPAiLpQ","https://giphy.com/gifs/happy-rainbow-capoo-XEgmzMLDhFQAga8umN","https://giphy.com/gifs/cat-color-capoo-dYZxsY7JIMSy2Afy6e","ระเบิดเวลา......**อ๊าาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาาา**","โฮ่... แทนที่แกจะเข้าค่ายอื่น แกกลับเดินมาค่ายคอม อย่างนั้นนะเรอะ","เปล่าประโยชน์ เปล่าประโยชน์ เปล่าประโยชน์ เปล่าประโยชน์","**How Dare You!!??**","เคยฟังรึเปล่า... X ติดไซเรน (https://pastebin.com/6a7u1b85)","พี่รู้ว่ามันเศร้า แต่จงทำโจทย์ต่อไปครับ","ญิรดีร์ฏ้อณรับสูเก็ฒเฎอร์ฌาวไฑญ",":thinking:",":joy:",":poop:",":+1:",":eyes:",":P"]
    return Words[randint(0,len(Words)-1)]

def Get_Random_Text_forHello():
    Words = ["สวัสดีเจ้า","สวัสดีจ้า","สวัสดีครับ","สวัสดีค่ะ","ສະບາຍດີ","Annyeonghaseyo","Kon'nichiwa","Hello","привет!","ว่าไง",";w;?","Meow Meooww?",":wave:","https://giphy.com/gifs/capoo-halloween-3ov9k0OmfNYeLdK4gg","Nǐ hǎo"]
    return Words[randint(0,len(Words)-1)] + " {0.author.mention}"

Contest_Time = INF
Contest_namae = "??"
Contest_End = INF

TimeTick = 0

def Reload_Incoming_Contest():
	global Contest_Time
	global Contest_namae
	global Contest_End
	global TimeTick
	TimeTick = 0
	response = requests.get("https://otog.cf/api/contest")
	if response.status_code != 200:
		Contest_Time = INF
		Contest_namae = "??"
		Contest_End = INF
	Con = response.json()

	if len(Con) == 0:
		Contest_namae = "!!None!!"

	for cc in Con:
		if cc['time_start'] < Contest_Time:
			Contest_Time = cc['time_start']
			Contest_End = cc['time_start']
			Contest_namae = "`" + str(cc['idContest']) + "`(หาชื่อไม่เจองะ)"

def Get_Incoming_Contest():
	global Contest_Time
	global Contest_namae
	global Contest_End
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

		Ap_Time = " ";
		if Delta > 60*60*24:
			Ap_Time = str(Delta//(60*60*24)) + " วัน "
		elif Delta > 60*60:
			Ap_Time = str(Delta//(60*60)) + " ชั่วโมง " + str((Delta%(60*60))//60) + " นาที "
		elif Delta > 60:
			Ap_Time = str(Delta//60) + " นาที "
		else:
			Ap_Time = "ไม่ถึงนาที! เตรียมมือเตรียมแขนเตรียมหัวเตรียมขาให้พร้อม"

		return "จะมีคอนเทสที่" + Contest_namae +"ในอีก `" + Ap_Time + "`" + Str_Time

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

def Get_Last_ContestID():
	response = requests.get("https://otog.cf/api/contest/history")
	if response.status_code != 200:
		return None
	return response.json()[-1]["idContest"]

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

	if Content[ANS]["id_Prob"] != id:

		Contest_api = Get_Last_ContestID()
		Contest_api_new = requests.get("https://otog.cf/api/contest/"+str(Contest_api))
		Contest_api_old = (requests.get("https://otog.cf/api/contest/history")).json()[-1]

		if Contest_api_new.status_code != 200:
			return "เว็ปบึ้มง่าาาาาา"

		Now_Time = int(time.time())
		if Now_Time <= Contest_api_old['time_end']:
			#print(type(id),id,Contest_api['problems'][0])
			if Now_Time < Contest_api_old['time_start'] :
				return "NANI!?!?!?!?!?"
			X = Contest_api_new['problem']

			for iid in X:
				iid = iid["id_Prob"]
				if id ==iid:
					#print("F")
					ALL_P = requests.get("https://otog.cf/api/admin/problem")
					if ALL_P.status_code != 200:
						return "เว็ปบึ้มง่าาาาาา"
					ALL_P = ALL_P.json()
					noi,mak = 0,len(ALL_P)
					ANS = -1
					while noi <= mak:
						mid = (noi+mak)//2
						if (id <= ALL_P[mid]['id_Prob']):
							mak = mid-1
							ANS = mid
						else:
							noi = mid+1
					if ALL_P[ANS]["id_Prob"] == id:
						return ALL_P[ANS]["name"]
					else:
						return "???????!??????"



		return "???????!??????"
	else:
		return Content[ANS]["name"]
Question_List = []
Question_User = {}

class MyClient(discord.Client):

	global Question_List
	global Question_User
	global Contest_Time
	global Contest_namae
	global Contest_End
	global TimeTick

	def sSave(self):
		ddata = {
			"Question_List":Question_List,
			"Question_User":Question_User
		}
		with open("Save_Data"+VER+".otog", 'w') as outfile:
			json.dump(ddata, outfile)

	def lLoad(self):
		global Question_User
		global Question_List
		if os.path.isfile("Save_Data"+VER+".otog"):
			with open("Save_Data"+VER+".otog") as json_file:
				ddata = json.load(json_file)
				Question_List = ddata["Question_List"]
				Question_User = ddata["Question_User"]


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
				new_content =ME_ADMIN.content
				for i in range(2,6):
					if new_content[i] == " ":
						new_content = "Q" + str(Q_ind)+new_content[i:]
						break;

				await ME_ADMIN.edit(content = new_content)

				ME_ADMIN = await self.ID_To_Mes(L["Message"])

				if ME_ADMIN == None:
					RRR = Q_ind;

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
		global TimeTick


		await self.wait_until_ready()
		Reload_Incoming_Contest()
		st = 0
		channel = client.get_channel(691618323468779532)
		while True:

			Now_Time = int(time.time())
			if TimeTick == 60*30:
				TimeTick = 0
				Reload_Incoming_Contest()


			if Contest_Time != INF:
				if Now_Time > Contest_Time:
					if Contest_End != INF :
						if Now_Time < Contest_End:
							await client.change_presence(activity=discord.Game(name='กำลังทำคอนเทสจ้าา help()'))
				else:
					await client.change_presence(activity=discord.Game(name='รอทำคอนเทส help()'))
			else:
				await client.change_presence(activity=discord.Game(name='นั่งทำโจทย์แบบเหงาๆ help()'))

			if st >= 7:
				st += 1
			if st == 12:
				st = 0

			if Contest_Time - Now_Time < 0:

				if st < 6:
					st = 6
					await channel.send("Contest เริ่มแว้ววว ขอให้ทุกๆคนโชคดีครับ")

				elif Contest_End - Now_Time < -1 and st < 7:
					await channel.send("TIME'S UP\nหมดเวลาแล้วครับ\nยกมือขึ้นครับ!!!")
					st = 7

			elif Contest_Time - Now_Time < 60 and st < 5:
				st = 5
				await channel.send('ทุกๆคนน\nอีกไม่ถึงนาทีจะมีคอนเทส '+Con_Namae+" น้าาา เตรียมตัวให้พร้อม")
			elif Contest_Time - Now_Time <= 60*10 and st < 4:
				st = 4
				await channel.send('ทุกๆคนน\nอีก `10 นาที` จะมีคอนเทส '+Con_Namae+" น้าาา เตรียมตัวให้พร้อม")
			elif Contest_Time - Now_Time <= 60*60 and st < 3:
				st = 3
				await channel.send('ทุกๆคนน\nอีก `1 ชั่วโมง` จะมีคอนเทส '+Con_Namae+" น้าาา เตรียมตัวให้พร้อม")
			elif Contest_Time - Now_Time <= 60*60*24 and st < 2:
				st = 2
				await channel.send('ทุกๆคนน\nอีก `1 วัน` จะมีคอนเทส '+Con_Namae+" น้าาานอนเล่นได้วันนี้")
			elif Contest_Time - Now_Time <= 60*60*24*2 and st < 1:
				st = 1
				await channel.send('ทุกๆคนน\nอีก `2 วัน` จะมีคอนเทส '+Con_Namae+" น้าาานอนเล่นได้วันนี้")

			TimeTick+= 1

			await asyncio.sleep(1)

	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		if DEB =="":
			channel = client.get_channel(691644349758308423)
			await channel.send('Bot is now online')


		self.lLoad()


	async def on_message(self, message):
		global Question_List
		global Question_User

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



		if message.content.startswith(DEB+'hello()'):
			await message.channel.send(Get_Random_Text_forHello().format(message))
		if message.content.startswith(DEB+'help()') or message.content.startswith('!help'):
			em = discord.Embed(title = "สิ่งที่น้อมทำได้",description = "มีแค่นี้แหละ")
			em.add_field(name = "help()",value = "ก็ที่ทำอยู่ตอนนี้แหละ")
			em.add_field(name = "hello()",value = "คำสั่งคนเหงา")
			em.add_field(name = "contest()",value = "คอนเทสที่กำลังจะมาถึง")
			em.add_field(name = "task()",value = "จำนวนโจทย์ตอนนี้")
			#em.add_field(name = "today_task()",value = "โจทย์ใหม่วันนี้")
			em.add_field(name = "ranking()",value = "คำสั่งไว้ขิงกัน")
			em.add_field(name = "question(<id>) <คำถาม>",value = "ถามคำถามเกี่ยวกับโจทย์ข้อที่ <id>\nและ<คำถาม>ควรตอบเป็น Yes/No(ใช่/ไม่ใช่)")
			em.add_field(name = "[OtogRadio] <ชื่อเพลง>",value = "ขอเพลงได้ๆๆ")

			await message.channel.send(content = None ,embed = em)

			if Is_Admin:
				em = discord.Embed(title = "สิ่งที่แอดมินทำได้",description = "แค่ในนี้เท่านั้น")
				em.add_field(name = "user_life()",value = "ดูว่าใครมีชีวิตอยู่บ้าง")
				em.add_field(name = "ann() <Text>",value = "ประกาศๆๆๆๆ")
				em.add_field(name = "say(<Channel_ID>) <Text>",value = "ส่ง <Text> ไปยังห้อง <Channel_ID>")
				em.add_field(name = "q_list()",value = "ดูคำถามทั้งหมดที่น้องๆถามมา")
				em.add_field(name = "q_answer(<id>) <text>",value = "ตอบคำถามที่ <id> โดยคำถามจะหายด้วย")
				em.add_field(name = "q_remove(<id>)",value = "ลบคำถามที่ <id>")
				em.add_field(name = "q_clear()",value = "clear คำถามทั้งหมด(ต้องแน่ใจจริงๆว่าจะทำ)")
				em.add_field(name = "shutdown()",value = "ชื่อก็บอกอยู่แล้ว")
				await message.channel.send(content = None ,embed = em)


		if message.content.startswith(DEB+'test()'):
			await message.channel.send('ยังมีชีวิตอยู่เด้อ')

		if message.content.startswith(DEB+'[OtogRadio] '):
			Mes_Str = message.content[len(DEB+'[OtogRadio] '):]
			await message.channel.send(':microphone:กำลังเปิด `'+Mes_Str+"`")

		if message.content.startswith(DEB+'contest()'):
			await message.channel.send(Get_Incoming_Contest().format(message))

		if message.content.startswith(DEB+'task()'):
			await message.channel.send('มีอยู่ '+ Count_All_Task() +" ข้อ")
			await message.channel.send('ไปทำด้วย!!!')

		if message.content.startswith(DEB+'today_task()'):
			await message.channel.send("อย่าถามเว้ย ไม่รุ")

		if message.content.startswith(DEB+'ranking()'):
			await message.channel.send(Get_Top10_User())

		if message.content.startswith(DEB+'question('):

			response = requests.get("https://otog.cf/api/problem")

			Message_Con = message
			if str(message.channel.type) != "private":
				await message.delete()

			if response.status_code != 200:
				await Message_Con.author.send("ตอนนี้ เซิฟบึ้มครับ\nค่อยถามในภายหลังน้าา")
				return

			Str_Content = Message_Con.content
			#question(<id>) <คำถาม>
			Id_Problem = Str_Content.find("(");


			for i in range(1,40):
				if Str_Content[Id_Problem+i]==")":
					if Id_Problem+i+2 >= len(Str_Content):
						await Message_Con.author.send("ไม่ใส่คำถามก็ไม่รู้จะตอบยังไงงง")
						return

					Question_Con =  Str_Content[Id_Problem+i+2:]
					Question_Con.replace("`","'")
					Id_Problem = Str_Content[Id_Problem+1:Id_Problem+i]
					break
			try:
				Id_Problem = int(Id_Problem)
			except ValueError:
				await Message_Con.author.send("ไหว้ล่ะ ใส่ <id> เป็นจำนวนเต็มเถอะ\nพี่ๆจะได้ตอบคำถามได้ง่ายๆ ?" + str(Id_Problem))
				return
			channel_Quation_All = client.get_channel(694444493570572288)

			Problem_Name = Get_Problem_Name(Id_Problem)

			if Problem_Name == "???????!??????":
				await Message_Con.author.send("อย่าถามในข้อที่ยังไม่เปิดสิฟะ (ข้อที่"+str(Id_Problem)+")")
				return
			elif Problem_Name == "NANI!?!?!?!?!?":
				await Message_Con.author.send("เห้ย!? เจ้ารู้ได้ไงว่ามันจะออกข้อที่"+str(Id_Problem)+"\nหรือว่า แกน่ะ คือผู้ใช้แสตนอย่างงั้นรึ")
				return

			Name_Sender = message.author.display_name
			Id_Sender = str(message.author.id)

			#print("Id_Sender =",Id_Sender)
			#print("Question_User =",Question_User)
			#print(Id_Sender in Question_User)
			if Id_Sender in Question_User:
				#print("Find ID")
				if Id_Problem in Question_User[Id_Sender]:
					#print("Find Problem")
					for QQ in Question_List:
						if QQ["Id_Sender"] == Id_Sender and QQ["Problem_Id"] == Id_Problem:
							#print("GetQuestion")
							#replace User Message
							Mess = await self.ID_To_Mes(QQ["Message"])
							Mess_Str = Mess.content
							i = Mess_Str.find("\nQ : `")
							i+=len("\nQ : `")

							Mess_Str = Mess_Str[:i]
							Mess_Str+=Question_Con + "`"

							#replace Admin message
							Mess = await self.ID_To_Mes(QQ["Message_Admin"])
							Mess_Str = Mess.content
							i = Mess_Str.find("ซึ่งถามมาว่า `")
							i+=len("ซึ่งถามมาว่า `")

							Mess_Str = Mess_Str[:i]
							Mess_Str+=Question_Con + "`"

							await Mess.edit(content = Mess_Str)

							str_sen = "แก้คำถาม `{id}:{Pro_name}` เรียบร้อยแล้ว".format(id = Id_Problem,Pro_name = Problem_Name)
							await Message_Con.author.send(str_sen)

							return
				else:
					if len(Question_User[Id_Sender]) == 5:
						await Message_Con.author.send("รู้สึกว่าเจ้าจะถามเยอะไปแล้วน่ะ **นี่ปาไป 5 คำถามแว้วว**\nให้คนอื่นได้ถามบ้าง งิ")
						return
					else:
						Question_User[Id_Sender].append(Id_Problem)
			else:
				Question_User[Id_Sender] = [Id_Problem]




			Message_Sent = await Message_Con.author.send("**ถามสำเร็จ**\nในข้อ `{id_name} : {id}` \nQ : `{mes}`\nA : รอไปก่อนแบบใจเย็นๆ...".format(id_name = Problem_Name,id = Id_Problem,mes = Question_Con))

			Question_Ind = len(Question_List)+1
			Mes_Str = """Q{ind} : มีน้อง`{namae}`ถามมาว่า ข้อ `{id_name} : {id}` ซึ่งถามมาว่า `{mes}`""".format(namae = Name_Sender,ind = Question_Ind,id_name = Problem_Name,id = Id_Problem,mes = Question_Con)
			Message_Sent_G = await channel_Quation_All.send(Mes_Str)

			Question_List.append(\
			{"Name_Sender" : Name_Sender, \
			"Id_Sender" : Id_Sender, \
			"Que_Ind" : Question_Ind, \
			"Problem_Id" : Id_Problem, \
			"Problem_name" : Problem_Name, \
			"Que_Message" : Question_Con, \
			"Message" : self.Mes_To_ID(Message_Sent), \
			"Message_Admin" : self.Mes_To_ID(Message_Sent_G), \
			"ANS" : "Q : ในข้อ `{id_name} : {id}` ถามว่า `{mes}`\nA : ".format(id_name = Problem_Name,id = Id_Problem,mes = Question_Con) \
			})
			self.sSave()




		for Mem in message.mentions:
			if self.user.name == Mem.display_name:
				await message.channel.send(Get_Random_Text_forMention())
				break



		##Admin Command
		if Is_Admin:

			if message.content.startswith(DEB+'user_life()'):
				await message.channel.send(Get_User_Ongoing())

			if message.content.startswith(DEB+'shutdown()'):
				channel = client.get_channel(691644349758308423)
				await channel.send('Bot is now shutting down')
				exit(0)

			if message.content.startswith(DEB+'ann()'):
				Mes_Str = message.content[len(DEB+'ann()')+1:]
				channel = client.get_channel(691575760674226217)
				await channel.send(Mes_Str)

			if message.content.startswith(DEB+'say('):
				Str_Content = message.content
				#Say(4412) ไอ้นี้มันอู้งานครับบ
				Id_channel = Str_Content.find("(");

				for i in range(1,40):
					if Str_Content[Id_channel+i]==")":
						channel = client.get_channel(int(Str_Content[Id_channel+1:Id_channel+i]))
						await channel.send(Str_Content[Id_channel+i+2:])
						break

			if message.content.startswith(DEB+'q_answer('):

				response = requests.get("https://otog.cf/api/problem")


				if response.status_code != 200:
					await message.channel.send("ตอนนี้ เซิฟบึ้มครับ\nค่อยตอบในภายหลังน้าา")
					return

				Str_Content = message.content
				#question(<id>) <คำถาม>
				Id_Problem = Str_Content.find("(");


				for i in range(1,40):
					if Str_Content[Id_Problem+i]==")":
						if Id_Problem+i+2 >= len(Str_Content):
							await message.channel.send("ไม่ใส่คำตอบก็ไม่รู้จะตอบยังไงงง")
							return

						Ans_Con =  Str_Content[Id_Problem+i+2:]
						Id_Question = Str_Content[Id_Problem+1:Id_Problem+i]
						break
				try:
					Id_Question = int(Id_Question)
				except ValueError:
					await message.channel.send("ไหว้ล่ะ ใส่ <id> เป็นจำนวนเต็มเถอะ\nเดวน้องบึ้ม>>>" + str(Id_Question))
					return


				if Id_Question > len(Question_List):
					await message.channel.send("อย่าตอบคำถามที่คำถามมันไม่มีจริงสิฟะ (ข้อที่"+str(Id_Question)+")")
					return

				Message_Sender = Question_List[Id_Question-1]["Message"]

				Message_Sender = await self.ID_To_Mes(Message_Sender)

				channel_Quation_All = client.get_channel(694444493570572288)

				if Message_Sender == None:
					await channel_Quation_All.send("น้องลบคำถามข้อที่ {ind} ไปแล้ว ;w;".format(ind = Id_Question))
					Question_User[Question_List[Id_Question-1]["Id_Sender"]].remove(Question_List[Id_Question-1]["Problem_Id"])
					Question_List.pop(Id_Question-1)
					await self.Reload_Question()
					return

				#Ans_Con
				await Message_Sender.edit(content=(Question_List[Id_Question-1]["ANS"]+'`'+Ans_Con+'`'))


				Mes_Admin = await self.ID_To_Mes(Question_List[Id_Question-1]["Message_Admin"])

				if Mes_Admin != None:
					await Mes_Admin.delete()
				await message.delete()
				await channel_Quation_All.send("ตอบคำถามจากน้อง {namae} ในข้อที่ {ind} สำเร็จ ".format(ind = Id_Question,namae = Question_List[Id_Question-1]["Name_Sender"]))
				await channel_Quation_All.send(content=(Question_List[Id_Question-1]["ANS"]+'`'+Ans_Con+'`'))

				Question_User[Question_List[Id_Question-1]["Id_Sender"]].remove(Question_List[Id_Question-1]["Problem_Id"])
				Question_List.pop(Id_Question-1)
				await self.Reload_Question()

			if message.content.startswith(DEB+'q_remove('):

				Str_Content = message.content
				#question(<id>) <คำถาม>
				Id_Problem = Str_Content.find("(");


				for i in range(1,40):
					if Str_Content[Id_Problem+i]==")":
						Id_Question = Str_Content[Id_Problem+1:Id_Problem+i]
						break
				try:
					Id_Question = int(Id_Question)
				except ValueError:
					await message.channel.send("ไหว้ล่ะ ใส่ <id> เป็นจำนวนเต็มเถอะ\nเดวน้องบึ้ม>>>" + str(Id_Question))
					return


				if Id_Question > len(Question_List):
					await message.channel.send("อย่าลบคำถามที่คำถามมันไม่มีจริงสิฟะ (ข้อที่"+str(Id_Question)+")")
					return



				Message_Sender = await self.ID_To_Mes(Question_List[Id_Question-1]["Message"])
				if Message_Sender != None:
					await Message_Sender.delete()

				Mes_Admin = await self.ID_To_Mes(Question_List[Id_Question-1]["Message_Admin"])
				if Mes_Admin != None:
					await Mes_Admin.delete()

				channel_Quation_All = client.get_channel(694444493570572288)

				await channel_Quation_All.send("ลบคำถามในข้อที่ {ind} สำเร็จ (คำถามจะเรียงใหม่ในทุกๆครั้งที่ตอบ)".format(ind = Id_Question))

				Question_User[Question_List[Id_Question-1]["Id_Sender"]].remove(Question_List[Id_Question-1]["Problem_Id"])
				Question_List.pop(Id_Question-1)
				await self.Reload_Question()

			if message.content.startswith(DEB+'q_clear()'):
				channel_Quation_All = client.get_channel(694444493570572288)
				await channel_Quation_All.send("ลาก่อย")

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

			if message.content.startswith(DEB+'q_list()'):
				channel_Quation_All = client.get_channel(694444493570572288)
				if len(Question_List) > 0:

					Str_Content = "มีคำถามอยู่ `{crt}` ข้อ...\n".format(crt = len(Question_List))

					Q_ind = 1

					#{"Name_Sender" : message.author.display_name,"Que_Ind" : Question_Ind,"Problem_Id" : Id_Problem,"Que_Message" : Question_Con,"Message" : Message_Sent,"ANS"

					for q in Question_List:
						Str_Content += "Q{ind} : จาก `{namae}` ถามในข้อ `{pro_ind}` : `{pro_name}` ว่า `{mess}`\n".format(ind = Q_ind,namae = q["Name_Sender"],pro_ind = q["Problem_Id"],pro_name = q["Problem_name"],mess = q["Que_Message"])
						Q_ind+=1

					await message.channel.send(Str_Content)

				else:
					await message.channel.send("ไม่มีใครถามมางะ เหงาจุง")




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
client.loop.create_task(client.Content_Announcement())
client.run(TOKEN)
