zabbix_haproxy
==============

Zabbix script for monitoring haproxy

Usage:

* zhaproxy.py -d : Discovers the frontends/backends configurations
* zhaproxy.py -c : Check all the frontends/backends configurations
* zhaproxy.py -p &lt;proxy_name&gt; -s &lt;server_name&gt; -v &lt;attribute&gt; : Gets the specified value

UserParameters:

* haproxy.discovery: returns all available metrics
* haproxy.parameter: returns the value of the defined metric

See haproxy.cfg contains the configuration of the zabbix UserParameters.
For example.
UserParameter=haproxy.discovery,/usr/local/check_openstack/zhaproxy.py -d
UserParameter=haproxy.allstatus,/usr/local/check_openstack/zhaproxy.py -c
UserParameter=haproxy.parameter[*],/usr/local/check_openstack/zhaproxy.py -p $1 -s $2 -v $3
UserParameter=haproxy.mysql_galera_cluster,/usr/local/check_openstack/zhaproxy.py -p mysql_galera_cluster -s FRONTEND  -v status


TODO: Zabbix template
