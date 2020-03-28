import discord
import requests
import json
import time
from random import randint
from urllib.request import Request, urlopen
req = Request('https://otog.cf/main', headers={'User-Agent': 'Mozilla/5.0'})

DEB = ""#Before Command

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

			e = webpage[i:i+j].split(",");

			Text_ALL = "";
			for stt in e:
				Text_ALL += stt + ", "

			return "ฮั่นแน่ มี "+Text_ALL[:-2]+" ทำโจทย์อยู่"
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

		Ap_Time = " ";
		if Delta > 60*60*24:
			Ap_Time = str(Delta//(60*60*24)) + " วัน "
		elif Delta > 60*60:
			Ap_Time = str(Delta//(60*60)) + " ชั่วโมง " + str((Delta%(60*60))//60) + " นาที "
		elif Delta > 60:
			Ap_Time = str(Delta//60) + " นาที "
		else:
			Ap_Time = "ไม่ถึงนาที! เตรียมมือเตรียมแขนเตรียมหัวเตรียมขาให้พร้อม"

		return "จะมีคอนเทส `" + Con['name'] + "` ในอีก `" + Ap_Time + "`" + Str_Time

	else:
		if Now_Time < Con['time_end'] :
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
		Rank_Str += "อันดับที่ " + StrNum[i] +" "+Content[i]["sname"]+" <"+str(Content[i]["rating"])+">\n"
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

	if Content[ANS]["id_Prob"] != id:

		Contest_api = requests.get("https://otog.cf/api/contest")
		if Contest_api.status_code != 200:
			return "เว็ปบึ้มง่าาาาาา"
		Contest_api = Contest_api.json()[-1]
		Now_Time = int(time.time())
		if Now_Time >= Contest_api['time_start'] and   Now_Time <= Contest_api['time_end']:
			#print(type(id),id,Contest_api['problems'][0])

			X = Contest_api['problems'][1:-1].split(',')

			for iid in X:
				iid = int(iid)
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

	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		await client.change_presence(activity=discord.Game(name='ขายวิญญาณ'))



	async def on_message(self, message):
		global Question_List
		global Question_User
        # we do not want the bot to reply to itself
		if message.author.id == self.user.id:
			return

		Is_Admin = False
		for r in message.author.roles:
			if str(r) == "Adminstator":
				Is_Admin = True

		Is_Channel_Admin = False
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
			em.add_field(name = "today_task()",value = "โจทย์ใหม่วันนี้")
			em.add_field(name = "question(<id>) <คำถาม>",value = "ถามคำถามเกี่ยวกับโจทย์ข้อที่ <id>\nและ<คำถาม>ควรตอบเป็น Yes/No(ใช่/ไม่ใช่)")

			await message.channel.send(content = None ,embed = em)

			if Is_Admin:
				em = discord.Embed(title = "สิ่งที่น้อมแอดมินทำได้",description = "แค่ในนี้เท่านั้น")
				em.add_field(name = "user_life()",value = "ดูว่าใครมีชีวิตอยู่บ้าง")
				em.add_field(name = "ann() <Text>",value = "ประกาศๆๆๆๆ")
				em.add_field(name = "say(<Channel_ID>) <Text>",value = "ส่ง <Text> ไปยังห้อง <Channel_ID>")
				em.add_field(name = "q_list()",value = "ดูคำถามทั้งหมดที่น้องๆถามมา")
				em.add_field(name = "q_answer(<id>) <text>",value = "ตอบคำถามที่ <id> โดยคำถามจะหายด้วย")
				em.add_field(name = "q_remove(<id>)",value = "ลบคำถามที่ <id>")
				em.add_field(name = "q_clear()",value = "clear คำถามทั้งหมด(ต้องแน่ใจจริงๆว่าจะทำ)")
				await message.channel.send(content = None ,embed = em)


		if message.content.startswith(DEB+'test()'):
			await message.channel.send('ยังมีชีวิตอยู่เด้อ')

		if message.content.startswith(DEB+'contest()'):
			await message.channel.send(Get_Incoming_Contest().format(message))

		if message.content.startswith(DEB+'task()'):
			await message.channel.send('มีอยู่ '+ Count_All_Task() +" ข้อ")
			await message.channel.send('ไปทำด้วย!!!')

		if message.content.startswith(DEB+'today_task()'):
			await message.channel.send('มีโจทย์ใหม่ '+ Count_Today_Task() +" ข้อ")
			await message.channel.send('ไปทำด้วย!!!')

		if message.content.startswith(DEB+'ranking()'):
			await message.channel.send(Get_Top10_User())

		if message.content.startswith(DEB+'question('):

			response = requests.get("https://otog.cf/api/problem")

			Message_Con = message
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
					Id_Problem = Str_Content[Id_Problem+1:Id_Problem+i]
					break
			try:
				Id_Problem = int(Id_Problem)
			except ValueError:
				await Message_Con.author.send("ไหว้ล่ะ ใส่ <id> เป็นจำนวนเต็มเถอะ\nพี่ๆจะได้ตอบคำถามได้ง่ายๆ ?" + str(Id_Problem))
				return
			channel_Quation_All = client.get_channel(693370035410042922)

			Problem_Name = Get_Problem_Name(Id_Problem)

			if Problem_Name == "???????!??????":
				await Message_Con.author.send("อย่าถามในข้อที่ยังไม่เปิดสิฟะ (ข้อที่"+str(Id_Problem)+")")
				return

			Name_Sender = message.author.display_name
			#Complete
			if Name_Sender in Question_User :
				Question_User[Name_Sender]+= 1
			else:
				Question_User[Name_Sender] = 1



			Message_Sent = await Message_Con.author.send("**ถามสำเร็จ**\nQ : ในข้อ `{id_name} : {id}` ถามว่า `{mes}`\nA : รอไปก่อนแบบใจเย็นๆ...".format(id_name = Problem_Name,id = Id_Problem,mes = Question_Con))

			Question_Ind = len(Question_List)+1
			Mes_Str = """Q{ind} : มีน้องๆถามมาว่า ข้อ `{id_name} : {id}` ว่า `{mes}`""".format(ind = Question_Ind,id_name = Problem_Name,id = Id_Problem,mes = Question_Con)
			Message_Sent_G = await channel_Quation_All.send(Mes_Str)

			Question_List.append(\
			{"Name_Sender" : Name_Sender, \
			"Que_Ind" : Question_Ind, \
			"Problem_Id" : Id_Problem, \
			"Problem_name" : Problem_Name, \
			"Que_Message" : Question_Con, \
			"Message" : Message_Sent, \
			"Message_Admin" : Message_Sent_G, \
			"ANS" : "Q : ในข้อ `{id_name} : {id}` ถามว่า `{mes}`\nA : ".format(id_name = Problem_Name,id = Id_Problem,mes = Question_Con) \
			})




		for Mem in message.mentions:
			if self.user.name == Mem.display_name:
				await message.channel.send(Get_Random_Text_forMention())
				break



		##Admin Command
		if Is_Admin:

			if message.content.startswith(DEB+'user_life()'):
				await message.channel.send(Get_User_Ongoing())

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
				#Ans_Con
				await Message_Sender.edit(content=(Question_List[Id_Question-1]["ANS"]+'`'+Ans_Con+'`'))

				channel_Quation_All = client.get_channel(693370035410042922)
				await Question_List[Id_Question-1]["Message_Admin"].delete()

				await channel_Quation_All.send("ตอบคำถามในข้อที่ {ind} สำเร็จ (คำถามจะเรียงใหม่ในทุกๆครั้งที่ตอบ)".format(ind = Id_Question))
				await channel_Quation_All.send(content=(Question_List[Id_Question-1]["ANS"]+'`'+Ans_Con+'`'))

				Question_List.pop(Id_Question-1)
				if len(Question_List) > 0:
					Q_ind = 1
					for L in Question_List:
						L["Que_Ind"] = Q_ind

						new_content =L["Message_Admin"].content
						for i in range(2,6):
							if new_content[i] == " ":
								new_content = "Q" + str(Q_ind)+new_content[i:]
								break;

						await L["Message_Admin"].edit(content = new_content)
						Q_ind+=1

			if message.content.startswith(DEB+'q_remove('):

				response = requests.get("https://otog.cf/api/problem")


				if response.status_code != 200:
					await message.channel.send("ตอนนี้ เซิฟบึ้มครับ\nค่อยตอบในภายหลังน้าา")
					return

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

				Message_Sender = Question_List[Id_Question-1]["Message"]

				await Message_Sender.delete()
				await Question_List[Id_Question-1]["Message_Admin"].delete()

				channel_Quation_All = client.get_channel(693370035410042922)

				await channel_Quation_All.send("ลบคำถามในข้อที่ {ind} สำเร็จ (คำถามจะเรียงใหม่ในทุกๆครั้งที่ตอบ)".format(ind = Id_Question))

				Question_List.pop(Id_Question-1)
				if len(Question_List) > 0:
					Q_ind = 1
					for L in Question_List:
						L["Que_Ind"] = Q_ind

						new_content =L["Message_Admin"].content
						for i in range(2,6):
							if new_content[i] == " ":
								new_content = "Q" + str(Q_ind)+new_content[i:]
								break;

						await L["Message_Admin"].edit(content = new_content)
						Q_ind+=1

			if message.content.startswith(DEB+'q_clear()'):
				channel_Quation_All = client.get_channel(693370035410042922)
				await channel_Quation_All.send("ลาก่อย")

				if len(Question_List) > 0:
					for q in Question_List:
						await q["Message"].delete()
						await q["Message_Admin"].delete()
				Question_List = []

			if message.content.startswith(DEB+'q_list()'):
				channel_Quation_All = client.get_channel(693370035410042922)
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
client.run(TOKEN)
