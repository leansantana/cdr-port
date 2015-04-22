from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from .models import cdr, DispositionPercent, Stats_ANSWERED, Stats_NOANSWER, Stats_BUSY, Info
from .models import VwDayStats, VwMonthStats,VwLast10, VwOperadoras, VwStatsAnswered, VwStatsBusy, VwStatsNoanswer, VwRamais,\
                    VwDisposition, VwCdr, VwCidades, VwEstados
from django.db.models import Sum, Count, Avg, Max, Min
from datetime import datetime, timedelta, time
from django.db.models import Q


def error(request):
    info = Info.objects.values_list('ativo')
    info = str(info)[2]
    template = loader.get_template('error.html')
    context = RequestContext(request, {'info': info})
    return HttpResponse(template.render(context))


def registro(request):
    info = Info.objects.values('uuid', 'system_number','system_name', 'mac','frequencia', 'data_ativacao', 'data_expira', 'ativo')
    template = loader.get_template('registro.html')
    context = RequestContext(request, {'info': info})
    return HttpResponse(template.render(context))



def index(request):
    info = Info.objects.values_list('ativo')
    info = str(info)[2]
    perc = DispositionPercent.objects.values_list('disposition', 'valor', 'perc')
    total = DispositionPercent.objects.aggregate(Sum('valor'))['valor__sum']
    stats_AN = VwStatsAnswered.objects.values_list('dia', 'semana', 'mes')
    stats_NO = VwStatsNoanswer.objects.values_list('dia', 'semana', 'mes')
    stats_BU = VwStatsBusy.objects.values_list('dia', 'semana', 'mes')
    ultimo = VwLast10.objects.values_list('dst','operadora', 'tipo','calldate','cidade', 'estado', 'portado')
    byDay = VwDayStats.objects.values_list('dia', 'mes', 'total')
    byMonth = VwMonthStats.objects.values_list('mes', 'total')
    operadora = VwOperadoras.objects.values_list('operadora', 'total')
    cidade = VwCidades.objects.values_list('cidade').count()
    portados_s = cdr.objects.filter(portado='Sim').count()
    portados_n = cdr.objects.filter(portado='Nao').count()
    template = loader.get_template('index.html')
    context = RequestContext(request, { 'info':info, 'perc': perc, 'total': total, 'stats_AN':stats_AN, 'stats_NO':stats_NO,'cidade':cidade,'portados_s':portados_s,
								    	'portados_n':portados_n,'stats_BU':stats_BU, 'ultimo':ultimo, 'byDay':byDay, 'byMonth':byMonth, 'operadora':operadora })
    return HttpResponse(template.render(context))


