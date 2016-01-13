from django.shortcuts import render, redirect
import json as simplejson
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from teams.models import TeamsInfo, CoachsInfo, PlayersInfo, MatchesInfo, SponsorsInfo, Relationship_Sponsors_teams
from datetime import datetime, date
from django.db import connection
import numpy as np
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
# Create your views here.


def insert_delete_update(sql):
    try:
        if "INSERT" in sql:
            query_id = 1
        elif "DELETE" in sql:
            query_id = 2
        elif "UPDATE" in sql:
            query_id = 3
        cursor = connection.cursor()
        '"' + sql + '"'
        cursor.execute(sql)
        rows_count = cursor.rowcount
        return rows_count, query_id
    except:
        query_id = 5
        rows_count = 0
        return rows_count, query_id


def select_query(sql):
    print sql
    cursor = connection.cursor()
    '"' + sql + '"'
    print sql
    cursor.execute(sql)
    rows = cursor.fetchall()
    rows.sort()
    rows_count = cursor.rowcount
    print rows, type(rows)
    desc = cursor.description
    print desc
    # print rows
    array_shape = np.array(desc).shape
    # print array_shape
    attr_len = array_shape[0]
    # print rows_count
    dict_attr = {}
    attributes = []
  #  if rows_count > 0:
    for i in range(attr_len):
        attributes.append(desc[i][0])
    # print attributes
    L = []
    for i in range(attr_len):
        L.append([])
    # print L,L[0]
    if rows_count > 0:
        for row in rows:
            for i in range(attr_len):
                L[i].append(row[i])
                dict_attr[attributes[i]] = L[i]
                # print dict_attr
    else:
        for i in range(attr_len):
            dict_attr[attributes[i]] = L[i]
        print dict_attr

    print dict_attr.items()
    return dict_attr, attributes, rows, rows_count


@csrf_exempt
def Query(request):
    try:
        if request.method == 'POST':
            print request.POST
            sql_get = str(request.POST.get('sql'))

            sql = sql_get.upper()
            print sql_get
            query_id = 0
            rows_act = 0
            if "INSERT" in sql:
                rows_act, query_id = insert_delete_update(sql)
                print rows_act
                # a=insert_delete_update(sql)
                # query_id = 1
                context = {'query_id': query_id, 'rows_act': rows_act}
 #               print context
 #               return render(request, 'teams/query.html', context)
            elif "DELETE" in sql:
                rows_act, query_id = insert_delete_update(sql)
                # query_id = 2
                context = {'query_id': query_id, 'rows_act': rows_act}
#                print context
#                return render(request, 'teams/query.html', context)
            elif "UPDATE" in sql:
                rows_act, query_id = insert_delete_update(sql)
                # query_id = 3
                context = {'query_id': query_id, 'rows_act': rows_act}
 #               print context
#                return render(request, 'teams/query.html', context)
            elif "SELECT" in sql:
                sel_mode, attributes, rows, rows_count = select_query(sql)
                print attributes
                query_id = 4
                # col_name = []
                # col_value = []
                print sel_mode, len(sel_mode)
                # for k,v in
                context = {'dict_attr': sel_mode, 'query_id': query_id,
                           'attributes': attributes, 'rows_act': rows_count, 'rows': rows}
#                print context
            else:
                context = {'query_id': query_id, 'rows_act': rows_act}
            print context
        return render(request, 'teams/query.html', context)
    except:
        print 'something wrong'
        query_id = 5
        rows_act = 5
 #       context = {'query_id': query_id, 'rows_act': rows_act}
#        print context
    return render(request, 'teams/query.html')


def Hello(request):
    return render(request, 'teams/index.html')


