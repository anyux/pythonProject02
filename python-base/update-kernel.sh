#!/bin/bash
preVersion=5.19.2
currentVersion=$(uname -a | awk -F '[ .-]' '{print $3"."$4"."$5}')
function checkKernelVersion() {
  if [ ${currentVersion} == ${preVersion} ]; then
    echo "uname -r : ${currentVersion} is ${preVersion}, Is the latest version"
  else
    updateKernelVersion
  fi
}

function updateKernelVersion() {
  echo "记得首先更新仓库"
  yum -y update
  echo "查看可用的系统内核包:"
  yum --disablerepo="*" --enablerepo="elrepo-kernel" list available
  echo "安装最新内核:"
  yum --enablerepo=elrepo-kernel install kernel-ml -y
  echo "查看系统上的所有可用内核："
  sudo awk -F"'" '$1=="menuentry " {print i++ " : " $2}' /etc/grub2.cfg
  echo "通过 grub2-set-default 0 命令设置"
  grub2-set-default 0
  echo "设置 GRUB_DEFAULT=0，表示使用上一步的 awk 命令显示的编号为 0 的内核作为默认内核："
  if [ $(grep GRUB_DEFAULT=0 /etc/default/grub | wc -l) == 1 ]; then
    echo 1
  else
    echo "GRUB_DEFAULT=0" >>/etc/default/grub
  fi
  echo "通过 gurb2-mkconfig 命令创建 grub2 的配置文件，然后重启"
  grub2-mkconfig -o /boot/grub2/grub.cfg
  echo "please run "
  echo "sudo reboot "
}

function main() {
    checkKernelVersion
}

main