# -*- coding: GBK -*-
import MySQLdb
import sys
import re
import progressbar
import nltk
from nltk.stem import PorterStemmer as ps
class Sql_Deal:
    #类的构造函数，构造ps实例，定义mysql.connect实例
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='931011', db='webservice1', charset='utf8mb4')
        self.ps=ps()
        self.bar = progressbar.ProgressBar()
    #定义释放connect函数
    def close(self):
        self.conn.close()

    def write_arry(self):
        self.cur=self.conn.cursor()
        Id_Title_Query='(select ID,Name,Description from `apibasic`  limit 12000,2000)'
        Else_Tag_Query='(select CateID from apicate where ApiID=%s and IsPri=0)'
        First_Tag_Query='(select CateID from apicate where ApiID=%s and IsPri=1)'
        self.cur.execute(Id_Title_Query)
        Id_Title = self.cur.fetchall()
        Else_Tag=[]                                             #Else_Tag      [((20090,),(20047,)),()]
        First_Tag=[]                                            #First_Tag     [((20090L,),), ((20015L,),), ((20024L,),), ((20162L,),)]
        Else_Tag_f=[]
        #定义一个将数组转化为字符串的功能函数，返回字符串
        def arry_to_str(self, arry):
            self.str = ' '.join(map(lambda i: str(i), arry))
            return self.str
        #以apiID为参数，查询对应的除第一标签之外的标签
        for i in Id_Title:
            self.cur.execute(Else_Tag_Query,(i[0],))
            Else_Tag.append(self.cur.fetchall())
        #将Else_Tag转化为[[20142L], [20208L, 20202L, 20206L], [20220L]]存在Else_Tag_f中
        for tag in Else_Tag:
            temp=[]
            for i in range(len(tag)):
                temp.append(tag[i][0])
            Else_Tag_f.append(temp)
        #以apiID为参数，查询对应的除第一标签之外的标签
        for i in Id_Title:
            self.cur.execute(First_Tag_Query, (i[0],))
            First_Tag.append(self.cur.fetchall())
        Id_Title_f=[]
        #将Id_Title转化为[[A,B,C],[A,B,C]]  A为ID,B为TITLE,C为DESCRIPTION,存放在Id_Title_f中
        for i in Id_Title:
            Id_Title_f.append(list(i))
        for i in self.bar(range(len(Id_Title_f))):
            Id_Title_f[i][1]=Id_Title_f[i][1].lower()                                                         #将标题小写
            Id_Title_f[i][2]=Id_Title_f[i][2].lower()                                                         #将描述小写
            Id_Title_f[i][2]=re.sub("http:.*? | http:.*|https:.*? |https:.*",'',Id_Title_f[i][2])                             #删除描述中的网址网址
            #删除标题和描述中的停用符号
            Id_Title_f[i][1]=Id_Title_f[i][1].replace(',','').replace('.','').replace('[','').replace(']','').replace('(','').replace(')','').replace("'",'').replace('-','').replace(':','').replace('!','').replace('/','')
            Id_Title_f[i][2]=Id_Title_f[i][2].replace(',','').replace('.','').replace('[','').replace(']','').replace('(','').replace(')','').replace("'",'').replace('-','').replace(':','').replace('!','').replace('\n',' ').replace('/','')
            #将描述字符串以空格分隔为数组，去掉其中的纯数字和空格（其中可能存在字符之间有多个空格现象）
            temp_list_des=filter(lambda i: not i.isdigit() and i != '',Id_Title_f[i][2].split(' '))
            #对描述内容进行词性标注，保留我们所需词性
            temp_list_des_f=[]
            tagged_list_des=nltk.pos_tag(temp_list_des)
            #将词性标注后的数组中，保留我们需要的词性
            for j in range(len(tagged_list_des)):
                if (tagged_list_des[j][1]=='NN'or tagged_list_des[j][1]=='NNS'or tagged_list_des[j][1]=='JJ'or tagged_list_des[j][1]=='NNP'or tagged_list_des[j][1]=='NNPS' or tagged_list_des[j][1]=='JJR' or tagged_list_des[j][1]=='JJS' or tagged_list_des[j][1]=='FW'):
                    temp_list_des_f.append(self.ps.stem(temp_list_des[j]))             #stem函数对每个词提取词干
            #将处理后的数组重新组合成字符串存入Id_Title_f中
            Id_Title_f[i][2]=' '.join(temp_list_des_f)
            #对标题进行词性标注 操作同上
            temp_list_title = filter(lambda i: not i.isdigit() and i != '', Id_Title_f[i][1].split(' '))
            temp_list_title_f=[]
            #对标题内容进行词性标注，保留我们所需词性
            tagged_list_title = nltk.pos_tag(temp_list_title)
            for j in range(len(tagged_list_title)):
                if (tagged_list_title[j][1] == 'NN' or tagged_list_title[j][1] == 'NNS' or tagged_list_title[j][1] == 'JJ' or tagged_list_title[j][1]=='NNP' or tagged_list_title[j][1]=='NNPS' or tagged_list_title[j][1]=='JJR' or tagged_list_title[j][1]=='JJS' or tagged_list_title[j][1]=='FW'):
                    temp_list_title_f.append(self.ps.stem(temp_list_title[j]))

            Id_Title_f[i][1] = ' '.join(temp_list_title_f)

        Process_Text=[]
        #生成完整训练数据
        # for i in range(len(Id_Title_f)):
        #     #下列if语句对数组中元素进行判空，防止数组越界，并将最后结果按行保存到数组Process_Text中
        #     if len(First_Tag[i])==0 and len(Else_Tag_f[i])==0:
        #         continue
        #     elif len(First_Tag[i])!=0 and len(Else_Tag_f[i])==0:
        #         p=str(Id_Title_f[i][0])+':'+'['+str(First_Tag[i][0][0])+']'+str(Id_Title_f[i][1])+' '+str(Id_Title_f[i][2])
        #         Process_Text.append(p)
        #     elif len(First_Tag[i])==0 and len(Else_Tag_f[i])!=0:
        #         p=str(Id_Title_f[i][0])+':'+'['+arry_to_str(self,Else_Tag_f[i])+']'+str(Id_Title_f[i][1])+' '+str(Id_Title_f[i][2])
        #         Process_Text.append(p)
        #     else:
        #         p=str(Id_Title_f[i][0])+':'+'['+str(First_Tag[i][0][0])+' '+arry_to_str(self,Else_Tag_f[i])+']'+str(Id_Title_f[i][1])+' '+str(Id_Title_f[i][2])
        #         Process_Text.append(p)

        #生成无标签测试数据
        for i in range(len(Id_Title_f)):
            #下列if语句对数组中元素进行判空，防止数组越界，并将最后结果按行保存到数组Process_Text中
            if len(First_Tag[i])==0 and len(Else_Tag_f[i])==0:
                continue
            elif len(First_Tag[i])!=0 and len(Else_Tag_f[i])==0:
                p=str(Id_Title_f[i][0])+':'+'['+']'+str(Id_Title_f[i][1])+' '+str(Id_Title_f[i][2])
                Process_Text.append(p)
            elif len(First_Tag[i])==0 and len(Else_Tag_f[i])!=0:
                p=str(Id_Title_f[i][0])+':'+'['+']'+str(Id_Title_f[i][1])+' '+str(Id_Title_f[i][2])
                Process_Text.append(p)
            else:
                p=str(Id_Title_f[i][0])+':'+'['+']'+str(Id_Title_f[i][1])+' '+str(Id_Title_f[i][2])
                Process_Text.append(p)
        #将Process_Text以换行符为分割写入文件中
        fp = open('C:/Users/PSY/Desktop/result_test.txt', 'w')
        a_str = '\n'.join(map(lambda i: str(i), Process_Text))
        fp.write(a_str)
        fp.close()
reload(sys)
sys.setdefaultencoding('utf-8')
G=Sql_Deal()
G.write_arry()
# G.close()


