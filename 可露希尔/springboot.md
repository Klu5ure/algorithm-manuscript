# linux安装、权限、目录

```shell
# linux安装软件方式，以ubuntu为例
# 二进制方式
    # 安装deb包
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i google-chrome-stable_current_amd64.deb
    sudo apt -f install
    或者直接apt install xxx.deb，会自动帮你dpkg
    # 安装直接二进制文件
    wget https://下载链接
    chmod +x 文件名
    sudo mv 文件名 /usr/local/bin/
# apt
	# 相当于直接从网上下载deb包，然后安装，帮你省略了繁琐的dpkg步骤
	apt install ./软件名.deb

# 关于可执行文件和配置文件的路径
当你使用 apt 安装软件时，Ubuntu 会自动安装软件包的所有相关文件，包括可执行文件、库文件、文档和配置文件。安装过程通常包括以下几个步骤：
可执行文件：会被放置到系统的标准路径，如 /usr/bin 或 /usr/local/bin。
库文件：通常位于 /lib、/usr/lib 或 /usr/local/lib 下。
配置文件：通常会被放置到 /etc 目录中。例如，安装 nginx 时，配置文件可能会出现在 /etc/nginx 目录下。
依赖关系：apt 会自动处理软件包的依赖关系，确保所有必需的库文件和工具都已经安装。
	
# 关于权限
# 上面的二进制直接文件需要chmod +x 文件名来赋予权限
ls -l /path/to/your/binary
-rw-r--r-- 1 user user 12345678 Dec 23 12:00 your_binary
chmod +x /path/to/your/binary
ls -l /path/to/your/binary
-rwxr-xr-x 1 user user 12345678 Dec 23 12:00 your_binary

# 怎么看
-rwxr-xr--为例
# 第一个-代表文件，如果是d则是目录，
rw-：所有者有读写权限。
r--：所属组有只读权限。
r--：其他人有只读权限。
# 关于数字表示法：r=4,w=2,x=1, so 7=rwx,6=rw-,5=r-x,4=r--
# chmod修改权限，可以用符号模式和数字模式
chmod 644 example.txt # 所有者读写，组、其他只读
chmod a+x script.sh # 所有用户添加执行权限
chmod o-w example.txt # 删除其他人的写权限
chmod +x script.sh：# 可以省略a，为 script.sh 文件添加可执行权限（对所有用户）。
chmod u+x file.txt：# 给文件所有者（user）添加执行权限。
chmod g-w file.txt：# 去掉同组用户的写权限。
chmod o=r file.txt：# 将其他用户的权限设置为只读。
```

```shell
# 关于服务，软件可以做成服务放在系统运行
sudo nano /etc/systemd/system/your_service_name.service
# -----------------
[Unit]
Description=描述服务的功能
After=network.target  # 确保在网络服务启动后运行（如果需要网络）

[Service]
ExecStart=/path/to/your/program    # 程序的路径和参数
WorkingDirectory=/path/to/working/directory  # （可选）指定工作目录
Restart=always                     # （可选）在程序退出后自动重启
User=your_username                 # （可选）指定运行的用户
Group=your_groupname               # （可选）指定运行的用户组
Environment="VAR_NAME=value"       # （可选）指定环境变量

# 日志输出
StandardOutput=append:/vms/output.log
StandardError=append:/vms/output.log

[Install]
WantedBy=multi-user.target         # 服务运行的目标环境
# ------------
sudo systemctl daemon-reload
sudo systemctl start your_service_name
sudo systemctl status your_service_name

sudo systemctl stop your_service_name 
sudo systemctl enable your_service_name # 开机启用
sudo systemctl disable your_service_name # 禁止开机启用

# 如果不是root用户，用这个可能会有问题，用java -jar的话，并且yml在外面，要加上WorkingDirectory

# 有时候SELinux会导致无法输入日志到某个文件，需要关闭
# setenforce 0 临时禁用
# chcon -t var_log_t /root/wvp/ 或者将日志文件的目录添加到这里

# 排错流程，先直接运行一下，再看看日志journalctl -u vms.service，再看看权限，防火墙和SELinux
```

# docker、yum

```shell
安装docker
sudo yum update -y
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io
# 上面会自动帮你装一个docker.service，所以这里可以直接start
sudo systemctl start docker
sudo docker run hello-world
sudo systemctl enable docker

yum配置镜像源
如果sudo yum install -y yum-utils报错，要给yum加上镜像源，可以手动修改配置文件，但推荐直接下载
先备份原来的yum配置文件
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
下载阿里云镜像源文件到/etc/yum.repos.d/CentOS-Base.repo
curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum clean all
yum makecache
yum update -y

如果某个仓库始终无法访问，可以禁用
yum-config-manager --disable base

如果缺一些库，可以装这个
sudo yum install epel-release

```

