
#from xml.dom.minidom import parse
#import xml.dom.minidom

#from BaseClass import *
#from DBoperat_class import *

#import MySQLdb

#import sys
#import os
#import time



BaseVoltages = dict()
Substations = dict()
VoltageLevels = dict()
GeneratingUnits = dict()
SynchronousMachines = dict()
RegulatingControls = dict()
PowerTransformers = dict()
EnergyConsumers = dict()
PowerTransformerEnds = dict()
Breakers = dict()
RatioTapChangers = dict()
ACLineSegments = dict()
ConnectivityNodes = dict()
Terminals = dict()
BusbarSections = dict()
LinearShuntCompensators = dict()


BaseVoltages['EQ'] = Needed_Child['EQ']['BaseVoltage']
Substations['EQ'] = Needed_Child['EQ']['Substation']
VoltageLevels['EQ'] = Needed_Child['EQ']['VoltageLevel']
GeneratingUnits['EQ'] = Needed_Child['EQ']['GeneratingUnit']
SynchronousMachines['EQ'] = Needed_Child['EQ']['SynchronousMachine']
SynchronousMachines['SSH'] = Needed_Child['SSH']['SynchronousMachine']
RegulatingControls['EQ'] = Needed_Child['EQ']['RegulatingControl']
RegulatingControls['SSH'] = Needed_Child['SSH']['RegulatingControl']
PowerTransformers['EQ'] = Needed_Child['EQ']['PowerTransformer']
EnergyConsumers['EQ'] = Needed_Child['EQ']['EnergyConsumer']
EnergyConsumers['SSH'] = Needed_Child['SSH']['EnergyConsumer']
PowerTransformerEnds['EQ'] = Needed_Child['EQ']['PowerTransformerEnd']
Breakers['EQ'] = Needed_Child['EQ']['Breaker']
Breakers['SSH'] = Needed_Child['SSH']['Breaker']
RatioTapChangers['EQ'] = Needed_Child['EQ']['RatioTapChanger']
RatioTapChangers['SSH'] = Needed_Child['SSH']['RatioTapChanger']
ACLineSegments['EQ'] = Needed_Child['EQ']['ACLineSegment']
ConnectivityNodes['EQ'] = Needed_Child['EQ']['ConnectivityNode']
Terminals['EQ'] = Needed_Child['EQ']['Terminal']
Terminals['SSH'] = Needed_Child['SSH']['Terminal']
BusbarSections['EQ'] = Needed_Child['EQ']['BusbarSection']
LinearShuntCompensators['EQ'] = Needed_Child['EQ']['LinearShuntCompensator']
LinearShuntCompensators['SSH'] = Needed_Child['SSH']['LinearShuntCompensator']

#Build instances of all the information
BaseVoltageTable= Feed_Table_BV(BaseVoltages, cur, conn)
SubstationTable= Feed_Table_SS(Substations, cur, conn)
VoltageLevelTable= Feed_Table_VL(VoltageLevels, cur, conn)
GeneratingUnitTable= Feed_Table_GU(GeneratingUnits, cur, conn)
SynchronousMachineTable= Feed_Table_SYM(SynchronousMachines, cur, conn)
RegulatingControlTable= Feed_Table_RC(RegulatingControls, cur, conn)
PowerTransformerTable= Feed_Table_PT(PowerTransformers, cur, conn)
EnergyConsumerTable= Feed_Table_EC(EnergyConsumers, cur, conn)
PowerTransformerEndTable= Feed_Table_PTE(PowerTransformerEnds, cur, conn)
BreakerTable= Feed_Table_BR(Breakers, cur, conn)
RatioTapChangerTable= Feed_Table_RTC(RatioTapChangers, cur, conn)
ACLineSegmentTable= Feed_Table_ACL(ACLineSegments, cur, conn)
ConnectivityNodeTable= Feed_Table_CNN(ConnectivityNodes, cur, conn)
TerminalTable= Feed_Table_TMN(Terminals, cur, conn)
BusbarSectionTable = Feed_Table_BBS(BusbarSections, cur, conn)
LinearShuntCompensatorTable = Feed_Table_LSC(LinearShuntCompensators, cur, conn)

