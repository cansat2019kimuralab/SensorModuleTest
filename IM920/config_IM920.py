import sys
import IM920

if __name__ == "__main__":
	args = sys.argv
	
	if(args[1] == "RDCH"):
		data = IM920.Rdch()
	elif(args[1] == "STCH"):
		data = IM920.Stch(args[2])
	elif(args[1] == "ENWR"):
		data = IM920.Enwr()
	elif(args[1] == "RDID"):
		data = IM920.Rdid()
	#elif(args[1] == "SBRT"):
	#	data = IM920.Sbrt(args[2])
	elif(args[1] == "RDRT"):
		data = IM920.Rdrt()
	elif(args[1] == "SRID"):
		data = IM920.Srid(args[2])
	elif(args[1] == "RRID"):
		data = IM920.Rrid()
	else:
		data = "None"
	print(data)