@csrf_exempt
def Match(request):
    try:
        if request.method == 'POST':
            print request.POST
            match_id_s = request.POST.get('match_id_s')
            match_code_s = request.POST.get('match_code_s')
            team_home_goals_s = request.POST.get('team_home_goals_s')
            team_away_goals_s = request.POST.get('team_away_goals_s')

            match_id_d = request.POST.get('match_id_d')
            match_code_d = request.POST.get('match_code_d')
            team_home_goals_d = request.POST.get('team_home_goals_d')
            team_away_goals_d = request.POST.get('team_away_goals_d')

            match_id_u = request.POST.get('match_id_u')
            match_code_u = request.POST.get('match_code_u')
            team_home_goals_u = request.POST.get('team_home_goals_u')
            team_away_goals_u = request.POST.get('team_away_goals_u')

            textinput = str(request.POST.get('textinput'))

            #match_id_new = request.POST.get('id_new')
            match_code_new = request.POST.get('code_new')
            team_home_goals_new = request.POST.get('home_goals_new')
            team_away_goals_new = request.POST.get('away_goals_new')

            # , match_id_new, type(match_id_new)
            print match_id_s, type(match_id_s), match_id_d, type(match_id_d), match_id_u, type(match_id_u)
            print match_code_s, type(match_code_s), match_code_d, type(match_code_d), match_code_u, type(match_code_u), match_code_new, type(match_code_new)
            print team_home_goals_s, type(team_home_goals_s), team_home_goals_d, type(team_home_goals_d), team_home_goals_u, type(team_home_goals_u), team_home_goals_new, type(team_home_goals_new)
            print team_away_goals_s, type(team_away_goals_s), team_away_goals_d, type(team_away_goals_d), team_away_goals_u, type(team_away_goals_u), team_away_goals_new, type(team_away_goals_new)
            print textinput, type(textinput)

            error_code = 0  # 0 errors
            count_m = 0
            del_num = 0
            up_num = 0
            if match_id_s is not None:
                action_code = 1
                if "*"in match_id_s:
                    print 'ok'
                    match = MatchesInfo.objects.all()
                    # print match
                    count_m = match.count()
                elif match_id_s == '':
                    error_code = 1  # no data in
                    match = []  # maybe raise error laterly
                else:
                    match_s_filter = MatchesInfo.objects.filter(
                        match_id=match_id_s)
                    count_m = match_s_filter.count()
                    # print count_m
                    if count_m > 0:
                        match = match_s_filter
                    else:
                        error_code = 2  # nothing filtered
                        match = match_s_filter
                context = {'match': match, 'count_m': count_m,
                           'error_code': error_code, 'action_code': action_code}
                # print match
            elif match_code_s is not None:
                action_code = 1
                Match_code_s = match_code_s.upper()
                len_code_s = len(match_code_s)
                # print len_code_s
                if match_code_s == '':
                    error_code = 1  # no data in
                    match_s_filter = MatchesInfo.objects.filter(
                        match_code=Match_code_s)
                    # print match_s_filter
                    match = match_s_filter

                elif len_code_s > 4:
                    error_code = 3  # exceed the default length
                    # print error_code
                    match = []  # maybe raise error laterly

                elif len_code_s == 4:
                    match_s_filter = MatchesInfo.objects.filter(
                        match_code=Match_code_s)
                    count_m = match_s_filter.count()
                    match = match_s_filter
                    # print match_s_filter, count_m
                else:
                    error_code = 4  # shorter than the default length
                    # print error_code
                    match = []  # maybe raise error laterly
                context = {'match': match, 'count_m': count_m,
                           'error_code': error_code, 'action_code': action_code}

            elif team_home_goals_s is not None:
                action_code = 1
                if team_home_goals_s == '':
                    error_code = 1  # no data in
                    match = []  # maybe raise error laterly
                else:
                    team_home_goals_s_filter = MatchesInfo.objects.filter(
                        team_home_goals=team_home_goals_s)
                    # print team_home_goals_s_filter
                    match = team_home_goals_s_filter
                    count_m = match.count()
                context = {'match': match, 'count_m': count_m,
                           'error_code': error_code, 'action_code': action_code}

            elif team_away_goals_s is not None:
                action_code = 1
                if team_away_goals_s == '':
                    error_code = 1  # no data in
                    match = []  # maybe raise error laterly
                else:
                    team_away_goals_s_filter = MatchesInfo.objects.filter(
                        team_away_goals=team_away_goals_s)
                    print team_away_goals_s_filter
                    match = team_away_goals_s_filter
                    count_m = match.count()
                context = {'match': match, 'count_m': count_m,
                           'error_code': error_code, 'action_code': action_code}

            elif match_id_d is not None:
                action_code = 2
                if "*"in match_id_d:
                    print 'ok'
                    match = MatchesInfo.objects.all()
                    del_tuple = match.delete()
                    del_num = del_tuple[0]
                    # print del_tuple,del_num
                elif match_id_d == '':
                    error_code = 1  # no data in
                else:
                    match_d_filter = MatchesInfo.objects.filter(
                        match_id=match_id_d)
                    del_tuple = match_d_filter.delete()
                    del_num = del_tuple[0]
                    # print del_tuple, del_num
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}
            elif match_code_d is not None:
                action_code = 2
                Match_code_d = match_code_d.upper()
                len_code_d = len(match_code_d)
                # print len_code_s
                if match_code_d == '':
                    error_code = 1  # no data in
                    match_d_filter = MatchesInfo.objects.filter(
                        match_code=Match_code_d)
                    # print match_s_filter
                    match = match_d_filter
                    del_tuple = match.delete()
                    del_num = del_tuple[0]
                    print del_tuple, del_num
                elif len_code_d > 4:
                    error_code = 3  # exceed the default length
                    # print error_code
                elif len_code_d == 4:
                    match_d_filter = MatchesInfo.objects.filter(
                        match_code=Match_code_d)
                    match = match_d_filter
                    # print match_s_filter
                    del_tuple = match.delete()
                    del_num = del_tuple[0]
                    # print del_tuple, del_num
                else:
                    error_code = 4  # shorter than the default length
                    # print error_code
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}

            elif team_home_goals_d is not None:
                action_code = 2
                if team_home_goals_d == '':
                    error_code = 1  # no data in

                else:
                    team_home_goals_d_filter = MatchesInfo.objects.filter(
                        team_home_goals=team_home_goals_d)
                    # print team_home_goals_s_filter
                    match = team_home_goals_d_filter
                    del_tuple = match.delete()
                    del_num = del_tuple[0]
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}

            elif team_away_goals_d is not None:
                action_code = 2
                if team_away_goals_d == '':
                    error_code = 1  # no data in

                else:
                    team_away_goals_d_filter = MatchesInfo.objects.filter(
                        team_away_goals=team_away_goals_d)
                    match = team_away_goals_d_filter
                    del_tuple = match.delete()
                    del_num = del_tuple[0]
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}

            elif match_id_u is not None:
                action_code = 3
                # print action_code
                if match_id_u == '':
                    error_code = 1  # no data in

                else:
                    match_u_filter = MatchesInfo.objects.filter(
                        match_id=match_id_u)

                    if match_code_new is not None:
                        Match_code_new = match_code_new.upper()
                        len_code_new = len(Match_code_new)
                        if len_code_new > 4:
                            error_code = 33  # set a exceed the  length
                        elif len_code_new == 4:
                            match_u = match_u_filter.update(
                                match_code=Match_code_new)
                            up_num = match_u
                        else:
                            error_code = 44  # set a shorter value than the default length

                    elif team_home_goals_new is not None:
                        # print team_home_goals_new
                        if team_home_goals_new == '':
                            error_code = 11  # no new data in
                            # print error_code
                        else:
                            match_u = match_u_filter.update(
                                team_home_goals=team_home_goals_new)
                            up_num = match_u
                    elif team_away_goals_new is not None:
                        if team_away_goals_new == '':
                            error_code = 11  # no new data in
                        else:
                            match_u = match_u_filter.update(
                                team_away_goals=team_away_goals_new)
                            up_num = match_u
                context = {
                    'error_code': error_code, 'action_code': action_code, 'up_num': up_num}

            elif match_code_u is not None:
                action_code = 3
                Match_code_u = match_code_u.upper()
                len_code_u = len(match_code_u)
                print len_code_u

                if match_code_u == '':
                    error_code = 1  # no data in
                elif len_code_u > 4:
                    error_code = 3  # exceed the default length
                    # print error_code
                elif len_code_u == 4:
                    match_u_filter = MatchesInfo.objects.filter(
                        match_code=Match_code_u)
                    print match_u_filter

                    if match_code_new is not None:
                        Match_code_new = match_code_new.upper()
                        len_code_new = len(Match_code_new)
                        # print len_code_u, len_code_new
                        if len_code_new > 4:
                            error_code = 33  # set a exceed the  length
                        elif len_code_new == 4:
                            match_u = match_u_filter.update(
                                match_code=Match_code_new)
                        else:
                            error_code = 44  # set a shorter value than the default length

                    elif team_home_goals_new is not None:
                        print team_home_goals_new
                        if team_home_goals_new == '':
                            error_code = 11  # no new data in
                            # print error_code
                        else:
                            match_u = match_u_filter.update(
                                team_home_goals=team_home_goals_new)
                            up_num = match_u
                    elif team_away_goals_new is not None:
                        if team_away_goals_new == '':
                            error_code = 11  # no new data in
                        else:
                            match_u = match_u_filter.update(
                                team_away_goals=team_away_goals_new)
                            up_num = match_u
                else:
                    error_code = 4  # shorter than the default length
                    # print error_code
                context = {
                    'error_code': error_code, 'action_code': action_code, 'up_num': up_num}

            elif textinput is not None:
                action_code = 4
                in_num = 0
                text_list = textinput.strip().split('&')
                if len(text_list) == 4:
                    match_id = int(text_list[0])
                    match_code = text_list[1].upper()
                    team_home_goals = int(text_list[2])
                    team_away_goals = int(text_list[3])
                    print match_id, match_code, team_home_goals, team_away_goals

                    try:
                        match, created = MatchesInfo.objects. get_or_create(
                            match_id=match_id, match_code=match_code, team_home_goals=team_home_goals, team_away_goals=team_away_goals)
                        # print match,type(match)
                    except:
                        created = False
                    if created == True:
                        in_num = 1
                    else:
                        in_num = 0
                        error_code = 5  # already have
                else:
                    error_code = 6
                context = {'in_num': in_num,
                           'error_code': error_code, 'action_code': action_code}

            print context
        return render(request, 'teams/transaction-m.html', context)

    except:
        print 'something wrong'

        return render(request, 'teams/transaction-m.html')


