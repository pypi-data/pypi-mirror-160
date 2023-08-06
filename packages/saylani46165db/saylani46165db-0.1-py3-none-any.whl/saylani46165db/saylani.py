class Teacher: 
    totTeachers = 0   
    
    def __init__(self):
        self._teacherID = 0 
        self._teacherName = ""
        self._compName = ""
        self._Course = ""
        self._TeacherList = []    
        
    def AddNewTeacher(self, TeacherName, CompanyName, CourseName):
        x = (Teacher.__CheckTeacherExists(self, TeacherName)[0])
        if x == False:
            self.totTeachers += 1
            self._teacherName = TeacherName
            self._compName = CompanyName
            self._Course = CourseName
            tempList = [self.totTeachers, TeacherName, CompanyName, CourseName]
            self._TeacherList.extend([tempList])
        else:
            print("Teacher Name is already Exists!!!!")
            
    def UpdateTeacherInfo(self, TeacherID, TeacherName, CompanyName, CourseName):
        if TeacherID > self.totTeachers:
            print("Teacher ID {} is not Exists !!!".format(TeacherID))
        else:
            myIndex = [(idx) for idx, x in enumerate(self._TeacherList) for y in x if y == TeacherID]
            self._teacherID = TeacherID
            self._teacherName = TeacherName
            self._compName = CompanyName
            self._Course = CourseName
            self._TeacherList[myIndex[0]] = [TeacherID, TeacherName, CompanyName, CourseName]
            Teacher.__PrintTeacherInfo(self, 'S')
        
    def __CheckTeacherExists(self, TeacherName):
        isExists = False
        IndexL = 0
        rList = []
        for idx, x in enumerate(self._TeacherList):
            for y in x:                
                if y == TeacherName:
                    isExists = True
                    IndexL = idx
                    break
              
        rList.append(isExists)  
        rList.append(IndexL)
        return rList
    
    def GetTeacherList(self, TeacherID='A'):
        if TeacherID != 'A':
            try:
                tList = [(x) for idx, x in enumerate(self._TeacherList) for y in x if y == TeacherID]
                self._teacherID = tList[0][0]
                self._teacherName = tList[0][1]
                self._compName = tList[0][2]
                self._Course = tList[0][3]
                Teacher.__PrintTeacherInfo(self, 'S')
            except IndexError:  
                print("Teacher Information is not Exists !!")
        else:
            Teacher.__PrintTeacherInfo(self, 'A')
            
    def __PrintTeacherInfo(self, show='S'):
        TeacherTemp = (f"""Teacher ID\tTeacher Name\t\t\tCompany Name\t\tCourses\n{'-'*100}\n""")
        if show == 'S':
            TeacherTemp += (f"""{self._teacherID}\t\t{self._teacherName}\t\t{self._compName}\t\t\t{self._Course}""")
        else:
            for names in self._TeacherList:
                TeacherTemp +=(f"""{names[0]}\t\t{names[1]}\t\t{names[2]}\t\t\t{names[3]}\n""")
            
        print(TeacherTemp.expandtabs(10))
        
