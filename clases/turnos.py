class Funciones:
    

    concepto_dia = []

    recargos={
        'RD':'Recargo Diurno', 
        'RN':'Recargo nocturno',
        'RDF':'Recargo diurno festivo', 
        'RNF':'Recargo nocturno festivo',
        'ED':'Extra diurno',
        'EDF':'Extra diurno festivo', 
        'EN':'Extra nocturno', 
        'ENF':'Extra nocturno festivo'}
    
    turnos={
        'D':'Turno Diurno', 
        'N':'Turno Nocturno',
        'X':'Descasa o no trabaja',}

    turno_diurno={
        'hora_ini':6,
        'hora_fin':18,
    }

    turno_nocturno={
        'hora_ini':18,
        'hora_fin':6,
        'inicio_n':21,
        'fin_n_dia':24,
        'inicio_n_sig':0,
        'fin_n_sig':6,
    }

    @classmethod
    def calcular_turnos (cls, dia:str,turno:str,horas_totales:int):
        turno=turno.upper()
        if(turno.upper() =='X'):
            concepto=[{'turno':cls.turnos[turno],'dia':dia,'hora_ini':0,'hora_fin':0,'concepto':'Dia no laborado','horas_trabajadas':0}]
            cls.concepto_dia.append(concepto)
            horas_totales+=0
            return cls.concepto_dia , horas_totales
        
        sigdia, sig_es_festv=cls.validar_siguiente_dia (dia)

        
        if(turno.upper() =='D' and dia=='domingo'):
            print('Turno diurno festivo')
            hora_ini=cls.turno_diurno['hora_ini']
            hora_fin=cls.turno_diurno['hora_fin']
            concepto_final,horas_totales=cls.calcular_concepto (hora_ini,hora_fin,horas_totales,dia,sig_es_festv,sigdia,turno)
            cls.concepto_dia.append(concepto_final)

        elif(turno.upper() =='N' and dia=='domingo'):
            print('Turno nocturno festivo')
            cls.horas_partidas=cls.partir_horas_nocturnas()
            for dato in cls.horas_partidas:
                concepto_final,horas_totales=cls.calcular_concepto (dato['inicio'],dato['final'],horas_totales,dia,sig_es_festv,sigdia,turno)
                cls.concepto_dia.append(concepto_final)


        elif(turno.upper() =='D'):
            print('Turno diurno')
            hora_ini=cls.turno_diurno['hora_ini']
            hora_fin=cls.turno_diurno['hora_fin']
            concepto_final,horas_totales=cls.calcular_concepto (hora_ini,hora_fin,horas_totales,dia,sig_es_festv,sigdia,turno)
            cls.concepto_dia.append(concepto_final)

        elif(turno.upper() =='N'):
            print('Turno nocturno')
            cls.horas_partidas=cls.partir_horas_nocturnas()
            for dato in cls.horas_partidas:
                concepto_final,horas_totales=cls.calcular_concepto (dato['inicio'],dato['final'],horas_totales,dia,sig_es_festv,sigdia,turno)
                cls.concepto_dia.append(concepto_final)


        return cls.concepto_dia, horas_totales

    @classmethod
    def validar_siguiente_dia (cls,dia):
        match dia:
            case 'lunes':
                sig_es_festv=False
                sigdia='martes'
                return sigdia, sig_es_festv
            case 'martes':
                sig_es_festv=False
                sigdia='miercoles'
                return sigdia, sig_es_festv
            case 'miercoles':
                sig_es_festv=False
                sigdia='jueves'
                return sigdia, sig_es_festv
            case 'jueves':
                sig_es_festv=False
                sigdia='viernes'
                return sigdia, sig_es_festv
            case 'viernes':
                sig_es_festv=False
                sigdia='sabado'
                return sigdia, sig_es_festv
            case 'sabado':
                sig_es_festv=True
                sigdia='domingo'
                return sigdia, sig_es_festv
            case 'domingo':
                sig_es_festv=False
                sigdia='lunes'
                return sigdia, sig_es_festv
    
    
    @classmethod
    def partir_horas_nocturnas (cls):
        cls.horas_partidas = []
        ini=cls.turno_nocturno['hora_ini']
        fin=cls.turno_nocturno['inicio_n']
        horario={'inicio':ini,'final':fin}
        cls.horas_partidas.append(horario)

        ini=cls.turno_nocturno['inicio_n']
        fin=cls.turno_nocturno['fin_n_dia']
        horario={'inicio':ini,'final':fin}
        cls.horas_partidas.append(horario)

        ini=cls.turno_nocturno['inicio_n_sig']
        fin=cls.turno_nocturno['fin_n_sig']
        horario={'inicio':ini,'final':fin}
        cls.horas_partidas.append(horario)
        return cls.horas_partidas


    def val_si_hay_extra (horas_totales,horas_trabajadas):
        if(horas_totales+horas_trabajadas>44):
            resta=(horas_totales+horas_trabajadas)-44
            return resta
        else:
            return False
        
    @classmethod
    def dia_festivo (cls,dia,turno,ext):
        if(turno=='D'):
            if(dia!='domingo' and ext==True):
                con=cls.recargos['ED']
                return con
            elif(dia=='domingo' and ext==True):
                con=cls.recargos['EDF']
                return con
            elif(dia!='domingo' and ext==False):
                con=cls.recargos['RD']
                return con
            else:# elif(dia=='domingo' and ext==False):
                con=cls.recargos['RDF']
                return con
        elif(turno=='N'):
            if(dia!='domingo' and ext==True):
                con=cls.recargos['EN']
                return con
            elif(dia=='domingo' and ext==True):
                con=cls.recargos['ENF']
                return con
            elif(dia!='domingo' and ext==False):
                con=cls.recargos['RN']
                return con
            else:# elif(dia=='domingo' and ext==False):
                con=cls.recargos['RNF']
                return con
    
    @classmethod
    def calcular_concepto (cls, hora_ini,hora_fin,horas_totales,dia,sig_es_festv,sigdia,turno):
        cls.historial_conceptos = []
        if(horas_totales<=44):
            # ACA SE CALCULA EL TURNO DIURNO ENTRE LAS 6AM Y 6PM
            if(hora_ini >= cls.turno_diurno['hora_ini'] and hora_fin <= cls.turno_diurno['hora_fin']):
                horas_trabajadas=hora_fin-hora_ini
                extra=cls.val_si_hay_extra (horas_totales,horas_trabajadas)
                if(extra):
                    if((horas_trabajadas-extra)>0):
                        horas_trabajadas=horas_trabajadas-extra
                        con=cls.dia_festivo (dia,turno,ext=False)
                        concepto={'turno':cls.turnos[turno],'dia':dia,'hora_ini':cls.turno_diurno['hora_ini'],'hora_fin':cls.turno_diurno['hora_ini']+horas_trabajadas,'concepto':con,'horas_trabajadas':horas_trabajadas}
                        cls.historial_conceptos.append(concepto)
                        horas_totales+=horas_trabajadas
                    con=cls.dia_festivo (dia,turno,ext=True)
                    concepto={'turno':cls.turnos[turno],'dia':dia,'hora_ini':cls.turno_diurno['hora_fin']-extra,'hora_fin':cls.turno_diurno['hora_fin'],'concepto':con,'horas_trabajadas':extra}
                    cls.historial_conceptos.append(concepto)
                    horas_totales+=extra
                else:
                    con=cls.dia_festivo (dia,turno,ext=False)
                    concepto={'turno':cls.turnos[turno],'dia':dia,'hora_ini':cls.turno_diurno['hora_ini'],'hora_fin':cls.turno_diurno['hora_fin'],'concepto':con,'horas_trabajadas':horas_trabajadas}
                    cls.historial_conceptos.append(concepto)
                    horas_totales+=horas_trabajadas

            # ACA SE CALCULA EL TURNO NOCTURNO ENTRE LAS 6PM Y 9PM
            if(hora_ini >= cls.turno_nocturno['hora_ini'] and hora_fin <= cls.turno_nocturno['inicio_n']):
                horas_trabajadas=hora_fin-hora_ini
                extra=cls.val_si_hay_extra (horas_totales,horas_trabajadas)
                if(extra):
                    if((horas_trabajadas-extra)>0):
                        horas_trabajadas=horas_trabajadas-extra
                        con=cls.dia_festivo (dia,turno,ext=False)
                        concepto={'turno':cls.turnos[turno],'dia':dia,'hora_ini':cls.turno_nocturno['hora_ini'],'hora_fin':cls.turno_nocturno['hora_ini']+horas_trabajadas,'concepto':con,'horas_trabajadas':horas_trabajadas}
                        cls.historial_conceptos.append(concepto)
                        horas_totales+=horas_trabajadas
                    con=cls.dia_festivo (dia,turno,ext=True)
                    concepto={'turno':cls.turnos[turno],'dia':dia,'hora_ini':cls.turno_nocturno['hora_fin']-extra,'hora_fin':cls.turno_nocturno['inicio_n'],'concepto':con,'horas_trabajadas':extra}
                    cls.historial_conceptos.append(concepto)
                    horas_totales+=extra
                else:
                    con=cls.dia_festivo (dia,turno,ext=False)
                    concepto={'turno':cls.turnos[turno],'dia':dia,'hora_ini':cls.turno_nocturno['hora_ini'],'hora_fin':cls.turno_nocturno['inicio_n'],'concepto':con,'horas_trabajadas':horas_trabajadas}
                    cls.historial_conceptos.append(concepto)
                    horas_totales+=horas_trabajadas
            
            # ACA SE CALCULA EL TURNO NOCTURNO ENTRE LAS 9PM Y 12PM
            if(hora_ini >= cls.turno_nocturno['inicio_n'] and hora_fin <= cls.turno_nocturno['fin_n_dia']):
                horas_trabajadas=hora_fin-hora_ini
                extra=cls.val_si_hay_extra (horas_totales,horas_trabajadas)
                if(extra):
                    if((horas_trabajadas-extra)>0):
                        horas_trabajadas=horas_trabajadas-extra
                        con=cls.dia_festivo (dia,turno,ext=False)
                        concepto={'turno':cls.turnos[turno],'dia':dia,'hora_ini':cls.turno_nocturno['inicio_n'],'hora_fin':cls.turno_nocturno['inicio_n']+horas_trabajadas,'concepto':con,'horas_trabajadas':horas_trabajadas}
                        cls.historial_conceptos.append(concepto)
                        horas_totales+=horas_trabajadas
                    con=cls.dia_festivo (dia,turno,ext=True)
                    concepto={'turno':cls.turnos[turno],'dia':dia,'hora_ini':cls.turno_nocturno['fin_n_dia']-extra,'hora_fin':cls.turno_nocturno['inicio_n'],'concepto':con,'horas_trabajadas':extra}
                    cls.historial_conceptos.append(concepto)
                    horas_totales+=extra
                else:
                    con=cls.dia_festivo (dia,turno,ext=False)
                    concepto={'turno':cls.turnos[turno],'dia':dia,'hora_ini':cls.turno_nocturno['inicio_n'],'hora_fin':cls.turno_nocturno['fin_n_dia'],'concepto':con,'horas_trabajadas':horas_trabajadas}
                    cls.historial_conceptos.append(concepto)
                    horas_totales+=horas_trabajadas

            # ACA SE CALCULA EL TURNO NOCTURNO ENTRE LAS 12PM Y 6AM (DIA SIGUIENTE)
            if(hora_ini >= cls.turno_nocturno['inicio_n_sig'] and hora_fin <= cls.turno_nocturno['fin_n_sig'] and not sig_es_festv):
                horas_trabajadas=hora_fin-hora_ini
                extra=cls.val_si_hay_extra (horas_totales,horas_trabajadas)
                if(extra):
                    if((horas_trabajadas-extra)>0):
                        horas_trabajadas=horas_trabajadas-extra
                        con=cls.dia_festivo (sigdia,turno,ext=False)
                        concepto={'turno':cls.turnos[turno],'dia':sigdia,'hora_ini':cls.turno_nocturno['inicio_n_sig'],'hora_fin':cls.turno_nocturno['inicio_n_sig']+horas_trabajadas,'concepto':con,'horas_trabajadas':horas_trabajadas}
                        cls.historial_conceptos.append(concepto)
                        horas_totales+=horas_trabajadas
                    con=cls.dia_festivo (sigdia,turno,ext=True)
                    concepto={'turno':cls.turnos[turno],'dia':sigdia,'hora_ini':cls.turno_nocturno['fin_n_sig']-extra,'hora_fin':cls.turno_nocturno['fin_n_sig'],'concepto':con,'horas_trabajadas':extra}
                    cls.historial_conceptos.append(concepto)
                    horas_totales+=extra
                else:
                    con=cls.dia_festivo (sigdia,turno,ext=False)
                    concepto={'turno':cls.turnos[turno],'dia':sigdia,'hora_ini':cls.turno_nocturno['inicio_n_sig'],'hora_fin':cls.turno_nocturno['fin_n_sig'],'concepto':con,'horas_trabajadas':horas_trabajadas}
                    cls.historial_conceptos.append(concepto)
                    horas_totales+=horas_trabajadas

            # ACA SE CALCULA EL TURNO NOCTURNO ENTRE LAS 12PM Y 6AM (DIA SIGUIENTE FESTIVO O DOMINICAL)
            elif(hora_ini >= cls.turno_nocturno['inicio_n_sig'] and hora_fin <= cls.turno_nocturno['fin_n_sig'] and sig_es_festv):
                horas_trabajadas=hora_fin-hora_ini
                extra=cls.val_si_hay_extra (horas_totales,horas_trabajadas)
                if(extra):
                    if((horas_trabajadas-extra)>0):
                        horas_trabajadas=horas_trabajadas-extra
                        con=cls.dia_festivo (sigdia,turno,ext=False)
                        concepto={'turno':cls.turnos[turno],'dia':sigdia,'hora_ini':cls.turno_nocturno['inicio_n_sig'],'hora_fin':cls.turno_nocturno['inicio_n_sig']+horas_trabajadas,'concepto':con,'horas_trabajadas':horas_trabajadas}
                        cls.historial_conceptos.append(concepto)
                        horas_totales+=horas_trabajadas
                    con=cls.dia_festivo (sigdia,turno,ext=True)
                    concepto={'turno':cls.turnos[turno],'dia':sigdia,'hora_ini':cls.turno_nocturno['fin_n_sig']-extra,'hora_fin':cls.turno_nocturno['fin_n_sig'],'concepto':con,'horas_trabajadas':extra}
                    cls.historial_conceptos.append(concepto)
                    horas_totales+=extra
                else:
                    con=cls.dia_festivo (sigdia,turno,ext=False)
                    concepto={'turno':cls.turnos[turno],'dia':sigdia,'hora_ini':cls.turno_nocturno['inicio_n_sig'],'hora_fin':cls.turno_nocturno['fin_n_sig'],'concepto':con,'horas_trabajadas':horas_trabajadas}
                    cls.historial_conceptos.append(concepto)
                    horas_totales+=horas_trabajadas

            return cls.historial_conceptos,horas_totales


        # ACA SE CALCULA EL TURNO SI SE PASA DE LAS 44 HORAS TRABAJADAS (EXTRAS)
        elif(horas_totales>44):
            # ACA SE CALCULA EL TURNO DIURNO ENTRE LAS 6AM Y 6PM
            if(hora_ini >= cls.turno_diurno['hora_ini'] and hora_fin <= cls.turno_diurno['hora_fin']):
                horas_trabajadas=hora_fin-hora_ini
                con=cls.dia_festivo (dia,turno,ext=True)
                concepto={'turno':cls.turnos[turno],'dia':dia,'hora_ini':cls.turno_diurno['hora_ini'],'hora_fin':cls.turno_diurno['hora_fin'],'concepto':con,'horas_trabajadas':horas_trabajadas}
                cls.historial_conceptos.append(concepto)
                horas_totales+=horas_trabajadas

            # ACA SE CALCULA EL TURNO NOCTURNO ENTRE LAS 6PM Y 9PM
            if(hora_ini >= cls.turno_nocturno['hora_ini'] and hora_fin <= cls.turno_nocturno['inicio_n']):
                horas_trabajadas=hora_fin-hora_ini
                con=cls.dia_festivo (dia,turno,ext=True)
                concepto={'turno':cls.turnos[turno],'dia':dia,'hora_ini':cls.turno_nocturno['hora_ini'],'hora_fin':cls.turno_nocturno['inicio_n'],'concepto':con,'horas_trabajadas':horas_trabajadas}
                cls.historial_conceptos.append(concepto)
                horas_totales+=horas_trabajadas
            
            # ACA SE CALCULA EL TURNO NOCTURNO ENTRE LAS 9PM Y 12PM
            if(hora_ini >= cls.turno_nocturno['inicio_n'] and hora_fin <= cls.turno_nocturno['fin_n_dia']):
                horas_trabajadas=hora_fin-hora_ini
                con=cls.dia_festivo (dia,turno,ext=True)
                concepto={'turno':cls.turnos[turno],'dia':dia,'hora_ini':cls.turno_nocturno['inicio_n'],'hora_fin':cls.turno_nocturno['fin_n_dia'],'concepto':con,'horas_trabajadas':horas_trabajadas}
                cls.historial_conceptos.append(concepto)
                horas_totales+=horas_trabajadas

            # ACA SE CALCULA EL TURNO NOCTURNO ENTRE LAS 12PM Y 6AM (DIA SIGUIENTE)
            if(hora_ini >= cls.turno_nocturno['inicio_n_sig'] and hora_fin <= cls.turno_nocturno['fin_n_sig'] and not sig_es_festv):
                horas_trabajadas=hora_fin-hora_ini
                con=cls.dia_festivo (sigdia,turno,ext=True)
                concepto={'turno':cls.turnos[turno],'dia':sigdia,'hora_ini':cls.turno_nocturno['inicio_n_sig'],'hora_fin':cls.turno_nocturno['fin_n_sig'],'concepto':con,'horas_trabajadas':horas_trabajadas}
                cls.historial_conceptos.append(concepto)
                horas_totales+=horas_trabajadas

            # ACA SE CALCULA EL TURNO NOCTURNO ENTRE LAS 12PM Y 6AM (DIA SIGUIENTE FESTIVO O DOMINICAL)
            elif(hora_ini >= cls.turno_nocturno['inicio_n_sig'] and hora_fin <= cls.turno_nocturno['fin_n_sig'] and sig_es_festv):
                horas_trabajadas=hora_fin-hora_ini
                con=cls.dia_festivo (sigdia,turno,ext=True)
                concepto={'turno':cls.turnos[turno],'dia':sigdia,'hora_ini':cls.turno_nocturno['inicio_n_sig'],'hora_fin':cls.turno_nocturno['fin_n_sig'],'concepto':con,'horas_trabajadas':horas_trabajadas}
                cls.historial_conceptos.append(concepto)
                horas_totales+=horas_trabajadas
        
            return cls.historial_conceptos,horas_totales