@csrf_exempt
def Team(request):
    try:
        if request.method == 'POST':
            print request.POST
            team_code_s = request.POST.get('team_code_s')
            country_name_s = request.POST.get('country_name_s')
            country_code_s = request.POST.get('country_code_s')
            total_score_s = request.POST.get('total_score_s')
            #m_id_s = request.POST.get('m_id_s')

            team_code_d = request.POST.get('team_code_d')
            country_name_d = request.POST.get('country_name_d')
            country_code_d = request.POST.get('country_code_d')
            total_score_d = request.POST.get('total_score_d')
           # m_id_d = request.POST.get('m_id_d')

            team_code_u = request.POST.get('team_code_u')
            country_name_u = request.POST.get('country_name_u')
            country_code_u = request.POST.get('country_code_u')
            total_score_u = request.POST.get('total_score_u')
         #   m_id_u = request.POST.get('m_id_u')

            textinput = str(request.POST.get('textinput'))

            team_code_new = request.POST.get('team_code_new')
            country_name_new = request.POST.get('country_name_new')
            country_code_new = request.POST.get('country_code_new')
            total_score_new = request.POST.get('total_score_new')
          #  m_id_new = request.POST.get('m_id_new')

            print team_code_s, type(team_code_s), team_code_d, type(team_code_d), team_code_u, type(team_code_u)
            print country_name_s, type(country_name_s), country_name_d, type(country_name_d), country_name_u, type(country_name_u), country_name_new, type(country_name_new)
            print country_code_s, type(country_code_s), country_code_d, type(country_code_d), country_code_u, type(country_code_u), country_code_new, type(country_code_new)
            print total_score_s, type(total_score_s), total_score_d, type(total_score_d), total_score_u, type(total_score_u), total_score_new, type(total_score_new)
     # print m_id_s, type(m_id_s), m_id_d, type(m_id_d), m_id_u, type(m_id_u),
     # m_id_new, type(m_id_new)

            print textinput, type(textinput)

            error_code = 0  # 0 errors
            count_t = 0
            del_num = 0
            up_num = 0
            if team_code_s is not None:
                action_code = 1
                if "*"in team_code_s:
                    print 'ok'
                    team = TeamsInfo.objects.all()
                    # print team
                    count_t = team.count()
                elif team_code_s == '':
                    error_code = 1  # no data in
                    team = []  # maybe raise error laterly
                else:
                    team_s_filter = TeamsInfo.objects.filter(
                        team_code=team_code_s)
                    count_t = team_s_filter.count()
                    # print count_t
                    if count_t > 0:
                        team = team_s_filter
                    else:
                        error_code = 2  # nothing filtered
                        team = team_s_filter
                context = {'team': team, 'count_t': count_t,
                           'error_code': error_code, 'action_code': action_code}
                # print team
            elif country_name_s is not None:
                action_code = 1
                Country_name_s = country_name_s.upper()
                len_code_s = len(country_name_s)
                # print len_code_s
                if country_name_s == '':
                    error_code = 1  # no data in
                    team_s_filter = TeamsInfo.objects.filter(
                        country_name=Country_name_s)
                    # print team_s_filter
                    team = team_s_filter

                elif len_code_s > 2:
                    error_code = 3  # exceed the default length
                    # print error_code
                    team = []  # maybe raise error laterly

                elif len_code_s == 2:
                    team_s_filter = TeamsInfo.objects.filter(
                        country_name=Country_name_s)
                    count_t = team_s_filter.count()
                    team = team_s_filter
                    print team_s_filter, count_t
                else:
                    error_code = 4  # shorter than the default length
                    # print error_code
                    team = []  # maybe raise error laterly
                context = {'team': team, 'count_t': count_t,
                           'error_code': error_code, 'action_code': action_code}

            elif country_code_s is not None:
                action_code = 1
                if country_code_s == '':
                    error_code = 1  # no data in
                    team = []  # maybe raise error laterly
                else:
                    country_code_s_filter = TeamsInfo.objects.filter(
                        country_code=country_code_s)
                    # print country_code_s_filter
                    team = country_code_s_filter
                    count_t = team.count()
                context = {'team': team, 'count_t': count_t,
                           'error_code': error_code, 'action_code': action_code}

            elif total_score_s is not None:
                action_code = 1
                if total_score_s == '':
                    error_code = 1  # no data in
                    team = []  # maybe raise error laterly
                else:
                    total_score_s_filter = TeamsInfo.objects.filter(
                        total_score=total_score_s)
                    print total_score_s_filter
                    team = total_score_s_filter
                    count_t = team.count()
                context = {'team': team, 'count_t': count_t,
                           'error_code': error_code, 'action_code': action_code}

            elif team_code_d is not None:
                action_code = 2
                if "*"in team_code_d:
                    print 'ok'
                    team = TeamsInfo.objects.all()
                    del_tuple = team.delete()
                    del_num = del_tuple[0]
                    # print del_tuple,del_num
                elif team_code_d == '':
                    error_code = 1  # no data in
                else:
                    team_d_filter = TeamsInfo.objects.filter(
                        team_code=team_code_d)
                    del_tuple = team_d_filter.delete()
                    del_num = del_tuple[0]
                    # print del_tuple, del_num
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}
            elif country_name_d is not None:
                action_code = 2
                Country_name_d = country_name_d.upper()
                len_code_d = len(country_name_d)
                # print len_code_s
                if country_name_d == '':
                    error_code = 1  # no data in
                    team_d_filter = TeamsInfo.objects.filter(
                        country_name=Country_name_d)
                    # print team_s_filter
                    team = team_d_filter
                    del_tuple = team.delete()
                    del_num = del_tuple[0]
                    print del_tuple, del_num
                elif len_code_d > 2:
                    error_code = 3  # exceed the default length
                    # print error_code
                elif len_code_d == 2:
                    team_d_filter = TeamsInfo.objects.filter(
                        country_name=Country_name_d)
                    team = team_d_filter
                    # print team_s_filter
                    del_tuple = team.delete()
                    del_num = del_tuple[0]
                    # print del_tuple, del_num
                else:
                    error_code = 4  # shorter than the default length
                    # print error_code
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}

            elif country_code_d is not None:
                action_code = 2
                if country_code_d == '':
                    error_code = 1  # no data in

                else:
                    country_code_d_filter = TeamsInfo.objects.filter(
                        country_code=country_code_d)
                    # print country_code_s_filter
                    team = country_code_d_filter
                    del_tuple = team.delete()
                    del_num = del_tuple[0]
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}

            elif total_score_d is not None:
                action_code = 2
                if total_score_d == '':
                    error_code = 1  # no data in

                else:
                    total_score_d_filter = TeamsInfo.objects.filter(
                        total_score=total_score_d)
                    team = total_score_d_filter
                    del_tuple = team.delete()
                    del_num = del_tuple[0]
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}

            elif team_code_u is not None:
                action_code = 3
                # print action_code
                if team_code_u == '':
                    error_code = 1  # no data in

                else:
                    team_u_filter = TeamsInfo.objects.filter(
                        team_code=team_code_u)
                    print team_u_filter

                    if country_name_new is not None:
                        Country_name_new = country_name_new.upper()
                        len_code_new = len(Country_name_new)
                        print country_name_new, len_code_new
                        if len_code_new > 2:
                            error_code = 33  # set a exceed the  length
                        elif len_code_new == 2:
                            team_u = team_u_filter.update(
                                country_name=Country_name_new)
                            up_num = team_u
                        else:
                            error_code = 44  # set a shorter value than the default length

                    elif country_code_new is not None:
                        # print country_code_new
                        if country_code_new == '':
                            error_code = 11  # no new data in
                            # print error_code
                        else:
                            team_u = team_u_filter.update(
                                country_code=country_code_new)
                            up_num = team_u
                    elif total_score_new is not None:
                        if total_score_new == '':
                            error_code = 11  # no new data in
                        else:
                            team_u = team_u_filter.update(
                                total_score=total_score_new)
                            up_num = team_u
                context = {
                    'error_code': error_code, 'action_code': action_code, 'up_num': up_num}

            elif country_name_u is not None:
                action_code = 3
                Country_name_u = country_name_u.upper()
                len_code_u = len(country_name_u)
                print len_code_u

                if country_name_u == '':
                    error_code = 1  # no data in
                elif len_code_u > 2:
                    error_code = 3  # exceed the default length
                    # print error_code
                elif len_code_u == 2:
                    team_u_filter = TeamsInfo.objects.filter(
                        country_name=Country_name_u)
                    print team_u_filter

                    if country_name_new is not None:
                        Country_name_new = country_name_new.upper()
                        len_code_new = len(Country_name_new)
                        # print len_code_u, len_code_new
                        if len_code_new > 2:
                            error_code = 33  # set a exceed the  length
                        elif len_code_new == 2:
                            team_u = team_u_filter.update(
                                country_name=Country_name_new)
                        else:
                            error_code = 44  # set a shorter value than the default length

                    elif country_code_new is not None:
                        print country_code_new
                        if country_code_new == '':
                            error_code = 11  # no new data in
                            # print error_code
                        else:
                            team_u = team_u_filter.update(
                                country_code=country_code_new)
                            up_num = team_u
                    elif total_score_new is not None:
                        if total_score_new == '':
                            error_code = 11  # no new data in
                        else:
                            team_u = team_u_filter.update(
                                total_score=total_score_new)
                            print total_score_new
                            up_num = team_u
                else:
                    error_code = 4  # shorter than the default length
                    # print error_code
                context = {
                    'error_code': error_code, 'action_code': action_code, 'up_num': up_num}

            elif textinput is not None:
                action_code = 4
                in_num = 0
                text_list = textinput.strip().split('&')
                if len(text_list) == 5:
                    team_code = int(text_list[0])
                    country_name = text_list[1].upper()
                    country_code = int(text_list[2])
                    total_score = int(text_list[3])
                    m_id = int(text_list[4])
                    print team_code, country_name, country_code, total_score, m_id
                    if len(country_name) > 2:
                        error_code = 3  # exceed the default length
                    elif len(country_name) < 2:
                        error_code = 4  # shorter
                    else:
                        try:
                            team, created = TeamsInfo.objects. get_or_create(
                                team_code=team_code, country_name=country_name, country_code=country_code, total_score=total_score, m_id=m_id)
                            # print team,type(team)
                        except:
                            created = False
                        if created == True:
                            in_num = 1
                        else:
                            in_num = 0
                            error_code = 5  # already have
                else:
                    error_code = 6  # input wrong
                context = {'in_num': in_num,
                           'error_code': error_code, 'action_code': action_code}

            print context
        return render(request, 'teams/transaction-t.html', context)

    except:
        print 'something wrong'

        return render(request, 'teams/transaction-t.html')


