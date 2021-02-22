from tkinter import *
import pyrebase 
import os
import sys

config = {  "apiKey": "AIzaSyD16bXpEedpnDQSTAntK2yDk6cITflHR3c",  "authDomain": "gsuathleticsystem.firebaseapp.com",  "databaseURL": "https://gsuathleticsystem.firebaseio.com",  "storageBucket": "gsuathleticsystem.appspot.com",  "serviceAccount": "/Users/liamcurtis/Downloads/gsuathleticsystem-44a680934309.json"} 
firebase = pyrebase.initialize_app(config)
auth = firebase.auth() #authenticate a user 
db = firebase.database()
# Let's create the Tkinter window


#Method for authentication
def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote

class GSUASGUI:
    
    ###STARTUP PAGE
    def __init__(self, master):
        self.master = master
        master.title("GSU Athletics")

        self.signInLbl = Label(master, text = "Sign in")
        self.signInLbl.grid(row=0)
        
        self.signInEmail = Label(master, text = "Email")
        self.signInEmail.grid(row = 1) 
        
        self.RealEmail = Entry(master)
        self.RealEmail.grid(row = 1, column = 1)
        
        self.signInPass = Label(master, text = "Password")
        self.signInPass.grid(row = 2) 
        
        self.RealPasser = Entry(master)
        self.RealPasser.grid(row = 2, column = 1) 
        
        self.SignInBtn = Button(master, text = "Sign in", command = self.signIn)
        self.SignInBtn.grid(row = 3, column =1)
        
        self.SignUpLbl = Label(master, text = "Sign up")
        self.SignUpLbl.grid(row=4)
        
        self.SignUpRoleLbl = Label(master, text= "Role")
        self.SignUpRoleLbl.grid(row=5)
        
        self.variable = StringVar(master)
        self.variable.set("Student-Athlete") # default value
        self.roleOption = OptionMenu(master, self.variable, "Student-Athlete", "Coach")
        self.roleOption.grid(row=5, column=1)
        
        self.SignUpNameLbl = Label(master, text = "Full Name")
        self.SignUpNameLbl.grid(row = 6) 
        
        self.fullName = Entry(master)
        self.fullName.grid(row = 6, column = 1) 
        
        self.SignUpEmailLbl = Label(master, text = "Email")
        self.SignUpEmailLbl.grid(row = 7) 
        
        self.makeEmail = Entry(master)
        self.makeEmail.grid(row = 7, column = 1)
        
        self.SignUpPassLbl = Label(master, text = "Password")
        self.SignUpPassLbl.grid(row = 8)
        
        self.makePassword = Entry(master)
        self.makePassword.grid(row = 8, column = 1)
        
        self.ConfirmPassLbl = Label(master, text = "Confirm Password")
        self.ConfirmPassLbl.grid(row = 9) 
        
        self.confirmPassword = Entry(master)
        self.confirmPassword.grid(row = 9, column = 1) 
        
        self.SignUpBtn = Button(master, text = "Sign up")
        self.SignUpBtn.grid(row=10, column =1)

    ###Login Functionality
    def signIn(self):
        self.user = auth.sign_in_with_email_and_password(self.RealEmail.get(),self.RealPasser.get())
        self.setEmail()
        myUser = db.child("users").order_by_child("email").equal_to(self.email).get()
        myUserString = str(myUser.val())
        self.master.destroy()
        if ("Head Coach" in myUserString):
            self.headCoachDashboard()
        elif ("Coach" in myUserString):
            self.coachDashboard()
        elif ("Student-Athlete" in myUserString):
            self.studentDashboard()
        else:
            print("none")
         
    
    def setEmail(self):
        self.email = self.RealEmail.get()

    
    def logOut(self,auth):
        self.master.destroy()
        auth.current_user = None
        master = Tk()
        self.master = master    
        self.__init__(master)
    
    #COACH DASHBOARD PAGE
    
    
    ###HEAD COACH PAGE
    def headCoachDashboard(self):
        master = Tk()
        self.master = master
        master.title("GSU Head Coach")
        
        # Welcome Message / Logo
        myUser = db.child("users").order_by_child("email").equal_to(self.email).get()
        for user in myUser.each():
            key = user.key()
        
        self.welcomeLbl = Label(master, text = "Welcome Head Coach: " + key)
        self.welcomeLbl.grid(row=0,column=1)
        
        self.createAccountLbl = Label(master, text = "Create Account: ")
        self.createAccountLbl.grid(row=1) 
        self.createAccountBtn = Button(master, text = "Create Account", command = self.createAccount)
        self.createAccountBtn.grid(row=1,column=2)

        
        self.editTeamsLbl = Label(master, text = "Edit Teams: ")
        self.editTeamsLbl.grid(row=2) 
        self.editTeamsBtn = Button(master, text = "Edit Teams", command = self.editTeams)
        self.editTeamsBtn.grid(row=2,column=2)
        
        self.logoutBtn = Button(master, text = "Log Out", command = lambda: self.logOut(auth))
        self.logoutBtn.grid(row=4,column=1) 

    def createAccount(self):
        self.master.destroy()
        master = Tk()
        self.master = master
        master.title("GSU Head Coach")
        
        self.createAccountLbl = Label(master, text = "Create Account")
        self.createAccountLbl.grid(row=0)
        
        self.setRoleLbl = Label(master, text = "Role: ")
        self.setRoleLbl.grid(row=1)
        
        self.variable = StringVar(master)
        optionList = ["Student-Athlete","Coach"]
        self.variable.set("Select a Role") # default value
        self.roleOption = OptionMenu(master, self.variable, *optionList, command = self.setRoleValue)
        self.roleOption.grid(row=1, column=1)
        
        self.newNameLbl = Label(master, text = "Full Name:")
        self.newNameLbl.grid(row = 2)
        
        self.newName = Entry(master)
        self.newName.grid(row = 2, column = 1) 
        
        self.newEmailLbl = Label(master, text = "Email:")
        self.newEmailLbl.grid(row = 3) 
        
        self.newEmail = Entry(master)
        self.newEmail.grid(row = 3, column = 1) 
        
        self.newPassLbl = Label(master, text = "Password:")
        self.newPassLbl.grid(row = 4) 
        
        self.newPass = Entry(master)
        self.newPass.grid(row = 4, column = 1) 
        
        self.submitUserBtn = Button(master, text = "Submit", command = self.confirmCreateAccount)
        self.submitUserBtn.grid(row=5)
        
        self.logoutBtn = Button(master, text = "Log Out", command = lambda: self.logOut(auth))
        self.logoutBtn.grid(row=6) 
   
    def setRoleValue(self,value):
        self.role = value   

    def confirmCreateAccount(self):
        auth.create_user_with_email_and_password(self.newEmail.get(), self.newPass.get())
        newUser = {"name": self.newName.get(), "email": self.newEmail.get(), "role": self.role, "team": "None"}
        db.child("users").child(self.newName.get()).set(newUser)
        self.master.destroy()
        self.headCoachDashboard()

    def editTeams(self):
        self.master.destroy()
        master = Tk()
        self.master = master
        master.title("GSU Head Coach")
        
        self.addCoachLbl = Label(master, text = "Add/Update Coach: ")
        self.addCoachLbl.grid(row=0) 
        self.addCoachBtn = Button(master, text = "Assign Coach", command = self.assignCoach)
        self.addCoachBtn.grid(row=0,column=2) 

        self.addStudentLbl = Label(master, text = "Assign Team Roster: ")
        self.addStudentLbl.grid(row=1) 
        self.addStudentBtn = Button(master, text = "Assign Student", command = self.assignStudent)
        self.addStudentBtn.grid(row=1,column=2) 
        
        self.createTeamsLbl = Label(master, text = "Create Team: ")
        self.createTeamsLbl.grid(row=2) 
        self.createTeamsBtn = Button(master, text = "New Team", command=self.createTeam)
        self.createTeamsBtn.grid(row=2,column=2)
        
        self.logoutBtn = Button(master, text = "Log Out", command = lambda: self.logOut(auth))
        self.logoutBtn.grid(row=3,column=1) 
        
    def assignCoach(self):
        self.master.destroy()
        master = Tk()
        self.master = master
        master.title("GSU Head Coach")
        
        self.setTeamLbl = Label(master, text = "Select a Team: ")
        self.setTeamLbl.grid(row=0)
        
        self.variable = StringVar(master)
        teamList = []
        all_teams = db.child("teams").get()
        for team in all_teams.each():
            teamList.append(team.key()) 
        self.variable.set("Team") # default value
        self.teamOption = OptionMenu(master, self.variable, *teamList, command = self.setTeamValue)
        self.teamOption.grid(row=0, column=2)
        
        self.setCoachLbl = Label(master, text = "Select a Coach: ")
        self.setCoachLbl.grid(row=1)
        
        self.variable = StringVar(master)
        coachList = []
        all_coaches = db.child("users").order_by_child("role").equal_to("Coach").get()

        for coaches in all_coaches.each():
            coachList.append(coaches.key())
            
        self.variable.set("Coach") # default value
        self.coachOption = OptionMenu(master, self.variable, *coachList, command = self.setCoachValue)
        self.coachOption.grid(row=1, column=2)
        
        self.submitBtn = Button(master, text = "Submit", command = self.submitCoachAssign)
        self.submitBtn.grid(row=2, column=1) 
        
        self.logoutBtn = Button(master, text = "Log Out", command = lambda: self.logOut(auth))
        self.logoutBtn.grid(row=3, column=1) 
        
    def setTeamValue(self,value):
        self.team = value 
        
    def setCoachValue(self,value):
        self.coach = value  
    
    def setStudentValue(self,value):
        self.student = value 
        
    def submitCoachAssign(self):
        db.child("teams").child(self.team).update({"coach": self.coach})
        self.master.destroy()
        self.editTeams()
        
    def submitStudentAssign(self):
        student = {"name": self.student}
        db.child("users").child(self.student).update({"team": self.team})
        db.child("teams").child(self.team).child("students").child(self.student).set(student)
        self.editTeams()

    def assignStudent(self):
        self.master.destroy()
        master = Tk()
        self.master = master
        master.title("GSU Head Coach")
        
        self.setTeamLbl = Label(master, text = "Select a Team: ")
        self.setTeamLbl.grid(row=0)
        
        self.variable = StringVar(master)
        teamList = []
        all_teams = db.child("teams").get()
        for team in all_teams.each():
            teamList.append(team.key()) 
        self.variable.set("Team") # default value
        self.teamOption = OptionMenu(master, self.variable, *teamList, command = self.setTeamValue)
        self.teamOption.grid(row=0, column=2)
        
        self.setTeamLbl = Label(master, text = "Select a Student: ")
        self.setTeamLbl.grid(row=1)
        
        self.variable = StringVar(master)
        studentList = []
        all_students = db.child("users").order_by_child("role").equal_to("Student-Athlete").get()

        for students in all_students.each():
            studentList.append(students.key())
            
        self.variable.set("Student") # default value
        self.coachOption = OptionMenu(master, self.variable, *studentList, command = self.setStudentValue)
        self.coachOption.grid(row=1, column=2)
        
        self.submitBtn = Button(master, text = "Submit", command = self.submitStudentAssign)
        self.submitBtn.grid(row=2, column=1) 
        
        self.logoutBtn = Button(master, text = "Log Out", command = lambda: self.logOut(auth))
        self.logoutBtn.grid(row=3, column=1) 
        
    def createTeam(self):
        self.master.destroy()
        master = Tk()
        self.master = master
        master.title("GSU Head Coach")
        
        self.createTeamLbl = Label(master, text = "Create Team")
        self.createTeamLbl.grid(row=0)
        
        self.teamNameLbl = Label(master, text = "Team Name: ")
        self.teamNameLbl.grid(row = 1) 
        
        self.newTeamName = Entry(master)
        self.newTeamName.grid(row = 1, column = 2)
        
        self.chooseSportLbl = Label(master, text = "Sport: ")
        self.chooseSportLbl.grid(row = 2) 
        
        self.newSport = Entry(master)
        self.newSport.grid(row = 2, column = 2) 
        
        self.setCoachLbl = Label(master, text = "Select a Coach: ")
        self.setCoachLbl.grid(row=3)
        
        self.variable = StringVar(master)
        coachList = []
        all_coaches = db.child("users").order_by_child("role").equal_to("Coach").get()

        for coaches in all_coaches.each():
            coachList.append(coaches.key())
            
        self.variable.set("Coach") # default value
        self.coachOption = OptionMenu(master, self.variable, *coachList, command = self.setCoachValue)
        self.coachOption.grid(row=3, column=2)
        
        self.submitBtn = Button(master, text = "Submit", command = self.submitTeamAssign)
        self.submitBtn.grid(row=4, column=1) 
        
        self.logoutBtn = Button(master, text = "Log Out", command = lambda: self.logOut(auth))
        self.logoutBtn.grid(row=5, column=1) 
        
    def submitTeamAssign(self):
        team = {"name": self.newTeamName.get(), "sport": self.newSport.get(), "coach": self.coach}
        db.child("teams").child(self.newTeamName.get()).set(team)
        self.editTeams()
        
    ###STUDENT DASHBOARD PAGE
    
    def studentDashboard(self):
        
        myUser = db.child("users").order_by_child("email").equal_to(self.email).get()
        for user in myUser.each():
            self.userName = user.key()
        message = db.child("users").child(self.userName).child("reminders").get()
        if(message.val() == None):
            master = Tk()
            self.master = master
            master.title("GSU Student")
            myTeam = db.child("users").child(self.userName).child("team").get().val()
            self.setTeamValue(myTeam)
            # Welcome Message / Logo

            self.welcomeLbl = Label(master, text = "Welcome Student: " + self.userName)
            self.welcomeLbl.grid(row=0,column=1)

            self.surveyLbl = Label(master, text = "Take Surveys: ")
            self.surveyLbl.grid(row=1)

            self.variable = StringVar(master)
            surveyList = []
            all_surveys = db.child("teams").child(myTeam).child("surveys").get()
            for survey in all_surveys.each():
                surveyList.append(survey.key()) 
            self.variable.set("Select Survey") # default value
            self.teamOption = OptionMenu(master, self.variable, *surveyList, command = self.setSurveyValue)
            self.teamOption.grid(row=1, column=1)     

            self.surveyBtn = Button(master, text = "Take Survey", command = self.takeSurvey)
            self.surveyBtn.grid(row=1,column=2)

            self.changePassLbl = Label(master, text = "Reset Your Password: ")
            self.changePassLbl.grid(row=2)

            self.changePassBtn = Button(master, text = "Reset Password")
            self.changePassBtn.grid(row=2,column=2)

            self.logoutBtn = Button(master, text = "Log Out", command = lambda: self.logOut(auth))
            self.logoutBtn.grid(row=3, column=1) 
        else:
            self.checkReminder()
        
        
    def checkReminder(self):
        message = db.child("users").child(self.userName).child("reminders").get()
        count = 0
        master = Tk()
        self.master = master
        master.title("GSU Student")
        for alert in message.each():
            self.newAlertLbl = Label(master, text = alert.val())
            self.newAlertLbl.grid(row=count)
            count+=1
        self.okBtn = Button(master, text = "Ok",command = self.exitReminder)
        self.okBtn.grid(row=count)
                      
    def exitReminder(self):
        db.child("users").child(self.userName).child("reminders").remove()
        self.master.destroy()
        self.studentDashboard()
          
    
    def setSurveyValue(self,value):
        self.survey = value
            
    def takeSurvey(self):
        self.questionList = []
        self.questionNumber = []
        self.userName = self.userName
        myQuestions = db.child("teams").child(self.team).child("surveys").child(self.survey).get()
        for question in myQuestions.each():
            self.questionNumber.append(question.key())
            self.questionList.append(question.val())
        self.nextQuestion(self.questionNumber,self.questionList,self.userName,self.survey,0)  
    
    def nextQuestion(self,questionNumber,questionList,userName,survey,count):
        if (count == len(questionNumber)):
            self.submitStudentSurvey()   
        else:
            self.master.destroy()
            
            self.questionNumber = questionNumber
            self.questionList = questionList
            self.userName = userName
            self.survey = survey
            self.count = count
            
            master = Tk()
            self.master = master
            master.title("GSU Student")

            self.newLabel = Label(master, text = questionNumber[count])
            self.newLabel.grid(row=0)

            self.newQuestion = Label(master, text = questionList[count])
            self.newQuestion.grid(row=0,column=1)

            self.newAnswer = Entry(master)
            self.newAnswer.grid(row=1)

            self.submitBtn = Button(master, text = "Submit", command = lambda:self.submitAnswer())
            self.submitBtn.grid(row=1,column=1)
        
    def submitAnswer(self):
        db.child("users").child(self.userName).child("surveys").child(self.survey).child("Answer "+str(self.count+1)).set(self.newAnswer.get())
        self.nextQuestion(self.questionNumber,self.questionList,self.userName,self.survey,self.count+1)
  

    def submitStudentSurvey(self):
        db.child("teams").child(self.team).child("surveys").child(self.survey).child("Students Taken").child(self.userName).set(self.userName)
        self.master.destroy()
        self.studentDashboard()
        
    def  changePass(self):
        email = db.child("users").child(self.userName).child("email").get().val()
        auth.send_password_reset_email(email)
        self.studentDashboard()
    
   

    ###COACH DASHBOARD PAGE
    
    def coachDashboard(self):
        master = Tk()
        self.master = master
        master.title("GSU Coach")
        myUser = db.child("users").order_by_child("email").equal_to(self.email).get()
        for user in myUser.each():
            self.userName = user.key()
        myTeam = db.child("users").child(self.userName).child("team").get().val()
        self.setTeamValue(myTeam)

        # Welcome Message / Logo
        
        self.welcomeLbl = Label(master, text = "Welcome Coach: " + self.userName)
        self.welcomeLbl.grid(row=0,column=1)

        self.surveyLbl = Label(master, text = "Create Survey: ")
        self.surveyLbl.grid(row=1)    
        
        self.surveyBtn = Button(master, text = "New Survey", command = lambda:self.createSurvey(1))
        self.surveyBtn.grid(row=1,column=2) 

        self.changePassLbl = Label(master, text = "Delete Survey: ")
        self.changePassLbl.grid(row=2)  
        
        self.changePassBtn = Button(master, text = "Delete", command = self.deleteSurvey)
        self.changePassBtn.grid(row=2,column=2) 
        
        self.changePassLbl = Label(master, text = "Assign a Survey: ")
        self.changePassLbl.grid(row=3)
        
        self.changePassBtn = Button(master, text = "Assign", command = self.assignSurvey)
        self.changePassBtn.grid(row=3,column=2)  
        
        self.changePassLbl = Label(master, text = "Remind Students to Finish Survey: ")
        self.changePassLbl.grid(row=4)
        
        self.variable = StringVar(master)
        surveyList = []
        surveys = db.child("users").child(self.userName).child("My Surveys").get()
        if (surveys.key() == "None"):
            self.variable.set("None")
        else:
            for survey in surveys.each():
                surveyList.append(survey.key())
            self.variable.set("Select a Survey") # default value
        self.chooseSurvey = OptionMenu(master, self.variable, *surveyList, command = self.setSurveyName)
        self.chooseSurvey.grid(row=4,column=2)
        
        self.logoutBtn = Button(master, text = "Send Reminder", command = self.sendRemind)
        self.logoutBtn.grid(row=5, column=1)
        
        self.logoutBtn = Button(master, text = "Log Out", command = lambda: self.logOut(auth))
        self.logoutBtn.grid(row=6, column=1) 
        
        
    def createSurvey(self,value):
        self.master.destroy()
        master = Tk()
        self.master = master
        master.title("GSU Coach")
        
        self.surveyNameLbl = Label(master, text = "Enter a Survey Name:")
        self.surveyNameLbl.grid(row=0)
        
        self.surveyNameEntry = Entry(master)
        self.surveyNameEntry.grid(row=0,column=1)
                                 
        self.saveNameBtn = Button(master, text = "Save Name", command = lambda:self.surveyPage(value))
        self.saveNameBtn.grid(row=1)
        self.saveName=""
        
        
    def surveyPage(self,value):
        if (self.saveName == ""):
            saveName = self.surveyNameEntry.get()
            questions = []
        else:
            saveName = self.saveName
            questions = self.questions
        self.master.destroy()
        master = Tk()
        self.master = master
        master.title("Survey " + saveName)
        self.saveName = saveName
        self.questions = questions
        self.questionLbl = Label(master, text = ("Question " + str(value)))
        self.questionLbl.grid(row=0)
        self.questionEntry = Entry(master)
        self.questionEntry.grid(row=1)
                                 
        self.submitQuestionBtn = Button(master, text = "Submit Question", command = lambda:self.submitQuestion(value))
        self.submitQuestionBtn.grid(row=2)
         
        self.submitSurveyBtn = Button(master, text = "Save Survey", command = self.submitSurvey)
        self.submitSurveyBtn.grid(row=3)                         
        
    def submitQuestion(self,value):
        self.questions.append(self.questionEntry.get())
        self.surveyPage(value+1)
    
    def submitSurvey(self):
        count = 1
        for question in self.questions:
            db.child("users").child(self.userName).child("My Surveys").child(self.saveName).child("Question " + str(count)).set(question)
            count+=1
        myUser = db.child("users").order_by_child("email").equal_to(self.email).get()
        for user in myUser.each():
            self.userName = user.key()
        myTeam = db.child("users").child(self.userName).child("team").get().val()
        self.setTeamValue(myTeam)
        db.child("teams").child(self.team).child("surveys").child(self.saveName).child("Students Taken").set("None")
        self.master.destroy()
        self.coachDashboard()
        
    def deleteSurvey(self):
        self.master.destroy()
        master = Tk()
        self.master = master
        master.title("GSU Coach")
        
        self.whichSurveyLbl = Label(master, text = "Pick a Survey: ")
        self.whichSurveyLbl.grid(row=0)
        
        self.variable = StringVar(master)
        surveyList = []
        surveys = db.child("users").child(self.userName).child("My Surveys").get()
        for survey in surveys.each():
            surveyList.append(survey.key())
        self.variable.set("Select a Survey") # default value
        self.chooseSurvey = OptionMenu(master, self.variable, *surveyList, command = self.setSurveyName)
        self.chooseSurvey.grid(row=1)
        
        self.deleteBtn = Button(master, text = "Delete Survey", command = self.deleteSurveyDB)
        self.deleteBtn.grid(row=2)
        
    def setSurveyName(self,value):
        self.surveyName = value
        
    def deleteSurveyDB(self):
        db.child("users").child(self.userName).child("My Surveys").child(self.surveyName).remove()
        db.child("teams").child(self.team).child("surveys").child(self.surveyName).remove()
        self.master.destroy()
        self.coachDashboard()
        
    def assignSurvey(self):
        self.master.destroy()
        master = Tk()
        self.master = master
        master.title("GSU Coach")
        
        self.chooseSurveyLbl = Label(master, text = "Assign Survey:")
        self.chooseSurveyLbl.grid(row=0)
        
        self.variable = StringVar(master)
        surveyList = []
        surveys = db.child("users").child(self.userName).child("My Surveys").get()
        for survey in surveys.each():
            surveyList.append(survey.key())
        self.variable.set("Select a Survey") # default value
        self.chooseSurvey = OptionMenu(master, self.variable, *surveyList, command = self.setSurveyName)
        self.chooseSurvey.grid(row=1)
        
        self.teamLbl = Label(master, text = "Assign this survey to: " + self.team)
        self.teamLbl.grid(row=2)
        
        self.submitBtn = Button(master, text = "Assign", command = self.assignSurveyDB)
        self.submitBtn.grid(row=2,column=1)
        
    def assignSurveyDB(self):
        assignedSurvey = db.child("users").child(self.userName).child("My Surveys").child(self.surveyName).get().val()
        db.child("teams").child(self.team).child("surveys").child(self.surveyName).set(assignedSurvey)
        self.master.destroy()
        self.coachDashboard()

    def sendRemind(self):
        studentsOnTeam = db.child("users").order_by_child("team").equal_to(self.team).get()
        studentsCompleted = db.child("teams").child(self.team).child("surveys").child(self.surveyName).child("Students Taken").get()   
        teamStudent = []
        completeStudent = []
        incompleteStudent = []
        
        for student in studentsOnTeam.each():
            if(student.key() != self.userName):
                teamStudent.append(student.key()) 
        if (studentsCompleted.each() == None):
            print("no students have completed this survey")
        else:
            for student in studentsCompleted.each():
                completeStudent.append(student.key())
            
        for student in teamStudent:
            if student in completeStudent:
                print("")
            else:
                incompleteStudent.append(student)
                
        for student in incompleteStudent:
            msg = {"Reminder":"Reminder: " + student + ", your " + self.surveyName + " is incomplete!"}
            db.child("users").child(student).child("reminders").set(msg)
            
        self.master.destroy()
        self.coachDashboard()
        
root = Tk()
my_gui = GSUASGUI(root)
root.mainloop()
