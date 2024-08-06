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

java -jar wvp-pro-2.7.2-07080233.jar > normal.log 2> error.log

查看公网地址
curl ifconfig.me
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



spend

补充方面的知识，捧着一摞书

修理工 看完一本书

扩散性百万甜面包 十小时

i spent several months doing reasearch and making notes





五金少女