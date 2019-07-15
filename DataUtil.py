from rauth import OAuth2Service
import numpy
from fpdf import FPDF
import re
import random

range_str = "range"
oneof_str = "oneof"


class Question():
    IsSection = False
    vaild = False

    def __inti__(self, hasSection):
        self.vaild = False
        self.IsSection = hasSection


    def construct(self, text, selectCount, random):
        if self.IsSection:
            self.text =text
            self.selectCount=selectCount
            self.QestionRandom= random


    def Construct(self, text, count, vars, marks, image, ImageHeight, ImageWidth,ImageLeftDistance):
        if self.IsSection == False:
            self.number = count
            self.text = text
            self.image = image
            self.ImageHeight=ImageHeight
            self.ImageWidth=ImageWidth
            self.ImageLeftDistance=ImageLeftDistance
            self.variables = vars
            self.vaild = True
            self.marks = marks


    def AddSubSectionQuestion(self, list):
        if self.IsSection:
            self.SubQuestion=list
            if len(list) >= self.selectCount:
                self.vaild=True


    def getStr(self, prefix, count):
        text = self.text
        for item in self.variables:
            name = item[0]
            val = item[2][random.randrange(len(item[2]))]
            #print(name, val)
            question_str = "\("+ name+"\)"
            #print(type(val).__name__)
            if "int" in type(val).__name__:
                rep_val = str(val)
            elif "float" in type(val).__name__:
                rep_val = str(val).rstrip('0').rstrip('.')
            else:
                rep_val = str(val)

            #print(question_str, "\t", rep_val, "\t", self.text)

            text, i= re.subn(question_str, rep_val, text)
            #print("HERE\t", self.text, "\t", i) '{0:g}'.format(3.140)
        if self.marks > 0:
            text = text + " (Marks: " + str(self.marks) + ")"
        if len(prefix)>0:
            text = prefix + str(count) + ". " + text
        else:
            text = str(count) + ". " + text
        return text


    def Print(self, pdf, header, prefix, count):
        if (self.vaild):
            if(self.IsSection):
                text = prefix+str(count)+". "+ self.text
                pdf.multi_cell(header.NormalLineWidth, header.get_NormalLineHeight(), align="L", txt =text)
                section_count = 0
                section_prefix="\t"+prefix+str(count)+"."
                if(self.QestionRandom):
                    random.shuffle(self.SubQuestion)
                if(self.selectCount>0):
                    list = random.sample(self.SubQuestion,k=self.selectCount)
                else:
                    list = self.SubQuestion
                for question in list:
                    section_count=section_count+1
                    question.Print(pdf,header,section_prefix,section_count)
                return
            else:
                q_str = self.getStr(prefix, count)
                pdf.multi_cell(header.NormalLineWidth, header.get_NormalLineHeight(), align="L", txt=q_str)
                if len(self.image)>0:
                    pdf.image(self.image,pdf.x+self.ImageLeftDistance,pdf.y,w=self.ImageWidth,h=self.ImageHeight)
                    pdf.y=pdf.y+self.ImageHeight


