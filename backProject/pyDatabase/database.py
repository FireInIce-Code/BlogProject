import sqlite3
import os
class Data:
    def __init__(self,dic:dict,table,connection):
        self._table=table
        self._dic={}
        self._connection=connection
        for i in dic:
            setattr(self,i,dic[i])
        self._pd=dic.copy()
    def save(self):
        ditems=self._dic.items()
        pitems=self._pd.items()
        sets=",".join([str(x[0])+"=?" for x in ditems])
        setValues=tuple([x[1] for x in ditems])
        pds=" and ".join(str(x[0])+"=?" for x in pitems)
        pdValues=tuple(x[1] for x in pitems)
        values=setValues+pdValues
        sql=f"update {self._table} set "+sets+" where "+pds+";"
        print(sql)
        self._connection.execute(sql,values)
        self._connection.commit()
        self._pd=self._pd.copy()
    def __setattr__(self,item,value):
        self.__dict__[item]=value
        if item not in ("_table","_dic","_connection","_pd"):
            self._dic[item]=value
    def __str__(self):
        return self.__dict__.__str__()
    
    __repr__=__str__

class Datas:
    def __init__(self,arr,table,connection,pd):
        self.table=table
        self.arr=arr
        self.connection=connection
        self.pd=pd
    def first(self):
        return self.arr[0]
    def last(self):
        return self.arr[-1]
    def add(self,data):
        self.arr.append(data)
    def __str__(self):
        return self.arr.__str__()
    def __len__(self):
        return len(self.arr)
    def __iter__(self):
        return self.arr.__iter__()
    def __getitem__(self,index):
        return self.arr[index]
    def __setitem__(self,index,value):
        self.arr[index]=value
    
    __repr__=__str__
    

class Database:
    def __init__(self,path):
        self.connection=sqlite3.connect(path,check_same_thread=False)
    @classmethod
    def pd(cls,**kw):
        pd=""
        for i in kw:
            if type(kw[i])==str:
                pd+=f"{i}=\"{kw[i]}\"\r"
            else:
                pd+=f"{i}={kw[i]}\r"
        return pd
    def filter(self,table,**kw):
        pd=self.pd(**kw).strip("\r").replace("\r"," and ")
        if(len(kw)!=0):
            sql=f"select * from {table} where {pd};"
        else:
            sql=f"select * from {table};"
        cursor=self.connection.execute(sql)
        keys=[x[0] for x in cursor.description]
        result=cursor.fetchall()
        ans=Datas([],table,self.connection,pd)
        for i in result:
            d=dict()
            for j in range(len(keys)):
                d[keys[j]]=i[j]
            ans.add(Data(d,table,self.connection))
        return ans
    def get(self,table,**kw):
        datas=self.filter(table,**kw)
        if len(datas)!=1:
            raise ValueError("没有数据或查到多个数据")
        return datas.first()
    def remove(self,table,**kw):
        sql=f"delete from {table} where "+self.pd(**kw).replace('\r',' and ')+";"
        self.connection.execute(sql)
        self.save()
    def lastRow(self,table):
        return self.connection.execute(f"select last_insert_rowid() from {table}").fetchall()[0][0]
    def create(self,table,**kw):
        keys=list(kw.keys())
        values=list(kw.values())
        sql=f"insert into {table} ({','.join(keys)}) values ({','.join(list('?'*len(values)))});"
        self.connection.execute(sql,values)
        self.save()
        if "id" in [x[0] for x in self.connection.execute(f"select * from {table}").description]:
            obj=self.get(table,id=self.lastRow(table))
        return obj
        
        
        
    def filterNum(self,table,orderkey,reverse=False,num=-1,**kw):
        pd=self.pd(**kw).strip("\r").replace("\r"," and ")
        sql=f"select * from {table} {'where {pd}' if len(pd) else ''} order by {orderkey} {'asc' if not reverse else 'desc'} {'limit '+str(num) if num!=-1 else ''};"
        cursor=self.connection.execute(sql)
        keys=[x[0] for x in cursor.description]
        result=cursor.fetchall()
        ans=Datas([],table,self.connection,pd)
        for i in result:
            d=dict()
            for j in range(len(keys)):
                d[keys[j]]=i[j]
            ans.add(Data(d,table,self.connection))
        return ans
    def __del__(self):
        self.connection.commit()
        self.connection.close()
    def save(self):
        self.connection.commit()