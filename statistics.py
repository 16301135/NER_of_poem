import re
import math
N = 700
sourcePath = 'data/corpus_tangshi'
zi = {}
ci = {}
dictionary = {}
ziyou_zi = {}
targetPath1 = 'data/word_tansghi_1'
f_to_write_1 = open(targetPath1,'w')

targetPath2 = 'data/word_tansghi_2'
f_to_write_2 = open(targetPath2,'a')

def addWordOrCh(db,k):
    if k in db:
        db[k] = db[k] + 1
    else:
        db[k] = 1



with open(sourcePath) as file_to_read:


    while True:
        line = file_to_read.readline()
        if not line:
            break
            pass

        line = line.replace("{","")
        line = line.replace("}", "")
        line = line.replace("/", "")
        line = line.replace("|", "")
        line = line.replace("[", "")
        line = line.replace("]", "")
        line = line.replace("《", "")
        line = line.replace("》", "").replace("\n","")
        sentences = re.split('，|？|。',line)
        for sentence in sentences:
            for ch in sentence:
                addWordOrCh(zi,ch)
            if len(sentence) == 5:
                addWordOrCh(zi,sentence[3])
                word = sentence[0]+sentence[1]
                addWordOrCh(ci,word)
                for i in range(2):
                    word = sentence[2 + i] + sentence[3 + i]
                    addWordOrCh(ci, word)
                pass
            elif len(sentence) == 7:
                addWordOrCh(zi,sentence[5])
                word = sentence[0] + sentence[1]
                addWordOrCh(ci, word)
                word = sentence[2]+sentence[3]
                addWordOrCh(ci,word)
                for i in range(2):
                    word = sentence[4 + i] + sentence[5 + i]
                    addWordOrCh(ci, word)
                pass
            else:

                for i in range(len(sentence)-1):
                    word = sentence[i]+sentence[i+1]
                    if i!=0:
                        addWordOrCh(zi,sentence[i])

                pass
        #print('*******processed ：'+line+'***********')

I = {}
C = {}
R = {}



count = 1
while count < 5:
    # 初始化自由的字
    for z, z_value in zi.items():
        ziyou_zi[z] = z_value

    for d,d_value in dictionary.items():
        for d_ch in d:
            ziyou_zi[d_ch] = ziyou_zi[d_ch] - d_value
            pass
        pass
    for key,value in ci.items():

        if key in dictionary:
            continue
        #I[key] = math.log(N*value/(zi[key[0]]*zi[key[1]]))

        pri = key+','+key[0]
        bac = key+','+key[1]
        R[pri] = ci[key]*math.log(ci[key])/ziyou_zi[key[0]]
        R[bac] = ci[key]*math.log(ci[key])/ziyou_zi[key[1]]
        C[key] = R[pri] + R[bac]
        pass

    C_ = sorted(C.items(),key=lambda x:x[1],reverse=True)
    #I_ = sorted(I.items(),key=lambda x:x[1],reverse=True)
    #設定共現度的閾值，存在梯度消失的問題
    # for C_item in C_:
    #     if C_item[1] <2 or C_item[0] in dictionary:
    #         break
    #     else:
    #         dictionary[C_item[0]] = ci[C_item[0]]
    #設定一個每次認為前50個是確定的 詞
    record = 0
    for C_item in C_:
        if record >=50:
            break
        if C_item[0] in dictionary:
            continue
        dictionary[C_item[0]] = ci[C_item[0]]
        record = record + 1




    #tmp_f = open('data/fenci_'+str(count),'a')
    # for key,value in dictionary.items():
    #     tmp_f.write(key+'\n')
    # tmp_f.close()

    count = count + 1


for C_item in C_:
    if ci[C_item[0]] >= 2:
        output = C_item[0] + '\t'  + '共現度：\t' + str(C_item[1]) + '\n'
        f_to_write_1.write(output)

# for I_item in I_:
#     if ci[I_item[0]] >= 2:
#         output = I_item[0] + '\t' + '互信息：\t' + str(I_item[1]) + '\t' + '共現度：\t' + str(C[I_item[0]]) + '\n'
#         f_to_write_2.write(output)



f_to_write_1.close()
f_to_write_2.close()