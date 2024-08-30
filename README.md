# 准备工作：

## 配置运行环境

1. 安装python3.8～python3.11的任意python版本
2. 在代码库下面安装虚拟环境到venv文件夹, 然后运行`source venv/bin/activate`
3. 在虚拟环境中运行`pip install -r requirements.txt`

## 配置网络和浏览器

1. 找个http或socks 代理在系统层连接上
2. 下载安装Chrome浏览器, 并设为默认浏览器
3. 安装SwitchyOmega浏览器插件

## 配置GitHub CLI

1. 打开Chrome浏览器，并登录上自己的GitHub账号
2. 在GitHub账号中创建一个名字为vpn的代码库，并提交需要的文件
3. 运行`brew install gh`
4. 运行`gh auth login`
5. 运行`gh auth refresh -h github.com -s codespace`
7. 运行`gh codespace create -R <username>/<repo> -b <branch>`
8. 将codespace name配置到config.json，比如`shiny-space-yodel-r7wg7j4r5pr3xqrp`

## 配置gcloud

1. 下载安装gcloud
2. 创建gmail账号，并创建一个GCP project
3. 运行`gcloud init --skip-diagnostics --console-only`
4. 运行`gcloud auth login --no-launch-browser`
5. 运行`gcloud config set project <PROJECT_ID>`
6. 运行`gcloud alpha cloud-shell ssh --dry-run --force-key-file-overwrite`来创建公钥和私钥
7. 运行`gcloud config set proxy/type socks5 && gcloud config set proxy/address localhost && gcloud config set proxy/port 8888`
8. 通过浏览器登陆到cloud shell, 并上传需要的文件到vpn2中
9. 在cloud shell中创建`.customize_environment`文件，并写入如下内容：
    ```shell
    #!/bin/sh
    sudo apt-get -y install screen iputils-ping
    ```

## 配置系统版本
1. 将system配置到config.json，比如`linux`或者`macos`
   
## 配置浏览器插件
1. github vpn: localhost:8888
2. gcp vpn: localhost:8889


## 安装桌面快捷方式
运行`./install.sh`