class HeaderData():

    def __inti__(self):
        self.vaild = False

    def Construct(self, HeadLine, TitleFontSize, Head_SubLine, SubTitleFontSize, SecondHeadLine, ExamTitleFontSize,
                  SecondHeadLineSubLine, ExamSubTitleFontSize, PassWord, FullWord, NormalLineHeight, NormalLineWidth,
                  NormalLineFontSize, TitleWidth, TitleLineHeight, SubTitleWidth, SubTitleLineHeight,RandomQuestionOrder,
                  PickQuestionCount, ExamTitleWidth, ExamTitleLineHeight, ExamSubTitleWidth, ExamSubTitleLineHeight):
        self.MainHeadLine = HeadLine
        self.MainHeadLineFontSize = TitleFontSize
        self.MainHeadLineSubLine = Head_SubLine
        self.SubTitleFontSize = SubTitleFontSize
        self.SecondHeadLine = SecondHeadLine
        self.ExamTitleFontSize =ExamTitleFontSize
        self.SecondHeadLineSubLine = SecondHeadLineSubLine
        self.ExamSubTitleFontSize = ExamSubTitleFontSize
        self.PassWord = PassWord
        self.FullWord = FullWord
        self.FullWordFontSize = 10
        self.NormalLineWidth = NormalLineWidth
        self.NormalLineFontSize = NormalLineFontSize
        self.RandomQuestionOrder =RandomQuestionOrder
        self.PickQuestionCount = PickQuestionCount
        self.PassWordFontSize = 10
        self.NormalLineHeight = NormalLineHeight
        self.TitleWidth = TitleWidth
        self.TitleLineHeight = TitleLineHeight
        self.SubTitleWidth = SubTitleWidth
        self.SubTitleLineHeight = SubTitleLineHeight
        self.ExamTitleWidth = ExamTitleWidth
        self.ExamTitleLineHeight=ExamTitleLineHeight
        self.ExamSubTitleWidth=ExamSubTitleWidth
        self.ExamSubTitleLineHeight=ExamSubTitleLineHeight
        self.vaild = True


    def get_NormalLineHeight(self):
        return self.NormalLineHeight

    def get_FullWord(self):
        return self.FullWord


    def get_PassWord(self):
        return self.PassWord

    def get_FullWordFontSize(self):
        return self.FullWordFontSize


    def get_PassWordFontSize(self):
        return self.PassWordFontSize


    def get_ExamTitleFontSize(self):
        return self.ExamTitleFontSize


    def get_ExamSubTitleFontSize(self):
        return self.ExamSubTitleFontSize


    def get_SubTitleFontSize(self):
        return self.SubTitleFontSize


    def get_MainHeadLineFontSize(self):
        return self.MainHeadLineFontSize


    def IsValid(self):
        return self.vaild


    def get_SecondHeadLine(self):
        return self.SecondHeadLine


    def get_SecondHeadLineSubLine(self):
        return self.SecondHeadLineSubLine


    def get_MainHeadLineSubLine(self):
        return self.MainHeadLineSubLine


    def get_MainHeadLine(self):
        return self.MainHeadLine


def ParseSectionGen(text, count):
    question = Question()
    question.__inti__(True)
    if len(text) == 0:
        return question

    #print(text)
    sec_str = re.findall("SectionText[\s]*=[ \t\r\f\v\w(@).=,-]+\n", text)
    if (len(sec_str)==0):
        print ("SectionText not found. Details:\n", text)
        return question
    sec_str = re.split('=', sec_str[0])[1]
    sec_sel_count =0
    sec_sel_count_str = re.findall("SectionSelect[\s]*=[ \t\r\f\v\w(@).=,-]+\n", text)
    if len(sec_sel_count_str)>0:
        sec_sel_count = int(re.split('=', sec_sel_count_str[0])[1])
    section_random = question
    sec_sel_random_str = re.findall("SectionRandom[\s]*=[ \t\r\f\v\w(@).=,-]+\n", text)
    if len(sec_sel_random_str)>0:
        sec_sel_random_str_val = re.split('=', sec_sel_random_str[0])[1]
        sec_sel_random_str_val = re.sub('[^0-9a-zA-Z]+', '', sec_sel_random_str_val)
        sec_sel_random_str_val = sec_sel_random_str_val.strip().upper()
        if sec_sel_random_str_val =="TRUE":
            section_random = True
    #print(sec_str, sec_sel_count, section_random)
    question.construct(sec_str, sec_sel_count, section_random)

    #get all possibel options
    que=[]

    list = re.findall("Question{[\s\w(@).=,-]*}",text)
    #print ("List",list)
    que = ProcessQuestionList(list, que)
    #print(que)
    question.AddSubSectionQuestion(que)
    return question


