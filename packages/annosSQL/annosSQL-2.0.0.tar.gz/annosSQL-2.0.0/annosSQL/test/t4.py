from annosSQL.Innos.Interface import Interface, Handler
from annosSQL.Donos.doconn import Connection
from annosSQL.Donos.dosql import execute

@Interface()
class T4:
    #配置处理器，这是入口，是必须
    @Handler()
    def hand(self) -> list: pass

    #配置连接池
    @Connection(driver="mysql", host="127.0.0.1", user="root", password="123456", port=3306, database="czh")
    def conn(self) -> any: pass

    '''
    查询所有数据，p1方法不能有任何的形参变量，必须是空函数，'->'箭头后面跟的是返回值类型，'list'或'dict'或'tuple'都行
    这里返回list数据类型
    '''
    @execute(sql="select * from user_copy1")
    def p1(self) -> list: pass

    @execute(sql="select * from user_copy1")
    def p2(self) -> dict: pass

    @execute(sql="select * from user_copy1")
    def p3(self) -> tuple: pass

    '''
    占位符使用 {}/#{}/%s,
    条件查询时，函数的形参必须带类型，如s1方法里的id必须写出：id:int
    '''
    # {}占位符是通过str().format()实现的，此时，函数形参的位置十分重要，它将影响sql的条件的正确性
    @execute(sql="select * from user_copy1 where id={}")
    def s1(self,id:int) -> list: pass
    # #{}占位符的基本形式如下：#{1}，通过#{}大括号里的数值来定位绑定到函数的形参
    @execute(sql="select * from user_copy1 where id=#{1}")
    def s2(self, id: int) -> dict: pass
    # %s 多行占位符 支持数据多行数据类型：列表与元组
    @execute(sql="select * from user_copy1 where id=%s")
    def s3(self, id: int) -> tuple: pass

    '''
    快捷符的使用：A(select)
    '''
    @execute(sql="A(select) user_copy1")
    def a1(self) -> tuple: pass



if __name__=='__main__':
    t4=T4()
    t4.hand() #调用入口
    print('p1返回的数据：')
    p1=t4.p1()
    print(p1)

    print('p2返回的数据：')
    p2 = t4.p2()
    print(p2)

    print('p3返回的数据：')
    p3 = t4.p3()
    print(p3)

    print('s1返回的数据：')
    s1 = t4.s1(1)
    print(s1)

    print('s2返回的数据：')
    s2 = t4.s2(1)
    print(s2)

    print('s3返回的数据：')
    s3 = t4.s2(1)
    print(s3)

    print('a1返回的数据：')
    a1 = t4.a1()
    print(a1)

