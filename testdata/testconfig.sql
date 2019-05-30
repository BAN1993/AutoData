INSERT INTO `autodata_config`.`config` 
(
	`id`,
	`flag`,
	`needSVNCommit`,
	`desc`,
	`path`,
	`filename`,
	`dbip`,
	`dbport`,
	`dbuser`,
	`dbpwd`,
	`dbname`,
	`sql`,
	`drawconfig`,
	`control`
)
VALUES
(
	'120',
	'1',
	'1',
	'监控-web邮件量',
	'/root/bantest/tool/AutoData/Data/monitor/',
	'web邮件量.xls',
	'127.0.0.1',
	'3306',
	'sa1',
	'sa1',
	'mobile_log',
	'SELECT\r\n	date(logtime) AS \'day\',\r\n	`code`,\r\n	count(*) AS \'count\'\r\nFROM\r\n	log_post_mail\r\nWHERE\r\n	logtime BETWEEN DATE_FORMAT(\r\n		(\r\n			SELECT\r\n				date(adddate(now() ,- 1))\r\n		),\r\n		\"%Y-%m-%d 00:00:00\"\r\n	)\r\nAND DATE_FORMAT(\r\n	(\r\n		SELECT\r\n			date(adddate(now() ,- 1))\r\n	),\r\n	\"%Y-%m-%d 23:59:59\"\r\n)\r\nGROUP BY\r\n	date(logtime),\r\n	`code`\r\nORDER BY\r\n	`code`',
	'{1:{\'fname\':\'web邮件量.png\',\'title\':\'mail\',\'index\':\'day\',\'columns\':\'code\',\'data\':\'count\'}}',
	''
);


INSERT INTO `autodata_config`.`config` (
	`id`,
	`flag`,
	`needSVNCommit`,
	`desc`,
	`path`,
	`filename`,
	`dbip`,
	`dbport`,
	`dbuser`,
	`dbpwd`,
	`dbname`,
	`sql`,
	`drawconfig`,
	`control`
)
VALUES
(
	'124',
	'1',
	'1',
	'监控-登录大厅失败',
	'/root/bantest/tool/AutoData/Data/monitor/',
	'登录大厅失败.xls',
	'127.0.0.1',
	'3306',
	'sa1',
	'sa1',
	'mobile_log',
	'SELECT\r\n	date(logtime) AS \'day\',\r\n	flag,\r\n	count(*) AS \'count\'\r\nFROM\r\n	dbsvr_login_lobby\r\nWHERE\r\n	logtime BETWEEN DATE_FORMAT(\r\n		(\r\n			SELECT\r\n				date(adddate(now() ,- 1))\r\n		),\r\n		\"%Y-%m-%d 00:00:00\"\r\n	)\r\nAND DATE_FORMAT(\r\n	(\r\n		SELECT\r\n			date(adddate(now() ,- 1))\r\n	),\r\n	\"%Y-%m-%d 23:59:59\"\r\n)\r\nAND flag <> 0\r\nGROUP BY\r\n	date(logtime),\r\n	flag\r\nORDER BY\r\n	flag',
	'{1:{\'fname\':\'登录大厅失败.png\',\'title\':\'loginLobby\',\'index\':\'day\',\'columns\':\'flag\',\'data\':\'count\'}}',
	''
);


INSERT INTO `autodata_config`.`config` (
	`id`,
	`flag`,
	`needSVNCommit`,
	`desc`,
	`path`,
	`filename`,
	`dbip`,
	`dbport`,
	`dbuser`,
	`dbpwd`,
	`dbname`,
	`sql`,
	`drawconfig`,
	`control`
)
VALUES
(
	'135',
	'1',
	'1',
	'监控-进程监控-Tool',
	'/root/bantest/tool/AutoData/Data/monitor/',
	'进程监控-Tool.xls',
	'47.98.44.38',
	'3306',
	'auto_user',
	'wpHkqhM^CbFYRjPBJ',
	'mobile_count',
	'SELECT\r\n	date(logtime) AS \'day\',\r\n	appid,\r\n	avg(usecpu) AS \'avgcpu\',\r\n	avg(userss) AS \'avgrss\',\r\n	max(usecpu) AS \'maxcpu\',\r\n	max(userss) AS \'maxrss\'\r\nFROM\r\n	count_cpuinfo\r\nWHERE\r\n	logtime BETWEEN DATE_FORMAT(\r\n		(\r\n			SELECT\r\n				date(adddate(now() ,- 1))\r\n		),\r\n		\"%Y-%m-%d 00:00:00\"\r\n	)\r\nAND DATE_FORMAT(\r\n	(\r\n		SELECT\r\n			date(adddate(now() ,- 1))\r\n	),\r\n	\"%Y-%m-%d 23:59:59\"\r\n)\r\nAND svrtype = 62\r\nGROUP BY\r\n	date(logtime),\r\n	appid',
	'{1:{\'fname\':\'进程监控-Tool-平均cpu.png\',\'title\':\'avgCpu\',\'index\':\'day\',\'columns\':\'appid\',\'data\':\'avgcpu\'},1:{\'fname\':\'进程监控-Tool-平均rss.png\',\'title\':\'avgRss\',\'index\':\'day\',\'columns\':\'appid\',\'data\':\'avgrss\'}}',
	''
);

