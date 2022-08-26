cat >/bin/update.sh <<EOF
#!/bin/bash
source /etc/profile
echo "开始同步华为yum仓库"
reposync -n --repoid=extras7 /yum/extras/
reposync -n --repoid=updates7 /yum/update/
reposync -n --repoid=base7 -p /yum/base/
reposync -n --repoid=epel7 -p /yum/epel/
echo "更新yum仓库元数据"
createrepo --update /yum/base
createrepo --update /yum/epel
createrepo --update /yum/updates
createrepo --update /yum/extras
EOF
