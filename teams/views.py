from django.shortcuts import render ,redirect
import json as simplejson
from django.views.decorators.csrf import csrf_exempt  
from django.http import HttpResponse
from teams.models import TeamsInfo , CoachsInfo ,PlayersInfo , MatchesInfo , SponsorsInfo , Relationship_Sponsors_teams
from datetime import datetime,date
from django.db import connection
# Create your views here.


def insert_delete_update(sql):
    cursor = connection.cursor()
    '"'+sql+'"'
    cursor.execute(sql)
    #return 

def select(sql):
    dict_info={}
    #dict_teamsinfo={}
    #dict_coachsinfo={}
    #dict_playersinfo={}
    #dict_sponsorsinfo={}
    #dict_relationship={}

    cursor = connection.cursor()
    sql1=sql
    list=sql1.split(' ')
    from_index=list.index('FROM')
    if '*' not in list:
        '"'+sql+'"'
        cursor.execute(sql)
        raw=cursor.fetchall()

        attributes=list[1].split(',')
        att_len=len(attributes)
        dict={}
        list_l=[()]*att_len
        for i in attributes:
	for j in raw:
	    dict[i]=list_l[i].append(raw[j][i])

    elif '*' in list:
        if 'teams_matchesinfo' in list and 'teams_teamsinfo'  not in list  and\
         'teams_coachsinfo' not in list and 'teams_playersinfo' not in list  and \
         'teams_sponsorsinfo' not in list  and 'teams_relationship_Sponsors_teamsinfo' not in list:
        	'"'+sql+'"'
        	cursor.execute(sql)
        	raw=cursor.fetchall()
        	list_l1=[()]*5
        	for i in ['match_id','match_code','date_of_match','team_home_goals','team_away_goals']:
        	    for j in raw:
        	        dict_info[i]=list_l1[i].append(raw[j][i])

        if 'teams_teamsinfo' in list and 'teams_matchesinfo'  not in list  and\
         'teams_coachsinfo' not in list and 'teams_playersinfo' not in list  and \
         'teams_sponsorsinfo' not in list  and 'teams_relationship_Sponsors_teamsinfo' not in list:
        	'"'+sql+'"'
        	cursor.execute(sql)
        	raw=cursor.fetchall()
        	list_l1=[()]*4
        	for i in ['team_code','country_name','country_code','total_score']:
        	    for j in raw:
        	        dict_info[i]=list_l1[i].append(raw[j][i])


        if 'teams_coachsinfo' in list and 'teams_teamsinfo'  not in list  and\
         'teams_matchesinfo' not in list and 'teams_playersinfo' not in list  and \
         'teams_sponsorsinfo' not in list  and 'teams_relationship_Sponsors_teamsinfo' not in list:
        	'"'+sql+'"'
        	cursor.execute(sql)
        	raw=cursor.fetchall()
        	list_l1=[()]*5
        	for i in ['coach_code','coach_name','coach_birthday','coach_country','coach_team']:
        	    for j in raw:
        	        dict_info[i]=list_l1[i].append(raw[j][i])


        if 'teams_playersinfo' in list and 'teams_teamsinfo'  not in list  and\
         'teams_coachsinfo' not in list and 'teams_matchesinfo' not in list  and \
         'teams_sponsorsinfo' not in list  and 'teams_relationship_Sponsors_teamsinfo' not in list:
        	'"'+sql+'"'
        	cursor.execute(sql)
        	raw=cursor.fetchall()
        	list_l1=[()]*6
        	for i in ['player_name','player_code','player_loc','player_height','team','coach']:
        	    for j in raw:
        	        dict_info[i]=list_l1[i].append(raw[j][i])


        if 'teams_sponsorsinfo' in list and 'teams_teamsinfo'  not in list  and\
         'teams_coachsinfo' not in list and 'teams_playersinfo' not in list  and \
         'teams_matchesinfo' not in list  and 'teams_relationship_Sponsors_teamsinfo' not in list:
        	'"'+sql+'"'
        	cursor.execute(sql)
        	raw=cursor.fetchall()
        	list_l1=[()]*3
        	for i in ['sponsor_name','nasdaq','date_of_found']:
        	    for j in raw:
        	        dict_info[i]=list_l1[i].append(raw[j][i])

        if 'teams_relationship_Sponsors_teamsinfo' in list and 'teams_teamsinfo'  not in list  and\
         'teams_coachsinfo' not in list and 'teams_playersinfo' not in list  and \
         'teams_matchesinfo' not in list  and 'teams_matchesinfo' not in list:
        	'"'+sql+'"'
        	cursor.execute(sql)
        	raw=cursor.fetchall()
        	list_l1=[()]*3
        	for i in ['team','sponsor','date_of_sponsor']:
        	    for j in raw:
        	        dict_info[i]=list_l1[i].append(raw[j][i])



@csrf_exempt
def Query(request):
    
    try:
    	if request.method=='POST':
	    print request.POST
#get the querydict of post ------userdata
	    sql_get=str(request.POST.get('sql'))
	   # sql=eval(sql_get)
	    sql=sql_get.upper()

	    if  sql.find('INSERT')>= 0:
	    	insert_delete_update(sql)
	     	return HttpResponse('OK_IN')   
	    if  sql.find('DELETE')>= 0:
	    	insert_delete_update(sql)
	    	return HttpResponse('OK_DE') 
	    if  sql.find('UPDATE')>= 0:
	    	insert_delete_update(sql)
	    	return HttpResponse('OK_UP') 	    	
	    #print '"'+sql+'"'
	    #cursor = connection.cursor() 	
	    #cursor.execute(sql)
	    #raw=cursor.fetchall()
	    #print raw
	    #dic = {}
	    #dic[match_id]=raw[1]
	

	return HttpResponse('ok')



    except:
	print 'something wrong'
        
    return HttpResponse('ERROR')