@csrf_exempt
def Player(request):
    try:
        if request.method == 'POST':
            print request.POST
            player_code_s = request.POST.get('player_code_s')
            player_name_s = request.POST.get('player_name_s')
            player_loc_s = request.POST.get('player_loc_s')
            player_height_s = request.POST.get('player_height_s')
            #team_id_s = request.POST.get('team_id_s')
           # co_id_s = request.POST.get('co_id_s')

            player_code_d = request.POST.get('player_code_d')
            player_name_d = request.POST.get('player_name_d')
            player_loc_d = request.POST.get('player_loc_d')
            player_height_d = request.POST.get('player_height_d')
            #team_id_d = request.POST.get('team_id_d')
            #co_id_s = request.POST.get('co_id_s')

            player_code_u = request.POST.get('player_code_u')
            player_name_u = request.POST.get('player_name_u')
            player_loc_u = request.POST.get('player_loc_u')
            player_height_u = request.POST.get('player_height_u')
           # team_id_u = request.POST.get('team_id_u')
            #co_id_s = request.POST.get('co_id_s')

            textinput = str(request.POST.get('textinput'))

            player_code_new = request.POST.get('player_code_new')
            player_name_new = request.POST.get('player_name_new')
            player_loc_new = request.POST.get('player_loc_new')
            player_height_new = request.POST.get('player_height_new ')
            #team_id_new = request.POST.get('team_id_new')

            print player_code_s, type(player_code_s), player_code_d, type(player_code_d), player_code_u, type(player_code_u)
            print player_name_s, type(player_name_s), player_name_d, type(player_name_d), player_name_u, type(player_name_u), player_name_new, type(player_name_new)
            print player_loc_s, type(player_loc_s), player_loc_d, type(player_loc_d), player_loc_u, type(player_loc_u), player_loc_new, type(player_loc_new)
            print player_height_s, type(player_height_s), player_height_d, type(player_height_d), player_height_u, type(player_height_u), player_height_new, type(player_height_new)
            # print team_id_s, type(team_id_s), team_id_d, type(team_id_d),
            # team_id_u, type(team_id_u), team_id_new, type(team_id_new)

            print textinput, type(textinput)

            error_code = 0  # 0 errors
            count_p = 0
            del_num = 0
            up_num = 0
            if player_code_s is not None:
                action_code = 1
                if "*"in player_code_s:
                    print 'ok'
                    player = PlayersInfo.objects.all()
                    # print player
                    count_p = player.count()
                elif player_code_s == '':
                    error_code = 1  # no data in
                    player = []  # maybe raise error laterly
                else:
                    player_s_filter = PlayersInfo.objects.filter(
                        player_code=player_code_s)
                    count_p = player_s_filter.count()
                    # print count_p
                    if count_p > 0:
                        player = player_s_filter
                    else:
                        error_code = 2  # nothing filtered
                        player = player_s_filter
                context = {'player': player, 'count_p': count_p,
                           'error_code': error_code, 'action_code': action_code}
                # print player
            elif player_name_s is not None:
                action_code = 1
                Player_name_s = player_name_s.upper()
                len_code_s = len(player_name_s)
                # print len_code_s
                if player_name_s == '':
                    error_code = 1  # no data in
                    player_s_filter = PlayersInfo.objects.filter(
                        player_name=Player_name_s)
                    # print player_s_filter
                    player = player_s_filter

                elif len_code_s > 4:
                    error_code = 3  # exceed the default length
                    # print error_code
                    player = []  # maybe raise error laterly

                elif len_code_s == 4:
                    player_s_filter = PlayersInfo.objects.filter(
                        player_name=Player_name_s)
                    count_p = player_s_filter.count()
                    player = player_s_filter
                    # print player_s_filter, count_p
                else:
                    error_code = 4  # shorter than the default length
                    # print error_code
                    player = []  # maybe raise error laterly
                context = {'player': player, 'count_p': count_p,
                           'error_code': error_code, 'action_code': action_code}

            elif player_loc_s is not None:
                action_code = 1
                if player_loc_s == '':
                    error_code = 1  # no data in
                    player = []  # maybe raise error laterly
                else:
                    player_loc_s_filter = PlayersInfo.objects.filter(
                        player_loc=player_loc_s)
                    # print player_loc_s_filter
                    player = player_loc_s_filter
                    count_p = player.count()
                context = {'player': player, 'count_p': count_p,
                           'error_code': error_code, 'action_code': action_code}

            elif player_height_s is not None:
                action_code = 1
                if player_height_s == '':
                    error_code = 1  # no data in
                    player = []  # maybe raise error laterly
                else:
                    player_height_s_filter = PlayersInfo.objects.filter(
                        player_height=player_height_s)
                    print player_height_s_filter
                    player = player_height_s_filter
                    count_p = player.count()
                context = {'player': player, 'count_p': count_p,
                           'error_code': error_code, 'action_code': action_code}

            elif player_code_d is not None:
                action_code = 2
                if "*"in player_code_d:
                    print 'ok'
                    player = PlayersInfo.objects.all()
                    del_tuple = player.delete()
                    del_num = del_tuple[0]
                    # print del_tuple,del_num
                elif player_code_d == '':
                    error_code = 1  # no data in
                else:
                    player_d_filter = PlayersInfo.objects.filter(
                        player_code=player_code_d)
                    del_tuple = player_d_filter.delete()
                    del_num = del_tuple[0]
                    # print del_tuple, del_num
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}
            elif player_name_d is not None:
                action_code = 2
                Player_name_d = player_name_d.upper()
                len_code_d = len(player_name_d)
                # print len_code_s
                if player_name_d == '':
                    error_code = 1  # no data in
                    player_d_filter = PlayersInfo.objects.filter(
                        player_name=Player_name_d)
                    # print player_s_filter
                    player = player_d_filter
                    del_tuple = player.delete()
                    del_num = del_tuple[0]
                    print del_tuple, del_num
                elif len_code_d > 4:
                    error_code = 3  # exceed the default length
                    # print error_code
                elif len_code_d == 4:
                    player_d_filter = PlayersInfo.objects.filter(
                        player_name=Player_name_d)
                    player = player_d_filter
                    # print player_s_filter
                    del_tuple = player.delete()
                    del_num = del_tuple[0]
                    # print del_tuple, del_num
                else:
                    error_code = 4  # shorter than the default length
                    # print error_code
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}

            elif player_loc_d is not None:
                action_code = 2
                if player_loc_d == '':
                    error_code = 1  # no data in

                else:
                    player_loc_d_filter = PlayersInfo.objects.filter(
                        player_loc=player_loc_d)
                    # print player_loc_s_filter
                    player = player_loc_d_filter
                    del_tuple = player.delete()
                    del_num = del_tuple[0]
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}

            elif player_height_d is not None:
                action_code = 2
                if player_height_d == '':
                    error_code = 1  # no data in

                else:
                    player_height_d_filter = PlayersInfo.objects.filter(
                        player_height=player_height_d)
                    player = player_height_d_filter
                    del_tuple = player.delete()
                    del_num = del_tuple[0]
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}

            elif player_code_u is not None:
                action_code = 3
                # print action_code
                if player_code_u == '':
                    error_code = 1  # no data in

                else:
                    player_u_filter = PlayersInfo.objects.filter(
                        player_code=player_code_u)

                    if player_name_new is not None:
                        Player_name_new = player_name_new.upper()
                        len_code_new = len(Player_name_new)
                        if len_code_new > 4:
                            error_code = 33  # set a exceed the  length
                        elif len_code_new == 4:
                            player_u = player_u_filter.update(
                                player_name=Player_name_new)
                            up_num = player_u
                        else:
                            error_code = 44  # set a shorter value than the default length

                    elif player_loc_new is not None:
                        # print player_loc_new
                        if player_loc_new == '':
                            error_code = 11  # no new data in
                            # print error_code
                        else:
                            player_u = player_u_filter.update(
                                player_loc=player_loc_new)
                            up_num = player_u
                    elif player_height_new is not None:
                        if player_height_new == '':
                            error_code = 11  # no new data in
                        else:
                            player_u = player_u_filter.update(
                                player_height=player_height_new)
                            up_num = player_u
                context = {
                    'error_code': error_code, 'action_code': action_code, 'up_num': up_num}

            elif player_name_u is not None:
                action_code = 3
                Player_name_u = player_name_u.upper()
                len_code_u = len(player_name_u)
                print len_code_u

                if player_name_u == '':
                    error_code = 1  # no data in
                elif len_code_u > 4:
                    error_code = 3  # exceed the default length
                    # print error_code
                elif len_code_u == 4:
                    player_u_filter = PlayersInfo.objects.filter(
                        player_name=Player_name_u)
                    print player_u_filter

                    if player_name_new is not None:
                        Player_name_new = player_name_new.upper()
                        len_code_new = len(Player_name_new)
                        # print len_code_u, len_code_new
                        if len_code_new > 4:
                            error_code = 33  # set a exceed the  length
                        elif len_code_new == 4:
                            player_u = player_u_filter.update(
                                player_name=Player_name_new)
                        else:
                            error_code = 44  # set a shorter value than the default length

                    elif player_loc_new is not None:
                        print player_loc_new
                        if player_loc_new == '':
                            error_code = 11  # no new data in
                            # print error_code
                        else:
                            player_u = player_u_filter.update(
                                player_loc=player_loc_new)
                            up_num = player_u
                    elif player_height_new is not None:
                        if player_height_new == '':
                            error_code = 11  # no new data in
                        else:
                            player_u = player_u_filter.update(
                                player_height=player_height_new)
                            up_num = player_u
                else:
                    error_code = 4  # shorter than the default length
                    # print error_code
                context = {
                    'error_code': error_code, 'action_code': action_code, 'up_num': up_num}

            elif textinput is not None:
                action_code = 4
                in_num = 0
                text_list = textinput.strip().split('&')
                if len(text_list) == 6:
                    player_code = int(text_list[0])
                    player_name = text_list[1].upper()
                    player_loc = int(text_list[2])
                    player_height = int(text_list[3])
                    co_id = int(text_list[4])
                    team_id = int(text_list[5])
                    print player_code, player_name, player_loc, player_height, co_id, team_id

                    try:
                        player, created = PlayersInfo.objects. get_or_create(
                            player_code=player_code, player_name=player_name, player_loc=player_loc, player_height=player_height, co_id=co_id, team_id=team_id)
                        # print player,type(player)
                    except:
                        created = False
                    if created == True:
                        in_num = 1
                    else:
                        in_num = 0
                        error_code = 5  # already have
                else:
                    error_code = 6  # input wrong
                context = {'in_num': in_num,
                           'error_code': error_code, 'action_code': action_code}

            print context
        return render(request, 'teams/transaction-p.html', context)

    except:
        print 'something wrong'

        return render(request, 'teams/transaction-p.html')