def ParseGen(text, count):

    question = Question()
    if len(text) == 0:
        return question

    var=[]
    ImageWidthVal=0
    ImageLeftDistance=0
    ImageHeightVal=0
    q_str = re.findall("Text[\s]*=[ \t\r\f\v\w(@).=,-]+\n", text)
    q_str = re.split('=', q_str[0])[1]
    var_list = re.findall("@var[\d]+[\s]*=[ \t\r\f\v\w(),.=-]+\n", text)
    mark_line = re.findall("marks[\s]*=[ \t\r\f\v\d.]+", text, flags=re.IGNORECASE)
    image=re.findall("Image[\s]*=[ \t\r\f\v\w(@).=,-]+\n", text, flags=re.IGNORECASE)
    if len(image)>0:
        image = re.split('=', image[0])[1]
        image = re.sub("\n","",image)
        ImageWidth = re.findall("ImageWidth[\s]*=[ \t\r\f\v\d.]+", text, flags=re.IGNORECASE)
        if len(ImageWidth) == 1:
            ImageWidthVal = float(re.split('=',ImageWidth[0])[1])
        ImageHeight = re.findall("ImageHeight[\s]*=[ \t\r\f\v\d.]+", text, flags=re.IGNORECASE)
        if len(ImageHeight) == 1:
            ImageHeightVal = float(re.split('=',ImageHeight[0])[1])
        if ImageHeightVal == 0 or ImageWidthVal == 0:
            print("image without hight and width ignored. Def: ", text)
            image = ""
        LeftDistance = re.findall("ImageLeftDistance[\s]*=[ \t\r\f\v\d.]+", text, flags=re.IGNORECASE)
        if len(ImageHeight) == 1:
            ImageLeftDistance = float(re.split('=', LeftDistance[0])[1])
    else:
        image=""

    #print(q_str)
    #print(mark_line)
    marks = 0
    if len(mark_line) == 1:
        marks = float(re.split('=',mark_line[0])[1])
    for item in var_list:
        #print(item)
        type=""
        value=[]
        side=re.split('=',item)
        if (len(side)!=2):
            print ("Bad variable. Section: ", text)
            return question
        #print(side)
        if side[1].startswith(range_str):
            type = range_str
            temp = re.findall("[\d]+-[\d]+,[\d.]+",side[1])
            if (len(temp)!=1):
                print("Bad variable. Section: ", text, side)
                return question
            coma_split = re.split(',', temp[0])
            range_split = re.split('-',coma_split[0])
            #print(temp,range_split[0],range_split[1],coma_split[1])
            value = numpy.arange(float(range_split[0]),float(range_split[1])+float(coma_split[1]),float(coma_split[1]))#list(pl.frange(float(range_split[0]),float(range_split[1])+float(coma_split[1]),float(coma_split[1])))
        elif side[1].startswith(oneof_str):
            type = oneof_str
            temp = re.findall(".*?\((.*?)\)",side[1])
            if (len(temp)!=1):
                print("Bad variable. Section: ", text, side)
                return question
            value = re.split(',',temp[0])

        #print(type)
        #print(value)
        var.append([side[0],type,value])
    #print(var)
    question.Construct(q_str, count, var, marks, image, ImageHeightVal, ImageWidthVal, ImageLeftDistance)
    return question


def ProcessQuestionList(list, questions):
    count = 1
    for item in list:
        #print(item)
        question = ParseGen(item, count)
        if question.vaild:
            questions.append(question)
        count = count + 1
    return questions


def ProcessSectionList (list):
    count = 1
    questions = []
    for item in list:
        #print(item)
        question = ParseSectionGen(item, count)
        if question.vaild:
            questions.append(question)
        count = count + 1
    return questions


