import json
from docx import Document

def Process_docx(filePath):
    doc = Document(filePath)
    paragraph = doc.paragraphs[0]
    result = paragraph.text.split('，')
    return result

def Take_first(elem):
    return elem[1]

targetPath = 'data/1labed_tangshi'
yixiangs=Process_docx('data/古诗意象.docx')
shijians=Process_docx('data/古文时间词.docx')
qixiangs=Process_docx('data/古诗气象词.docx')
target_f = open(targetPath,'a')


#jsonPath = 'chinese-poetry/json/poet.tang.0.json'
num = 0
while num<=57:
    jsonPath = 'chinese-poetry/json/poet.tang.'+str(num*1000)+'.json'
    f = open(jsonPath,encoding='utf-8')
    res = json.load(f)

    for content in res:
        for paragraph in content['paragraphs']:
            index_list = []
            for yixiang in yixiangs:
                index = paragraph.find(yixiang)
                if index == -1:
                    continue
                else:
                    index_list.append((index,index+len(yixiang)-1,'Image'))

            for qixiang in qixiangs:
                index = paragraph.find(qixiang)
                if index == -1:
                    continue
                else:
                    index_list.append((index,index+len(qixiang)-1,'ATMOS'))
            for shijian in shijians:
                index = paragraph.find(shijian)
                if index == -1:
                    continue
                else:
                    index_list.append((index,index+len(shijian)-1,'TIME'))

            index_list.sort(key=Take_first)
            index2 = 0
            #flag = 0
            if len(index_list) > 0:
                for (index1,ch) in enumerate(paragraph):

                    if len(index_list) < index2+1 :
                        target_f.write(ch + ' O')
                    elif index1 == index_list[index2][0]:
                        target_f.write(ch+' B-'+index_list[index2][2])
                        #flag = 1
                        if index1 == index_list[index2][1]:
                            index2 = index2+1

                    elif index1 > index_list[index2][0] and index1 <= index_list[index2][1]:
                        #flag = 1
                        target_f.write(ch + ' I-' + index_list[index2][2])
                        if index1 == index_list[index2][1]:
                            index2 = index2+1

                    else:
                        #flag = 1
                        target_f.write(ch+' O')

                    target_f.write('\n')
                #if flag == 1:
                target_f.write('\n')
    num = num + 1
target_f.close()