@csrf_exempt
def Coach(request):
    try:
        if request.method == 'POST':
            print request.POST
            coach_code_s = request.POST.get('coach_code_s')
            coach_name_s = request.POST.get('coach_name_s')
            coach_country_s = request.POST.get('coach_country_s')
            coach_team_id_s = request.POST.get('coach_team_id_s')

            coach_code_d = request.POST.get('coach_code_d')
            coach_name_d = request.POST.get('coach_name_d')
            coach_country_d = request.POST.get('coach_country_d')
            coach_team_id_d = request.POST.get('coach_team_id_d')

            coach_code_u = request.POST.get('coach_code_u')
            coach_name_u = request.POST.get('coach_name_u')
            coach_country_u = request.POST.get('coach_country_u')
            coach_team_id_u = request.POST.get('coach_team_id_u')

            textinput = str(request.POST.get('textinput'))

            coach_code_new = request.POST.get('coach_code_new')
            coach_name_new = request.POST.get('name_new')
            coach_country_new = request.POST.get('coach_country_new')
            coach_team_id_new = request.POST.get('coach_team_new ')

            print coach_code_s, type(coach_code_s), coach_code_d, type(coach_code_d), coach_code_u, type(coach_code_u)
            print coach_name_s, type(coach_name_s), coach_name_d, type(coach_name_d), coach_name_u, type(coach_name_u), coach_name_new, type(coach_name_new)
            print coach_country_s, type(coach_country_s), coach_country_d, type(coach_country_d), coach_country_u, type(coach_country_u), coach_country_new, type(coach_country_new)
            print coach_team_id_s, type(coach_team_id_s), coach_team_id_d, type(coach_team_id_d), coach_team_id_u, type(coach_team_id_u), coach_team_id_new, type(coach_team_id_new)

            print textinput, type(textinput)

            error_code = 0  # 0 errors
            count_c = 0
            del_num = 0
            up_num = 0
            if coach_code_s is not None:
                action_code = 1
                if "*"in coach_code_s:
                    print 'ok'
                    coach = CoachsInfo.objects.all()
                    # print coach
                    count_c = coach.count()
                elif coach_code_s == '':
                    error_code = 1  # no data in
                    coach = []  # maybe raise error laterly
                else:
                    coach_s_filter = CoachsInfo.objects.filter(
                        coach_code=coach_code_s)
                    count_c = coach_s_filter.count()
                    # print count_c
                    if count_c > 0:
                        coach = coach_s_filter
                    else:
                        error_code = 2  # nothing filtered
                        coach = coach_s_filter
                context = {'coach': coach, 'count_c': count_c,
                           'error_code': error_code, 'action_code': action_code}
                # print coach
            elif coach_name_s is not None:
                action_code = 1
                Coach_name_s = coach_name_s.upper()
                len_code_s = len(coach_name_s)
                # print len_code_s
                if coach_name_s == '':
                    error_code = 1  # no data in
                    coach_s_filter = CoachsInfo.objects.filter(
                        coach_name=Coach_name_s)
                    # print coach_s_filter
                    coach = coach_s_filter

                elif len_code_s > 4:
                    error_code = 3  # exceed the default length
                    # print error_code
                    coach = []  # maybe raise error laterly

                elif len_code_s == 4:
                    coach_s_filter = CoachsInfo.objects.filter(
                        coach_name=Coach_name_s)
                    count_c = coach_s_filter.count()
                    coach = coach_s_filter
                    # print coach_s_filter, count_c
                else:
                    error_code = 4  # shorter than the default length
                    # print error_code
                    coach = []  # maybe raise error laterly
                context = {'coach': coach, 'count_c': count_c,
                           'error_code': error_code, 'action_code': action_code}

            elif coach_country_s is not None:
                action_code = 1
                if coach_country_s == '':
                    error_code = 1  # no data in
                    coach = []  # maybe raise error laterly
                else:
                    coach_country_s_filter = CoachsInfo.objects.filter(
                        coach_country=coach_country_s)
                    # print coach_country_s_filter
                    coach = coach_country_s_filter
                    count_c = coach.count()
                context = {'coach': coach, 'count_c': count_c,
                           'error_code': error_code, 'action_code': action_code}

            elif coach_team_id_s is not None:
                action_code = 1
                if coach_team_id_s == '':
                    error_code = 1  # no data in
                    coach = []  # maybe raise error laterly
                else:
                    coach_team_id_s_filter = CoachsInfo.objects.filter(
                        coach_team_id=coach_team_id_s)
                    print coach_team_id_s_filter
                    coach = coach_team_id_s_filter
                    count_c = coach.count()
                context = {'coach': coach, 'count_c': count_c,
                           'error_code': error_code, 'action_code': action_code}

            elif coach_code_d is not None:
                action_code = 2
                if "*"in coach_code_d:
                    print 'ok'
                    coach = CoachsInfo.objects.all()
                    del_tuple = coach.delete()
                    del_num = del_tuple[0]
                    # print del_tuple,del_num
                elif coach_code_d == '':
                    error_code = 1  # no data in
                else:
                    coach_d_filter = CoachsInfo.objects.filter(
                        coach_code=coach_code_d)
                    del_tuple = coach_d_filter.delete()
                    del_num = del_tuple[0]
                    # print del_tuple, del_num
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}
            elif coach_name_d is not None:
                action_code = 2
                Match_code_d = coach_name_d.upper()
                len_code_d = len(coach_name_d)
                # print len_code_s
                if coach_name_d == '':
                    error_code = 1  # no data in
                    coach_d_filter = CoachsInfo.objects.filter(
                        coach_name=Match_code_d)
                    # print coach_s_filter
                    coach = coach_d_filter
                    del_tuple = coach.delete()
                    del_num = del_tuple[0]
                    print del_tuple, del_num
                elif len_code_d > 4:
                    error_code = 3  # exceed the default length
                    # print error_code
                elif len_code_d == 4:
                    coach_d_filter = CoachsInfo.objects.filter(
                        coach_name=Match_code_d)
                    coach = coach_d_filter
                    # print coach_s_filter
                    del_tuple = coach.delete()
                    del_num = del_tuple[0]
                    # print del_tuple, del_num
                else:
                    error_code = 4  # shorter than the default length
                    # print error_code
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}

            elif coach_country_d is not None:
                action_code = 2
                if coach_country_d == '':
                    error_code = 1  # no data in

                else:
                    coach_country_d_filter = CoachsInfo.objects.filter(
                        coach_country=coach_country_d)
                    # print coach_country_s_filter
                    coach = coach_country_d_filter
                    del_tuple = coach.delete()
                    del_num = del_tuple[0]
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}

            elif coach_team_id_d is not None:
                action_code = 2
                if coach_team_id_d == '':
                    error_code = 1  # no data in

                else:
                    coach_team_id_d_filter = CoachsInfo.objects.filter(
                        coach_team_id=coach_team_id_d)
                    coach = coach_team_id_d_filter
                    del_tuple = coach.delete()
                    del_num = del_tuple[0]
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}

            elif coach_code_u is not None:
                action_code = 3
                # print action_code
                if coach_code_u == '':
                    error_code = 1  # no data in

                else:
                    coach_u_filter = CoachsInfo.objects.filter(
                        coach_code=coach_code_u)

                    if coach_name_new is not None:
                        Match_code_new = coach_name_new.upper()
                        len_code_new = len(Match_code_new)
                        if len_code_new > 4:
                            error_code = 33  # set a exceed the  length
                        elif len_code_new == 4:
                            coach_u = coach_u_filter.update(
                                coach_name=Match_code_new)
                            up_num = coach_u
                        else:
                            error_code = 44  # set a shorter value than the default length

                    elif coach_country_new is not None:
                        # print coach_country_new
                        if coach_country_new == '':
                            error_code = 11  # no new data in
                            # print error_code
                        else:
                            coach_u = coach_u_filter.update(
                                coach_country=coach_country_new)
                            up_num = coach_u
                    elif coach_team_id_new is not None:
                        if coach_team_id_new == '':
                            error_code = 11  # no new data in
                        else:
                            coach_u = coach_u_filter.update(
                                coach_team_id=coach_team_id_new)
                            up_num = coach_u
                context = {
                    'error_code': error_code, 'action_code': action_code, 'up_num': up_num}

            elif coach_name_u is not None:
                action_code = 3
                Match_code_u = coach_name_u.upper()
                len_code_u = len(coach_name_u)
                print len_code_u

                if coach_name_u == '':
                    error_code = 1  # no data in
                elif len_code_u > 4:
                    error_code = 3  # exceed the default length
                    # print error_code
                elif len_code_u == 4:
                    coach_u_filter = CoachsInfo.objects.filter(
                        coach_name=Match_code_u)
                    print coach_u_filter

                    if coach_name_new is not None:
                        Match_code_new = coach_name_new.upper()
                        len_code_new = len(Match_code_new)
                        # print len_code_u, len_code_new
                        if len_code_new > 4:
                            error_code = 33  # set a exceed the  length
                        elif len_code_new == 4:
                            coach_u = coach_u_filter.update(
                                coach_name=Match_code_new)
                        else:
                            error_code = 44  # set a shorter value than the default length

                    elif coach_country_new is not None:
                        print coach_country_new
                        if coach_country_new == '':
                            error_code = 11  # no new data in
                            # print error_code
                        else:
                            coach_u = coach_u_filter.update(
                                coach_country=coach_country_new)
                            up_num = coach_u
                    elif coach_team_id_new is not None:
                        if coach_team_id_new == '':
                            error_code = 11  # no new data in
                        else:
                            coach_u = coach_u_filter.update(
                                coach_team_id=coach_team_id_new)
                            up_num = coach_u
                else:
                    error_code = 4  # shorter than the default length
                    # print error_code
                context = {
                    'error_code': error_code, 'action_code': action_code, 'up_num': up_num}

            elif textinput is not None:
                action_code = 4
                in_num = 0
                text_list = textinput.strip().split('&')
                if len(text_list) == 4:
                    coach_code = int(text_list[0])
                    coach_name = text_list[1].upper()
                    coach_country = int(text_list[2])
                    coach_team_id = int(text_list[3])
                    print coach_code, coach_name, coach_country, coach_team_id

                    try:
                        coach, created = CoachsInfo.objects. get_or_create(
                            coach_code=coach_code, coach_name=coach_name, coach_country=coach_country, coach_team_id=coach_team_id)
                        # print coach,type(coach)
                    except:
                        created = False
                    if created == True:
                        in_num = 1
                    else:
                        in_num = 0
                        error_code = 5  # already have
                else:
                    error_code = 6  # shorter
                context = {'in_num': in_num,
                           'error_code': error_code, 'action_code': action_code}
            print context
        return render(request, 'teams/transaction-c.html', context)

    except:
        print 'something wrong'

        return render(request, 'teams/transaction-c.html')


