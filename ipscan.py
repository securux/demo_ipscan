import os,socket,Queue,threading,argparse,time,sys,os,platform
parser = argparse.ArgumentParser();
parser.add_argument("-ip",nargs="+",help="xxx.py -ip 192.168.1.* 20 or -ip 192.168.*.* 20");
args = parser.parse_args()
pat = os.path.dirname(os.path.abspath(__file__)).replace("\\","/");
n,y = 0,255

def get_os(): 

  os = platform.system() 
  if os == "Windows": 
    return "n" 
  else: 
    return "c" 
   
def IsOpen(ip_str): 
	print ip_str,"---> Testing"
	cmd = ["ping", "-{op}".format(op=get_os()), "1", ip_str] 
	output = os.popen(" ".join(cmd)).readlines() 
	flag = False 
	for line in list(output): 
		if not line: 
			continue 
		if str(line).upper().find("TTL") >=0: 
			flag = True 
			break 
	q.get()
	if flag: 
		print "ip: %s is ok ***"%ip_str 
		f=open(pat+'/ip.txt','a')
		f.write("%s -----> is open \r\n" % ip_str)
		f.close()

try:
	ip,t =  args.ip[0],int(args.ip[1]);
	ip_l = ip.split('.');
	if len(ip_l) < 1:
		print 'IP error!';
		exit()
	else:
		for int_i in ip_l:
			if int_i != "*":
				if not int_i.isdigit() or len(int_i) >= 4 or int_i>255 and int_i<0:
					print "ip error!";exit();
except:
	print 'error:list index out of range;\r\nhelp: xx.py -ip 192.168.1.* 20'
	exit();

q = Queue.Queue(t);



if ip_l[0] == "172" and ip_l[1] == "*":
	n,y=16,32
elif ip_l[0] == "192" and ip_l[1] == "*":
	n,y=168,169
for x1 in xrange(n,y):
	ip1 = ip.replace("*",str(x1),1);
	ip1_count = ip.count('*');
	
	if ip1_count == 1:
		while True:
			if not q.full():
				t = threading.Thread(target=IsOpen,args=[ip1]).start();
				q.put(1)
				break;
			else:
				time.sleep(0.5)
	if ip1_count >= 2:
		for x2 in xrange(0,255):
			ip2 = ip1.replace("*",str(x2),1);
			ip2_count = ip.count('*');
			if ip2_count == 2:
				while True:
					if not q.full():
						t = threading.Thread(target=IsOpen,args=[ip2]).start();
						q.put(1)
						break;
					else:
						time.sleep(0.5)
			if ip2_count >= 3:
				for x3 in xrange(0,255):
					ip3 = ip2.replace("*",str(x2),1);
					ip3_count = ip.count('*');
					if ip3_count == 2:
						while True:
							if not q.full():
								t = threading.Thread(target=IsOpen,args=[ip3]).start();
								q.put(1)
								break;
							else:
								time.sleep(0.5)
