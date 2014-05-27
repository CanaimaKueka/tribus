# Overview

MySQL is a fast, stable and true multi-user, multi-threaded SQL database server.
SQL (Structured Query Language) is the most popular database query language in
the world. The main goals of MySQL are speed, robustness and ease of use.

Percona is fork of MySQL by Percona Inc. which focuses on maximizing
performance, particularly for heavy workloads. It is a drop-in replacement for
MySQL and features XtraDB, a drop-in replacement for the InnoDB storage engine.

[http://www.mysql.com](http://www.mysql.com)

[http://www.percona.com/software/percona-server](http://www.percona.com/software/percona-server)

# Usage

## General

To deploy a MySQL service:

    juju deploy mysql

Once deployed, you can retrive the MySQL root user password by logging in to the machine via `juju ssh`
and readin the `/var/lib/mysql/mysql.passwd` file. To log in as root MySQL User at the MySQL console
you can issue the following:

    juju ssh mysql/0
    mysql -u root -p=`cat /var/lib/mysql/mysql.passwd`

To change deployment to a Percona server:

    juju set mysql flavor=percona

## Optimization

You can tweak various options to optimize your MySQL deployment:

* max-connections - Maximum connections allowed to server or '-1' for default.

* preferred-storage-engine - A comma separated list of storage engines to
  optimize for. First in the list is marked as default storage engine. 'InnoDB'
  or 'MyISAM' are acceptable values.

* tuning-level - Specify 'safest', 'fast' or 'unsafe' to choose required
  transaction safety. This option determines the flush value for innodb commit
  and binary logs. Specify 'safest' for full ACID compliance. 'fast' relaxes the
  compliance for performance and 'unsafe' will remove most restrictions.

* dataset-size - Memory allocation for all caches (InnoDB buffer pool, MyISAM
  key, query). Suffix value with 'K', 'M', 'G' or 'T' to indicate unit of
  kilobyte, megabyte, gigabyte or terabyte respectively. Suffix value with '%'
  to use percentage of machine's total memory.

* query-cache-type - Specify 'ON', 'DEMAND' or 'OFF' to turn query cache on,
  selectively (dependent on queries) or off.

* query-cache-size - Size of query cache (no. of bytes) or '-1' to use 20%
  of memory allocation.

Each of these can be applied by running:

    juju set <service> <option>=<value>

e.g.

    juju set mysql preferred-storage-engine=InnoDB
    juju set mysql dataset-size=50%
    juju set mysql query-cache-type=ON
    juju set mysql query-cache-size=-1

## Replication

MySQL supports the ability to replicate databases to slave instances. This
allows you, for example, to load balance read queries across multiple slaves or
use a slave to perform backups, all whilst not impeding the master's
performance.

To deploy a slave:

    # deploy second service
    juju deploy mysql mysql-slave

    # add master to slave relation
    juju add-relation mysql:master mysql-slave:slave

Any changes to the master are reflected on the slave.

Any queries that modify the database(s) should be applied to the master only.
The slave should be treated strictly as read only.

You can add further slaves with:

    juju add-unit mysql-slave

## Monitoring

This charm provides relations that support monitoring via either Nagios or
Munin. Refer to the appropriate charm for usage.
