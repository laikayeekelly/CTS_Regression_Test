## Project Title: 

CTS Regression Test


## 1. Purpose of this project: 

Develop a program that can generate the CTS Regression Test plan based on the failed test cases stated in the CTS Report.


## 2. Requirement Specification

### 2.1 Input

* CTS Report

The CTS Report is a XML document which is generated after the CTS test finished 

The file name for the CTS Report can be defined by the user when a XSLT processor is being used.

### 2.2 System Requirement

* XSLT Processor

Recommended XSLT Processor for Linux/MacOS : xsltproc

Recommended XSLT Processor for WindowsOS : Saxon

### 2.3 Output

* Regression Test Plan

The test plan is a XML document that contains some reference identifiers referencing to test package that contains the failed test cases stated in the input CTS report. The file name for the output test plan can be defined by user when a xslt processor is being used.


## 3. User's Guide

### 3.1 Installing xsltproc or Saxon

1. For Linux/MacOS, install xsltproc. For WindowsOS, install Saxon.

2. The installation step can be found from the webpage of the specific xslt processor developer

### 3.2 Run the regression test plan generating system

1. Run the xslt processor to generate the xml document of the regression test plan.

For xsltproc, the command should be 'xsltproc -o (output xml file name) regression.xsl (input xml file name)'

For Saxon on Java platform, the command should be 'java -jar saxon9he.jar -o (output xml file name) regression.xsl (input xml file name)'

### 3.3 Run CTS Regression Test

1.	Go to the directory for the CTS files

2.	Go to the folder ‘repository’

3.	Go to the folder ‘plans’ 

4.	Put the xml document outputted by the xslt processor into the folder ‘plans’

5.	Follow the steps for running the CTS Test, except the step for launching and run the cts plan, that is the step which requires the command ‘run cts –plan CTS ’. The command should be changed to ‘run cts –plan (filename of xml doc) ’


## 4. Repository Documents List

### 1.  regression.xsl

A xsl document which can be used to generate the regression test plan with the use of a xslt processor and the xml document of the CTS test report.

### 2.  regression_version1.py

A python document which is the source of the version one of the program. For the documentation for this version, please refer to the repository CTS_Regression_Test_Python.

### 3.  regression_version2.py

A python document which is the source of the version two of the program. For the documentation for this version, please refer to the repository CTS_Regression_Test_Python.
