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

1. Install xsltproc if Linux/MacOS is being used, install Saxon if WindowsOS is being used.

2. The installation step can be found from the webpage of specific xslt processor developer

### 3.2 Run the regression test plan generating system

1. Run the xslt processor document with the input of the xsl document (regression.xsl) and the xml document of the CTS Report. User should also specify the output file with the use of the command provided by specific xslt processor.

### 3.3 Run CTS Regression Test

1.	Go to the directory for the CTS files

2.	Go to the folder ‘repository’

3.	Go to the folder ‘plans’ 

4.	Put the xml document outputted by the xslt processor into the folder ‘plans’

5.	Follow the steps for running the CTS Test, except the step for launching and run the cts plan, that is the step which requires the command ‘run cts –plan CTS ’. The command should be changed to ‘run cts –plan (filename of xml doc) ’

## Documents List

### 1. regression.xsl
A xsl document which can be used to generate the regression test plan with the use of a xslt processor and the xml document of the CTS test report.