class Student(): 
    totStudents = 0
    
    def __init__(self):
        self._studentID = 0 
        self._studentName = ""
        self._BatchName = ""
        self._RollNum = ""
        self._Course = ""
        self._StudentList = []
        
    
    def AddNewStudent(self, StudentName, BatchName, RollNum, Course):
        x = (Student.__CheckStudentExists(self, StudentName)[0])
        if x == False:
            self.totStudents += 1
            self._studentName = StudentName
            self._BatchName = BatchName
            self._RollNum = RollNum
            self._Course = Course
            tempList = [self.totStudents, StudentName, BatchName, RollNum, Course]
            self._StudentList.extend([tempList])
        else:
            print("Student Name is already Exists!!!!")
        
    def UpdateStudentInfo(self, StudentID, StudentName, BatchName, RollNum, Course):
        if StudentID > self.totStudents:
            print("Student ID {} is not Exists !!!".format(StudentID))
        else:
            myIndex = [(idx) for idx, x in enumerate(self._StudentList) for y in x if y == StudentID]
            self._studentID = StudentID
            self._studentName = StudentName
            self._BatchName = BatchName
            self._RollNum = RollNum
            self._Course = Course
            print(myIndex)
            self._StudentList[myIndex[0]] = [StudentID, StudentName, BatchName, RollNum, Course]
            Student.__PrintStudentInfo(self, 'S')
        
        
    def __CheckStudentExists(self, StudentName):
        isExists = False
        IndexL = 0
        rList = []
        for idx, x in enumerate(self._StudentList):
            for y in x:                
                if y == StudentName:
                    isExists = True
                    IndexL = idx
                    break
              
        rList.append(isExists)  
        rList.append(IndexL)
        return rList
    
    def GetStudentList(self, StudentID='A'):
        if StudentID != 'A':
            try:
                tList = [(x) for idx, x in enumerate(self._StudentList) for y in x if y == StudentID]
                self._studentID = tList[0][0]
                self._studentName = tList[0][1]
                self._BatchName = tList[0][2]
                self._RollNum = tList[0][3]
                self._Course = tList[0][4]
                Student.__PrintStudentInfo(self)
            except IndexError:  
                print("Student Information is not Exists !!")
        else:
            Student.__PrintStudentInfo(self, 'A')    
        
    def __PrintStudentInfo(self, show='S'):
        StudentTemp = (f"""Student ID\tStudent Name\t\tBatch Name\t\tRoll Num\t\tCourses\n{'-'*120}\n""")
        if show == 'S':
            StudentTemp += (f"""{self._studentID}\t\t{self._studentName}\t\t\t{self._BatchName}\t\t{self._RollNum}\t\t{self._Course}""")
        else:
            for names in self._StudentList:
                StudentTemp +=(f"""{names[0]}\t\t{names[1]}\t\t\t{names[2]}\t\t{names[3]}\t\t{names[4]}\n""")
            
        print(StudentTemp.expandtabs(10))

class Courses(): 
    totCourse = 0
    
    def __init__(self):
        self._courseID = 0 
        self._shortName = ""
        self._courseName = ""
        self._Duration = ""
        self._Fees = ""
        self._CourseList = []
        
    
    def AddNewCourse(self, ShortName, CourseName, Duration, Fees):
        x = (Courses.__CheckCourseExists(self, ShortName)[0])
        if x == False:
            self.totCourse += 1      
            self._courseName = CourseName
            self._shortName = ShortName
            self._Duration = Duration
            self._Fees = Fees
            tempList = [self.totCourse, ShortName, CourseName, Duration, Fees]
            self._CourseList.extend([tempList])
        else:
            print("Course Name is already Exists!!!!")
        
    def UpdateCourseInfo(self, CourseID, ShortName, CourseName, Duration, Fees):
        if CourseID > self.totCourse:
            print("Course ID {} is not Exists !!!".format(CourseID))
        else:
            myIndex = [(idx) for idx, x in enumerate(self._CourseList) for y in x if y == CourseID]
            self._courseID = CourseID
            self._shortName = ShortName
            self._courseName = CourseName
            self._Duration = Duration
            self._Fees = Fees
            print(myIndex)
            self._StudentList[myIndex[0]] = [CourseID, ShortName, CourseName, Duration, Fees]
            Courses.__PrintCourseInfo(self)        
        
    def __CheckCourseExists(self, shortName):
        isExists = False
        IndexL = 0
        rList = []
        for idx, x in enumerate(self._CourseList):
            for y in x:                
                if y == shortName:
                    isExists = True
                    IndexL = idx
                    break
              
        rList.append(isExists)  
        rList.append(IndexL)
        return rList
    
    def GetCourseList(self, CourseID='A'):
        if CourseID != "A":
            try:
                tList = [(x) for idx, x in enumerate(self._CourseList) for y in x if y == CourseID]
                self._courseID = tList[0][0]
                self._shortName = tList[0][1]
                self._courseName = tList[0][2]
                self._Duration = tList[0][3]
                self._Fees = tList[0][4]
                Courses.__PrintCourseInfo(self)        
            except IndexError:  
                print("Course is not Exists !!")
        else:
            Courses.__PrintCourseInfo(self, 'A')           
        
    def __PrintCourseInfo(self, show='S'):
        CourseTemp = (f"""Course ID\t\tShort Name\t\tCourse Name\t\tDuration\t\tFees\n{'-'*120}\n""")
        if show == 'S':
            CourseTemp += (f"""{self._courseID}\t\t{self._shortName}\t\t\t{self._courseName}\t\t{self._Duration}\t\t{self._Fees}""")
        else:
            for names in self._CourseList:
                CourseTemp +=(f"""{names[0]}\t\t{names[1]}\t\t\t{names[2]}\t\t{names[3]}\t\t{names[4]}\n""")            
        print(CourseTemp.expandtabs(10))
    
