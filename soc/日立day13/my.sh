#!/usr/bin/env bash


function foo() {

name=$1
# shellcheck disable=SC2006
for version in `skopeo list-tags docker://registry.aliyuncs.com/k8sxio/${name} | jq .Tags[]`
do
v1=`echo ${name}:${version}|sed 's/\"//g'`
skopeo copy docker://registry.aliyuncs.com/k8sxio/${v1} docker://192.168.255.70/library/${v1} --insecure-policy --src-tls-verify=false --dest-tls-verify=false
done

}

function main() {
  comments=("kube-apiserver" "kube-controller-manager" "kube-scheduler" "kube-proxy" "pause" "etcd" "coredns"
)
    for comment in ${comments[*]} ; do
        echo ${comment}
    done
}

main