from xml.dom.minidom import parse
import xml.dom.minidom

import MySQLdb

import sys
import os
import time


class AllChilds():
    def __init__(self,collection_EQ,collection_SSH):
        self.Table_Names = list()
        self.length = dict()
        self.all_eles = list()
        self.collection_EQ = collection_EQ
        self.collection_SSH = collection_SSH
        self.length['EQ'] = len(self.collection_EQ.childNodes)
        self.length['SSH'] = len(self.collection_SSH.childNodes)


        self.Table_Names.append('BaseVoltage')
        self.Table_Names.append('Substation')
        self.Table_Names.append('VoltageLevel')
        self.Table_Names.append('GeneratingUnit')
        self.Table_Names.append('SynchronousMachine')
        self.Table_Names.append('RegulatingControl')
        self.Table_Names.append('PowerTransformer')
        self.Table_Names.append('EnergyConsumer')
        self.Table_Names.append('PowerTransformerEnd')
        self.Table_Names.append('Breaker')
        self.Table_Names.append('RatioTapChanger')
        self.Table_Names.append('ACLineSegment')
        self.Table_Names.append('Terminal')
        self.Table_Names.append('ConnectivityNode')
        self.Table_Names.append('BusbarSection')
        self.Table_Names.append('LinearShuntCompensator')




    def find_all_elements(self):
        for count in range(0,self.length['EQ']):
            name = self.collection_EQ.childNodes[count].localName
            if name == None : continue
            self.all_eles.append(name.encode())


        for count in range(0,self.length['SSH']):
            name = self.collection_SSH.childNodes[count].localName
            if name == None : continue
            self.all_eles.append(name.encode())

        self.all_eles = list(set(self.all_eles))


    def find_all_child(self):
        self.find_all_elements()
        self.All_Child = dict()
        self.All_Child['EQ'] = dict()
        self.All_Child['SSH'] = dict() 
        for name in self.all_eles:
            self.All_Child['EQ'][name] = self.collection_EQ.getElementsByTagName("cim:"+name)

            self.All_Child['SSH'][name] = self.collection_SSH.getElementsByTagName("cim:"+name)



    def pick_Needed_Child(self):
        self.find_all_child()
        self.Needed_Child = dict()
        self.Needed_Child['EQ'] = dict()
        self.Needed_Child['SSH']= dict()

        for table_name in self.Table_Names:
            for key in self.All_Child['EQ']:
                
                if table_name != key: continue
                self.Needed_Child['EQ'][key] = self.All_Child['EQ'][key]


        for table_name in self.Table_Names:
            for key in self.All_Child['SSH']:
                
                if table_name != key: continue
                self.Needed_Child['SSH'][key] = self.All_Child['SSH'][key]
        return self.Needed_Child