# linux命令

```shell
ps -ef | grep MediaServer
netstat -tulnp | grep :554
lsof -i:554
pkill MediaServer

systemctl stop firewalld
sudo firewall-cmd --zone=public --query-port=8080/tcp
sudo firewall-cmd --zone=public --add-port=8080/tcp --permanent
sudo systemctl stop firewalld
sudo systemctl disable firewalld
sudo systemctl status firewalld
sudo firewall-cmd --list-all

# 标准输出放到normal.log 错误输出放到error.log
java -jar wvp-pro-2.7.2-07080233.jar > normal.log 2> error.log

# 都放到output.log
nohup java -jar your-application.jar > output.log 2>&1 &
# 类似于上面的命令，1代表标准输出，2代表错误输出，&1代表放到1输出的地方也就是output.log，但是直接2>output.log可能会覆盖掉原来的标准输出，所以要用&1
nohup java -jar your-application.jar 1 > output.log 2>output.log &

# java远程debug，先在idea右上角添加配置，填上服务器ip，打包上传，然后服务器运行下面的命令，idea启动
java -Xdebug -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=0.0.0.0:5005 -jar


查看公网地址
curl ifconfig.me

# 查看大小，-h人类阅读 -r倒序排序
du -h --max-depth=1 . | sort -hr
# 正序，默认是按第一列的数字排序，加上-h后，它就知道这个k m g是什么意思，可以按文件大小排序
du -h --max-depth=1 . | sort -h
4.0K   ./file.txt
200K   ./dir1
50M    ./dir2
1.2G   ./dir3

grep "test" output.log
#ABC 后 前 前后
grep "test" output.log -A 3 
```

# git

```shell
# git 提交代码流程
git checkout master
git pull origin master
git checkout -b feature/your-feature-name # git branch xxx + git checkout xxx
修改代码
git add .
git commit -m "Implement new feature"
git push origin feature/your-feature-name
提交PR
git branch -d feature/your-feature-name     # Delete the branch locally
git push origin --delete feature/your-feature-name  # Delete the branch remotely
```

```shell
# git 查看旧版本，再回到新版本
git log
commit ea7bdffe3ce1d2f9f12d605416554d9f8472ed30 (HEAD, master)
Author: Klu5ure <errorhassei@qq.com>
Date:   Fri Aug 2 18:04:55 2024 +0800

    new

commit e1dd3d6bf1c057e5de671b18386999df6e647980
Author: Klu5ure <errorhassei@qq.com>
Date:   Fri Aug 2 18:04:21 2024 +0800

    init


git checkout e1dd3d
git checkout ea7bdffe
# 如果退回到init后不记得新版本的id了，直接看log是找不到的，可以用git reflog，然后git checkout
```

```shell
# how to send a PR to upstream
# 关联origin（git clone的时候已经关联）和upstream
git remote add upstream https://github.com/original-owner/original-repo.git
git fetch upstream

# 合并，有两种方法，第一种是merge，第二种是rebase
# 方法一，merge
git checkout main  # 如果你的分支是master，将main改成master
git merge upstream/main  
# 方法二，rebase
git checkout main  
git rebase upstream/main

git push origin

# 如果有冲突，git pull

# git pull拉取origin, git fetch拉取upstream，处理好冲突，然后git push提交到origin，就能从origin提交到upstream


# git pull upstream master = git fetch upstream + git merge upstream/master
```

# springboot

```java
// @PathVariable和@RequestParam
@GetMapping("/users/{id}")
public ResponseEntity<User> getUserByIdAndFilter(@PathVariable("id") Long id,
                                                 @RequestParam("filter") String filter) {
    // 使用id从路径中提取
    // 使用filter从查询参数中提取
    // 处理代码
}
```

```java
// @EventListener使用

@Service
public class OrderService {
    @Autowired
    private ApplicationEventPublisher applicationEventPublisher;

    public void placeOrder(String orderId) {
        // 处理订单逻辑
        System.out.println("Order placed: " + orderId);

        // 发布订单事件
        OrderPlacedEvent orderPlacedEvent = new OrderPlacedEvent(this, orderId);
        applicationEventPublisher.publishEvent(orderPlacedEvent);
    }
}
@Component
public class EmailService {
    @EventListener
    public void handleOrderPlacedEvent(OrderPlacedEvent event) {
        // 发送确认邮件
        System.out.println("Sending confirmation email for order: " + event.getOrderId());
    }
}
如果还有别的service，可以直接添加，不需要动orderservice的代码

在orderservice里发布事件，别的service里可以收到这个事件，然后执行
也就是说orderservice里不用添加别的service，也能调用别的service的方法
除此之外，传统方法里，每添加一个service，都要加到orderservice里才能继续调用，需要修改orderservice的代码，不好
用了event之后，只要在新的service上加监听器就行了，orderservice不用修改

总结：
使用事件驱动模型的主要优点之一就是减少了服务之间的直接依赖，使得在添加新功能时无需修改现有的服务逻辑
1. 松耦合：在OrderService中发布事件，而不是直接调用其他服务的方法。这使得OrderService不需要知道其他服务的存在，从而降低了耦合度。
2. 高扩展性：每次需要添加新功能时，只需创建新的事件监听器，而不需要修改OrderService的代码。这符合开闭原则（对扩展开放，对修改关闭）。
3. 单一职责原则：OrderService只负责处理订单和发布事件，具体的后续操作由各自独立的监听器完成，每个服务各司其职，职责明确。

```



