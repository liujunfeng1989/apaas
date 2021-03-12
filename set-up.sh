#! /bin/bash

## 引入变量
#source
apps=${*}
readonly now_path=$(dirname "$0")
readonly base_path=$(cd "${now_path}" && pwd)

## 生成要部署的inventory
function create_inventory() {

  if [ ${#apps} -eq 0 ]; then
    echo "#--> No Apps Specified, Exit" && exit 1
  elif [ "${apps}" == 'full' ]; then
    echo "#--> Try to Deploy All Apps"
    python get_inventory.py full
  else
    echo "${apps[*]} will be deploy"
    python get_inventory.py ${apps}
  fi

}

function untar_pkg() {
  app=$1
  pkg_path=${base_path}/medias/pkgs/${app}
  cd "${pkg_path}" && /bin/tar -zxf $(pkg_path)/"${app}".tar.gz
}

function replace_template() {
  app=$1
  python create_template.py app

}

function replace_playbook() {
  app=$1
  python create_template.py playbook

}

function tar_pkg() {
  app=$1
  pkg_path=${base_path}/medias/pkgs/${app}
  cd "${pkg_path}" && \
   /bin/tar -zcf "${app}".tar.gz ${app} && \
   /bin/rm -rf "${app}"

}

## 部署
function deploy_app() {
  app=$1
  ansible-playbook -i inventory_hosts install_app_playbook.yml
}

function main() {

  ## 要部署的app必须包含在machines.conf，并且包含要将app部署在那台机器
  ## 获取所有要部署的app的inventory，获取到inventory名字：inventory_hosts

  create_inventory

  for app in ${apps}; do
    untar_pkg "${app}"
    replace_template "${app}"
    replace_playbook "${app}"
    tar_pkg "${app}"
    deploy_app "${app}"
  done

}

main
