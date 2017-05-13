from xml.dom.minidom import parse
import xml.dom.minidom

from BaseClass import *
from Graph import *
import copy



import MySQLdb

import sys
import os


class YMatrixBuild():
    def __init__(self,cur,conn):
        self.cur = cur
        self.conn = conn
        self.busbarTable = dict()
        self.terminalTable = dict()
        self.nodeTable = dict()
        self.voltageLevelTable = dict()
        self.line_bus_table = dict()
        self.relevantNodeRdfIDList = list()
        self.relevantBusRdfIDList = list()
        self.numBus = 0
        self.S_MVA = 100

    #Define a function to read data from database
    def data_read(self, sql_read, rdf_key):
        self.cur.execute(sql_read, (rdf_key,))
        record = self.cur.fetchall()
        return record

    #Build a dictionary contains necessary information related to voltage levels, 
    #with rdfID as key
    def build_voltageLevelTable(self):
        sql_build_voltageLevelTable = """SELECT rdf,name,substation_rdf,baseVoltage_rdf
            FROM VoltageLevel WHERE rdf = %s """
        for key,value in self.nodeTable.items():
            voltageLevelRecords = self.data_read(sql_build_voltageLevelTable, value['ConnectivityNodeContainer_rdf'])
            for Record in voltageLevelRecords:
                tempVoltageLevel = dict()
                tempVoltageLevel['name'] = Record[1]
                tempVoltageLevel['substation_rdf'] = Record[2]
                tempVoltageLevel['baseVoltage_rdf'] = Record[3]
                self.voltageLevelTable[Record[0]] = tempVoltageLevel



        #print self.voltageLevelTable

    #Build a dictionary contains necessary information related to ShuntCompensator
    #with rdfID as key
    def build_ShuntCompensatorTable(self):
        self.ShuntCompensatorTable = dict()
        sql_build_ShuntCompensatorTable = """SELECT rdf,name,bPerSection,gPerSection,nomU,sections,
            equipmentContainer_rdf, controlEnabled FROM LinearShuntCompensator"""
        self.cur.execute(sql_build_ShuntCompensatorTable)
        ShuntCompensatorRecords = self.cur.fetchall()
        
        for Record in ShuntCompensatorRecords:
            tempShuntCompensator = dict()
            tempShuntCompensator['name'] = Record[1]
            tempShuntCompensator['bPerSection_nominal'] = Record[2]
            tempShuntCompensator['gPerSection_nominal'] = Record[3]
            tempShuntCompensator['nomU'] = Record[4]
            tempShuntCompensator['sections'] = Record[5]
            tempShuntCompensator['equipmentContainer_rdf'] = Record[6]
            tempShuntCompensator['controlEnabled'] = Record[7]
            tempShuntCompensator['b_pu'] = Record[2]/Record[4]/Record[4]*self.S_MVA * Record[5]
            tempShuntCompensator['g_pu'] = Record[3]/Record[4]/Record[4]*self.S_MVA * Record[5]
            self.ShuntCompensatorTable[Record[0]] = tempShuntCompensator
        #print self.ShuntCompensatorTable

    #Build a dictionary contains necessary information related to ACLineSegment
    #with rdfID as key
    def build_lineTable(self):
        self.lineTable = dict()
        sql_build_lineTable = """SELECT rdf,name,ACLineSegment_r,ACLineSegment_x,
            ACLineSegment_gch,ACLineSegment_bch,baseVoltage_rdf FROM ACLineSegment"""
        self.cur.execute(sql_build_lineTable)
        lineRecords = self.cur.fetchall()
        sql_baseVoltage = """SELECT name FROM VoltageLevel WHERE baseVoltage_rdf = %s """
        
        for Record in lineRecords:
            tempLine = dict()
            tempLine['name'] = Record[1]
            tempLine['r_nominal'] = Record[2]
            tempLine['x_nominal'] = Record[3]
            tempLine['gch_nominal'] = Record[4]
            tempLine['bch_nominal'] = Record[5]
            tempLine['baseVoltage_rdf'] = Record[6]
            tempLine['baseVoltage_kV'] = self.data_read(sql_baseVoltage,Record[6])[0][0]
            tempLine['r_pu'] = Record[2]/tempLine['baseVoltage_kV']/tempLine['baseVoltage_kV']*self.S_MVA
            tempLine['x_pu'] = Record[3]/tempLine['baseVoltage_kV']/tempLine['baseVoltage_kV']*self.S_MVA
            tempLine['bch_pu'] = Record[5]*tempLine['baseVoltage_kV']*tempLine['baseVoltage_kV']/self.S_MVA
            self.lineTable[Record[0]] = tempLine
        #print self.lineTable

    #Build a dictionary contains necessary information related to PowerTransformer
    #with rdfID as key
    def build_transformerTable(self):
        self.transformerTable = dict()
        sql_build_transformerTable = """SELECT rdf,name,equipmentContainer_rdf 
                FROM PowerTransformer"""
        self.cur.execute(sql_build_transformerTable)
        transformerRecords = self.cur.fetchall()
        for Record in transformerRecords:
            tempTransformer = dict()
            tempTransformer['name'] = Record[1]
            tempTransformer['equipmentContainer_rdf'] = Record[2]
            self.transformerTable[Record[0]] = tempTransformer
        #print self.transformerTable

    #Build a dictionary contains necessary information related to PowerTransformerEnd
    #with rdfID as key
    def build_transformerendTable(self):
        self.build_transformerTable()
        self.transformerendTable = dict()
        sql_build_transformerendTable = """SELECT rdf,name,Transformer_r,Transformer_x,
            Transformer_b, Transformer_g, Transformer_rdf, baseVoltage_rdf, Terminal_rdf FROM PowerTransformerEnd"""
        self.cur.execute(sql_build_transformerendTable)
        transformerendRecords = self.cur.fetchall()
        sql_baseVoltage = """SELECT name FROM VoltageLevel WHERE baseVoltage_rdf = %s """
        for Record in transformerendRecords:
            tempTransformerend = dict()
            tempTransformerend['name'] = Record[1]
            tempTransformerend['r_nominal'] = Record[2]
            tempTransformerend['x_nominal'] = Record[3]
            tempTransformerend['b_nominal'] = Record[4]
            tempTransformerend['g_nominal'] = Record[5]
            tempTransformerend['Transformer_rdf'] = Record[6]
            tempTransformerend['baseVoltage_rdf'] = Record[7]
            tempTransformerend['Terminal_rdf'] = Record[8]
            tempTransformerend['baseVoltage_kV'] = self.data_read(sql_baseVoltage,Record[7])[0][0]
            tempTransformerend['r_pu'] = Record[2]/tempTransformerend['baseVoltage_kV']/tempTransformerend['baseVoltage_kV']*self.S_MVA
            tempTransformerend['x_pu'] = Record[3]/tempTransformerend['baseVoltage_kV']/tempTransformerend['baseVoltage_kV']*self.S_MVA
            tempTransformerend['b_pu'] = Record[4]/tempTransformerend['baseVoltage_kV']/tempTransformerend['baseVoltage_kV']*self.S_MVA
            tempTransformerend['g_pu'] = Record[5]*tempTransformerend['baseVoltage_kV']*tempTransformerend['baseVoltage_kV']/self.S_MVA

            self.transformerendTable[Record[0]] = tempTransformerend
        #print self.transformerendTable

    #From the above PowerTransformerEnd dictionary, find the impedance of every transformer
    #and update the impedance
    def update_transformerTable(self):
        self.build_transformerendTable()
        for key_tsf, value_tst in self.transformerTable.items():
            tot_r = 0
            tot_x = 0
            for key_tsfd, value_tsfd in self.transformerendTable.items():
                if value_tsfd['Transformer_rdf'] == key_tsf:
                    tot_r = tot_r + value_tsfd['r_pu']
                    tot_x = tot_x + value_tsfd['x_pu']
                self.transformerTable[key_tsf]['r_pu'] = tot_r
                self.transformerTable[key_tsf]['x_pu'] = tot_x
        #print self.transformerTable

    #Build a dictionary contains necessary information related to Breaker
    #with rdfID as key
    def build_breakerTable(self):
        self.breakerTable = dict()
        sql_build_breakerTable = """SELECT rdf,name, state,equipmentContainer_rdf ,baseVoltage_rdf FROM Breaker"""
        self.cur.execute(sql_build_breakerTable)
        breakerRecords = self.cur.fetchall()
        for Record in breakerRecords:
            tempBreaker = dict()
            tempBreaker['name'] = Record[1]
            tempBreaker['stateOpen'] = Record[2]
            tempBreaker['equipmentContainer_rdf'] = Record[3]
            tempBreaker['baseVoltage_rdf'] = Record[4]
            self.breakerTable[Record[0]] = tempBreaker
        #print self.breakerTable

    #Build a dictionary contains all BusbarSections
    #with rdfID as key
    def build_busbarTable(self):
        self.build_breakerTable()
        sql_build_busbarTable = """SELECT rdf,name,equipmentContainer_rdf FROM BusbarSection"""
        self.cur.execute(sql_build_busbarTable)
        busbarRecords = self.cur.fetchall()
        for Record in busbarRecords:
            tempBusbar = dict()
            tempBusbar['name'] = Record[1]
            tempBusbar['equipmentContainer_rdf'] = Record[2]
            self.busbarTable[Record[0]] = tempBusbar
       

    #def update_busbarTable(self):
        
        for key_busbar, value_busbar in self.busbarTable.items():
            num = 0
            for key_breaker, value_breaker in self.breakerTable.items():
                if (value_breaker['equipmentContainer_rdf'] == value_busbar['equipmentContainer_rdf']) and (value_breaker['stateOpen']=='true'):
                    num = num +1
            #print num
            if num ==2:
                self.busbarTable.pop(key_busbar)
        #print self.busbarTable
        
    #Initialize a dictionary contains all ConductingEquipment
    #with rdfID as key
    def initial_ConductingEquipmentTable(self):
        self.ConductingEquipmentTable = dict()
        sql_initial_ConductingEquipmentTable = """SELECT ConductingEquipment_rdf FROM Terminal"""
        self.cur.execute(sql_initial_ConductingEquipmentTable)
        ConductingEquipment_rdfs = self.cur.fetchall()
        for rdf in ConductingEquipment_rdfs:
            if rdf[0] in self.ConductingEquipmentTable.keys(): continue
            self.ConductingEquipmentTable[rdf[0]] = dict()
            self.ConductingEquipmentTable[rdf[0]]['ConnectedTerminal'] = list()
        #print self.ConductingEquipmentTable

    #Build a dictionary contains all Terminals connected to the ConductingEquipment in above table
    #with rdfID as key   
    def build_terminalTable(self):
        sql_build_terminalTable = """SELECT rdf,name,ConductingEquipment_rdf,
            ConnectivityNode_rdf, ConnectCondition FROM Terminal 
            WHERE ConductingEquipment_rdf = %s """ 
        for key,value in self.ConductingEquipmentTable.items():
            terminalRecords = self.data_read(sql_build_terminalTable, key)
            for Record in terminalRecords:
                tempTerminal = dict()
                tempTerminal['name'] = Record[1]
                tempTerminal['ConductingEquipment_rdf'] = Record[2]
                tempTerminal['ConnectivityNode_rdf'] = Record[3]
                tempTerminal['ConnectCondition'] = Record[4]
                self.terminalTable[Record[0]] = tempTerminal
        
        #print self.terminalTable
        
    #Build a dictionary of ConductingEquipment
    #with rdfID as key, and terminal connected as value
    def build_ConductingEquipmentTable(self):
        self.initial_ConductingEquipmentTable()
        self.build_terminalTable()
        for key_CondEquip, value_CondEquip in self.ConductingEquipmentTable.items():
            for key_terminal, value_terminal in self.terminalTable.items():
                if value_terminal['ConductingEquipment_rdf'] == key_CondEquip:
                    self.ConductingEquipmentTable[key_CondEquip]['ConnectedTerminal'].append(key_terminal)

        #remove the ConductingEquipment who has only one terminal connected
        for key, value in self.ConductingEquipmentTable.items():
            if len(value['ConnectedTerminal']) != 2: self.ConductingEquipmentTable.pop(key)

        #print self.ConductingEquipmentTable
        
        
    #Label every ConductingEquipment by checking which table contains their rdfID
    def addType_ConductingEquipmentTable(self):
        self.build_lineTable()
        self.build_busbarTable()
        #self.build_breakerTable()
        self.update_transformerTable()
        self.build_ConductingEquipmentTable()
        for key_CondEquip, value_CondEquip in self.ConductingEquipmentTable.items():
            if key_CondEquip in self.lineTable.keys():
                self.ConductingEquipmentTable[key_CondEquip]['Type'] = 'ACLineSegment'
                self.ConductingEquipmentTable[key_CondEquip]['r_pu'] = dict()
                self.ConductingEquipmentTable[key_CondEquip]['x_pu'] = dict()
                #self.ConductingEquipmentTable[key_CondEquip]['gch_pu'] = dict()
                self.ConductingEquipmentTable[key_CondEquip]['bch_pu'] = dict()


                self.ConductingEquipmentTable[key_CondEquip]['r_pu'] = self.lineTable[key_CondEquip]['r_pu']
                self.ConductingEquipmentTable[key_CondEquip]['x_pu'] = self.lineTable[key_CondEquip]['x_pu']
                self.ConductingEquipmentTable[key_CondEquip]['bch_pu'] = self.lineTable[key_CondEquip]['bch_pu']

            if key_CondEquip in self.transformerTable.keys():
                self.ConductingEquipmentTable[key_CondEquip]['Type'] = 'Transformer'
                self.ConductingEquipmentTable[key_CondEquip]['r_pu'] = dict()
                self.ConductingEquipmentTable[key_CondEquip]['x_pu'] = dict()
                self.ConductingEquipmentTable[key_CondEquip]['r_pu'] = self.transformerTable[key_CondEquip]['r_pu']
                self.ConductingEquipmentTable[key_CondEquip]['x_pu'] = self.transformerTable[key_CondEquip]['x_pu']

            if key_CondEquip in self.breakerTable.keys():
                self.ConductingEquipmentTable[key_CondEquip]['Type'] = 'Breaker'
                self.ConductingEquipmentTable[key_CondEquip]['r'] = 0
                self.ConductingEquipmentTable[key_CondEquip]['x'] = 0

        #print self.ConductingEquipmentTable
        
    #check the status of breakers, if the breakeris opened, remove this breaker from ConductingEquipmentTable  
    def checkConnection_ConductingEquipmentTable(self):
        self.addType_ConductingEquipmentTable()
        for key_CondEquip,value_CondEquip in self.ConductingEquipmentTable.items():
            if (value_CondEquip['Type'] == 'Breaker') and (self.breakerTable[key_CondEquip]['stateOpen'] == 'true'):
                self.ConductingEquipmentTable.pop(key_CondEquip)


 
    #Build a simplified table which contains only terminal pairs
    def build_terminalConnectionList(self):
        self.terminalConnectionList = list()
        self.checkConnection_ConductingEquipmentTable()
        for key_CondEquip,value_CondEquip in self.ConductingEquipmentTable.items():
            tempConnection = [value_CondEquip['ConnectedTerminal'][0],value_CondEquip['ConnectedTerminal'][1]]
            self.terminalConnectionList.append(tempConnection)

        #print self.terminalConnectionList

    #Build a table contains only related terminals
    def build_relativeTerminalList(self):
        self.relativeTerminalList = list()
        self.build_terminalConnectionList()
        for key_CondEquip, value_CondEquip in self.ConductingEquipmentTable.items():
            if value_CondEquip['ConnectedTerminal'][0] not in self.relativeTerminalList:
                self.relativeTerminalList.append(value_CondEquip['ConnectedTerminal'][0])
            if value_CondEquip['ConnectedTerminal'][1] not in self.relativeTerminalList:
                self.relativeTerminalList.append(value_CondEquip['ConnectedTerminal'][1])
        #print self.relativeTerminalList

    #According to related terminals, build a table contains only related connectivity nodes
    def build_relativeNodeList(self):
        self.relativeNodeList = list()
        self.build_relativeTerminalList()
        for terminal in self.relativeTerminalList:
            tempNoderdf = self.terminalTable[terminal]['ConnectivityNode_rdf']
            if tempNoderdf not in self.relativeNodeList:
                self.relativeNodeList.append(tempNoderdf)

        #print self.relativeNodeList

    #For all the related connectivity nodes, build a table contains their information
    def build_nodeTable(self):
        self.build_relativeNodeList()
        self.nodeTable = dict()
        sql_build_nodeTable = """SELECT rdf,name,ConnectivityNodeContainer_rdf 
            FROM ConnectivityNode WHERE rdf = %s """ 
        for terminal in self.relativeNodeList:
            nodeRecords = self.data_read(sql_build_nodeTable, terminal)
            for Record in nodeRecords:
                tempNode = dict()
                if Record[0] not in self.nodeTable.keys():
                    tempNode['name'] = Record[1]
                    tempNode['ConnectivityNodeContainer_rdf'] = Record[2]
                    tempNode['ConnectedTerminal'] = list()
                    tempNode['isBusbar'] = 'false'
                    for key_terminal,value_terminal in self.terminalTable.items():
                        if value_terminal['ConnectivityNode_rdf'] == Record[0]:
                            tempNode['ConnectedTerminal'].append(key_terminal)
                    for terminal in tempNode['ConnectedTerminal']:
                        CondEquip_rdf = self.terminalTable[terminal]['ConductingEquipment_rdf']
                        if CondEquip_rdf in self.busbarTable.keys():
                            tempNode['isBusbar'] = 'true'
                    self.nodeTable[Record[0]] = tempNode
        #print len(self.nodeTable)
        
    #Build a dictionary contains all the related nodes and their connection path between each other      
    def build_nodeConnectionDict(self):
        self.build_nodeTable()
        self.nodeConnectionDict = dict()
        for key_node_from, value_node_from in self.nodeTable.items():
            self.nodeConnectionDict[key_node_from] = dict()
            self.nodeConnectionDict[key_node_from]['name'] = value_node_from['name']
            self.nodeConnectionDict[key_node_from]['isBusbar'] = value_node_from['isBusbar']
            self.nodeConnectionDict[key_node_from]['between'] = list()
            self.nodeConnectionDict[key_node_from]['ValueBetween'] = list()
            self.nodeConnectionDict[key_node_from]['path'] = list()
            self.nodeConnectionDict[key_node_from]['ConductingEquipment'] = list()
            self.nodeConnectionDict[key_node_from]['to'] = list()
            for terminal in value_node_from['ConnectedTerminal']:
                for TerminalConnect in self.terminalConnectionList:
                    if terminal == TerminalConnect[0]:
                        for key_node_to, value_node_to in self.nodeTable.items():
                            if TerminalConnect[1] in value_node_to['ConnectedTerminal']:
                                self.nodeConnectionDict[key_node_from]['path'].append(TerminalConnect)
                                self.nodeConnectionDict[key_node_from]['to'].append(key_node_to)

                    if terminal == TerminalConnect[1]:
                        for key_node_to, value_node_to in self.nodeTable.items():
                            if TerminalConnect[0] in value_node_to['ConnectedTerminal']:
                                self.nodeConnectionDict[key_node_from]['path'].append(TerminalConnect)
                                self.nodeConnectionDict[key_node_from]['to'].append(key_node_to)


        for key, value in self.nodeConnectionDict.items():
            for iter in range(len(value['to'])):
                for key_CondEquip, value_CondEquip in self.ConductingEquipmentTable.items():
                    if [value['path'][iter][0],value['path'][iter][1]] == value_CondEquip['ConnectedTerminal']:
                        self.nodeConnectionDict[key]['ConductingEquipment'].append(key_CondEquip)
                        #Add type to conducting equipment in between
                        self.nodeConnectionDict[key]['between'].append(value_CondEquip['Type']) 
                        
                        #Add value of conducting equipment in between
                        if value_CondEquip['Type'] == 'Breaker':
                            self.nodeConnectionDict[key]['ValueBetween'].append(0)

                        if value_CondEquip['Type'] == 'ACLineSegment':
                            impedance_line = complex(value_CondEquip['r_pu'] , value_CondEquip['x_pu'])
                            self.nodeConnectionDict[key]['ValueBetween'].append(impedance_line)

                        if value_CondEquip['Type'] == 'Transformer':
                            impedance_tsf = complex(value_CondEquip['r_pu'] , value_CondEquip['x_pu'])
                            self.nodeConnectionDict[key]['ValueBetween'].append(impedance_tsf)
                
                    
                    
        #print self.nodeConnectionDict
        #print ''

    #Add number to every connectivity node 
    #(busbar with smaller numer and normal node with bigger number)
    def add_nodeNumber(self):
        self.build_nodeConnectionDict()
        num = 1
        for key_nodeConnection, value_nodeConnection in self.nodeConnectionDict.items():
            if value_nodeConnection['isBusbar'] == 'true':
                self.nodeConnectionDict[key_nodeConnection]['nodeNo.'] = num
                num = num + 1

        for key_nodeConnection, value_nodeConnection in self.nodeConnectionDict.items():
            if value_nodeConnection['isBusbar'] == 'false':
                self.nodeConnectionDict[key_nodeConnection]['nodeNo.'] = num
                num = num + 1

    #Built a dictionary to show the node number and rdfID information 
    def build_nodeNo_rdf(self):
        self.add_nodeNumber()
        self.nodeNo_rdf = dict()
        for key_node, value_node in self.nodeConnectionDict.items():
            self.nodeNo_rdf[value_node['nodeNo.']] = key_node

    #Define a function to get the impedance between two nodes
    def get_value_between_nodes(self, from_rdf, to_rdf):
        value_between_nodes = 0
        from_to_list = list()
        from_to_list = self.nodeConnectionDict[from_rdf]['to']
        from_to_value = self.nodeConnectionDict[from_rdf]['ValueBetween']

        for iter in range(len(from_to_value)):
            one_value = 0
            if from_to_list[iter] == to_rdf:
                value_between_nodes = from_to_value[iter]

        return value_between_nodes

    #Define a function to get the ConductingEquipment rdfID between two nodes
    def get_components_between_nodes(self, from_rdf, to_rdf):
        components_between_nodes = str()
        from_to_list = list()
        from_to_list = self.nodeConnectionDict[from_rdf]['to']
        CondEquipList = self.nodeConnectionDict[from_rdf]['ConductingEquipment']

        for iter in range(len(from_to_list)):
            if from_to_list[iter] == to_rdf:
                components_between_nodes = CondEquipList[iter]
                #print value_between_nodes

        return components_between_nodes

    #Get impedance, ConductingEquipment rdfID and ConductingEquipment type between Bus
    def check_bus_impedance(self):
        self.build_nodeNo_rdf()
        #The below is an iinstance of graph class, 
        #the aim is to build a dictionary only contains connection relation between busbars
        busConnectionGraph = graph(self.nodeConnectionDict)
        busConnectionGraph.build_bus_route()
        self.busConnectionTable = busConnectionGraph.bus_route
        #print self.busConnectionTable

        self.impedance_table = dict()
        self.CondEquipBetween = dict()
        self.CondEquipTypeBetween = dict()

        for key_start, value_start in self.busConnectionTable.items():
            self.impedance_table[key_start] = dict()
            self.CondEquipBetween[key_start] = dict()
            self.CondEquipTypeBetween[key_start] = dict()
            for key_terminal, value_terminal in value_start.items():
                route_impedance = 0
                route_conduct = list()
                route_conductType = list()
                for item in value_terminal:

                    for num in range(len(item)):
                        one_impedance = 0
                        one_conduct = str()
                        one_conductType = str()
                        if num+1 <= len(item)-1:
                            first_rdf = self.nodeNo_rdf[item[num]]
                            second_rdf = self.nodeNo_rdf[item[num+1]]
                            one_impedance = self.get_value_between_nodes(first_rdf, second_rdf)
                            route_impedance = route_impedance + one_impedance

                            one_conduct = self.get_components_between_nodes(first_rdf, second_rdf)
                            route_conduct.append(one_conduct)

                            route_conductType.append(self.ConductingEquipmentTable[one_conduct]['Type'])
                            #print one_impedance

                self.impedance_table[key_start][key_terminal] = route_impedance
                self.CondEquipBetween[key_start][key_terminal] = route_conduct
                self.CondEquipTypeBetween[key_start][key_terminal] = route_conductType
        #print self.impedance_table, 'imp'

    #Define a function to get the reverse version of a list
    def reverse_list(self,input_list):
        reverse_list = list()
        ahead_list = copy.deepcopy(input_list)
        for item in input_list:
            reverse_list.append(ahead_list.pop())

        return reverse_list


    def pur(self,list1):
        for each1 in list1:
            for each2 in list1:
                 if each1 != each2:
                     if len(set(each1) & set(each2)) != 0:
                         list1.remove(each1)
                         list1.remove(each2)
                         list1.append(list(set(each1) | set(each2)))
                         return self.pur(list1)


    #Build a list contains all the busbars that has a 0 impedance in between
    #(which means they are actually same bus under this condition)
    def find_duplicate_busbar(self):
        self.check_bus_impedance()
        self.raw_duplicate_busbar = list()
        for key_start, value_start in self.impedance_table.items():
            for key_terminal, value_terminal in value_start.items():
                if value_terminal == 0:
                    one_duplicate = list()
                    one_duplicate = [key_start, key_terminal]
                    if one_duplicate in self.raw_duplicate_busbar or self.reverse_list(one_duplicate) in self.raw_duplicate_busbar:
                        continue
                    self.raw_duplicate_busbar.append(one_duplicate)

        self.raw_duplicate_busbar_1 = copy.deepcopy(self.raw_duplicate_busbar)

        #print self.raw_duplicate_busbar
        self.duplicate_busbar = list()
        self.pur(self.raw_duplicate_busbar)
        self.duplicate_busbar = copy.deepcopy(self.raw_duplicate_busbar)

        #print self.duplicate_busbar


    #Define a function to change the bus number
    def change_bus_number(self,table_name, current_number, target_number):
        for key_bus, value_bus in table_name.items():
            for key_term, value_term in value_bus.items():
                if key_term == current_number:
                    value_bus[target_number] = value_term
                    value_bus.pop(key_term)
                     

    #Number the duplicated busbar according to the self.duplicate_busbar above
    def combine_duplicate_busbar(self):
        self.find_duplicate_busbar()
        impedance_table = copy.deepcopy(self.impedance_table)
        CondEquipBetween = copy.deepcopy(self.CondEquipBetween)
        CondEquipTypeBetween = copy.deepcopy(self.CondEquipTypeBetween)
        for dup_busbar in self.duplicate_busbar:
            dup_busbar.sort()
            base_busbar = dup_busbar[0]
            for busbar_number in dup_busbar:
                if busbar_number != base_busbar:

                    for key_imp,value_imp in impedance_table[busbar_number].items():
                        self.change_bus_number(impedance_table, busbar_number,base_busbar)
                        impedance_table[base_busbar][key_imp] = value_imp

        self.new_impedance_table = copy.deepcopy(impedance_table)
        #print self.new_impedance_table, '11'

        for dup_busbar in self.duplicate_busbar:
            dup_busbar.sort()
            base_busbar = dup_busbar[0]
            for busbar_number in dup_busbar:
                if busbar_number != base_busbar:
                    self.new_impedance_table.pop(busbar_number)
        #print self.new_impedance_table, '22'


        for key_bus, value_bus in self.new_impedance_table.items():
            for key_term, value_term in value_bus.items():
                if key_term == key_bus:
                    value_bus.pop(key_term)

        new_impedance_table_2 = copy.deepcopy(self.new_impedance_table)




        #for key, value in self.new_impedance_table.items():
         #   print key, value
        #print 'NN'


    #Find the buses who have ACLineSegments in between
    #(in order to add line shunt capacitor)
    def find_has_line_between(self):
        self.has_line_between = list()
        self.cond_rdf_between = list()
        self.line_bch_value = list()
        for key_start, value_start in self.CondEquipTypeBetween.items():
            for key_term, value_term in value_start.items():
                if 'ACLineSegment' in value_term:
                    one_has_line = [key_start, key_term]
                    if one_has_line in self.has_line_between or self.reverse_list(one_has_line) in self.has_line_between:
                        continue
                    self.has_line_between.append(one_has_line)
                    cond_rdfs = self.CondEquipBetween[key_start][key_term]
                    one_bch_value = 0
                    for rdf in cond_rdfs:
                        if self.ConductingEquipmentTable[rdf]['Type'] == 'ACLineSegment':
                            one_bch_value = one_bch_value + self.ConductingEquipmentTable[rdf]['bch_pu']
                    self.line_bch_value.append(one_bch_value/2)
        
        for dup_busbar in self.duplicate_busbar:
            dup_busbar.sort()
            base_busbar = dup_busbar[0]
            for busbar_number in dup_busbar:
                if busbar_number != base_busbar:
                    for item in self.has_line_between:
                        if busbar_number in item:
                            item.remove(busbar_number)
                            item.append(base_busbar)

        #print self.has_line_between
        #print self.cond_rdf_between
        #print self.line_bch_value

    #Change impedance to admittance
    def impedance_to_admittance(self):
        self.find_has_line_between()
        self.admittance_table = dict()
        #change from impedance to admittance
        for key_start, value_start in self.new_impedance_table.items():
            self.admittance_table[key_start] = dict()
            for key_term, value_term in value_start.items():
                self.admittance_table[key_start][key_term] = 1/value_term

        
        #print self.admittance_table,'K'

    #add self admittance and line shunt capacitor
    def add_self_admittance(self):
        #add self admittance
        for key_start, value_start in self.admittance_table.items():
            self_admit = 0
            for key_term, value_term in value_start.items():
                one_value_term = copy.deepcopy(value_term)
                self_admit = self_admit + value_term
            self.admittance_table[key_start][key_start] = self_admit


        #add line shunt capacitor
        for iter_line in range(len(self.has_line_between)):
            for bus_number in self.has_line_between[iter_line]:
                self.admittance_table[bus_number][bus_number] = self.admittance_table[bus_number][bus_number] + complex(0,self.line_bch_value[iter_line])

        #print self.admittance_table
    
    #Add linearShuntCompensator if they are not controllable
    def add_shuntcompensator(self):
        self.build_ShuntCompensatorTable()
        for key_sc, value_sc in self.ShuntCompensatorTable.items():
            for key_tmn, value_tmn in self.terminalTable.items():
                if value_tmn['ConductingEquipment_rdf'] == key_sc:
                    self.ShuntCompensatorTable[key_sc]['ConnectivityNode_rdf'] = value_tmn['ConnectivityNode_rdf']
        for key_sc, value_sc in self.ShuntCompensatorTable.items():
            for key_nn, value_nn in self.nodeNo_rdf.items():
                if value_sc['ConnectivityNode_rdf'] == value_nn and value_sc['controlEnabled'] == 'false':
                    self.admittance_table[key_nn][key_nn] = self.admittance_table[key_nn][key_nn] + complex(value_sc['g_pu'],value_sc['b_pu'])
                    print value_sc['g_pu'],value_sc['b_pu'], key_nn


    #Output
    def build_YMatrix(self):
        self.combine_duplicate_busbar()
        self.impedance_to_admittance()
        self.add_self_admittance()
        self.add_shuntcompensator()
        self.YMatrix = dict()
        self.matrix_bus_original_number = list()
        self.matrix_bus_new_number = list()
        self.matrix_bus_number_relation = dict()
        self.matrix_bus_name = dict()
        self.duplicate_bus_name = dict()
        num = 1
        for key_imp, value_imp in self.admittance_table.items():
            self.matrix_bus_original_number.append(key_imp)
            self.matrix_bus_new_number.append(num)
            self.matrix_bus_number_relation[key_imp] = num
            bus_name = self.nodeConnectionDict[self.nodeNo_rdf[key_imp]]['name']
            self.matrix_bus_name[num] = bus_name
            num = num + 1

        for key_imp, value_imp in self.admittance_table.items():
            img_bus_number = self.matrix_bus_number_relation[key_imp]
            self.YMatrix[img_bus_number] = dict()
            for key_term, value_term in value_imp.items():
                self.YMatrix[img_bus_number][self.matrix_bus_number_relation[key_term]] = value_term

        
        
        num_dup = 1
        for dup_busbar in self.duplicate_busbar:
            self.duplicate_bus_name[num_dup] = list()
            for busbar in dup_busbar:
                self.duplicate_bus_name[num_dup].append(self.nodeConnectionDict[self.nodeNo_rdf[busbar]]['name'])
            num_dup = num_dup +1
        #print self.duplicate_bus_name
        #print self.matrix_bus_original_number
        #print self.matrix_bus_new_number
        #print self.matrix_bus_number_relation
        #print self.YMatrix
        
        #print self.matrix_bus_name

        return self.YMatrix