def time_line(request):

    info = Info.objects.values_list('ativo')
    info = str(info)[2]
    
    hora = datetime.now()
    hoje = hora.strftime("%Y-%m-%dT23:59:59") 
    ontem = hora - timedelta(days=1)
    ontem = ontem.strftime("%Y-%m-%dT00:00:00")

    byDay = VwDayStats.objects.values_list('dia', 'mes', 'total')
    byMonth = VwMonthStats.objects.values_list('mes', 'total')
    ultimo = VwLast10.objects.values_list('dst','operadora', 'tipo','calldate','cidade', 'estado')
    resultado = VwCdr.objects.values_list('dst', 'src', 'calldate', 'disposition', 'duration', 'billsec').order_by('-calldate')
    src = VwRamais.objects.all()
    numero = VwCdr.objects.values_list('dst', 'src', 'calldate', 'disposition', 'duration', 'billsec')
    calldate = VwCdr.objects.values_list('dst', 'src', 'calldate', 'disposition', 'duration', 'billsec')
    disposition = VwDisposition.objects.all()
    tipo = VwCdr.objects.values_list('tipo')
    operadora = VwOperadoras.objects.all()
    cidade = VwCidades.objects.all()
    estado = VwEstados.objects.all()
    pagina = 20,30,50,100,200

    
    numero_f = request.GET.get('numero', "")
    src_f = request.GET.get('src', "0")
    calldate1 = request.GET.get('calldate1', ontem)
    calldate2 = request.GET.get('calldate2', hoje)
    disposition_f = request.GET.get('disposition', "")
    paginas_f = request.GET.get('pagina', "")
    tipo_f = request.GET.get('tipo', "")
    operadora_f = request.GET.get('operadora', "")
    cidade_f = request.GET.get('cidade', "")
    estado_f = request.GET.get('estado', "")

    if paginas_f == '':
        paginas_f = 15
    else:
        paginas_f = paginas_f

    query = Q()

    if numero:
        query &=Q(dst__startswith=numero_f)
    if src:
        query &=Q(src__icontains=src_f)
    if calldate:
        query &=Q(calldate__range=(calldate1,calldate2))
    if disposition:
        query &=Q(disposition__icontains=disposition_f)
    if tipo:
        query &=Q(tipo__icontains=tipo_f)
    if operadora:
        query &=Q(operadora__icontains=operadora_f)
    if cidade:
        query &=Q(cidade__icontains=cidade_f)
    if estado:
        query &=Q(estado__icontains=estado_f)



    results = VwCdr.objects.filter(query).order_by('-calldate')
    print info
    if info == "1":
        url = "numero=%s&src=%s&calldate1=%s&calldate2=%s&disposition=%s&pagina=%s&cidade=%s&estado=%s"\
            % (numero_f, src_f, calldate1, calldate2, disposition_f, paginas_f, cidade_f, estado_f)
    else:
        url = "numero=%s&src=%s&calldate1=%s&calldate2=%s&disposition=%s&pagina=%s&tipo=%s&operadora=%s&cidade=%s&estado=%s"\
    % (numero_f, src_f, calldate1, calldate2, disposition_f, paginas_f, tipo_f, operadora_f, cidade_f, estado_f)

    tempo_medio = results.aggregate(Avg('billsec'))['billsec__avg']
    if tempo_medio == None:
        tempo_medio = '00:00:00'
    else:
        tempo_medio = int(tempo_medio)
        tempo_medio = timedelta(seconds=tempo_medio)

    tempo_maior = results.aggregate(Max('billsec'))['billsec__max']
    tempo_menor = results.aggregate(Min('billsec'))['billsec__min']
    tempo = results.aggregate(Sum('billsec'))['billsec__sum']
    if tempo == None:
        tempo = '00:00:00'
    else:
        tempo = int(tempo)
        tempo = timedelta(seconds=tempo)
    periodo_dia_1 = calldate1[8:10]
    periodo_dia_2 = calldate2[8:10]
    periodo_mes_1 = calldate1[5:7]
    periodo_mes_2 = calldate2[5:7]
    total = results.aggregate(Count('src'))['src__count']

    ### SQL personalizado
    from django.db import connection
    cursor = connection.cursor()
    
    if operadora_f == '':
        print 1

        atendeu = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'ANSWERED' AND src=%s AND tipo='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, tipo_f, calldate1, calldate2)
        print atendeu
        atendeu = cursor.execute(atendeu)
        atendeu = cursor.fetchone()[0]
        print atendeu

        n_atendeu = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'NO ANSWER' AND src=%s AND tipo='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, tipo_f, calldate1, calldate2)
        n_atendeu = cursor.execute(n_atendeu)
        n_atendeu = cursor.fetchone()[0]

        ocupado = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'BUSY' AND src=%s AND tipo='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, tipo_f, calldate1, calldate2)
        ocupado = cursor.execute(ocupado)
        ocupado = cursor.fetchone()[0]

        falhou = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'FAILED' AND src=%s AND tipo='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, tipo_f, calldate1, calldate2)
        falhou = cursor.execute(falhou)
        falhou = cursor.fetchone()[0]

        fixo = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'ANSWERED' AND src=%s AND tipo='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, tipo_f, calldate1, calldate2)
        fixo = cursor.execute(fixo)
        fixo = cursor.fetchone()[0]

        movel = """SELECT Count(disposition) FROM vw_cdr WHERE tipo = 'MOVEL' AND disposition = 'ANSWERED' AND src=%s AND tipo='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, tipo_f, calldate1, calldate2)
        movel = cursor.execute(movel)
        movel = cursor.fetchone()[0]

        radio = """SELECT Count(disposition) FROM vw_cdr WHERE tipo = 'RADIO' AND disposition = 'ANSWERED' AND src=%s AND tipo='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, tipo_f, calldate1, calldate2)
        radio = cursor.execute(radio)
        radio = cursor.fetchone()[0]

    elif tipo_f == '':
        print 2
        atendeu = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'ANSWERED' AND src=%s AND operadora ='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, operadora_f, calldate1, calldate2)
        atendeu = cursor.execute(atendeu)
        atendeu = cursor.fetchone()[0]

        n_atendeu = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'NO ANSWER' AND src=%s AND operadora ='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, operadora_f, calldate1, calldate2)
        n_atendeu = cursor.execute(n_atendeu)
        n_atendeu = cursor.fetchone()[0]

        ocupado = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'BUSY' AND src=%s AND operadora ='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, operadora_f, calldate1, calldate2)
        ocupado = cursor.execute(ocupado)
        ocupado = cursor.fetchone()[0]

        falhou = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'FAILED' AND src=%s AND operadora ='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, operadora_f, calldate1, calldate2)
        falhou = cursor.execute(falhou)
        falhou = cursor.fetchone()[0]

        fixo = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'ANSWERED' AND src=%s AND operadora ='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, operadora_f, calldate1, calldate2)
        fixo = cursor.execute(fixo)
        fixo = cursor.fetchone()[0]

        movel = """SELECT Count(disposition) FROM vw_cdr WHERE tipo = 'MOVEL' AND disposition = 'ANSWERED' AND src=%s AND operadora ='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, operadora_f, calldate1, calldate2)
        movel = cursor.execute(movel)
        movel = cursor.fetchone()[0]

        radio = """SELECT Count(disposition) FROM vw_cdr WHERE tipo = 'RADIO' AND disposition = 'ANSWERED' AND src=%s AND operadora ='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, operadora_f, calldate1, calldate2)
        radio = cursor.execute(radio)
        radio = cursor.fetchone()[0]


    elif operadora_f == '' and tipo_f == '':
        print 3
        atendeu = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'ANSWERED' AND src=%s AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, calldate1, calldate2)
        atendeu = cursor.execute(atendeu)
        atendeu = cursor.fetchone()[0]

        n_atendeu = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'NO ANSWER' AND src=%s AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, calldate1, calldate2)
        n_atendeu = cursor.execute(n_atendeu)
        n_atendeu = cursor.fetchone()[0]

        ocupado = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'BUSY' AND src=%s AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, calldate1, calldate2)
        ocupado = cursor.execute(ocupado)
        ocupado = cursor.fetchone()[0]

        falhou = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'FAILED' AND src=%s AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, calldate1, calldate2)
        falhou = cursor.execute(falhou)
        falhou = cursor.fetchone()[0]

        fixo = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'ANSWERED' AND src=%s AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, calldate1, calldate2)
        fixo = cursor.execute(fixo)
        fixo = cursor.fetchone()[0]

        movel = """SELECT Count(disposition) FROM vw_cdr WHERE tipo = 'MOVEL' AND disposition = 'ANSWERED' AND src=%s AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, calldate1, calldate2)
        movel = cursor.execute(movel)
        movel = cursor.fetchone()[0]

        radio = """SELECT Count(disposition) FROM vw_cdr WHERE tipo = 'RADIO' AND disposition = 'ANSWERED' AND src=%s AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, calldate1, calldate2)
        radio = cursor.execute(radio)
        radio = cursor.fetchone()[0]

    elif src_f == 98339 and tipo_f == '':
        print 33
        atendeu = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'ANSWERED' AND src=%s AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, calldate1, calldate2)
        atendeu = cursor.execute(atendeu)
        atendeu = cursor.fetchone()[0]

        n_atendeu = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'NO ANSWER' AND src=%s AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, calldate1, calldate2)
        n_atendeu = cursor.execute(n_atendeu)
        n_atendeu = cursor.fetchone()[0]

        ocupado = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'BUSY' AND src=%s AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, calldate1, calldate2)
        ocupado = cursor.execute(ocupado)
        ocupado = cursor.fetchone()[0]

        falhou = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'FAILED' AND src=%s AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, calldate1, calldate2)
        falhou = cursor.execute(falhou)
        falhou = cursor.fetchone()[0]

        fixo = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'ANSWERED' AND src=%s AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, calldate1, calldate2)
        fixo = cursor.execute(fixo)
        fixo = cursor.fetchone()[0]

        movel = """SELECT Count(disposition) FROM vw_cdr WHERE tipo = 'MOVEL' AND disposition = 'ANSWERED' AND src=%s AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, calldate1, calldate2)
        movel = cursor.execute(movel)
        movel = cursor.fetchone()[0]

        radio = """SELECT Count(disposition) FROM vw_cdr WHERE tipo = 'RADIO' AND disposition = 'ANSWERED' AND src=%s AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, calldate1, calldate2)
        radio = cursor.execute(radio)
        radio = cursor.fetchone()[0]

    else:
        print 4
        atendeu = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'ANSWERED' AND src=%s AND operadora ='%s' AND tipo='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, operadora_f, tipo_f, calldate1, calldate2)
        atendeu = cursor.execute(atendeu)
        atendeu = cursor.fetchone()[0]

        n_atendeu = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'NO ANSWER' AND src=%s AND operadora ='%s' AND tipo='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, operadora_f, tipo_f, calldate1, calldate2)
        n_atendeu = cursor.execute(n_atendeu)
        n_atendeu = cursor.fetchone()[0]

        ocupado = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'BUSY' AND src=%s AND operadora ='%s' AND tipo='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, operadora_f, tipo_f, calldate1, calldate2)
        ocupado = cursor.execute(ocupado)
        ocupado = cursor.fetchone()[0]

        falhou = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'FAILED' AND src=%s AND operadora ='%s' AND tipo='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, operadora_f, tipo_f, calldate1, calldate2)
        falhou = cursor.execute(falhou)
        falhou = cursor.fetchone()[0]

        fixo = """SELECT Count(disposition) FROM vw_cdr WHERE disposition = 'ANSWERED' AND src=%s AND operadora ='%s' AND tipo='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, operadora_f, tipo_f, calldate1, calldate2)
        fixo = cursor.execute(fixo)
        fixo = cursor.fetchone()[0]

        movel = """SELECT Count(disposition) FROM vw_cdr WHERE tipo = 'MOVEL' AND disposition = 'ANSWERED' AND src=%s AND operadora ='%s' AND tipo='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, operadora_f, tipo_f, calldate1, calldate2)
        movel = cursor.execute(movel)
        movel = cursor.fetchone()[0]

        radio = """SELECT Count(disposition) FROM vw_cdr WHERE tipo = 'RADIO' AND disposition = 'ANSWERED' AND src=%s AND operadora ='%s' AND tipo='%s' AND calldate BETWEEN ('%s') AND ('%s')""" % (src_f, operadora_f, tipo_f, calldate1, calldate2)
        radio = cursor.execute(radio)
        radio = cursor.fetchone()[0]

    ### FIM SQL personalizado

    if results:
        paginator = Paginator(results, int(paginas_f))
        page = request.GET.get('page')
      
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except (EmptyPage):
            results = paginator.page(paginator.num_pages)

        template = loader.get_template('cdr.html')
        context = RequestContext(request, { 'info':info, 'byDay':byDay, 'byMonth':byMonth, 'ultimo':ultimo, 'results':results,
                                            'src':src, 'src_f':src_f ,'numero':numero, 'calldate':calldate, 'hoje':hoje, 'ontem':ontem, 
                                            'disposition':disposition, 'url':url, 'tempo_medio':tempo_medio, 'tempo':tempo, 'periodo_dia_1':periodo_dia_1,
                                            'periodo_dia_2':periodo_dia_2, 'periodo_mes_1':periodo_mes_1, 'periodo_mes_2':periodo_mes_2,
                                            'total':total, 'tempo_maior':tempo_maior, 'tempo_menor':tempo_menor, 'atendeu':atendeu,
                                            'n_atendeu':n_atendeu, 'ocupado':ocupado, 'falhou':falhou, 'fixo':fixo, 'movel':movel, 'radio':radio,
                                             'pagina': pagina, 'operadora': operadora, 'cidade':cidade, 'estado':estado , 'total':total})
        return HttpResponse(template.render(context))
    else:
            template = loader.get_template('cdr.html')
            context = RequestContext(request, { 'info':info, 'byDay':byDay, 'byMonth':byMonth, 'ultimo':ultimo, 'results':results,
                                            'src':src, 'src_f':src_f ,'numero':numero, 'calldate':calldate, 'hoje':hoje, 'ontem':ontem, 
                                            'disposition':disposition, 'url':url, 'tempo_medio':tempo_medio, 'tempo':tempo, 'periodo_dia_1':periodo_dia_1,
                                            'periodo_dia_2':periodo_dia_2, 'periodo_mes_1':periodo_mes_1, 'periodo_mes_2':periodo_mes_2,
                                            'total':total, 'tempo_maior':tempo_maior, 'tempo_menor':tempo_menor, 'atendeu':atendeu,
                                            'n_atendeu':n_atendeu, 'ocupado':ocupado, 'falhou':falhou, 'fixo':fixo, 'movel':movel, 'radio':radio,
                                            'pagina': pagina, 'operadora': operadora,'cidade':cidade, 'estado':estado})
            return HttpResponse(template.render(context))