- Throwable
  - Error：系统级别的错误，jvm无法处理
  - Exception：可捕获和处理的异常
    - Checked Exception：如果不加try catch或者throw，编译无法通过。加了try catch之后，即使发生异常，程序不会停止
    - Unchecked Exception：不加try catch或者throw，可以运行，但是一旦发生异常，程序直接停止。加了try catch之后，即使发生异常，程序不会停止

```
Throwable
│
├── Error                      （严重问题，通常无法处理）
│   ├── OutOfMemoryError
│   ├── StackOverflowError
│   └── InternalError
│
└── Exception                  （检查异常，可以处理的异常）
    │
    ├── Checked Exception      （检查异常，必须处理）
    │   ├── IOException
    │   ├── SQLException
    │   └── ClassNotFoundException
    │
    └── Unchecked Exception    （非检查异常，不强制处理）
        └── RuntimeException
            ├── NullPointerException
            ├── ArrayIndexOutOfBoundsException
            ├── ClassCastException
            ├── IllegalArgumentException
            └── ArithmeticException

```

```java
/**
回调函数，将函数作为参数传递到另一个函数中，然而java做不到，所以要用接口来代替，做法
1.定义接口DataCallback
2.定义一个函数fetchData(DataCallback callback)
3.调用fetchData函数的时候，实现接口。其实这时候就相当于定义好了想要传入的函数具体是什么

**/
public interface DataCallback {
    void onSuccess(String data);
    void onError(String error);
}
public class DataService {
    public void fetchData(DataCallback callback) {
        // 模拟异步操作
        new Thread(() -> {
            try {
                // 模拟网络延迟
                Thread.sleep(2000);
                String result = "Fetched Data";
                callback.onSuccess(result); // 调用成功的回调
            } catch (InterruptedException e) {
                callback.onError("Error fetching data"); // 调用错误的回调
            }
        }).start();
    }
}
public class Main {
    public static void main(String[] args) {
        DataService dataService = new DataService();
        dataService.fetchData(new DataCallback() {
            @Override
            public void onSuccess(String data) {
                System.out.println("Data received: " + data);
            }

            @Override
            public void onError(String error) {
                System.err.println("Failed to fetch data: " + error);
            }
        });
        
        System.out.println("Fetching data...");
    }
}

```

# license minio

```java
// license
// 生成一个证书，里面包含过期时间、本机硬件等信息，将证书放到程序所在目录
// 程序运行的时候，获取当前时间和当前机器硬件信息，再获取上面生成的证书信息，作对比，通过了才继续运行

这样的话，假如用户换了一个机器，或者过期了，就无法继续运行程序
但是由于证书是跟程序放在一起的，用户如果修改了里面的过期时间，就又能继续用

所以需要用到非对称加密

```

```shell
# 环境配置
# minio client
# 安装minio client
wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
sudo mv mc /usr/local/bin/

# 设置minio的别名、地址、账号密码（与配置文件application-dev.yml里的minio配置一致）
mc alias set minio http://192.168.10.88:9000 minio miniostorage

# 测试mc client是否能正常使用，在minio所在的服务器创建一个桶，名为mybucket，使用以下命令进行传输，然后去minio查看文件
mc cp /path/to/local/file minio/mybucket/ 
```



模拟接入两百路摄像头，每个视频录制三十分钟

|                              | cpu占用  | 上传速度 | 推流速度 | 磁盘读写占用 | 223g硬盘占用 |
| ---------------------------- | -------- | -------- | -------- | ------------ | ------------ |
| 第一阶段：模拟两百路摄像头   | 1%       | 0        | 400Mb/s  | 0            | 0            |
| 第二阶段：vms拉流并录制视频  | 5% - 30% | 0        | 400Mb/s  | 0            | 0            |
| 第三阶段：vms上传视频到minio | 5% - 30% | 900Mb/s  | 400Mb/s  | 60% - 90%    | 30% - 75%    |

