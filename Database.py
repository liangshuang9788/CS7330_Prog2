class Database:
    data = []
    LockManager = ''

    def __init__(self, k, nonzero):

        if nonzero:
            for i in range(k):
                self.data.append(i + 1)
        else:
            for i in range(k):
                self.data.append(0)

    def GetLockManager(self, LockManagerAdress):
        self.LockManager = LockManagerAdress

    def Read(self, k):
        print("Read index", k, "The value is ", self.data[k])
        return self.data[k]

    def Write(self, k, w):
        print("Write index", k, "The value is ", w)
        self.data[k] = w
        return 0

    def Print(self):  # reqire slock
        print("Read the whole database")
        print(self.data)
        return 0


class LockManager:
    transaction_file_list_status = []
    transaction_file_list_stuck = []

    def __init__(self, transaction_file_amounts):
        self.transaction_file_list_status = [[]] * transaction_file_amounts
        self.transaction_file_list_stuck = ["Available"] * transaction_file_amounts

    def CheckEnd(self):
        print(self.transaction_file_list_stuck)
        if "Available" in self.transaction_file_list_stuck:
            return 0  # still can operate
        else:
            if set(self.transaction_file_list_stuck) == {"completed"}:
                return 2  # complete
            else:
                return 1  # deadlock

    def Request(self, tid, k, is_s_lock):  # 待重写
        set_s_lock_flags = 0
        set_x_lock_flags = 0
        for i in self.transaction_file_list_status:
            for j in i:
                # if j[0] == Database.data[k] and set_s_lock_flag:  # If can't add s_lock means any lock can't be add
                #     if j[1] == False:
                #         set_s_lock_flag = False
                #         set_x_lock_flag = False
                #         break
                #     else:
                #         if is_s_lock == True:
                #             set_s_lock_flag = True
                #             set_x_lock_flag = False
                #         else:
                #             set_s_lock_flag = False
                #             set_x_lock_flag = False
                #             break
                if j[0] == Database.data[k]:
                    if j[1] == True:
                        set_s_lock_flags += 1
                    else:
                        set_x_lock_flags += 1
        if set_x_lock_flags > 0:  # Is there possible for a trans have write（x）twice or more？ I assume no!
            self.transaction_file_list_stuck[tid] = "Disable"
            return 0  # denied
        else:
            if set_s_lock_flags > 0:
                if is_s_lock == True:
                    self.transaction_file_list_status[tid].append([Database.data[k], is_s_lock])
                    self.transaction_file_list_stuck = "Available"
                    return 1  # granted
                else:
                    if set_s_lock_flags == 1:
                        if [Database.data[k], True] in self.transaction_file_list_status[tid]:  # the only s-lock is
                            # from same tid(Also I assumed there's only read(X) once!)
                            self.transaction_file_list_status[tid].append([Database.data[k], is_s_lock])
                            self.transaction_file_list_stuck = "Available"
                            return 1  # granted
                        else:
                            self.transaction_file_list_stuck = "Disable"
                            return 0  # denied
                    else:
                        self.transaction_file_list_stuck = "Disable"
                        return 0  # denied

        # if set_x_lock_flag == False:
        #     return 0#denied
        # else:
        #     if set_s_lock_flag == False:
        #         return 0#denied
        #     else:
        #         if is_s_lock ==True:
        #             self.transaction_file_list_status[tid].append([Database.data[k], is_s_lock])
        #             return 1#granted

        # if is_s_lock:
        #     if set_s_lock_flag:
        #         self.transaction_file_list_status[tid].append([Database.data[k], is_s_lock])
        #         return 1#granted
        #     else:
        #         if is
        #         return 0#denied

        # self.transaction_file_list_status[tid].append([Database.data[k], is_s_lock])

        # if not self.transaction_file_list_status[tid]:
        #     return 1
        # else:
        #     return 0

    def ReleaseAll(self, tid):
        # for i in range(len(self.transaction_file_list_status[tid])):
        #     self.transaction_file_list_status[tid].pop()
        print(len(self.transaction_file_list_status[tid]), " locks released")
        self.transaction_file_list_status[tid] = []
        self.transaction_file_list_stuck = "completed"  # Tid stop

    def ShowLocks(self, tid):
        print(self.transaction_file_list_status[tid])


class Transaction:
    local_variables_list = []
    LockManager = ''
    tid = -100

    def __init__(self, k):
        self.local_variables_list = [0] * k

    def GetLockManager(self, LockManagerAdress):
        self.LockManager = LockManagerAdress

    def GetTid(self, Tid):
        self.tid = Tid

    def Read(self, db, source, dest):
        resultofrequest = self.LockManager.Request(tid=self.tid, k=source, is_s_lock=True)  # S-Lock
        if resultofrequest == 0:
            print("Denied and wait")
        else:
            self.local_variables_list[dest] = db.Read(source)

    def Write(self, db, source, dest):
        resultofrequest = self.LockManager.Request(tid=self.tid, k=source, is_s_lock=False)  # X-Lock
        if resultofrequest == 0:
            print("Denied and wait")
        else:
            db.Write(dest, self.local_variables_list[source])
        #     self.local_variables_list[dest] = db.data[source]
        # db.data[source] = self.local_variables_list[dest]

    def Add(self, source, v):
        self.local_variables_list[source] += v

    def Sub(self, source, v):
        self.local_variables_list[source] -= v

    def Mult(self, source, v):
        self.local_variables_list[source] = self.local_variables_list[source] * v

    def Copy(self, s1, s2):
        self.local_variables_list[s1] = self.local_variables_list[s2]

    def Combine(self, s1, s2):
        # print("s1",s1,type(s1),'s2',s2,type(s2))
        self.local_variables_list[s1] = int(self.local_variables_list[s1]) + (self.local_variables_list[s2])

    def Display(self):
        num_list_new = map(lambda x: str(x), self.local_variables_list)
        print(" ".join(num_list_new))
        # print(self.local_variables_list)


