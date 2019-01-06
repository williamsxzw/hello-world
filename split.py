###############################################################################
import sqlite3
import json


class DataManage():
    """
    DataManage class is used to manage the data using database
    including creating table needed, changing and getting data
    """
    
    def __init__(self):
        # connect to database and create project_table if not exists
        
        self.connect = sqlite3.connect('project_score.db')
        self.cursor = self.connect.cursor()
        self.expect_table = 'project_table'
        self.create_table_if_not_exist()
          
    def commmit_change(self):        
        self.connect.commit()
        
    def create_table_if_not_exist(self):
        # function to create project_table if not exists
        
        if self.expect_table not in self.get_table_names():
            self.create_expect_table()
                
    def create_expect_table(self):
        # function to create project_table
        
        table_creat_command = """
        CREATE TABLE project_table (project_name TEXT, num_member INT, \
        project_member TEXT, vote_dict TEXT)"""
        self.cursor.execute(table_creat_command)
        
    def get_table_names(self):
        # function to get the table names in this database
        
        name_command = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cursor.execute(name_command)
        table_names = [i[0] for i in self.cursor.fetchall()]
        return table_names
    
    def drop_all_table(self):
        # drop all tables, only for testing purpose
        
        for table in self.get_table_names():
            self.cursor.execute("DROP TABLE {}".format(table))
        
    def insert_project(self, project_name, project_member):
        # create a new line of data in project_table
        # when a project is created
        
        project_sql = "INSERT INTO project_table (project_name, num_member, \
        project_member, vote_dict) VALUES (?, ?, ?, ?)"
        num_member = len(project_member)
        project_member = self.serialize_data(project_member)
        vote_dict = self.serialize_data({})
        self.cursor.execute(project_sql, (project_name, num_member, \
                                          project_member, vote_dict))
        
    def serialize_data(self, data):
        # serialize data before passing in databse
        
        return json.dumps(data)
    
    def deserialize_data(self, data):
        # deserialize data from database before passing to others
        
        return json.loads(data)
    
    def update_vote(self, project_name, vote_dict):
        # update the votes for a particular project
        # thus, votes can be edited
        
        update_command = "UPDATE project_table SET vote_dict = '{}' \
        WHERE project_name = '{}';"\
        .format(self.serialize_data(vote_dict), project_name)
        self.cursor.execute(update_command)
        
    def get_project_name(self):
        # function to get the project names in project_table
        
        name_command = "SELECT project_name from project_table"
        self.cursor.execute(name_command)
        project_name = [i[0] for i in self.cursor.fetchall()]
        return project_name
    
    def get_project_info(self, project_name):
        # load data from database and deserilized the data
        # return the recovered data
        
        get_project_sql = "SELECT * from project_table \
        WHERE project_name == '{}'".format(project_name)        
        self.cursor.execute(get_project_sql)
        project_line = self.cursor.fetchall()[0]
        project_name, num_member, project_member, vote_dict  = project_line
        project_member = self.deserialize_data(project_member)
        vote_dict = self.deserialize_data(vote_dict)
        return project_name, num_member, project_member, vote_dict

    
class Project():
    """
    Project class is used when a project is created
    a project name is need when a instance is created for identification
    a new line of data will be created in database
    including project name, number of members, list of project member 
    and a dictionary storing all the votes
    when the project member is modified using a setter
    
    The dictionary storing votes will be empty at this stage until voted
    
    when project member is called, data will be recovered from database
    """
    
    
    def __init__(self, project_name):
        # initialized the instance with project name
        
        self.project_name = project_name

    
    @property
    def project_member(self):
        # a getter to recover a list of project member from database
        # when project_member is called
        
        if self.project_name in data_ma.get_project_name():
            project_name, num_member, project_member, vote_dict = \
            data_ma.get_project_info(self.project_name)
            return project_member
        else:
            return []

    @project_member.setter
    def project_member(self, project_member):
        # a setter create a new line of data in database 
        # when project member if modified
        
        data_ma.insert_project(self.project_name, project_member)

        
class Person():
    """
    Project class is used when a vote is created
    a project name is required to identify the corresponding project
    a member name is required to change the corresponding key of vote_dict
    the line of data with the corresponding project name will be modified
    where the key with represent the member of vote_dict will be altered
    a setter will be called to do the above action 
    when the person_vote is modified
    
    when person_vote is called, the value which represented by the member
    in vote_dict will be returned
    """
        
    
    def __init__(self, project_name, member_name):
        # initialize the Person class with project_name and member_name
        
        self.project_name = project_name
        self.member_name = member_name
       
        
    def get_vote_dict(self):
        # a function to get the vote_dict which stores all the votes
        # in corresponding project
        
        project_name, num_member, project_member, vote_dict = \
        data_ma.get_project_info(self.project_name)
        return vote_dict
    
    @property
    def person_vote(self):
        # a getter takes data from database and return value in vote dict 
        # which represented by the member name
        
        if self.project_name in data_ma.get_project_name():
            project_name, num_member, project_member, vote_dict = \
            data_ma.get_project_info(self.project_name)
            if self.member_name in vote_dict:
                return vote_dict[self.member_name]
            else:
                return {}
        else:
            return {}
    
    @person_vote.setter
    def person_vote(self, person_vote):
        # a getter takes data from database and return value in vote dict 
        # which represented by the member name
        
        vote_dict = self.get_vote_dict()
        vote_dict[self.member_name] = person_vote
        data_ma.update_vote(self.project_name, vote_dict)
        

