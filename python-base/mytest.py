# 需要提交准备好仓库的repo写入到yum服务器的/etc/yum.repos.d/目录下
# 定义repoid,repoid指的是repo文件中被中括号[],包起来的部分
list = ["base", "updates", "extras", "epel", "docker-ce-stable", "kubernetes", "ceph-jewel", "ceph-luminous",
        "ceph-nautilus", "gluster-10", "gluster-3.12", "gluster-4.0", "gluster-4.1", "gluster-5", "gluster-6",
        "gluster-7", "gluster-8", "gluster-9", "nfs-ganesha-28", "nfs-ganesha-30", "nfsganesha-28", "nfsganesha-30",
        "nfsganesha-4", "samba-411","elrepo","elrepo-testing","elrepo-kernel","elrepo-extras","gitlab-ce"]

# 生成update.sh脚本
def create_update_sh():
    print("#同步数据到本地节点")
    for item in list:
        my_str = "reposync -n --repoid={} -p /yum/{}/".format(item, item)
        print(my_str)

    print("#创建仓库数据")
    for item in list:
        my_str = "createrepo --update /yum/{}".format(item)
        print(my_str)


def other_base_repo():
    print("#其他节点配置yum源")
    for item in list:
        my_str = """[{}]
name={}
baseurl=http://192.168.255.60/{}
enabled=1
path=/
gpgcheck=0
	"""
        abc = my_str.format(item, item, item)
        print(abc)


if __name__ == '__main__':
    print('cat >/bin/update.sh <<EOF')
    print('#!/bin/bash')
    print('source /etc/profile')
    print('echo "starting Centos base sync yum repo"')
    # 更新update.sh脚本,用于同步镜像仓库,创建本地repo
    create_update_sh()
    print('EOF')
    print()
    # 打印输出内容
    print("cat >/etc/yum.repos.d/base.repo<<EOF")
    # 创建其他节点的基础repo文件,将此文件内容粘贴到其他节点的/etc/yum.repos.d/base.repo文件中即可
    other_base_repo()
    print("EOF")