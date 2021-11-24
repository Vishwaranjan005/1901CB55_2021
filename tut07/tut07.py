import os
import pandas as pd
import openpyxl
from openpyxl import load_workbook

def feedback_not_submitted():

	
	ltp_mapping_feedback_type = {1: 'lecture', 2: 'tutorial', 3:'practical'}
	output_file_name = "course_feedback_remaining.xlsx" 

	all_st_df = pd.read_csv('course_registered_by_all_students.csv')
	roll_col = all_st_df['rollno']
	roll_list=roll_col.drop_duplicates().values.tolist()

	subno_ltp_df=pd.read_csv('course_master_dont_open_in_excel.csv', usecols=['subno','ltp'])

	
	i=0
	ltp={}
	while(i< subno_ltp_df.shape[0] ):
		y=subno_ltp_df.subno[i]
		x=subno_ltp_df.ltp[i]
		nonzero= 3-x.count('0')
		ltp[y]=nonzero
		i+=1

	roll_subno= []
	for roll in roll_list:
		subno= all_st_df.loc[all_st_df['rollno']==roll]
		subno=subno['subno'].values.tolist()
		subno.insert(0,roll)
		roll_subno.append(subno)


	subm_roll_sub_df = pd.read_csv('course_feedback_submitted_by_students.csv')

	not_subm = []
	for k in roll_subno:
		for i in range(1,len(k)):
			df=subm_roll_sub_df[subm_roll_sub_df['stud_roll']==k[0]]
			bf=df[df['course_code']==k[i]]
			if( bf.shape[0]<ltp[k[i]]):
				not_subm.append([k[0],k[i]])


	st_info_df = pd.read_csv('studentinfo.csv',usecols=['Name', 'Roll No', 'email','aemail','contact'])
	not_subm_sheet=[]
	for i in range(0,len(not_subm)):
		x =not_subm[i][0]
		y=not_subm[i][1]

		kf=all_st_df[all_st_df['rollno']==not_subm[i][0]]
		kf=kf[kf['subno']==not_subm[i][1]]
		l=kf.iloc[0].values.tolist()
		l=l[:4]
		kf2=st_info_df[st_info_df['Roll No']==not_subm[i][0]]
		columns=kf2[['Name','email','aemail','contact']]
		new=columns.copy()
		if(new.shape[0]>0):
			m=new.iloc[0].values.tolist()
			l=l+m
		else:
			l=l+['nan','nan','nan','nan']
		not_subm_sheet.append(l)

	not_subm_sheet_df = pd.DataFrame(not_subm_sheet,columns=['rollno','register_sem','schedule_sem','subno','Name','email','aemail','contact'])
		
	not_subm_sheet_df.to_excel('course_feedback_remaining.xlsx',index=False)

feedback_not_submitted()