class Spliddit():
    
    def __init__(self):
        # initialize default option and welcome message
        
        self.valid_options = "ACVSQ"
        option_book = {'A':'About', 
                       'C':'Create Project', 
                       'V':'Enter Votes', 
                       'S':'Show Project', 
                       'Q':'Quit'}
        self.menu_message = '\nWelcome to Split-it\n\n'
        for key, item in option_book.items():
            self.menu_message += ('\t{:<16}{}\n'.format(item, key))        
        
    def back_to_main_menu(self):
        input('\n\nPress <Enter> to return to the main menu:')
        print('\n')
        
    def show_menu(self):
        # show menu message
        
        print(self.menu_message)
    
    def check_option(self, option):
        # check if input option is valid
        # return True when valid, False otherwise
        
        if option in self.valid_options:
            return True
        else:
            return False
        
    def option_a(self):
        # show menu when option A is called
        
        self.show_menu()    
    
    def check_int(self, num):
        # try to convert an input string to integer
        # return True when successfull, False otherwise
        
        try:
            int(num)
            return True
        except:
            return False
        
    def check_valid(self, num, value):
        # check if a number is in value range
        # return True when num is larger or equal to value
        # False otherwise
        
        if num >= value:
            return True
        else:
            return False
    
    def check_num(self, input_message, value):
        # keep asking user to input a valid integer using while loop
        # break only when a valid integer is entered
        message = '\nplease enter a ineger larger than or equal to {}\n'\
        .format(value)
        while 1:
            num = input(input_message)
            if self.check_int(num) == True:
                num = int(num)
                if self.check_valid(num, value):
                    return num
            print(message)
    
    def option_c(self):
        # create project when project does not exists in database
        # colltect number of member and a list of project member
        # the project information will automatically be store
        # into database using Project class
        
        project_name = str(input('\n\nEnter the project name:'))
        project_name_list = data_ma.get_project_name()
        if project_name in project_name_list:
            print('\nproject already exist, please start again')
            self.back_to_main_menu()
            return
        
        current_project = Project(project_name)
        num_member = self.check_num('Enter the number of team members:', 3)
        print()
        project_member = []
        for i in range(num_member):
            message = '\tEnter the name of team member {}:'.format(i+1)
            member_name = str(input(message))
            project_member.append(member_name)
        current_project.project_member = project_member
        self.back_to_main_menu()
        #self.show_menu()

    def option_v(self):
        # collect votes for the selected project
        # using a list of projecr member recovered from database
        # each member will vote everyone except themselves
        # votes will be stored in database using Person class
        
        project_name_list = data_ma.get_project_name()
        if len(project_name_list) == 0:
            print('\nno project found, please choose other options')
            self.back_to_main_menu()
            return
        
        project_name = input('\n\nEnter the project name:')
        if project_name not in project_name_list:
            print('\n\nproject name not recognized, please choose again')
            print('valid project names are {}'.format(project_name_list))
            self.back_to_main_menu()
            return
        
        _, num_member, project_member, _ = \
        data_ma.get_project_info(project_name)

        print('\nThere are {} team members\n'.format(num_member))

        for voter in project_member:
            current_person = Person(project_name, voter)
            person_vote = {}
            print("\nEnter {}'s votes, points must add up to 100:\n"\
                  .format(voter))
            for member in project_member:
                if member != voter:
                    person_vote[member] = \
                    self.check_num('\tEnter votes for {}:\t\t'\
                                   .format(member), 0)
            current_person.person_vote = person_vote
            
        self.back_to_main_menu()
        #self.show_menu()        
        
    def option_q(self):
        data_ma.commmit_change()
        
    def option_s(self):
        # a project name is required to locate the data
        # votes are recoverd from data base using project name
        # the share of different person is calculated
        # using given formula
        
        project_name_list = data_ma.get_project_name()
        if len(project_name_list) == 0:
            print('\n\nno project found, please choose other options\n\n')
            self.back_to_main_menu()
            return
        
        project_name = input('\n\nEnter the project name:')
        if project_name not in project_name_list:
            print('\n\nproject name not recognized, please choose again')
            print('valid project names are {}\n\n'.format(project_name_list))
            self.back_to_main_menu()
            return
        
        _, _, _, vote_dict = data_ma.get_project_info(project_name)
        
        if vote_dict == {}:
            print('\n\nvote not complete, please vote again\n\n')
            self.back_to_main_menu()
            return
        score_dict = {member:{} for member in vote_dict}
        for voter in vote_dict:
            person_vote = vote_dict[voter]

            for member in person_vote:
                if member not in score_dict:
                    print('\n\nvote not complete, please vote again\n\n')
                    self.back_to_main_menu()
                    return
                score_dict[member][voter] = person_vote[member]        
        
        print('\nThe point allocation based on votes is:\n')
                
        for member in score_dict:
            score_list = list(score_dict[member].values())
            if len(score_list) == 2:
                score = 1/(1 + (100 - score_list[0])/(score_list[0]) + \
                           (100 - score_list[1])/(score_list[1]))
                score = round(score * 100)
                print('\t{:<12}{:d}'.format(member + ':', score))
            else:
                print('\n\ncalculation is only valid for 3 members')
                print('2 votes required while {} votes were found\n\n'\
                      .format(len(score_list)))
                self.back_to_main_menu()
                return
            
        self.back_to_main_menu()
        #self.show_menu()
        
        
data_ma = DataManage()