#Choose the column needed in the table
#If one table has no foreign keys, it only has one dictionary including all the column names and their data format
#If one table has foreign key, it will have an additional dictionary indicating the foreign key and primary key
v='varchar(80)'
f = 'float(50)'

#BV = BaseVoltage
BV_name_type = {'nominalValue':f}

#SS = SubStation
SS_name_type = {'name':v, 'region_rdf':v,}

#VL = VoltageLevel
VL_name_type = {'name':f, 'substation_rdf':v,'baseVoltage_rdf':v}
VL_FK_from_to = {'substation_rdf':'Substation', 'baseVoltage_rdf':'BaseVoltage'}

#GU = Generating Unit
GU_name_type = {'name':v, 'maxP':f,'minP':f, 'equipmentContainer_rdf':v}

#SYM = Synchronousmachine
SYM_name_type = {'name':v, 'ratedS':f,'P':f,'Q':f,'genUnit_rdf':v ,'regControl_rdf':v , \
                'equipmentContainer_rdf':v, 'baseVoltage_rdf':v}
SYM_FK_from_to = {'genUnit_rdf':'GeneratingUnit', 'regControl_rdf':'RegulatingControl', \
                'baseVoltage_rdf':'BaseVoltage' }

#RC = Regulating Control
RC_name_type = {'name':v, 'targetValue':f}

#PT = PowerTransformer
PT_name_type = {'name':v, 'equipmentContainer_rdf':v}

#EC = EnergyConsumer
EC_name_type = {'name':v, 'P':f,'Q':f,'equipmentContainer_rdf':v ,'baseVoltage_rdf':v }
EC_FK_from_to = {'baseVoltage_rdf':'BaseVoltage' }

#PTE = PowerTransformerEnd
PTE_name_type = {'name':v, 'Transformer_r':f,'Transformer_x':f,'Transformer_b':f, \
                'Transformer_g':f,'Transformer_rdf':v ,'baseVoltage_rdf':v, 'Terminal_rdf':v, 'ratedU':f, 'ratedS':f}
PTE_FK_from_to = {'Transformer_rdf':'PowerTransformer','baseVoltage_rdf':'BaseVoltage',\
                 'Terminal_rdf':'Terminal'}

#BR = Breaker
BR_name_type = {'name':v, 'state':v,'equipmentContainer_rdf':v ,'baseVoltage_rdf':v }
BR_FK_from_to = {'baseVoltage_rdf':'BaseVoltage' }

#RTC = RationTapChanger
RTC_name_type = {'name':v, 'step':f,'TransformerEnd_rdf':v}
RTC_FK_from_to = {'TransformerEnd_rdf':'PowerTransformerEnd'}

#ACL = ACLineSegment
ACL_name_type = {'name':v, 'ACLineSegment_r':f, 'ACLineSegment_x':f, \
                'ACLineSegment_bch':f, 'ACLineSegment_gch':f,\
                'equipmentContainer_rdf':v, 'baseVoltage_rdf':v}

ACL_FK_from_to = {'baseVoltage_rdf':'BaseVoltage' }

#CNN = ConnectivityNode
CNN_name_type = {'name':v, 'ConnectivityNodeContainer_rdf':v}

#TNN = Terminal
TMN_name_type = {'name':v, 'ConductingEquipment_rdf':v, 'ConnectivityNode_rdf':v, 'ConnectCondition':v}
TMN_FK_from_to = {'ConnectivityNode_rdf':'ConnectivityNode'}

#BBS = BusbarSection
BBS_name_type = {'name':v,'equipmentContainer_rdf':v}

#LSC = LineShuntCompensator
LSC_name_type = {'name':v, 'bPerSection':f, 'gPerSection':f, \
                'nomU':f, 'equipmentContainer_rdf':v, 'sections' : f}

