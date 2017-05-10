***** This project is finished by Zhenmin Tao (Zhenmin@kth.se) and Mian Xiong(mxiong@kth.se) *****

***** Before running the program, you need to create a database called '5Bus' in your MySQL Server *****

***** The environment is Python 2.7 *****

***** MySQLdb downloading address https://sourceforge.net/projects/mysql-python/ ********
***** MySQLdb The version I used is : MySQL-python-1.2.4b4.win32-py2.7 *******


***** Brief introduction of each file: *****
1.SearchFile.py
  Find all the elements and catogorize them by their tag name, then put them into dictionary and use their name as key.

2.BaseClass.py
  Contains all the basic method of parsing the XML file and creating tables in database

3.DBOperateClass.py
  Contains all the method that is used to parse one specific node and write the node into tables

4.Find_Feed.py
  Based on the above 3 files, parse all the information, create tables and write the file into database.

5.Graph.py
  An algorithm to find the route and conducting equipment between two busbarsections.

6.Build_YMatrix.py
  Read all the necessary data from database and build some dictionaries, based on the graph algorithm to find the route and then calculate the admittance between each two of the buses.

7.GUI_Class.py
  A class for GUI window frame.


*****Please contact us if you met any problem******