class SaylaniMain(Teacher, Student, Courses):
    def __init__(self):
        self.InstituteName = "Salyani Welfare Trust"
        self.HO_Address = "A-25, Bahadurabad Chowrangi Karachi, Pakistan،"
#         self._Attribute1 = 0
#         self._Attribute2 = 0
#         self._Attribute3 = 0
#         self._Attribute4 = 0
#         self._Attribute5 = 0
        Student._StudentList = []
        Teacher._TeacherList = []
        Courses._CourseList = []
      
    def AboutUS(self):
        tempInfo = (f"""Institute Name\t\t:\t{self.InstituteName}\n""")
        tempInfo += (f"""Address\t\t\t:\t{self.HO_Address}\n\n""")
        tempInfo += (f"""Available Course(s)\t:\t{self.totCourse}\n""")
        tempInfo += (f"""Available Teacher(s)\t:\t{self.totTeachers}\n""")
        tempInfo += (f"""Register Student(s)\t:\t{self.totStudents}\n""")

        print(tempInfo)
        
    def StudentSummary(self, Student ='A'):
        CourseTemp = (f"""Student ID\tStudent Name\t\tBatch Name\t\tCourse Name\t\t\tTeacher Name\n{'-'*120}\n""")
        if Student != 'A':
            try:
                tList = [x for x in self._StudentList for y in x if y == Student]
                self._studentID = tList[0][0]
                self._studentName = tList[0][1]
                self._BatchName = tList[0][2]
                self._RollNum = tList[0][3]
                self._Course = tList[0][4]
                
                tList = [x for x in self._CourseList for y in x if y == self._Course]
                self._courseID = tList[0][0]
                self._shortName = tList[0][1]
                self._courseName = tList[0][2]
                self._Duration = tList[0][3]
                self._Fees = tList[0][4]
                
                tList = [x for x in self._TeacherList for y in x if y == self._shortName]
                self._teacherID = tList[0][0]
                self._teacherName = tList[0][1]
                self._compName = tList[0][2]
                self._Course = tList[0][3]
                
                CourseTemp += (f"""{self._studentID}\t\t{self._studentName}\t\t\t{self._BatchName}\t\t{self._courseName}\t\t{self._teacherName}""")   
            except IndexError: 
                print()
        else:
            totList = []
            for i in range(1, len(self._StudentList)+1):
                sinfo = [(x) for x in self._StudentList for y in x if y == i]
                cinfo = [(x) for x in self._CourseList for y in x if y == sinfo[0][4]]
                tinfo = [(x) for x in self._TeacherList for y in x if y == sinfo[0][4]]
                totList = []
                totList.extend(sinfo[0])
                totList.extend(cinfo[0])
                totList.extend(tinfo[0])
                CourseTemp += (f"""{totList[0]}\t\t{totList[1]}\t\t\t{totList[2]}\t\t{totList[7]}\t\t\t{totList[11]}\n""")   

            
        print(CourseTemp)
