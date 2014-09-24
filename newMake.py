#!/usr/bin/python
#Generate MakeFile

import os
import sys
CFLAGS="-O3 -fPIC"
#CFLAGS="-rdynamic -g -FPIC"
CPP="g++ "
C="gcc "
MIDPATH='build/'

MAIN_PROGRAM=['libglsl.so', 'test.out', 'gputest.out', 'display.out']
gDepends = ['', 'libglsl.so','libglsl.so', 'libglsl.so']
gDirs = [['core', 'fragment', 'math', 'package', 'transform', 'utils', 'vertex', 'GL'], ['test'], ['gltest'], []]
gSrcFiles = [[], ['./main.cpp'], ['./opengltest_main.cpp'], ['./display_main.cpp']]
gLinks = [' -lfreeimage ', ' -lfreeimage ./libglsl.so -lGL -lGLEW',' -lfreeimage ./libglsl.so -lGLEW -lGL -lglut', ' -lfreeimage ./libglsl.so -lGLEW -lGL -lglut -lm -lX11']

def Generate_Output(outName, srcDirs, srcFiles, CLINK, depend):
	#Find all files
	include_h = []
	sources_cpp = []
	sources_c = []
	for dir in srcDirs:
		cmd = "find include/" + dir + " -name \"*.h\""
		include_h_temp = os.popen(cmd).read().split('\n');
		for f in include_h_temp:
			if len(f) > 0:
				include_h.append(f)
		cmd = "find src/" + dir + " -name \"*.cpp\""
		temp_cpp = os.popen(cmd).read().split('\n');
		for f in temp_cpp:
			if len(f) > 0:
				sources_cpp.append(f)
		cmd = "find src/" + dir + " -name \"*.c\""
		temp_c = os.popen(cmd).read().split('\n');
		for f in temp_c:
			if len(f) > 0:
				sources_c.append(f)
	for f in srcFiles:
		sources_cpp.append(f)
	fileContents = ""
	#Head Files
	include_Flag = '-Iinclude'
	include = "ALL_INCLUES"+outName
	fileContents += include+'='
	for h in include_h:
		if len(h)>0:
			fileContents+=(' '+h)
	fileContents+='\n'
	def getNameWithofO(fileName):
		pos = 0
		while fileName[pos]!='/':
			pos+=1
		sta = pos+1
		pos+=1
		while fileName[pos]!='.':
			pos+=1
		result = fileName[sta:pos].replace('/','_')
		return result+'.o'
	#All cpp c and .o
	objs = []
	sequences = []
	def getSequencesAndAppend(src, program):
		obj = getNameWithofO(src)
		objs.append(obj)
		sequence = MIDPATH + obj + ' : ' + src + ' ${'+include + '}\n'
		sequence += '\t' + program + CFLAGS + ' -o ' + MIDPATH + obj + ' -c ' + src + ' '+include_Flag+' \n'
		sequences.append(sequence)
	for cpp in sources_cpp:
		if len(cpp)>0:
			getSequencesAndAppend(cpp, CPP)
	for c in sources_c:
		if len(c)>0:
			getSequencesAndAppend(c, C)
	fileContents+='\n'
	main = outName
	#objs
	fileContents += (main + ': ')
	for obj in objs:
		fileContents+=' '+MIDPATH+obj
	fileContents+= ' ' + depend
	fileContents+='\n'
	#Program
	target = ''
	if (main.find('.so')>-1):
		target = ' --share '
	fileContents+=('\t' + CPP + " " + CFLAGS +target+' -o ' + main+' ')
	for obj in objs:
		fileContents+=(' '+MIDPATH+obj)
	fileContents+=(' '+ CLINK  + ' ${SELF_VARIABLES}' + '\n')
	#All objs' make 
	for sequence in sequences:
		fileContents+=sequence
	return fileContents

files = 'all:'

for program in MAIN_PROGRAM:
	files+= (program + ' ')
files+='\n'

for i in range(0, len(gSrcFiles)):
	files+='\n'
	files+= Generate_Output(MAIN_PROGRAM[i], gDirs[i], gSrcFiles[i], gLinks[i], gDepends[i])

#clean
files+='\nclean:\n\trm '+MIDPATH+'*.o'
for main in MAIN_PROGRAM:
	files+='\n\trm '+main

makeFile = open('Makefile','w')
makeFile.write(files)

makeFile.close();
