### 1.MySQL中varchar与char的区别以及varchar(50)中的50代表的涵义

 

(1)、varchar与char的区别

 

char是一种固定长度的类型，varchar则是一种可变长度的类型

 

(2)、varchar(50)中50的涵义

 

最多存放50个字符，varchar(50)和(200)存储hello所占空间一样，但后者在排序时会消耗更多内存，因为order by col采用fixed_length计算col长度(memory引擎也一样)

 

(3)、int(20)中20的涵义

 

是指显示字符的长度

 

但要加参数的，最大为255，比如它是记录行数的id,插入10笔资料，它就显示00000000001 ~~~00000000010，当字符的位数超过11,它也只显示11位，如果你没有加那个让它未满11位就前面加0的参数，它不会在前面加0

 

20表示最大显示宽度为20，但仍占4字节存储，存储范围不变;

 

(4)、mysql为什么这么设计

 

对大多数应用没有意义，只是规定一些工具用来显示字符的个数;int(1)和int(20)存储和计算均一样;