# -*- coding: GBK -*-
import MySQLdb
import sys
import re
import progressbar
import nltk
from nltk.stem import PorterStemmer as ps
class Sql_Deal:
    #��Ĺ��캯��������psʵ��������mysql.connectʵ��
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='931011', db='backup', charset='utf8mb4')
        self.ps=ps()
        self.bar = progressbar.ProgressBar()
    #�����ͷ�connect����
    def close(self):
        self.conn.close()

    def write_arry(self):
        self.cur=self.conn.cursor()
        Cate_ID_Query='(select ID,Amount from `category` )'
        Api_Query='(select *  from new )'
        self.cur.execute(Cate_ID_Query)
        Cate_ID_tup = self.cur.fetchall()
        Cate_ID_list=[]
        Api_info_list=[]
        print Cate_ID_tup
        Api_num = 5068
        sum=0
        api_sum=0
        for i in Cate_ID_tup:
            sum+=i[1]/100
        for i in Cate_ID_tup:
            Cate_ID_list.append(list(i))
        for i in Cate_ID_list:
            i[1]=int(float((i[1]/100))/float(sum)*Api_num)
        for i in Cate_ID_list:
            api_sum+=i[1]
        print api_sum
        print Cate_ID_list
        self.cur.execute(Api_Query)
        Api_info=self.cur.fetchall()
        for i in Api_info:
            print i[5]
        for i in Api_info:
            Api_info_list.append(list(i))
        count_select=0
        for i in Cate_ID_list:
            print 'next class'
            count = 0
            for j in Api_info_list:
                if j[3] == i[0]:
                    count += 1
                    if count <= i[1]:
                        # for i in self.bar(range(len(Id_Title_f))):
                        j[1]=j[1].lower()                                                         #������Сд
                        j[2]=j[2].lower()                                                         #������Сд
                        j[2]=re.sub("http:.*? | http:.*|https:.*? |https:.*",'',j[2])        #ɾ�������е���ַ��ַ
                        #ɾ������������е�ͣ�÷���
                        j[1]=j[1].replace(',','').replace('.','').replace('[','').replace(']','').replace('(','').replace(')','').replace("'",'').replace('-','').replace(':','').replace('!','').replace('/','')
                        j[2]=j[2].replace(',','').replace('.','').replace('[','').replace(']','').replace('(','').replace(')','').replace("'",'').replace('-','').replace(':','').replace('!','').replace('\n',' ').replace('/','')
                        #�������ַ����Կո�ָ�Ϊ���飬ȥ�����еĴ����ֺͿո����п��ܴ����ַ�֮���ж���ո�����
                        temp_list_des=filter(lambda i: not i.isdigit() and i != '',j[2].split(' '))
                        #���������ݽ��д��Ա�ע�����������������
                        temp_list_des_f=[]
                        tagged_list_des=nltk.pos_tag(temp_list_des)
                        #�����Ա�ע��������У�����������Ҫ�Ĵ���
                        for x in range(len(tagged_list_des)):
                                if (tagged_list_des[x][1]=='NN'or tagged_list_des[x][1]=='NNS'or tagged_list_des[x][1]=='JJ'or tagged_list_des[x][1]=='NNP'or tagged_list_des[x][1]=='NNPS' or tagged_list_des[x][1]=='JJR' or tagged_list_des[x][1]=='JJS' or tagged_list_des[x][1]=='FW'):
                                    temp_list_des_f.append(self.ps.stem(temp_list_des[x]))             #stem������ÿ������ȡ�ʸ�
                                    #������������������ϳ��ַ�������Id_Title_f��
                                    j[2]=' '.join(temp_list_des_f)
                                    #�Ա�����д��Ա�ע ����ͬ��
                                    temp_list_title = filter(lambda i: not i.isdigit() and i != '', j[1].split(' '))
                                    temp_list_title_f=[]
                        #�Ա������ݽ��д��Ա�ע�����������������
                        tagged_list_title = nltk.pos_tag(temp_list_title)
                        for x in range(len(tagged_list_title)):
                                if (tagged_list_title[x][1] == 'NN' or tagged_list_title[x][1] == 'NNS' or tagged_list_title[x][1] == 'JJ' or tagged_list_title[x][1]=='NNP' or tagged_list_title[x][1]=='NNPS' or tagged_list_title[x][1]=='JJR' or tagged_list_title[x][1]=='JJS' or tagged_list_title[x][1]=='FW'):
                                    temp_list_title_f.append(self.ps.stem(temp_list_title[x]))
                                    j[1] = ' '.join(temp_list_title_f)

                        Process_Text=[]
                        #��������ѵ������
                        #����if����������Ԫ�ؽ����пգ���ֹ����Խ�磬������������б��浽����Process_Text��
                        if j[3]==None and j[5]==None:
                            continue
                        elif j[3]!=None and j[5]==None:
                            p=str(j[0])+':'+'['+str(j[3])+']'+str(j[1])+' '+str(j[2])+'\n'
                            Process_Text.append(p)
                        elif j[3]==None and j[5]!=None:
                            p=str(j[0])+':'+'['+str(j[5]).replace(',',' ')+']'+str(j[1])+' '+str(j[2])+'\n'
                            Process_Text.append(p)
                        else:
                            p=str(j[0])+':'+'['+str(j[3])+' '+str(j[5]).replace(',',' ')+']'+str(j[1])+' '+str(j[2])+'\n'
                            Process_Text.append(p)
                        fp = open('C:/Users/PSY/Desktop/result_test.txt', 'a+')
                        a_str = '\n'.join(map(lambda i: str(i), Process_Text))
                        fp.write(a_str)
                        fp.close()
                        print j[0]
                        count_select+=1
                    else:
                        break
        print count_select
