from xml.dom.minidom import parse
import xml.dom.minidom
import copy

import sys
import os



class graph():
    def __init__(self, connection_table):
        self.connection_table = connection_table
        self.bus_route = dict()
        for key, value in self.connection_table.items():
            if value['isBusbar'] == 'true':
                self.bus_route[value['nodeNo.']] = dict()
        #print self.bus_route

        self.init_visit_record = dict() 
        numNodes = range(len(self.connection_table))
        #print numNodes
        for num in numNodes:
            self.init_visit_record[num+1] = list()
            for key, value in self.connection_table.items():
                if value['nodeNo.'] == num+1:
                    initial_connect = {num+1:self.find_next(value)}
                    self.init_visit_record[num+1].append(initial_connect)
                    #print self.find_next(value), num+1
                    #print ''
        #print self.add_new_nodes(self.init_visit_record[4],2)
        self.node_typeList = dict()
        for key, value in self.connection_table.items():
            self.node_typeList[value['nodeNo.']] = value['isBusbar']
        #print self.node_typeList

    def find_next(self,element):
        next_nodes = list()
        for iter in range(len(element['to'])):           
            next_rdf = element['to'][iter]
            next_name = self.connection_table[next_rdf]['nodeNo.']
            next_nodes.append(next_name)
        return next_nodes


    #Define a function to get the last number in a list
    def get_last(self,input_list):
        return input_list[len(input_list)-1]

    #Define a functin to get current waiting list
    def get_waitingList(self, current_dict):
        for key, value in current_dict.items():
            return value

    #Define a functin to return to the previous father node
    def reverse(self, position_List_reverse, temp_view_List_reverse):
        position_List_reverse.pop()
        temp_view_List_reverse.pop()
        

    def judge_next(self, bus_number):
        if self.node_typeList[bus_number] == 'true':
            return 'is bus bar'
        if self.node_typeList[bus_number] == 'false':
            return 'not bus bar'

    def check_node_stop(self, node_number ,bus_stop):
        if node_number == bus_stop:
            return 'new route find'
        elif self.judge_next(node_number) == 'is bus bar':
            return 'reached another bus'
        elif self.judge_next(node_number) == 'not bus bar':
            return 'go to next branch'


    #Add the node connection to view_List above
    def add_new_nodes(self, current_List, new_node_number):
        new_records = list()
        check_list = list()
        records = self.init_visit_record[new_node_number][0][new_node_number]
        for values in current_List:
            check_list.append(values.keys()[0])
        for record in records:
            if record not in check_list:
                new_records.append(record)
        return {new_node_number:new_records}

    #Find the route between two buses
    def route_finder(self,bus_start, bus_stop):
        #view_List is a dictionary contains the information of how nodes are connected with each other
        view_List = self.init_visit_record[bus_start]
        temp_view_List = copy.deepcopy(view_List)

        #position list stores current node we are reading
        position_List = list()
        position_List.append(bus_start)

        
        #waiting_List contains the node waiting to be read
        waiting_List = self.get_waitingList(self.get_last(temp_view_List))
        current_father = bus_start
        while True:

            #Stop reading when 
            #(all the son of the start bus has been read) && (all the list only contains one empty unread node)
            if (len(temp_view_List[0][bus_start]) == 0) and (len(temp_view_List) == 1) :
                break

            #when all the nodes in waiting_List has been read, reverse to previous father node
            if len(waiting_List) == 0:
                self.reverse(position_List, temp_view_List)
                waiting_List = self.get_waitingList(self.get_last(temp_view_List))


            elif len(waiting_List) >= 1:
                
                #pick up the last son from waiting_List to read
                next_branch = waiting_List.pop()

                #Add the current reading node to position_List
                position_List.append(next_branch)

                
                #if the branch is the stop bus number we are looking for, add the position_list to route_list
                #and then reverse to previous father
                if self.check_node_stop(next_branch, bus_stop) == 'new route find':
                    #print position_List, 'position'
                    
                    self.bus_route[bus_start][bus_stop] = list()
                    #print self.bus_route, 'before'
                    one_route = copy.deepcopy(position_List)
                    self.bus_route[bus_start][bus_stop].append(one_route)                   
                    position_List.pop()

                #if the branch is a bus but not the stop bus number we are looking for
                #remove this branch from the position_List
                if self.check_node_stop(next_branch, bus_stop) == 'reached another bus':
                    position_List.pop()

                #if the branch is not a bus
                #We remember this node and see what node is connected to this node 
                #then add this node to our view_List and waiting_List                   
                if self.check_node_stop(next_branch, bus_stop) == 'go to next branch': 
                    temp_view_List.append(self.add_new_nodes(temp_view_List,next_branch))
                    waiting_List = self.get_waitingList(self.get_last(temp_view_List))

    #Find the route between all buses                  
    def build_bus_route(self):
        busbar_num_from = range(len(self.bus_route))
        busbar_num_to = range(len(self.bus_route))

        for num_from in busbar_num_from:
            for num_to in busbar_num_to:
                #print num_from+1, num_to+1
                if num_from != num_to:
                    #print num_from+1, num_to+1
                    self.route_finder(num_from+1, num_to+1)
            
        #print self.bus_route




        