#Create New Tables
if New_Table_Choice == 1:
    var_TabCheck.set('Waiting For Table Creating...')
    Stat_Para_TabCheck_wait = {'bd':1,'anchor':W, 'fg':'black'}
    win.AddStatus(Stat_Para_TabCheck_wait, TabCheckStructStatus, var_TabCheck.get())
    win.root.update()


    BaseVoltageTable.New_Table_No_FK('BaseVoltage',BV_name_type)
    New_Message = 'Table BaseVoltage Created!'
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    SubstationTable.New_Table_No_FK('Substation',SS_name_type)
    New_Message = 'Table Substation Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    VoltageLevelTable.New_Table_Has_FK('VoltageLevel',VL_name_type, VL_FK_from_to)
    New_Message = 'Table VoltageLevel Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    GeneratingUnitTable.New_Table_No_FK('GeneratingUnit',GU_name_type)
    New_Message = 'Table GeneratingUnit Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    SynchronousMachineTable.New_Table_Has_FK('SynchronousMachine',SYM_name_type, SYM_FK_from_to)
    New_Message = 'Table SynchronousMachine Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    RegulatingControlTable.New_Table_No_FK('RegulatingControl',RC_name_type)
    New_Message = 'Table RegulatingControl Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    PowerTransformerTable.New_Table_No_FK('PowerTransformer',PT_name_type)
    New_Message = 'Table PowerTransformer Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    EnergyConsumerTable.New_Table_Has_FK('EnergyConsumer',EC_name_type, EC_FK_from_to)
    New_Message = 'Table EnergyConsumer Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    PowerTransformerEndTable.New_Table_Has_FK('PowerTransformerEnd',PTE_name_type, PTE_FK_from_to)
    New_Message = 'Table PowerTransformerEnd Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    BreakerTable.New_Table_Has_FK('Breaker',BR_name_type, BR_FK_from_to)
    New_Message = 'Table Breaker Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    RatioTapChangerTable.New_Table_Has_FK('RatioTapChanger',RTC_name_type, RTC_FK_from_to)
    New_Message = 'Table RatioTapChanger Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    ACLineSegmentTable.New_Table_Has_FK('ACLineSegment',ACL_name_type, ACL_FK_from_to)
    New_Message = 'Table ACLineSegment Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)

    ConnectivityNodeTable.New_Table_No_FK('ConnectivityNode',CNN_name_type)
    New_Message = 'Table ConnectivityNode Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)

    TerminalTable.New_Table_Has_FK('Terminal',TMN_name_type, TMN_FK_from_to)
    New_Message = 'Table Terminal Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    BusbarSectionTable.New_Table_No_FK('BusbarSection',BBS_name_type)
    New_Message = 'Table BusbarSection Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)

    LinearShuntCompensatorTable.New_Table_No_FK('LinearShuntCompensator',LSC_name_type)
    New_Message = 'Table LinearShuntCompensator Created!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    var_TabCheck.set('All Tables Created')
    Stat_Para_TabCheck_create = {'bd':1,'anchor':W, 'fg':'#228B22'}
    win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
    win.root.update()
    time.sleep(0.3)