def ReadHeadLineData (data):
    HeadLine = ""
    Head_SubLine = ""
    SecondHeadLine = ""
    SecondHeadLineSubLine= ""
    PassWord= 0
    FullWord = 0
    TitleFontSize = 20
    SubTitleFontSize = 10
    ExamTitleFontSize = 15
    ExamSubTitleFontSize = 8
    NormalLineWidth=200
    NormalLineFontSize=12
    TitleLineHeight=10
    SubTitleWidth = 200
    SubTitleLineHeight=5
    TitleWidth=200
    ExamTitleWidth =200
    ExamTitleLineHeight = 5
    ExamSubTitleWidth=200
    ExamSubTitleLineHeight=5
    line = data.readline()
    cnt = 1
    NormalLineHeight = 0
    header = HeaderData()
    PickQuestionCount =0
    RandomQuestionOrder="False"

    while line:
        #print(line)
        match = re.match("Title[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            HeadLine = split[1]
        match = re.match("SubTitle[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            Head_SubLine = split[1]
        match = re.match("ExamTitle[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            SecondHeadLine = split[1]
        match = re.match("ExamSubTitle[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            SecondHeadLineSubLine = split[1]
        match = re.match("TitleFontSize[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            TitleFontSize = int(split[1])
        match = re.match("SubTitleFontSize[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            SubTitleFontSize = int(split[1])
        match = re.match("ExamTitleFontSize[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            ExamTitleFontSize = int(split[1])
        match = re.match("ExamSubTitleFontSize[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            ExamSubTitleFontSize = int(split[1])
        match = re.match("FullMarks[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            FullWord = int(split[1])
        match = re.match("PassMarks[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            PassWord = int(split[1])
        match = re.match("NormalLineHeight[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            NormalLineHeight = int(split[1])
        match = re.match("NormalLineWidth[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            NormalLineWidth = int(split[1])
        match = re.match("NormalLineFontSize[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            NormalLineFontSize = int(split[1])
        match = re.match("TitleLineHeight[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            TitleLineHeight = int(split[1])
        match = re.match("TitleWidth[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            TitleWidth = int(split[1])
        match = re.match("SubTitleWidth[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            SubTitleWidth = int(split[1])
        match = re.match("SubTitleLineHeight[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            SubTitleLineHeight = int(split[1])
        match = re.match("RandomQuestionOrder[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            RandomQuestionOrder = re.sub('[^0-9a-zA-Z]+', '', split[1])
            RandomQuestionOrder=RandomQuestionOrder.strip().upper()
        match = re.match("PickQuestionCount[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            PickQuestionCount = int(split[1])
        match = re.match("ExamTitleWidth[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            ExamTitleWidth = int(split[1])
        match = re.match("ExamTitleLineHeight[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            ExamTitleLineHeight = int(split[1])

        match = re.match("ExamSubTitleWidth[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            ExamSubTitleWidth = int(split[1])
        match = re.match("ExamSubTitleLineHeight[\s]*=", line, flags=re.IGNORECASE)
        if match != None:
            split = re.split('=', line)
            ExamSubTitleLineHeight = int(split[1])

        line = data.readline()
        cnt += 1
    header.Construct(HeadLine, TitleFontSize, Head_SubLine, SubTitleFontSize, SecondHeadLine, ExamTitleFontSize,
                     SecondHeadLineSubLine, ExamSubTitleFontSize, PassWord, FullWord, NormalLineHeight, NormalLineWidth,
                     NormalLineFontSize, TitleWidth, TitleLineHeight, SubTitleWidth, SubTitleLineHeight, RandomQuestionOrder,
                     PickQuestionCount, ExamTitleWidth, ExamTitleLineHeight, ExamSubTitleWidth, ExamSubTitleLineHeight)

    return header


def RemoveComment(data):
    #print(data)
    data,comment_count = re.subn("'''.*'''","",data)
    print("Comment_count=", comment_count)
    #print(data)
    return data


def RemoveSections(data):
    #print(data)
    data,comment_count = re.subn("Section\[[\s\w(@).=,-{}]*\]","",data)
    print("Section_Count=", comment_count)
    #print(data)
    return data


def ReadQFile (file_name):
    file = open(file_name,'r',encoding="utf-8")
    data = file.read()
    data = RemoveComment(data)
    #print (data)
    list = re.findall("Section\[[\s\w(@).=,-{}]*\]",data)       #\[
    #print("SectionList: ", list)
    qlist = ProcessSectionList(list)

    data = RemoveSections(data)
    list = re.findall("Question{[\s\w(@).=,-]*}",data)
    #print ("List",list)
    qlist = ProcessQuestionList(list, qlist)

    return qlist


def PrintHeader (pdf, header_data):
    str_val = header_data.get_MainHeadLine()
    if len(str_val) > 0:
        pdf.set_font("Arial", size=header_data.get_MainHeadLineFontSize())
        pdf.multi_cell(header_data.TitleWidth, header_data.TitleLineHeight, align="C", txt=str_val)
    str_val = header_data.get_MainHeadLineSubLine()
    if len(str_val) > 0:
        pdf.set_font("Arial", size=header_data.get_SubTitleFontSize())
        pdf.multi_cell(header_data.SubTitleWidth, header_data.SubTitleLineHeight, align="C", txt=str_val)
    str_val = header_data.get_SecondHeadLine()
    if len(str_val) > 0:
        pdf.set_font("Arial", size=header_data.get_ExamTitleFontSize())
        pdf.multi_cell(header_data.ExamTitleWidth, header_data.ExamTitleLineHeight, align="C", txt=str_val)
    str_val = header_data.get_SecondHeadLineSubLine()
    if len(str_val) > 0:
        pdf.set_font("Arial", size=header_data.get_ExamSubTitleFontSize())
        pdf.multi_cell(header_data.ExamSubTitleWidth, header_data.ExamSubTitleLineHeight, align="C", txt=str_val)
    str_data = ""
    val = header_data.get_FullWord()
    if val > 0:
        str_data= "Full Marks: " + str(val)
        #pdf.set_font("Arial", size=header_data.get_FullWordFontSize())
        #pdf.multi_cell(200, 10, align="L", txt="Full Marks: "+str(val))
    val = header_data.get_PassWord()
    if val > 0:
        str_data= str_data + " / Pass Marks: "+str(val)
        #pdf.set_font("Arial", size=header_data.get_PassWordFontSize())
        #pdf.multi_cell(200, 10, align="L", txt="Pass Marks: "+str(val).rstrip('0').rstrip('.'))
    if len(str_data) > 0:
        pdf.set_font("Arial", size=header_data.get_FullWordFontSize())
        pdf.multi_cell(200, 10, align="L", txt=str_data)
    pdf.dashed_line(pdf.get_x()-100,pdf.get_y(),pdf.get_x()+1000,pdf.get_y())
    return


def ReadNameValFile(file_name):
    file = open(file_name, 'r')
    header = ReadHeadLineData(file)
    if (header.IsValid() == False):
        print ("Invalid Header Info.")
        exit(0)
    return  header


def CreatePDF (copy_count):
    file_name = "question.txt"
    nameval_file = "NameVal.txt"
    header_data =ReadNameValFile(nameval_file)
    q_list = ReadQFile(file_name)
    for i in range(0, copy_count):
        pdf = FPDF()
        count = 1
        pdf.add_page()
        pdf.set_title("Ranbir Roshan")          #no effect
        pdf.set_subject("Ranbir Subject")       #no effect
        pdf.set_author("Author Ranbir")
        pdf.set_auto_page_break('auto')
        pdf.set_creator("Ranbir Creator")
        PrintHeader(pdf, header_data)
        pdf.set_font("Arial", size=header_data.NormalLineFontSize)
        if(header_data.RandomQuestionOrder=="TRUE"):
            random.shuffle(q_list)
        if(header_data.PickQuestionCount < len(q_list) and header_data.PickQuestionCount > 0):
            list = random.sample(q_list, k = header_data.PickQuestionCount)
        else:
            list = q_list
        for question in q_list:
            #PrintQuestion(question, pdf, count, header_data)
            question.Print(pdf,header_data,"",count)
            count = count + 1
        name = "sample_" + str(i) + ".pdf"
        pdf.output(name)


def PrintQuestion(question, pdf, count, header_data):
    q_str = question.getStr(count)
    if question.IsSection:
        question.print(pdf, header_data, "", count)
    else:
        pdf.multi_cell(header_data.NormalLineWidth,header_data.get_NormalLineHeight(), align="L",txt=q_str)