#         #��������ѵ������
#         # for i in range(len(Id_Title_f)):
#         #     #����if����������Ԫ�ؽ����пգ���ֹ����Խ�磬������������б��浽����Process_Text��
#         #     if len(First_Tag[i])==0 and len(Else_Tag_f[i])==0:
#         #         continue
#         #     elif len(First_Tag[i])!=0 and len(Else_Tag_f[i])==0:
#         #         p=str(Id_Title_f[i][0])+':'+'['+str(First_Tag[i][0][0])+']'+str(Id_Title_f[i][1])+' '+str(Id_Title_f[i][2])
#         #         Process_Text.append(p)
#         #     elif len(First_Tag[i])==0 and len(Else_Tag_f[i])!=0:
#         #         p=str(Id_Title_f[i][0])+':'+'['+arry_to_str(self,Else_Tag_f[i])+']'+str(Id_Title_f[i][1])+' '+str(Id_Title_f[i][2])
#         #         Process_Text.append(p)
#         #     else:
#         #         p=str(Id_Title_f[i][0])+':'+'['+str(First_Tag[i][0][0])+' '+arry_to_str(self,Else_Tag_f[i])+']'+str(Id_Title_f[i][1])+' '+str(Id_Title_f[i][2])
#         #         Process_Text.append(p)
#
#         #�����ޱ�ǩ��������
#         for i in range(len(Id_Title_f)):
#             #����if����������Ԫ�ؽ����пգ���ֹ����Խ�磬������������б��浽����Process_Text��
#             if len(First_Tag[i])==0 and len(Else_Tag_f[i])==0:
#                 continue
#             elif len(First_Tag[i])!=0 and len(Else_Tag_f[i])==0:
#                 p=str(Id_Title_f[i][0])+':'+'['+']'+str(Id_Title_f[i][1])+' '+str(Id_Title_f[i][2])
#                 Process_Text.append(p)
#             elif len(First_Tag[i])==0 and len(Else_Tag_f[i])!=0:
#                 p=str(Id_Title_f[i][0])+':'+'['+']'+str(Id_Title_f[i][1])+' '+str(Id_Title_f[i][2])
#                 Process_Text.append(p)
#             else:
#                 p=str(Id_Title_f[i][0])+':'+'['+']'+str(Id_Title_f[i][1])+' '+str(Id_Title_f[i][2])
#                 Process_Text.append(p)
#         #��Process_Text�Ի��з�Ϊ�ָ�д���ļ���
#         fp = open('C:/Users/PSY/Desktop/result_test.txt', 'w')
#         a_str = '\n'.join(map(lambda i: str(i), Process_Text))
#         fp.write(a_str)
#         fp.close()
reload(sys)
sys.setdefaultencoding('utf-8')
G=Sql_Deal()
G.write_arry()
G.close()