@csrf_exempt
def Sponsor(request):
    try:
        if request.method == 'POST':
            print request.POST
            nasdaq_s = request.POST.get('nasdaq_s')
            sponsor_name_s = request.POST.get('sponsor_name_s')
            loc_of_sponsor_s = request.POST.get('loc_of_sponsor_s')

            nasdaq_d = request.POST.get('nasdaq_d')
            sponsor_name_d = request.POST.get('sponsor_name_d')
            loc_of_sponsor_d = request.POST.get('loc_of_sponsor_d')

            nasdaq_u = request.POST.get('nasdaq_u')
            sponsor_name_u = request.POST.get('sponsor_name_u')
            loc_of_sponsor_u = request.POST.get('loc_of_sponsor_u')

            textinput = str(request.POST.get('textinput'))

            nasdaq_new = request.POST.get('nasdaq_new')
            sponsor_name_new = request.POST.get('sponsor_name_new')
            loc_of_sponsor_new = request.POST.get('loc_of_sponsor_new')
         #   total_score_new = request.POST.get('score_new ')
        #    m_id_new = request.POST.get('m_id_new')

            print nasdaq_s, type(nasdaq_s), nasdaq_d, type(nasdaq_d), nasdaq_u, type(nasdaq_u)
            print sponsor_name_s, type(sponsor_name_s), sponsor_name_d, type(sponsor_name_d), sponsor_name_u, type(sponsor_name_u), sponsor_name_new, type(sponsor_name_new)
            print loc_of_sponsor_s, type(loc_of_sponsor_s), loc_of_sponsor_d, type(loc_of_sponsor_d), loc_of_sponsor_u, type(loc_of_sponsor_u), loc_of_sponsor_new, type(loc_of_sponsor_new)
 #           print total_score_s, type(total_score_s), total_score_d, type(total_score_d), total_score_u, type(total_score_u), total_score_new, type(total_score_new)
     # print m_id_s, type(m_id_s), m_id_d, type(m_id_d), m_id_u, type(m_id_u),
     # m_id_new, type(m_id_new)

            print textinput, type(textinput)

            error_code = 0  # 0 errors
            count_s = 0
            del_num = 0
            up_num = 0
            if nasdaq_s is not None:
                action_code = 1
                if "*"in nasdaq_s:
                    print 'ok'
                    sponsor = SponsorsInfo.objects.all()
                    # print sponsor
                    count_s = sponsor.count()
                elif nasdaq_s == '':
                    error_code = 1  # no data in
                    sponsor = []  # maybe raise error laterly
                else:
                    sponsor_s_filter = SponsorsInfo.objects.filter(
                        nasdaq=nasdaq_s)
                    count_s = sponsor_s_filter.count()
                    # print count_s
                    if count_s > 0:
                        sponsor = sponsor_s_filter
                    else:
                        error_code = 2  # nothing filtered
                        sponsor = sponsor_s_filter
                context = {'sponsor': sponsor, 'count_s': count_s,
                           'error_code': error_code, 'action_code': action_code}
                # print sponsor
            elif sponsor_name_s is not None:
                action_code = 1
                Sponsor_name_s = sponsor_name_s.upper()
                len_code_s = len(sponsor_name_s)
                # print len_code_s
                if sponsor_name_s == '':
                    error_code = 1  # no data in
                    sponsor_s_filter = SponsorsInfo.objects.filter(
                        sponsor_name=Sponsor_name_s)
                    # print sponsor_s_filter
                    sponsor = sponsor_s_filter

                else:
                    sponsor_s_filter = SponsorsInfo.objects.filter(
                        sponsor_name=Sponsor_name_s)
                    count_s = sponsor_s_filter.count()
                    sponsor = sponsor_s_filter
                    # print sponsor_s_filter, count_s

                context = {'sponsor': sponsor, 'count_s': count_s,
                           'error_code': error_code, 'action_code': action_code}

            elif loc_of_sponsor_s is not None:
                action_code = 1
                if loc_of_sponsor_s == '':
                    error_code = 1  # no data in
                    sponsor = []  # maybe raise error laterly
                else:
                    loc_of_sponsor_s_filter = SponsorsInfo.objects.filter(
                        loc_of_sponsor=loc_of_sponsor_s)
                    # print loc_of_sponsor_s_filter
                    sponsor = loc_of_sponsor_s_filter
                    count_s = sponsor.count()
                context = {'sponsor': sponsor, 'count_s': count_s,
                           'error_code': error_code, 'action_code': action_code}

            elif nasdaq_d is not None:
                action_code = 2
                if "*"in nasdaq_d:
                    print 'ok'
                    sponsor = SponsorsInfo.objects.all()
                    del_tuple = sponsor.delete()
                    del_num = del_tuple[0]
                    # print del_tuple,del_num
                elif nasdaq_s == '':
                    error_code = 1  # no data in
                else:
                    sponsor_d_filter = SponsorsInfo.objects.filter(
                        nasdaq=nasdaq_d)
                    del_tuple = sponsor_d_filter.delete()
                    del_num = del_tuple[0]
                    # print del_tuple, del_num
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}
            elif sponsor_name_d is not None:
                action_code = 2
                Sponsor_name_d = sponsor_name_d.upper()
                len_code_d = len(sponsor_name_d)
                # print len_code_s
                if sponsor_name_d == '':
                    error_code = 1  # no data in
                    sponsor_d_filter = SponsorsInfo.objects.filter(
                        sponsor_name=Sponsor_name_d)
                    # print sponsor_s_filter
                    sponsor = sponsor_d_filter
                    del_tuple = sponsor.delete()
                    del_num = del_tuple[0]
                    print del_tuple, del_num

                else:
                    sponsor_d_filter = SponsorsInfo.objects.filter(
                        sponsor_name=Sponsor_name_d)
                    sponsor = sponsor_d_filter
                    # print sponsor_s_filter
                    del_tuple = sponsor.delete()
                    del_num = del_tuple[0]
                    # print del_tuple, del_num

                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}

            elif loc_of_sponsor_d is not None:
                action_code = 2
                if loc_of_sponsor_d == '':
                    error_code = 1  # no data in

                else:
                    loc_of_sponsor_d_filter = SponsorsInfo.objects.filter(
                        loc_of_sponsor=loc_of_sponsor_d)
                    # print loc_of_sponsor_s_filter
                    sponsor = loc_of_sponsor_d_filter
                    del_tuple = sponsor.delete()
                    del_num = del_tuple[0]
                context = {'del_num': del_num,
                           'error_code': error_code, 'action_code': action_code}

            elif nasdaq_u is not None:
                action_code = 3
                # print action_code
                if nasdaq_u == '':
                    error_code = 1  # no data in

                else:
                    sponsor_u_filter = SponsorsInfo.objects.filter(
                        nasdaq=nasdaq_u)

                    if sponsor_name_new is not None:
                        Sponsor_name_new = sponsor_name_new.upper()
                        len_code_new = len(Sponsor_name_new)

                        sponsor_u = sponsor_u_filter.update(
                            sponsor_name=Sponsor_name_new)
                        up_num = sponsor_u

                    elif loc_of_sponsor_new is not None:
                        # print loc_of_sponsor_new
                        if loc_of_sponsor_new == '':
                            error_code = 11  # no new data in
                            # print error_code
                        else:
                            sponsor_u = sponsor_u_filter.update(
                                loc_of_sponsor=loc_of_sponsor_new)
                            up_num = sponsor_u

                context = {
                    'error_code': error_code, 'action_code': action_code, 'up_num': up_num}

            elif sponsor_name_u is not None:
                action_code = 3
                Sponsor_name_u = sponsor_name_u.upper()
                len_code_u = len(sponsor_name_u)
                print len_code_u

                if sponsor_name_u == '':
                    error_code = 1  # no data in
                else:
                    sponsor_u_filter = SponsorsInfo.objects.filter(
                        sponsor_name=Sponsor_name_u)
                    print sponsor_u_filter

                    if sponsor_name_new is not None:
                        Sponsor_name_new = sponsor_name_new.upper()
                        len_code_new = len(Sponsor_name_new)
                        # print len_code_u, len_code_new

                        sponsor_u = sponsor_u_filter.update(
                            sponsor_name=Sponsor_name_new)

                    elif loc_of_sponsor_new is not None:
                        print loc_of_sponsor_new
                        if loc_of_sponsor_new == '':
                            error_code = 11  # no new data in
                            # print error_code
                        else:
                            sponsor_u = sponsor_u_filter.update(
                                loc_of_sponsor=loc_of_sponsor_new)
                            up_num = sponsor_u

                context = {
                    'error_code': error_code, 'action_code': action_code, 'up_num': up_num}

            elif textinput is not None:
                action_code = 4
                in_num = 0
                text_list = textinput.strip().split('&')
                if len(text_list) == 3:
                    nasdaq = int(text_list[0])
                    sponsor_name = text_list[1].upper()
                    loc_of_sponsor = int(text_list[2])
                    print nasdaq, sponsor_name, loc_of_sponsor
                    try:
                        sponsor, created = SponsorsInfo.objects. get_or_create(
                            nasdaq=nasdaq, sponsor_name=sponsor_name, loc_of_sponsor=loc_of_sponsor)
                        # print sponsor,type(sponsor)
                    except:
                        created = False
                    if created == True:
                        in_num = 1
                    else:
                        in_num = 0
                        error_code = 5  # already have
                else:
                    error_code = 6  # already have
                context = {'in_num': in_num,
                           'error_code': error_code, 'action_code': action_code}

            print context
        return render(request, 'teams/transaction-s.html', context)

    except:
        print 'something wrong'

        return render(request, 'teams/transaction-s.html')

#        selected = "#Team"
 #       context = {
  #          "selected": selected,
   #     }
        # print context