import random


def GetRamdom(length):
    return random.randint(0, length)


# !/usr/bin/python
# -*- coding:utf8 -*-

import os

allFileNum = 0


def printPath(level, path):
    global allFileNum
    ''''' 
    打印一个目录下的所有文件夹和文件 
    '''
    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    # 先添加目录级别
    dirList.append(str(level))
    for f in files:
        if (os.path.isdir(path + '/' + f)):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if f[0] == '.':
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
        if os.path.isfile(path + '/' + f):
            # 添加文件
            fileList.append(f)
            # 当一个标志使用，文件夹列表第一个级别不打印
    i_dl = 0
    for dl in dirList:
        if (i_dl == 0):
            i_dl = i_dl + 1
        # else:
        # 打印至控制台，不是第一个的目录
        # print('-' * (int(dirList[0])), dl)
        # 打印目录下的所有文件夹和文件，目录级别+1
        # printPath((int(dirList[0]) + 1), path + '/' + dl)
    for fl in fileList:
        # 打印文件
        print('-' * (int(dirList[0])), fl)
        # 随便计算一下有多少个文件
        allFileNum = allFileNum + 1


import os


def getabsroute(path):
    listdir = os.listdir(path)
    filepath = os.getcwd()
    allfile = []
    for file in listdir:
        allfile.append(path + '/' + file)
    # print(allfile)
    return allfile


if __name__ == '__main__':
    path = "t/"
    # path = "/Users/shuangliang/Documents/SMU/CS7330FileOrganizationDatabaseMgt/prog2/t/"
    transcation_file_list = getabsroute(path)
    # print(transcation_file_list)
    transcationS_comondS_list = []
    for i_path in transcation_file_list:
        transcationS_comondS_list.append([])
        transcationS_comondS_list[-1].append(i_path)
        # print(i_path)
        with open(i_path, "r") as f:
            for line in f.readlines():
                line = list(line.split())
                transcationS_comondS_list[-1].append(line)
                # print(line)
    # [['t//t1.txt', ['4', '3'], ['R', '1', '1'], ['R', '2', '2'], ['O', '2', '1'], ['W', '2', '2']],
    #  ['t//t3.txt', ['5', '3'], ['R', '0', '0'], ['A', '0', '1'], ['M', '0', '-1'], ['O', '1', '0'], ['W', '1', '0']],
    #  ['t//t2.txt', ['6', '3'], ['R', '0', '0'], ['M', '0', '2'], ['R', '1', '1'], ['A', '1', '4'], ['W', '1', '1'],
    #  ['W', '0', '0']],
    #  ['t//t4.txt', ['3', '3'], ['R', '2', '2'], ['M', '2', '3'], ['W', '2', '2']]]
    # transcationS_comondS_list
    Database_test = Database(10, True)
    # A.Print()
    LockManager_test = LockManager(len(transcationS_comondS_list))
    Transaction_list = []
    for transcation_id in transcationS_comondS_list:
        Transaction_list.append(Transaction(int(transcation_id[1][-1])))
        Transaction_list[-1].GetLockManager(LockManager_test)
        Transaction_list[-1].GetTid(transcationS_comondS_list.index(transcation_id))
    while True:

        current_Transaction = GetRamdom(len(transcationS_comondS_list)-1)
        print(transcationS_comondS_list[current_Transaction])
        if len(transcationS_comondS_list[current_Transaction])<=2:

            continue

        else:
            current_Order = transcationS_comondS_list[current_Transaction][2]
            if current_Order[0] == 'R':  # python3.6 don't have switch case
                Transaction_list[current_Transaction].Read(Database_test, int(current_Order[1]), int(current_Order[2]))
            elif current_Order[0] == 'W':
                Transaction_list[current_Transaction].Write(Database_test, int(current_Order[1]), int(current_Order[2]))
            elif current_Order[0] == 'A':
                Transaction_list[current_Transaction].Add(int(current_Order[1]), int(current_Order[2]))
            elif current_Order[0] == 'S':
                Transaction_list[current_Transaction].Sub(int(current_Order[1]), int(current_Order[2]))
            elif current_Order[0] == 'M':
                Transaction_list[current_Transaction].Mult(int(current_Order[1]), int(current_Order[2]))
            elif current_Order[0] == 'C':
                Transaction_list[current_Transaction].Copy(int(current_Order[1]), int(current_Order[2]))
            elif current_Order[0] == 'O':
                Transaction_list[current_Transaction].Combine(int(current_Order[1]), int(current_Order[2]))
            elif current_Order[0] == 'P':
                # Transaction_list[current_Transaction].Display()
                temp = []
                for i in range(len(Database_test.data)):
                    temp.append(LockManager_test.Request(current_Transaction, k=i,is_s_lock=True))
                if 0 not in temp:
                    Database_test.Print()



            else:
                print("Error Command")
            transcationS_comondS_list[current_Transaction].remove(current_Order)
            print(transcationS_comondS_list[current_Transaction])
            if len(transcationS_comondS_list[current_Transaction]) <= 2:
                LockManager_test.ReleaseAll(current_Transaction)

        if LockManager_test.CheckEnd() != 0:
            if LockManager_test.CheckEnd() == 1:
                print("deadlock")
            else:
                print("complete")
            break
    Database_test.Print()