#!/usr/bin/python
#-*- coding:utf-8 -*-

import json

def getdata(filename,gendata):
	sampledata = {
		'dokeycheck':True,
		'fixbrokenkeys':True
	}
	for i in sampledata:
		if i not in gendata:
			gendata[i] = sampledata[i]
	dokeycheck = True
	try:
		data = json.load(open(filename))
		generatedata = 0
	except IOError:
		generatedata = 1
		data = {}
	else:
		if 'dokeycheck' in data:
			dokeycheck = data['dokeycheck']

	if dokeycheck:
		class tempclass:pass
		tempclass.data = data
			
		def checkkeys(dict1,dict2):
			wrongkeys = {}
			if type(dict2) == dict:
				for key in dict2:
					#check if key missing
					if key not in dict1:
						wrongkeys[key]=None
					#check if value is in the right type
					elif type(dict1[key])!=type(dict2[key]):
						try: dict1[key] = type(dict2[key])(dict1[key])
						except:wrongkeys[key]=None
					#check if value is dict or list
					elif type(dict2[key]) is dict or type(dict2[key]) is list:
						deepkeycheckreturn = checkkeys(dict1[key],dict2[key])
						if len(deepkeycheckreturn) != 0:
							wrongkeys[key]=deepkeycheckreturn
			
			elif type(dict2) == list:
				for i in range(len(dict1)):
					d2p = i%len(dict2)
					#check if value is in the right type
					if type(dict1[i])!=type(dict2[d2p]):
						try: dict1[i] = type(dict2[d2p])(dict1[i])
						except Exception as exc:
							wrongkeys[i]=None
					#check if value is dict or list
					elif type(dict2[d2p]) is dict or type(dict2[d2p]) is list:
						deepkeycheckreturn = checkkeys(dict1[i],dict2[d2p])
						if len(deepkeycheckreturn) != 0:
							wrongkeys[i] = deepkeycheckreturn
			return(wrongkeys)
	
		if generatedata:
			wrongkeys = []
		else:
			wrongkeys = checkkeys(tempclass.data,gendata)
	
		if generatedata:
			print("genenerating a config file")
			data = gendata
			writedata = open("data.json","w")
			writedata.write(json.dumps(data,indent=4))
			writedata.close()
	
		elif len(wrongkeys) > 0:
			
			def fixkeys(brokendict,wrongkeys,sourcedict,prevkeys = ""):
				if prevkeys == "":
					print("fixing keys")
				else:
					print("fixing keys in " +prevkeys)
				for i in wrongkeys:
					if type(i) is int and type(sourcedict) is list:
						j = i%len(sourcedict)
					else:
						j = i
					if (i not in brokendict and type(brokendict) == dict) or (len(brokendict) <= i and type(brokendict) == list):
						brokendict[i] = sourcedict[j]
						if prevkeys == "":
							print("fixed missing key: %s"%(i))
						else:
							print("fixed missing key: %s,%s"%(prevkeys,i))
					elif type(sourcedict[j]) == dict or type(sourcedict[j]) is list:
						if prevkeys == "":
							fixkeys(brokendict[i],wrongkeys[i],sourcedict[j],i)
						else:
							fixkeys(brokendict[i],wrongkeys[i],sourcedict[j],"%s,%s"%(prevkeys,i))
					else:
						brokendict[i] = sourcedict[j]
						if prevkeys == "":
							print("fixed broken key: %s"%(i))
						else:
							print("fixed broken key: %s,%s"%(prevkeys,i))
				data = tempclass.data
				writedata = open("data.json","w")
				writedata.write(json.dumps(data,indent=4))
				writedata.close()
				
			if 'fixbrokenkeys' not in data:
				fixkeys(tempclass.data,wrongkeys,gendata)
			elif data['fixbrokenkeys']:
				fixkeys(tempclass.data,wrongkeys,gendata)
			else:
				def printbrokenkeys(keys,prevkeys = ""):
					for i in keys:
						if type(keys[i]) is dict:
							if prevkeys != "":
								printbrokenkeys(keys[i],i)
							else:
								printbrokenkeys(keys[i],"%s,%s"%(prevkeys,i))
						elif prevkeys == "":
							print("broken key: %s"%(i))
						else:
							print("broken key: %s,%s"%(prevkeys,i))
		return(data)


__all__ = [getdata]
