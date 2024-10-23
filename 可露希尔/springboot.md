```shell
安装docker
sudo yum update -y
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io
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
```

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



js插件分析成分
方舟音乐 文本播放器
东方
fx音乐播放
随机背景https://www.dmoe.cc/random.php



hexo版本，kami版本 音乐
音乐 妄想ai歌
人形日志 存档几
pixiv搜索https://pixiv.re/115293810.png 
大图书馆
幻灯夜话
梦莹流光 蝉在叫
丝滑动画 
eyesof
星铁
蛙pt
把我害惨了
表情包搜索数据库
取代 我们有十个io金牌 但不是我 周心境
我们所有的内容都是由人类编写的
背熟 xx 打底 不乏几百本精品xx打底
像呼吸一样自然
ppt ai绘图介绍 贴
runaway 但是敌人 一代目二代目多代 bgm庭院 

2033年，在一切纸质记录彻底消失于人类社会时，
古老的书籍宛如候鸟般回到了文字最初的起点，
没人想到那竟是一座未知的城。
城中唯一的建筑是栋无限延伸的图书馆，
记录着无限的当下，
即未来的过去和过去的未来。红魔馆数据殿堂

哦？东西丢了？
很符合你的风格
别担心，我自有办法（让我来吧）
下次可得长点心

战争间隙，博士利用难得的空闲时间，记录最近发生的事。

代码 数字艺术家 学画画
法国人 数学优雅 不管你懂不懂
集中、激烈和持续的练习可以增强大脑的可塑性，提高灰质密度和白质连通性

不能创不能理

Abishek在8个月前在朝九晚五之后学习代码编程。他没有告诉任何人在做什么，他推出了3个产品，其中2个是赚钱的



spend

补充方面的知识，捧着一摞书

修理工 看完一本书

扩散性百万甜面包 十小时

i spent several months doing reasearch and making notes







五金少女