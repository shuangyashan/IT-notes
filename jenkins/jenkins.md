### 1.��װjenkins (����jenkins.pdf)

1.��װjava(�ο��ĵ�)
2.��װtomcat (�ο��ĵ�)
3.�ϴ�war��(�ο��ĵ�)
4.�˿�����������80 ����8080 �����������ǲ���ʹ��,�Զ����ε�)
5.hostname (�鿴��������֮������Ƽ�163.53.91.49 i-b5b36fed ��ȥ)

  5.1�޸�config/server.xml ?(��8080�˿ں���� ���޸Ķ˿�80 address="0.0.0.0") 

  5.2����tomcat

?	�ٿ���netstat -lnpt �ڲ���ipv6�� 

?	**https://blog.csdn.net/weiwangchao_/article/details/49820101  �����tomcatֻ����ipv4��**

   5.3.����http://ip/war����

6.�м�ѧϰ������:
	$netstat -lnpt  �鿴������ռ�õĶ˿�
	$tail -300 catalina.out ��ӡ��־������cd tomcat/logs��
	ps -ef | grep java ���˳�����Ľ��� ��1. ����ȥ����kill -9 ���̺�  2.Ҳ����ͨ��binĿ¼��ȥִ�������ļ�����ֹͣ�ļ���

7.�м���������ļ�����
	ls -lta �鿴�����ļ�
	rm -rf  .server.xml.swp  ɾ�������ļ�



### 2.jenkins����̨����

1.����Ա���� :

?	$ cat /root/.jenkins/secrets/initialAdminPassword

2.�������߰�װ�Ľ���취:

?	$ vim root/.jenkins/hudson.model.UpdateCenter.xml ������һ��

?	(<url>https://updates.jenkins.io/update-center.json</url>)	

?	����������ʾ����

 <url>https://mirrors.tuna.tsinghua.edu.cn/jenkins/updates/update-center.json</url>

2. �޸����� 

3. ֮������ssh ��jenkins�� ʵ��������������ͨ��

   ```
   1.��̨������ͬ����
   ssh-keygen -trsa
   Ȼ�󣬲��ϵİ��س�����
   cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   2������Կ���Ƶ������ӻ�
   #ע������ж�Ļ�����ù�Կ�ֶ�ճ��������
   scp ~/.ssh/authorized_keys root@slave1:~/.ssh/
   scp ~/.ssh/authorized_keys root@slave2:~/.ssh/ 
   ```

4. ����֮��ҳ������������/root/.jenkins/config�ļ��������

   ```
    <authorizationStrategy class="hudson.security.LegacyAuthorizationStrategy"/>
     <securityRealm class="hudson.security.HudsonPrivateSecurityRealm">
       <disableSignup>false</disableSignup>
       <enableCaptcha>false</enableCaptcha>
     </securityRealm>
   ```

   

   

### 3.������Ľڵ� 

####  3.1django����� 

 https://blog.csdn.net/GitChat/article/details/78271099

```
1.����jdnago 1.7֮��İ汾�Ͳ�֧��python 2.6�ˣ�����������Ҫ����python 2.6-2.7��
[root@vagrant-centos65 ~]# yum -y install  zlib zlib-devel openssl openssl-devel  sqlite-devel
[root@vagrant-centos65 ~]# wget http://python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2

#�ӣ���Ҫ��װbzip2��װ���ߣ�$yum -y install  bzip2
[root@vagrant-centos65 ~]# tar -jxvf Python-2.7.3.tar.bz2

[root@vagrant-centos65 ~]# cd Python-2.7.3

#��, ԭ����: ȱ��gcc���뻷��:
     ����yum��������yum install -y  gcc 
     û������yum   : ���԰�װgcc�İ�װ��
[root@vagrant-centos65 Python-2.7.3]# ./configure    --prefix=/usr/local/python2.7
[root@vagrant-centos65 Python-2.7.3]# make && make install
[root@vagrant-centos65 Python-2.7.3]# cd /usr/bin/
[root@vagrant-centos65 bin]# ll | grep python
-rwxr-xr-x.   2 root root      4864 Nov 22  2013 python
lrwxrwxrwx.   1 root root         6 Jan 16  2014 python2 -> python
-rwxr-xr-x.   2 root root      4864 Nov 22  2013 python2.6
[root@vagrant-centos65 bin]# mv python python2.6.bak
[root@vagrant-centos65 bin]# ln -s /usr/local/python2.7/bin/python /usr/bin/python
[root@vagrant-centos65 bin]# vi /usr/bin/yum
#!/usr/bin/python2.6


2.��װsetuptools��pip�İ�װ��Ҫ����setuptools����ʵ��pip�İ�װsetup.py������һ������from setuptools import setup��
[root@vagrant-centos65 bin]# cd /opt/
[root@vagrant-centos65 opt]# wget https://pypi.python.org/packages/61/3c/8d680267eda244ad6391fb8b211bd39d8b527f3b66207976ef9f2f106230/setuptools-1.4.2.tar.gz
[root@vagrant-centos65 opt]# tar zxvf setuptools-1.4.2.tar.gz
[root@vagrant-centos65 opt]# cd setuptools-1.4.2
[root@vagrant-centos65 setuptools-1.4.2]# python setup.py install


3.��װpip��
[root@vagrant-centos65 ~]# cd /opt/
[root@vagrant-centos65 opt]# wget "https://pypi.python.org/packages/source/p/pip/pip-1.5.4.tar.gz#md5=834b2904f92d46aaa333267fb1c922bb" --no-check-certificate
[root@vagrant-centos65 opt]# tar zxvf pip-1.5.4.tar.gz
[root@vagrant-centos65 opt]# cd pip-1.5.4
[root@vagrant-centos65 pip-1.5.4]# python setup.py install
[root@vagrant-centos65 pip-1.5.4]# pip
-bash: pip: command not found
[root@vagrant-centos65 pip-1.5.4]# find / -name pip
/usr/local/python2.7/bin/pip
[root@vagrant-centos65 pip-1.5.4]# ln -s /usr/local/python2.7/bin/pip /usr/bin/pip

4.��װdjango��
[root@vagrant-centos65 pip-1.5.4]# pip install django
[root@vagrant-centos65 pip-1.5.4]# pip list
Django (1.11.3)
pip (1.5.4)
pytz (2017.2)
setuptools (1.4.2)
wsgiref (0.1.2)
```



#### 3.2jenkins����OpenSSH

**�ο� ��https://blog.csdn.net/tototuzuoquan/article/details/78568655**



#### 3.3jenkins����git

**jenkins��װgit:**

centos��װgit:

?		1 .yum install -y git ��:yum��װ�������⿴vim /usr/local/yum�İ汾 ���ĳɺ�pythonһ���İ汾
		2.  centos����git���� : https://www.cnblogs.com/kevingrace/p/8252517.html

?		3.jenkin����github :https://blog.csdn.net/boling_cavalry/article/details/78943061

### 4.�Զ���django����

#### 4.1 �ڱ����ƵĽڵ��django����

**�ο���https://blog.csdn.net/nunchakushuang/article/details/77118621**

