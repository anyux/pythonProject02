---建表语句
CREATE TABLE `universities`(
`name` varchar(100) NOT NULL COMMENT'学校名称',
`rank` int(8) NOT NULL DEFAULT '0' COMMENT '学校排名',
`country` varchar(128) DEFAULT NULL COMMENT '国家',
`city` varchar(128) DEFAULT NULL COMMENT '城市',
`state` varchar(128) DEFAULT NULL COMMENT '州省',
`undergraduate_num` varchar(128) DEFAULT NULL COMMENT '本科生人数',
`postgraduate_num` varchar(128) DEFAULT NULL COMMENT '研究生人数',
`website` text COMMENT '网站地址',
PRIMARY KEY (`name`))
engine=InnoDB DEFAULT charset=utf8mb4 COMMENT='大学信息表';

---授权语句
grant all on *.* to root@'192.168.255.%' identified by 'root' with grant option;