#Check whether all tables exist, if not, create
if New_Table_Choice == 0:
    var_TabCheck.set('Waiting For Table Checking...')
    Stat_Para_TabCheck_wait = {'bd':1,'anchor':W, 'fg':'black'}
    win.AddStatus(Stat_Para_TabCheck_wait, TabCheckStructStatus, var_TabCheck.get())
    win.root.update()


    BaseVoltageTable.Exist_Table_No_FK('BaseVoltage',BV_name_type)
    New_Message = 'Table BaseVoltage Checked!'
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    SubstationTable.Exist_Table_No_FK('Substation',SS_name_type)
    New_Message = 'Table Substation Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    VL_FK_from_to = {'substation_rdf':'Substation', 'baseVoltage_rdf':'BaseVoltage'}
    VoltageLevelTable.Exist_Table_Has_FK('VoltageLevel',VL_name_type, VL_FK_from_to)
    New_Message = 'Table VoltageLevel Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    GeneratingUnitTable.Exist_Table_No_FK('GeneratingUnit',GU_name_type)
    New_Message = 'Table GeneratingUnit Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    SynchronousMachineTable.Exist_Table_Has_FK('SynchronousMachine',SYM_name_type, SYM_FK_from_to)
    New_Message = 'Table SynchronousMachine Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    RegulatingControlTable.Exist_Table_No_FK('RegulatingControl',RC_name_type)
    New_Message = 'Table RegulatingControl Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    PowerTransformerTable.Exist_Table_No_FK('PowerTransformer',PT_name_type)
    New_Message = 'Table PowerTransformer Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    EnergyConsumerTable.Exist_Table_Has_FK('EnergyConsumer',EC_name_type, EC_FK_from_to)
    New_Message = 'Table EnergyConsumer Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    PowerTransformerEndTable.Exist_Table_Has_FK('PowerTransformerEnd',PTE_name_type, PTE_FK_from_to)
    New_Message = 'Table PowerTransformerEnd Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    BreakerTable.Exist_Table_Has_FK('Breaker',BR_name_type, BR_FK_from_to)
    New_Message = 'Table Breaker Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    RatioTapChangerTable.Exist_Table_Has_FK('RatioTapChanger',RTC_name_type, RTC_FK_from_to)
    New_Message = 'Table RatioTapChanger Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)


    ACLineSegmentTable.Exist_Table_Has_FK('ACLineSegment',ACL_name_type, ACL_FK_from_to)
    New_Message = 'Table ACLineSegment Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)

    ConnectivityNodeTable.Exist_Table_No_FK('ConnectivityNode',CNN_name_type)
    New_Message = 'Table ConnectivityNode Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)

    TerminalTable.Exist_Table_Has_FK('Terminal',TMN_name_type, TMN_FK_from_to)
    New_Message = 'Table Terminal Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)

    BusbarSectionTable.Exist_Table_No_FK('BusbarSection',BBS_name_type)
    New_Message = 'Table BusbarSection Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)

    LinearShuntCompensatorTable.Exist_Table_No_FK('LinearShuntCompensator',LSC_name_type)
    New_Message = 'Table LinearShuntCompensator Checked!'  
    Update_Status(New_Message, 'black')
    time.sleep(0.15)

    var_TabCheck.set('All Tables Checked!')
    Stat_Para_TabCheck_create = {'bd':1,'anchor':W, 'fg':'#228B22'}
    win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
    win.root.update()
    time.sleep(0.15)
   

#Write all the data into tables
var_TabCheck.set('Waiting For Table Writting...')
Stat_Para_TabCheck_wait = {'bd':1,'anchor':W, 'fg':'black'}
win.AddStatus(Stat_Para_TabCheck_wait, TabCheckStructStatus, var_TabCheck.get())
win.root.update()


BaseVoltageTable.table_write_ID()
BaseVoltageTable.feed_BV("""UPDATE BaseVoltage SET nominalValue=%s
                WHERE rdf = %s """)

New_Message = 'Table BaseVoltage Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



SubstationTable.table_write_ID()
SubstationTable.feed_SS("""UPDATE Substation SET name=%s, region_rdf = %s
                WHERE rdf = %s """)

New_Message = 'Table Substation Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



VoltageLevelTable.table_write_ID()
VoltageLevelTable.feed_VL("""UPDATE VoltageLevel SET name=%s, substation_rdf = %s, baseVoltage_rdf = %s
                WHERE rdf = %s """)
New_Message = 'Table VoltageLevel Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



GeneratingUnitTable.table_write_ID()
GeneratingUnitTable.feed_GU("""UPDATE GeneratingUnit SET name=%s,  maxP = %s, 
    minP = %s, equipmentContainer_rdf = %s WHERE rdf = %s """)

New_Message = 'Table GeneratingUnit Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



SynchronousMachineTable.table_write_ID()
SynchronousMachineTable.feed_SYM("""UPDATE SynchronousMachine SET name=%s,  
    ratedS = %s,genUnit_rdf = %s, regControl_rdf = %s, equipmentContainer_rdf = %s, baseVoltage_rdf = %s WHERE rdf = %s """)

SynchronousMachineTable.SSH_feed_SYM("""UPDATE SynchronousMachine SET P=%s,  
    Q = %s WHERE rdf = %s """)

New_Message = 'Table SynchronousMachine Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



RegulatingControlTable.table_write_ID()
RegulatingControlTable.feed_RC("""UPDATE RegulatingControl SET name=%s WHERE rdf = %s """)

RegulatingControlTable.SSH_feed_RC("""UPDATE RegulatingControl SET targetValue = %s WHERE rdf = %s """)

New_Message = 'Table RegulatingControl Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



PowerTransformerTable.table_write_ID()
PowerTransformerTable.feed_PT("""UPDATE PowerTransformer SET name=%s, equipmentContainer_rdf = %s 
    WHERE rdf = %s """)

New_Message = 'Table PowerTransformer Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



EnergyConsumerTable.table_write_ID()
EnergyConsumerTable.feed_EC("""UPDATE EnergyConsumer SET name=%s, equipmentContainer_rdf = %s,
    baseVoltage_rdf = %s WHERE rdf = %s """)

EnergyConsumerTable.SSH_feed_EC("""UPDATE EnergyConsumer SET P = %s, Q = %s WHERE rdf = %s """)

New_Message = 'Table EnergyConsumer Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



PowerTransformerEndTable.table_write_ID()
PowerTransformerEndTable.feed_PTE("""UPDATE PowerTransformerEnd SET name=%s, Transformer_r = %s,
    Transformer_x = %s,Transformer_b = %s,Transformer_g = %s, Transformer_rdf = %s , baseVoltage_rdf = %s, Terminal_rdf = %s, 
    ratedU = %s, ratedS = %s WHERE rdf = %s """)

New_Message = 'Table PowerTransformerEnd Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



BreakerTable.table_write_ID()
BreakerTable.feed_BR("""UPDATE Breaker SET name=%s, equipmentContainer_rdf = %s,
    baseVoltage_rdf = %s WHERE rdf = %s """)

BreakerTable.SSH_feed_BR("""UPDATE Breaker SET state = %s WHERE rdf = %s """)

New_Message = 'Table Breaker Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



RatioTapChangerTable.table_write_ID()
RatioTapChangerTable.feed_RTC("""UPDATE RatioTapChanger SET name=%s, TransformerEnd_rdf = %s  WHERE rdf = %s """)

RatioTapChangerTable.SSH_feed_RTC("""UPDATE RatioTapChanger SET step = %s WHERE rdf = %s """)

New_Message = 'Table RatioTapChanger Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



ACLineSegmentTable.table_write_ID()
ACLineSegmentTable.feed_ACL("""UPDATE ACLineSegment SET name=%s, ACLineSegment_r = %s,
    ACLineSegment_x = %s, ACLineSegment_bch = %s , ACLineSegment_gch = %s, 
        equipmentContainer_rdf = %s, baseVoltage_rdf = %s WHERE rdf = %s """)


New_Message = 'Table ACLineSegment Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



ConnectivityNodeTable.table_write_ID()
ConnectivityNodeTable.feed_CNN("""UPDATE ConnectivityNode SET name=%s, ConnectivityNodeContainer_rdf = %s
                 WHERE rdf = %s """)


New_Message = 'Table ConnectivityNode Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)



TerminalTable.table_write_ID()
TerminalTable.feed_TMN("""UPDATE Terminal SET name=%s, ConductingEquipment_rdf = %s,
             ConnectivityNode_rdf = %s  WHERE rdf = %s """)

TerminalTable.SSH_feed_TMN("""UPDATE Terminal SET ConnectCondition = %s WHERE rdf = %s """)

New_Message = 'Table Terminal Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)

BusbarSectionTable.table_write_ID()
BusbarSectionTable.feed_BBS("""UPDATE BusbarSection SET name=%s, equipmentContainer_rdf = %s  WHERE rdf = %s """)

New_Message = 'Table BusbarSection Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)


LinearShuntCompensatorTable.table_write_ID()
LinearShuntCompensatorTable.feed_LSC("""UPDATE LinearShuntCompensator SET name=%s, bPerSection = %s, 
            gPerSection = %s, nomU = %s ,equipmentContainer_rdf = %s  WHERE rdf = %s """)

LinearShuntCompensatorTable.SSH_feed_LSC("""UPDATE LinearShuntCompensator SET sections = %s WHERE rdf = %s """)


New_Message = 'Table LinearShuntCompensator Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)


New_Message = 'All Table Writen Succeed!'
Update_Status(New_Message, 'black')
time.sleep(0.2)

var_TabCheck.set('All Tables Written Succeeded!')
Stat_Para_TabCheck_create = {'bd':1,'anchor':W, 'fg':'#228B22'}
win.AddStatus(Stat_Para_TabCheck_create, TabCheckStructStatus, var_TabCheck.get())
win.root.update()
time.sleep(0.15)

conn.close()