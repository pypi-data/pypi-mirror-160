#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Utility included in cartolidar project 
cartolidar: tools for Lidar processing focused on Spanish PNOA datasets

qlidtwins is an example that uses clidtwins within the cartolidar configuration.
clidtwins provides classes and functions that can be used to search for
areas similar to a reference one in terms of dasometric Lidar variables (DLVs).
DLVs (Daso Lidar Vars): vars that characterize forest or land cover structure.

@author:     Jose Bengoa
@copyright:  2022 @clid
@license:    GNU General Public License v3 (GPLv3)
@contact:    cartolidar@gmail.com
'''

import sys
import os
import re
import time
import argparse
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import importlib
import importlib.util
# import logging
# import traceback
# import warnings
# import errno
# print {i:os.strerror(i) for i in sorted(errno.errorcode)}
# import random

# ==============================================================================
spec = importlib.util.find_spec('cartolidar')
if not spec is None:
    from cartolidar.clidax import clidconfig
    from cartolidar.clidtools import clidtwcfg
    from cartolidar.clidtools.clidtwcfg import GLO
    from cartolidar.clidtools.clidtwins import DasoLidarSource
    from cartolidar.clidtools.clidtwinx import comprobarTipoMasaDeCapaVectorial
    from cartolidar.clidtools.clidtwinx import getParametroConPath
else:
    try:
        from cartolidar.clidax import clidconfig
        from cartolidar.clidtools import clidtwcfg
        from cartolidar.clidtools.clidtwcfg import GLO
        from cartolidar.clidtools.clidtwins import DasoLidarSource
        from cartolidar.clidtools.clidtwinx import comprobarTipoMasaDeCapaVectorial
        from cartolidar.clidtools.clidtwinx import getParametroConPath
    except ModuleNotFoundError:
        if '-vv' in sys.argv or '--verbose' in sys.argv:
            sys.stderr.write(f'qlidtwins-> Aviso: cartolidar no esta instalado en site-packages (se esta ejecutando una version local sin instalar).\n')
            sys.stderr.write(f'\t-> Se importan paquetes de cartolidar desde qlidtwins del directorio local {os.getcwd()}/clidtools.\n')
        from clidax import clidconfig
        # print('qlidtwins-> ok clidconfig')
        from clidtools import clidtwcfg
        # print('qlidtwins-> ok clidtwcfg')
        from clidtools.clidtwcfg import GLO
        # print('qlidtwins-> ok GLO')
        from clidtools.clidtwins import DasoLidarSource
        # print('qlidtwins-> ok DasoLidarSource')
        from clidtools.clidtwinx import comprobarTipoMasaDeCapaVectorial
        # print('qlidtwins-> ok comprobarTipoMasaDeCapaVectorial')
        from clidtools.clidtwinx import getParametroConPath
        # print('qlidtwins-> ok getParametroConPath')
    except ModuleNotFoundError:
        sys.stderr.write(f'\nATENCION: qlidtwins.py requiere los paquetes de cartolidar clidtools y clidax.\n')
        sys.stderr.write(f'          Para lanzar el modulo qlidtwins.py desde linea de comandos ejecutar:\n')
        sys.stderr.write(f'              $ python -m cartolidar\n')
        sys.stderr.write(f'          Para ver las opciones de qlidtwins en linea de comandos:\n')
        sys.stderr.write(f'              $ python qlidtwins -h\n')
        sys.exit(0)
    except SystemError as excpt:
        program_name = 'qlidtwins.py'
        sys.stderr.write(f'\n{program_name}-> Error SystemError:\n{excpt}', exc_info=True)
        sys.exit(0)
    except OSError as excpt:
        program_name = 'qlidtwins.py'
        sys.stderr.write(f'\n{program_name}-> Error OSError:\n{excpt}', exc_info=True)
        sys.exit(0)
    except PermissionError as excpt:
        program_name = 'qlidtwins.py'
        sys.stderr.write(f'\n{program_name}-> Error PermissionError:\n{excpt}', exc_info=True)
        sys.exit(0)
    except Exception as excpt:
        program_name = 'qlidtwins.py'
        # sys.stderr.write(f'\n{program_name}-> Error Exception:\n{excpt}', exc_info=True)
    
        # https://stackoverflow.com/questions/1278705/when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
        exc_type, exc_obj, exc_tb = sys.exc_info()
        # ==================================================================
        fileNameError = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        funcError = os.path.split(exc_tb.tb_frame.f_code.co_name)[1]
        lineError = exc_tb.tb_lineno
        typeError = exc_type.__name__
        try:
            lineasTraceback = list((traceback.format_exc()).split('\n'))
            codigoConError = lineasTraceback[2]
        except:
            codigoConError = ''
        try:
            descError = exc_obj.strerror
        except:
            descError = exc_obj
        sys.stderr.write(f'\nOps! Ha surgido un error inesperado.\n')
        sys.stderr.write(f'Si quieres contribuir a depurar este programa envía el\n')
        sys.stderr.write(f'texto que aparece a continacion a: cartolidar@gmail.com\n')
        sys.stderr.write(f'\tError en:    {fileNameError}\n')
        sys.stderr.write(f'\tFuncion:     {funcError}\n')
        sys.stderr.write(f'\tLinea:       {lineError}\n')
        sys.stderr.write(f'\tDescripcion: {descError}\n') # = {exc_obj}
        sys.stderr.write(f'\tTipo:        {typeError}\n')
        sys.stderr.write(f'\tError en:    {codigoConError}\n')
        sys.stderr.write(f'Gracias!\n')
        # ==================================================================
        sys.stderr.write(f'\nFor help use:\n')
        sys.stderr.write(f'\thelp for main arguments:         python {program_name}.py -h\n')
        sys.stderr.write(f'\thelp for main & extra arguments: python {program_name}.py -e -h\n')
        # ==================================================================
        sys.exit(0)
# ==============================================================================

# ==============================================================================
# ========================== Variables globales ================================
# ==============================================================================
MAIN_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# ==============================================================================
# Ver https://peps.python.org/pep-0008/#module-level-dunder-names
# Ver https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
# ==============================================================================
VERSIONFILE = os.path.abspath(os.path.join(MAIN_FILE_DIR, '_version.py'))
if not os.path.exists(VERSIONFILE):
    VERSIONFILE = os.path.abspath(os.path.join(MAIN_FILE_DIR, '..', '_version.py'))
    if not os.path.exists(VERSIONFILE):
        VERSIONFILE = os.path.abspath(os.path.join(MAIN_FILE_DIR, '../..', '_version.py'))
        if not os.path.exists(VERSIONFILE):
            VERSIONFILE = os.path.abspath('_version.py')
if os.path.exists(VERSIONFILE):
    try:
        verstrline = open(VERSIONFILE, "rt").read()
        VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
        mo = re.search(VSRE, verstrline, re.M)
        if mo:
            # __version__ = mo.groups()[0]
            __version__ = mo.group(1)
        else:
            # raise RuntimeError(f'Revisar fichero {VERSIONFILE} -> Debe incluir la linea __version__ = "a.b.c"')
            sys.stderr.write(f'Revisar fichero {VERSIONFILE} -> Debe incluir la linea __version__ = "a.b.c"\n')
            __version__ = '0.0a0'
        VSRE = r"^__date__ = ['\"]([^'\"]*)['\"]"
        mo = re.search(VSRE, verstrline, re.M)
        mo = re.search(VSRE, verstrline, re.M)
        if mo:
            __date__ = mo.group(1)
        else:
            # raise RuntimeError(f'Revisar fichero {VERSIONFILE} -> Debe incluir la linea __date__ = "year1-year2"')
            sys.stderr.write(f'Revisar fichero {VERSIONFILE} -> Debe incluir la linea __date__ = "year1-year2"\n')
            __date__ = '2016-2022'
        VSRE = r"^__updated__ = ['\"]([^'\"]*)['\"]"
        mo = re.search(VSRE, verstrline, re.M)
        mo = re.search(VSRE, verstrline, re.M)
        if mo:
            __updated__ = mo.group(1)
        else:
            # raise RuntimeError(f'Revisar fichero {VERSIONFILE} -> Debe incluir la linea __updated__ = "date"')
            sys.stderr.write(f'Revisar fichero {VERSIONFILE} -> Debe incluir la linea __updated__ = "date"\n')
            __updated__ = '2022-07-01'
        VSRE = r"^__copyright__ = ['\"]([^'\"]*)['\"]"
        mo = re.search(VSRE, verstrline, re.M)
        mo = re.search(VSRE, verstrline, re.M)
        if mo:
            __copyright__ = mo.group(1)
        else:
            # raise RuntimeError(f'Revisar fichero {VERSIONFILE} -> Debe incluir la linea __copyright__ = "..."')
            sys.stderr.write(f'Revisar fichero {VERSIONFILE} -> Debe incluir la linea __copyright__ = "..."')
            __copyright__ = '@clid 2016-22'
    except:
        sys.stderr.write(f'clidtools.__init__-> no se ha podido leer {VERSIONFILE}\n')
        __version__ = '0.0a0'
        __date__ = '2016-2022'
        __updated__ = '2022-07-01'
        __copyright__ = '@clid 2016-22'
else:
    __version__ = '0.0a0'
    __date__ = '2016-2022'
    __updated__ = '2022-07-01'
    __copyright__ = '@clid 2016-22'
# ==============================================================================

# ==============================================================================
if not '-e' in sys.argv and(
    '-0' in sys.argv
    or '-1' in sys.argv
    or '-2' in sys.argv
    or '-3' in sys.argv
    or '-4' in sys.argv
    or '-Z' in sys.argv
    or '-X' in sys.argv
    or '-C' in sys.argv
    or '-N' in sys.argv
    or '-L' in sys.argv
    or '-D' in sys.argv
    or '-S' in sys.argv
    or '-M' in sys.argv
    or '-R' in sys.argv
    or '-A' in sys.argv
    or '-P' in sys.argv
    or '-T' in sys.argv
    or '-O' in sys.argv
    or '-U' in sys.argv
    or '-I' in sys.argv
    or '-B' in sys.argv
):
    sys.argv.append('-e')
# ==============================================================================


# No se importa nada con: from qlidtwins import *
__all__ = []
# ==============================================================================
# Verbose provisional para la version alpha
if '-vvv' in sys.argv:
    __verbose__ = 3
elif '-vv' in sys.argv:
    __verbose__ = 2
elif '-v' in sys.argv or '--verbose' in sys.argv:
    __verbose__ = 1
else:
    # En eclipse se adopta el valor indicado en Run Configurations -> Arguments
    __verbose__ = 0
# ==============================================================================
if '-q' in sys.argv:
    __quiet__ = 1
    __verbose__ = 0
else:
    __quiet__ = 0
# ==============================================================================
if '-e' in sys.argv or '--extraArguments' in sys.argv:
    TRNS_LEER_EXTRA_ARGS = True
else:
    TRNS_LEER_EXTRA_ARGS = False
TRNS_soloAdmitirOpcionesPermitidas = False
# ==============================================================================
# TB = '\t'
TB = ' ' * 12
TV = ' ' * 3
# ==============================================================================
if (
    'tests/test_' in sys.argv[0]
    or 'tests\\test_' in sys.argv[0]
    or r'tests\test_' in sys.argv[0]
    or '/pytest' in sys.argv[0]
    or r'\pytest' in sys.argv[0]
    or 'prueba' in sys.argv[0]
):
    TRNS_testTwins = True
else:
    TRNS_testTwins = False
# ==============================================================================

# ==============================================================================
# https://docs.python.org/3/library/warnings.html#warning-filter
# https://docs.pytest.org/en/stable/how-to/capture-warnings.html
# warnings.warn()
# ==============================================================================
# https://docs.python.org/3/library/logging.html
# https://docs.python.org/3/howto/logging-cookbook.html#logging-to-multiple-destinations
# https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout
# https://realpython.com/python-logging/
# https://realpython.com/python-logging-source-code/
# ==============================================================================
# myModule = __name__.split('.')[-1]
myModule = os.path.basename(sys.argv[0]).split('.')[0]
myUser = clidconfig.infoUsuario()
# sys.stdout.write(f'\nqlidtwins-> usuario: {myUser}\n')
if sys.argv[0].endswith('__main__.py') and 'cartolidar' in sys.argv[0]:
    # print('qlidtwins-> logFile ya iniciado, se inicia logCons')
    # myLog = clidconfig.iniciaConsLog(myModule=myModule, myVerbose=__verbose__)
    myLog = clidconfig.iniciaConsLog(myModule='qlidtwins', myVerbose=__verbose__)
else:
    myLog = clidconfig.creaLog(consLogYaCreado=False, myModule=myModule, myPath='../data/log', myVerbose=__verbose__, myVerboseFile=__verbose__)
# ==============================================================================
# print(f'qlidtwins->')
# print(f'{TB}-> myLog.name: {myLog.name}')
# print(f'{TB}-> myLog.level: {myLog.level}')
# print(f'{TB}-> myLog.handlers: {myLog.handlers}')
myLog.debug('\n{:_^80}'.format(''))
myLog.debug('qlidtwins-> Debug & alpha version info:')
myLog.debug(f'{TB}-> __verbose__:  <{__verbose__}>')
myLog.debug(f'{TB}-> __package__ : <{__package__ }>')
myLog.debug(f'{TB}-> __name__:     <{__name__}>')
myLog.debug(f'{TB}-> sys.argv:     <{sys.argv}>')
myLog.debug(f'{TB}-> extraArgs:    <{TRNS_LEER_EXTRA_ARGS}>')
myLog.debug(f'{TB}-> testTwins:    <{TRNS_testTwins}>')
myLog.debug('{:=^80}'.format(''))
# ==============================================================================

# ==============================================================================
# El idProceso sirve para dar nombres unicos a los ficheros de configracion y
# asi poder lanzar trabajos paralelos con distintas configuraciones.
# Sin embargo, qlidtwins no esta pensada para lanzar trabajos en paralelo.
# Mantengo el idProceso por si acaso
# ==============================================================================
if '--idProceso' in sys.argv and len(sys.argv) > sys.argv.index('--idProceso') + 1:
    ARGS_idProceso = sys.argv[sys.argv.index('--idProceso') + 1]
else:
    # ARGS_idProceso = str(random.randint(1, 999998))
    ARGS_idProceso = '999999'
    sys.argv.append('--idProceso')
    sys.argv.append(ARGS_idProceso)
# ==============================================================================
if type(ARGS_idProceso) == int:
    MAIN_idProceso = ARGS_idProceso
elif type(ARGS_idProceso) == str:
    try:
        MAIN_idProceso = int(ARGS_idProceso)
    except:
        print(f'qlidtwins-> ATENCION: revisar asignacion de idProceso.')
        print(f'ARGS_idProceso: {type(ARGS_idProceso)} {ARGS_idProceso}')
        print(f'sys.argv: {sys.argv}')
else:
    MAIN_idProceso = 0
    print(f'qlidtwins-> ATENCION: revisar codigo de idProceso.')
    print(f'ARGS_idProceso: {type(ARGS_idProceso)} {ARGS_idProceso}')
    print(f'sys.argv: {sys.argv}')
# ==============================================================================


# ==============================================================================
# ============================ Constantes globales =============================
# ==============================================================================
TESTRUN = 0
PROFILE = 0
TRNS_preguntarPorArgumentosEnLineaDeComandos = __verbose__ > 1
# ==============================================================================


# ==============================================================================
# Gestion de errores de argumentos en linea de comandos con argparse
class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = f'qlidtwins-> ATENCION - error: {msg}' 
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg


# ==============================================================================
def checkRun():
    '''Chequeo de la forma de ejecucion. Provisional para la version alpha'''
    # ==========================================================================
    tipoEjecucion = 0
    myLog.debug('')
    myLog.debug('{:_^80}'.format(''))
    try:
        if len(sys.argv) == 0:
            myLog.critical(f'qlidtwins-> Revisar esta forma de ejecucion. sys.argv: <{sys.argv}>')
            sys.exit(0)
        elif sys.argv[0].endswith('__main__.py') and 'cartolidar' in sys.argv[0]:
            # Tb cumple:
            # __name__:    <cartolidar.qlidtwins>
            # __package__: <cartolidar>
            tipoEjecucion = 1
            myLog.debug('qlidtwins.py se ejecuta lanzando el paquete cartolidar desde linea de comandos:')
            myLog.debug(f'{TB} python -m cartolidar')
        elif sys.argv[0].endswith('qlidtwins.py'):
            tipoEjecucion = 2
            myLog.debug('qlidtwins.py se ha lanzado desde linea de comandos:')
            myLog.debug(f'{TB} python qlidtwins.py')
        elif sys.argv[0] == '':
            tipoEjecucion = 3
            # Al importar el modulo no se pueden incluir el argumento -v (ni ningun otro)
            myLog.debug('qlidtwins se esta importando desde el interprete interactivo:')
            myLog.debug(f'{TB}>>> from cartolidar import qlidtwins')
            myLog.debug('o, si esta accesible (en el path):')
            myLog.debug(f'{TB}>>> import qlidtwins')
        else:
            tipoEjecucion = 4
            myLog.debug(f'checkRun-> qlidtwins.py se esta importando desde el modulo: {sys.argv[0]}')
    except:
        # myLog.critical(qlidtwins-> Revisar MAIN_idProceso:', exc_info=True)
        myLog.exception('qlidtwins-> Revisar MAIN_idProceso:')
        myLog.critical(f'MAIN_idProceso: <{MAIN_idProceso}> type: {type(MAIN_idProceso)}')
        myLog.critical(f'sys.argv:       <{sys.argv}>')
    # ==========================================================================

    if sys.argv[0] == '':
        if __verbose__ > 1:
            myLog.warning('AVISO: clidqins.py es un modulo escrito para ejecutarse desde linea de comandos:')
            myLog.warning(f'{TB}  python -m cartolidar')
            myLog.warning('o bien:')
            myLog.warning(f'{TB}  python qlidtwins.py')
            myLog.warning('Sin embargo, se esta importando desde el interprete interactivo de python y')
            myLog.warning('no se pueden incluir argumentos en linea de comandos.')
            myLog.warning(f'Se usa fichero de configuracion: {GLO.configFileNameCfg}')
            myLog.warning('(si existe) o configuracion por defecto (en caso contrario).')
            if __verbose__ > 1:
                selec = input('\r\nLanzar el modulo como si se ejecutara desde linea de comandos (S/n): ')
            else:
                selec = 's'
        else:
            selec = 's'
    elif len(sys.argv) == 3 and TRNS_preguntarPorArgumentosEnLineaDeComandos:
        myLog.warning('AVISO: no se han introducido argumentos en linea de comandos')
        myLog.warning(f'{TB}-> Para obtener ayuda sobre estos argumentos escribir:')
        myLog.warning(f'{TB}{TV}python {os.path.basename(sys.argv[0])} -h')
        selec = input('\nContinuar con la configuracion por defecto? (S/n): ')
    else:
        selec = 's'

    if (
        'qlidtwins' in __name__
        or (len(sys.argv) == 3 and TRNS_preguntarPorArgumentosEnLineaDeComandos)
    ):
        try:
            if selec.upper() == 'N':
                sys.argv.append("-h")
                myLog.debug('')
        except (Exception) as thisError: # Raised when a generated error does not fall into any category.
            # myLog.critical(f'\nqlidtwins-> ATENCION: revisar codigo. selec: {type(selec)}´<{selec}>', exc_info=True)
            myLog.exception(f'\nqlidtwins-> ATENCION: revisar codigo. selec: {type(selec)}´<{selec}>')
            myLog.critical(f'{TB}Revisar error: {thisError}')
            sys.exit(0)
    myLog.debug('{:=^80}'.format(''))

    return tipoEjecucion


# ==============================================================================
def testRun():
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'qlidtwins_profile.txt'
        cProfile.run('leerArgumentosEnLineaDeComandos()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)


# ==============================================================================
def leerArgumentosEnLineaDeComandos(argv: list = None) -> argparse.Namespace:
    '''Command line options.
    These arguments take precedence over configuration file
    and over default parameters.
    '''
    # https://peps.python.org/pep-3107/#syntax
    # https://stackoverflow.com/questions/38727520/how-do-i-add-default-parameters-to-functions-when-using-type-hinting

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    listaMainArgs = (
        'extraArguments', 'mainAction',
        'rutaAscRaizBase', 'rutaCompletaMFE', 'cartoMFEcampoSp',
        'patronVectrName', 'patronLayerName', 'patronFieldName',
        'testeoVectrName', 'testeoLayerName',
    )
    listaExtraArgs = (
        'menuInteractivo', 'marcoCoordMiniX', 'marcoCoordMaxiX', 'marcoCoordMiniY',
        'marcoCoordMaxiY', 'marcoPatronTest', 'nPatronDasoVars', 'rasterPixelSize',
        'radioClusterPix', 'nivelSubdirExpl', 'outRasterDriver', 'outputSubdirNew',
        'cartoMFErecorte', 'varsTxtFileName', 'ambitoTiffNuevo', 'noDataTiffProvi',
        'noDataTiffFiles', 'noDataTipoDMasa', 'umbralMatriDist', 'distMaxScipyAdm',
        'compilaConNumba',
    )

    program_name = os.path.basename(sys.argv[0])
    program_version = 'v{}'.format(__version__)
    program_build_date = str(__updated__)
    program_version_message = '{} {} ({})'.format(program_name, program_version, program_build_date)
    # program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    # program_shortdesc = __import__('__main__').__doc__
    program_shortdesc = '''  qlidtwins searchs for similar areas to a reference one in terms of
  lidar variables that characterize forest structure (dasoLidar variables).
  Utility included in cartolidar suite.'''

    program_license = '''{}

  Created by @clid {}.
  Licensed GNU General Public License v3 (GPLv3) https://fsf.org/
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.
'''.format(program_shortdesc, str(__date__))

    # ==========================================================================
    # https://docs.python.org/es/3/howto/argparse.html
    # https://docs.python.org/3/library/argparse.html
    # https://ellibrodepython.com/python-argparse
    try:
        # Setup argument parser
        parser = ArgumentParser(
            description=program_license,
            formatter_class=RawDescriptionHelpFormatter,
            fromfile_prefix_chars='@',
            )

        # Opciones:
        parser.add_argument('-V', '--version',
                            action='version',
                            version=program_version_message,)
        parser.add_argument('-v', '--verbose',
                            dest='verbose',
                            action='count', # Cuenta el numero de veces que aparece la v (-v, -vv, -vvv, etc.)
                            # action="store_true",
                            help='set verbosity level [default: %(default)s]',
                            default = GLO.GLBLverbose,)
        parser.add_argument('-q', '--quiet',
                            dest='quietMode',
                            action="store_false",
                            help='Activates quiet mode (mude, not output). Default: %(default)s',
                            default = __quiet__,)
        parser.add_argument('-e', '--extraArguments',
                            dest='extraArguments',
                            # action='count', # Cuenta el numero de veces que aparece la e (-e, -ee, etc.)
                            action="store_false",
                            help='Activates extra arguments in command line. Default: %(default)s',
                            default = TRNS_LEER_EXTRA_ARGS,)
        if TRNS_soloAdmitirOpcionesPermitidas:
            optionsHelp = 'Opciones del menu principal cuando se ejecuta con python -m cartolidar'
            parser.add_argument('-o',  # '--option',
                                dest='menuOption',
                                type=int,
                                help=f'{optionsHelp}. Default: %(default)s',
                                default = '0',)

        parser.add_argument('-a',  # '--action',
                            dest='mainAction',
                            type=int,
                            help='Accion a ejecutar: \n1. Verificar analogia con un determinado patron dasoLidar; \n2. Generar raster con presencia de un determinado patron dasoLidar. Default: %(default)s',
                            default = GLO.GLBLaccionPrincipalPorDefecto,)
        parser.add_argument('-I',  '--menuInteractivo',
                            dest='menuInteractivo',
                            action="store_true",
                            # type=int,
                            help='La aplicacion pregunta en tiempo de ejecucion para elegir o confirmar opciones. Default: %(default)s',
                            default = GLO.GLBLmenuInteractivoPorDefecto,)

        parser.add_argument('-i',  # '--inputpath',
                            dest='rutaAscRaizBase',
                            help='Ruta (path) en la que estan los ficheros de entrada con las variables dasolidar. Default: %(default)s',
                            default = GLO.GLBLrutaAscRaizBasePorDefecto,)

        parser.add_argument('-p',  # '--patron',
                            dest='patronVectrName',
                            help='Nombre del poligono de referencia (patron) para caracterizacion dasoLidar. Default: %(default)s',
                            default = GLO.GLBLpatronVectrNamePorDefecto,)
        parser.add_argument('-l',  # '--patronLayer',
                            dest='patronLayerName',
                            help='Nombre del layer del gpkg (en su caso) de referencia (patron) para caracterizacion dasoLidar. Default: %(default)s',
                            default = GLO.GLBLpatronLayerNamePorDefecto,)
        parser.add_argument('-c',  # '--patronField',
                            dest='patronFieldName',
                            help='Nombre del campo de la capa de referencia (patron) con el tipo de masa para caracterizacion dasoLidar. Default: %(default)s',
                            default = GLO.GLBLpatronFieldNamePorDefecto,)
        parser.add_argument('-t',  # '--testeo',
                            dest='testeoVectrName',
                            help='Nombre del poligono de contraste (testeo) para verificar su analogia con el patron dasoLidar. Default: %(default)s',
                            default = GLO.GLBLtesteoVectrNamePorDefecto,)
        parser.add_argument('-y',  # '--testeoLayer',
                            dest='testeoLayerName',
                            help='Nombre del layer del gpkg (en su caso) de contraste (testeo) para verificar su analogia con el patron dasoLidar. Default: %(default)s',
                            default = GLO.GLBLtesteoLayerNamePorDefecto,)

        parser.add_argument('-m',  # '--mfepath',
                            dest='rutaCompletaMFE',
                            help='Nombre (con ruta y extension) del fichero con la capa MFE. Default: %(default)s',
                            default = GLO.GLBLrutaCompletaMFEPorDefecto,)
        parser.add_argument('-f',  # '--mfefield',
                            dest='cartoMFEcampoSp',
                            help='Nombre del campo con el codigo numerico de la especie principal o tipo de bosque en la capa MFE. Default: %(default)s',
                            default = GLO.GLBLcartoMFEcampoSpPorDefecto,)

        # ======================================================================
        if TRNS_LEER_EXTRA_ARGS:
            parser.add_argument('-1',  # '--marcoCoordMiniX',
                                dest='marcoCoordMiniX',
                                type=float,
                                help='Limite inferior X para delimitar la zona de analisis. Default: %(default)s',
                                default = GLO.GLBLmarcoCoordMiniXPorDefecto,)
            parser.add_argument('-2',  # '--marcoCoordMaxiX',
                                dest='marcoCoordMaxiX',
                                type=float,
                                help='Limite superior X para delimitar la zona de analisis. Default: %(default)s',
                                default = GLO.GLBLmarcoCoordMaxiXPorDefecto,)
            parser.add_argument('-3',  # '--marcoCoordMiniY',
                                dest='marcoCoordMiniY',
                                type=float,
                                help='Limite inferior Y para delimitar la zona de analisis. Default: %(default)s',
                                default = GLO.GLBLmarcoCoordMiniYPorDefecto,)
            parser.add_argument('-4',  # '--marcoCoordMaxiY',
                                dest='marcoCoordMaxiY',
                                type=float,
                                help='Limite superior Y para delimitar la zona de analisis. Default: %(default)s',
                                default = GLO.GLBLmarcoCoordMaxiYPorDefecto,)
            parser.add_argument('-Z',  # '--marcoPatronTest',
                                dest='marcoPatronTest',
                                type=int,
                                help='Zona de analisis definida por la envolvente de los poligonos de referencia (patron) y de chequeo (testeo). Default: %(default)s',
                                default = GLO.GLBLmarcoPatronTestPorDefecto,)

            parser.add_argument('-X',  # '--pixelsize',
                                dest='rasterPixelSize',
                                type=int,
                                help='Lado del pixel dasometrico en metros (pte ver diferencia con GLBLmetrosCelda). Default: %(default)s',
                                default = GLO.GLBLrasterPixelSizePorDefecto,)
            parser.add_argument('-C',  # '--clustersize',
                                dest='radioClusterPix',
                                type=int,
                                help='Numero de anillos de pixeles que tiene el cluster, ademas del central. Default: %(default)s',
                                default = GLO.GLBLradioClusterPixPorDefecto,)

            parser.add_argument('-N',  # '--numvars',
                                dest='nPatronDasoVars',
                                type=int,
                                help='Si es distinto de cero, numero de dasoVars con las que se caracteriza el patron (n primeras dasoVars). Default: %(default)s',
                                default = GLO.GLBLnPatronDasoVarsPorDefecto,)
            parser.add_argument('-L',  # '--level',
                                dest='nivelSubdirExpl',
                                type=int,
                                help='nivel de subdirectorios a explorar para buscar ficheros de entrada con las variables dasolidar. Default: %(default)s',
                                default = GLO.GLBLnivelSubdirExplPorDefecto,)
            parser.add_argument('-D',  # '--outrasterdriver',
                                dest='outRasterDriver',
                                type=str,
                                help='Nombre gdal del driver para el formato de fichero raster de salida para el dasolidar. Default: %(default)s',
                                default = GLO.GLBLoutRasterDriverPorDefecto,)
            parser.add_argument('-S',  # '--outsubdir',
                                dest='outputSubdirNew',
                                type=str,
                                help='Subdirectorio de GLBLrutaAscRaizBasePorDefecto donde se guardan los resultados. Default: %(default)s',
                                default = GLO.GLBLoutputSubdirNewPorDefecto,)
            parser.add_argument('-M',  # '--clipMFEfilename',
                                dest='cartoMFErecorte',
                                type=str,
                                help='Nombre del fichero en el que se guarda la version recortada raster del MFE. Default: %(default)s',
                                default = GLO.GLBLcartoMFErecortePorDefecto,)
            parser.add_argument('-R',  # '--rangovarsfilename',
                                dest='varsTxtFileName',
                                type=str,
                                help='Nombre de fichero en el que se guardan los intervalos calculados para todas las variables. Default: %(default)s',
                                default = GLO.GLBLvarsTxtFileNamePorDefecto,)
    
            parser.add_argument('-A',  # '--ambitoTiffNuevo',
                                dest='ambitoTiffNuevo',
                                type=str,
                                help='Tipo de ambito para el rango de coordenadas (loteASC, CyL, CyL_nw, etc). Default: %(default)s',
                                default = GLO.GLBLambitoTiffNuevoPorDefecto,)
    
            parser.add_argument('-P',  # '--noDataTiffProvi',
                                dest='noDataTiffProvi',
                                type=int,
                                help='NoData temporal para los ficheros raster de salida para el dasolidar. Default: %(default)s',
                                default = GLO.GLBLnoDataTiffProviPorDefecto,)
            parser.add_argument('-T',  # '--noDataTiffFiles',
                                dest='noDataTiffFiles',
                                type=int,
                                help='NoData definitivo para los ficheros raster de salida para el dasolidar. Default: %(default)s',
                                default = GLO.GLBLnoDataTiffFilesPorDefecto,)
            parser.add_argument('-O',  # '--noDataTipoDMasa',
                                dest='noDataTipoDMasa',
                                type=int,
                                help='NoData definitivo para el raster de salida con el tipo de masa para el dasolidar. Default: %(default)s',
                                default = GLO.GLBLnoDataTipoDMasaPorDefecto,)
            parser.add_argument('-U',  # '--umbralMatriDist',
                                dest='umbralMatriDist',
                                type=int,
                                help='Umbral de distancia por debajo del cual se considera que una celda es parecida a otra enla matriz de distancias entre dasoVars. Default: %(default)s',
                                default = GLO.GLBLumbralMatriDistPorDefecto,)
            parser.add_argument('-Y',  # '--distMaxScipyAdm',
                                dest='distMaxScipyAdm',
                                type=int,
                                help='Umbral de distancia Scipy (entre histogramas) por encima del cual se descarta que una celda sea parecida a la patron aunque sea la de distancia minima. Default: %(default)s',
                                default = GLO.GLBLdistMaxScipyAdmPorDefecto,)
            parser.add_argument('-B',  # '--compilaConNumba',
                                dest='compilaConNumba',
                                type=int,
                                help='Activar el compilado numba con LLVM. Requiere numba == 0.53.0, llvmlite 0.36.0 y NumPy >=1.15 (si numba=0.55.0 -> NumPy >=1.18,<1.23). Default: %(default)s',
                                default = GLO.GLBLcompilaConNumbaPorDefecto,)

        parser.add_argument('--idProceso',
                            dest='idProceso',
                            type=int,
                            help='Numero aleatorio para identificar el proceso que se esta ejecutando (se asigna automaticamente; no usar este argumento)',)

        # Argumentos posicionales:
        # Opcionales
        parser.add_argument(dest='listTxtDasoVars',
                            help='Lista de variables dasoLidar: '
                            'Secuencia de cadenas de texto (uno por variable), del tipo: '
                            '"texto1", "texto2", etc. de forma que: '
                            '    Opcion a: cada texto es un identificador de DLV. Ejemplo: alt95 fcc05 fcc03 (no llevan comas ni comillas) ' 
                            '    Opcion b: cada texto es una secuencia de cinco elementos separados por comas del tipo: '
                            '        "FileTypeId, NickName, RangoLinf, RangoLsup, NumClases, Movilidad(0-100), Ponderacion(0-10)" '
                            '        Ejemplo: ["alt95,hDom,0,36,18,40,10", "fcc05,FCC,0,100,5,30,8"] '
                            '[default: %(default)s]',
                            default = GLO.GLBLlistTxtDasoVarsPorDefecto,
                            nargs='*') # Admite entre 0 y n valores
        # Obligatorios:
        # parser.add_argument('uniParam',
        #                     help='Un parametro unico.',)
        # parser.add_argument(dest='paths',
        #                     help='paths to folder(s) with source file(s)',
        #                     metavar='path',
        #                     nargs='+') # Admite entre 0 y n valores

        # Process arguments
        if TRNS_soloAdmitirOpcionesPermitidas:
            argsConfig = parser.parse_args()
        else:
            argsConfig, unknown = parser.parse_known_args()
            if __verbose__ == 3:
                myLog.debug('{:_^80}'.format(''))
                myLog.debug(f'qlidtwins-> Argumentos leidos en linea de comandos y/o fichero de configuracion ({type(argsConfig)}):')
                myLog.debug(f'{TB}{argsConfig}')
            if not unknown is None and unknown != []:
                myLog.debug(f'qlidtwins-> Argumentos ignorados: {type(unknown)} {unknown}')
                myLog.debug(f'{TB}-> Revisando argumentos ignorados:')
            if type(unknown) == list and unknown != []:
                for argumentoIgnorado in unknown:
                    if argumentoIgnorado in sys.argv:
                        myLog.debug(f'{TB}-> argumentoIgnorado: {argumentoIgnorado}')
                    if argumentoIgnorado in sys.argv and len(sys.argv) > sys.argv.index(argumentoIgnorado) + 1:
                        valorDelArgumentoIgnorado = sys.argv[sys.argv.index(argumentoIgnorado) + 1]
                        if valorDelArgumentoIgnorado[0] != '-':
                            myLog.debug(f'{TB}{TV}-> Eliminando valorDelArgumentoIgnorado: {valorDelArgumentoIgnorado}')
                            if __verbose__ == 3:
                                myLog.debug(f'{TB}{TV}{TV}-> sys.argv pre:  {sys.argv}')
                            del sys.argv[sys.argv.index(argumentoIgnorado) + 1]
                            if __verbose__ == 3:
                                myLog.debug(f'{TB}{TV}{TV}-> sys.argv post: {sys.argv}')
                            if argsConfig.listTxtDasoVars == [valorDelArgumentoIgnorado]:
                                if __verbose__ == 3:
                                    myLog.debug(f'{TB}{TV}-> Este valor se habia asignado a listTxtDasoVars: {argsConfig.listTxtDasoVars}')
                                    myLog.debug(f'{TB}{TV}{TV}-> Se elimina ese valor y asigna el valor por defecto')
                                try:
                                    del argsConfig.listTxtDasoVars
                                    # myLog.debug('borrado ok2')
                                except:
                                    del argsConfig['listTxtDasoVars']
                                    myLog.debug(f'\nqlidtwins-> No se ha podido borrar el argumento {argumentoIgnorado}. Revisar codigo.')
                                argsConfig.listTxtDasoVars = GLO.GLBLlistTxtDasoVarsPorDefecto
                                if __verbose__ == 3:
                                    myLog.debug(f'{TB}{TV}-> Valor asignado a listTxtDasoVars: {argsConfig.listTxtDasoVars}')
                            elif valorDelArgumentoIgnorado in argsConfig.listTxtDasoVars:
                                (argsConfig.listTxtDasoVars).remove(valorDelArgumentoIgnorado)
                    if argumentoIgnorado in sys.argv:
                        myLog.debug(f'{TB}{TV}-> Eliminando argumentoIgnorado: {argumentoIgnorado}')
                        if __verbose__ == 3:
                            myLog.debug(f'{TB}{TV}{TV}-> sys.argv pre:  {sys.argv}')
                        del sys.argv[sys.argv.index(argumentoIgnorado)]
                        if __verbose__ == 3:
                            myLog.debug(f'{TB}{TV}{TV}-> sys.argv post: {sys.argv}')
            if __verbose__ == 3:
                myLog.debug(f'{TB}-> argsConfig post: {argsConfig}')
            myLog.debug('{:=^80}'.format(''))

    except KeyboardInterrupt:
        program_name = 'qlidtwins.py'
        clidtwcfg.mensajeError(program_name)
        sys.exit(0)

    except Exception as excpt:
        if TESTRUN:
            raise(excpt)
        program_name = 'qlidtwins.py'
        clidtwcfg.mensajeError(program_name)
        sys.exit(0)

    # ==========================================================================
    # Si no TRNS_LEER_EXTRA_ARGS, ArgumentParser no asigna
    # el valor por defecto a estos argumentos extras en linea de comandos.
    # Se asignan los valores del archivo cfg o por defecto.
    if not 'menuInteractivo' in dir(argsConfig):
        argsConfig.menuInteractivo = GLO.GLBLmenuInteractivoPorDefecto
    if not 'marcoCoordMiniX' in dir(argsConfig):
        argsConfig.marcoCoordMiniX = GLO.GLBLmarcoCoordMiniXPorDefecto
    if not 'marcoCoordMaxiX' in dir(argsConfig):
        argsConfig.marcoCoordMaxiX = GLO.GLBLmarcoCoordMaxiXPorDefecto
    if not 'marcoCoordMiniY' in dir(argsConfig):
        argsConfig.marcoCoordMiniY = GLO.GLBLmarcoCoordMiniYPorDefecto
    if not 'marcoCoordMaxiY' in dir(argsConfig):
        argsConfig.marcoCoordMaxiY = GLO.GLBLmarcoCoordMaxiYPorDefecto
    if not 'marcoPatronTest' in dir(argsConfig):
        argsConfig.marcoPatronTest = GLO.GLBLmarcoPatronTestPorDefecto
    if not 'nPatronDasoVars' in dir(argsConfig):
        argsConfig.nPatronDasoVars = GLO.GLBLnPatronDasoVarsPorDefecto
    if not 'rasterPixelSize' in dir(argsConfig):
        argsConfig.rasterPixelSize = GLO.GLBLrasterPixelSizePorDefecto
    if not 'radioClusterPix' in dir(argsConfig):
        argsConfig.radioClusterPix = GLO.GLBLradioClusterPixPorDefecto
    if not 'nivelSubdirExpl' in dir(argsConfig):
        argsConfig.nivelSubdirExpl = GLO.GLBLnivelSubdirExplPorDefecto
    if not 'outRasterDriver' in dir(argsConfig):
        argsConfig.outRasterDriver = GLO.GLBLoutRasterDriverPorDefecto
    if not 'outputSubdirNew' in dir(argsConfig):
        argsConfig.outputSubdirNew = GLO.GLBLoutputSubdirNewPorDefecto
    if not 'cartoMFErecorte' in dir(argsConfig):
        argsConfig.cartoMFErecorte = GLO.GLBLcartoMFErecortePorDefecto
    if not 'varsTxtFileName' in dir(argsConfig):
        argsConfig.varsTxtFileName = GLO.GLBLvarsTxtFileNamePorDefecto
    if not 'ambitoTiffNuevo' in dir(argsConfig):
        argsConfig.ambitoTiffNuevo = GLO.GLBLambitoTiffNuevoPorDefecto
    if not 'noDataTiffProvi' in dir(argsConfig):
        argsConfig.noDataTiffProvi = GLO.GLBLnoDataTiffProviPorDefecto
    if not 'noDataTiffFiles' in dir(argsConfig):
        argsConfig.noDataTiffFiles = GLO.GLBLnoDataTiffFilesPorDefecto
    if not 'noDataTipoDMasa' in dir(argsConfig):
        argsConfig.noDataTipoDMasa = GLO.GLBLnoDataTipoDMasaPorDefecto
    if not 'umbralMatriDist' in dir(argsConfig):
        argsConfig.umbralMatriDist = GLO.GLBLumbralMatriDistPorDefecto
    if not 'distMaxScipyAdm' in dir(argsConfig):
        argsConfig.distMaxScipyAdm = GLO.GLBLdistMaxScipyAdmPorDefecto
    if not 'compilaConNumba' in dir(argsConfig):
        argsConfig.compilaConNumba = GLO.GLBLcompilaConNumbaPorDefecto

    for myMainArg in listaMainArgs:
        if not myMainArg in dir(argsConfig):
            myLog.critical('qlidtwins-> Revisar codigo para que lea todos los argumentos principales por defecto.')
            sys.exit(0)

    for myExtraArg in listaExtraArgs:
        if not myExtraArg in dir(argsConfig):
            myLog.critical('qlidtwins-> Revisar codigo para que lea todos los argumentos extras por defecto.')
            sys.exit(0)

    return argsConfig


# ==============================================================================
def saveArgs(args: argparse.Namespace) -> str:
    if (GLO.configFileNameCfg).endswith('.cfg'):
        argsFileName = (GLO.configFileNameCfg).replace('.cfg', '.args')
    elif sys.argv[0].endswith('.py'):
        argsFileName = sys.argv[0].replace('.py', '.args')
    elif sys.argv[0].endswith('pytest'):
        argsFileName = 'argsForTest.cfg'
    else:
        argsFileName = 'unknownLaunch.cfg'
    try:
        with open(argsFileName, mode='w+') as argsFileControl:
            argsFileControl.write(f'# sys.argv[0]={sys.argv[0]}\n')
            argsFileControl.write(f'# argsFileName={argsFileName}\n')
            if 'mainAction' in dir(args):
                argsFileControl.write(f'-a={args.mainAction}\n')
            if 'rutaAscRaizBase' in dir(args):
                argsFileControl.write(f'-i={args.rutaAscRaizBase}\n')
            if 'rutaCompletaMFE' in dir(args):
                argsFileControl.write(f'-m={args.rutaCompletaMFE}\n')
            if 'cartoMFEcampoSp' in dir(args):
                argsFileControl.write(f'-f={args.cartoMFEcampoSp}\n')
            if 'patronVectrName' in dir(args):
                argsFileControl.write(f'-p={args.patronVectrName}\n')
            if 'patronLayerName' in dir(args):
                argsFileControl.write(f'-l={args.patronLayerName}\n')
            if 'patronFieldName' in dir(args):
                argsFileControl.write(f'-l={args.patronFieldName}\n')
            if 'testeoVectrName' in dir(args):
                argsFileControl.write(f'-t={args.testeoVectrName}\n')
            if 'testeoLayerName' in dir(args):
                argsFileControl.write(f'-y={args.testeoLayerName}\n')
            if 'verbose' in dir(args):
                argsFileControl.write(f'-v={__verbose__}\n')

            if 'menuInteractivo' in dir(args):
                argsFileControl.write(f'-0={args.menuInteractivo}\n')

            if 'marcoCoordMiniX' in dir(args):
                argsFileControl.write(f'-1={args.marcoCoordMiniX}\n')
            if 'marcoCoordMaxiX' in dir(args):
                argsFileControl.write(f'-2={args.marcoCoordMaxiX}\n')
            if 'marcoCoordMiniY' in dir(args):
                argsFileControl.write(f'-3={args.marcoCoordMiniY}\n')
            if 'marcoCoordMaxiY' in dir(args):
                argsFileControl.write(f'-4={args.marcoCoordMaxiY}\n')
            if 'marcoPatronTest' in dir(args):
                argsFileControl.write(f'-Z={args.marcoPatronTest}\n')

            if 'rasterPixelSize' in dir(args):
                argsFileControl.write(f'-X={args.rasterPixelSize}\n')
            if 'radioClusterPix' in dir(args):
                argsFileControl.write(f'-C={args.radioClusterPix}\n')
            if 'nPatronDasoVars' in dir(args):
                argsFileControl.write(f'-N={args.nPatronDasoVars}\n')
            if 'nivelSubdirExpl' in dir(args):
                argsFileControl.write(f'-L={args.nivelSubdirExpl}\n')
            if 'outRasterDriver' in dir(args):
                argsFileControl.write(f'-D={args.outRasterDriver}\n')
            if 'outputSubdirNew' in dir(args):
                argsFileControl.write(f'-S={args.outputSubdirNew}\n')
            if 'cartoMFErecorte' in dir(args):
                argsFileControl.write(f'-M={args.cartoMFErecorte}\n')
            if 'varsTxtFileName' in dir(args):
                argsFileControl.write(f'-R={args.varsTxtFileName}\n')
            if 'ambitoTiffNuevo' in dir(args):
                argsFileControl.write(f'-A={args.ambitoTiffNuevo}\n')
            if 'noDataTiffProvi' in dir(args):
                argsFileControl.write(f'-P={args.noDataTiffProvi}\n')
            if 'noDataTiffFiles' in dir(args):
                argsFileControl.write(f'-T={args.noDataTiffFiles}\n')
            if 'noDataTipoDMasa' in dir(args):
                argsFileControl.write(f'-O={args.noDataTipoDMasa}\n')
            if 'umbralMatriDist' in dir(args):
                argsFileControl.write(f'-U={args.umbralMatriDist}\n')
            if 'distMaxScipyAdm' in dir(args):
                argsFileControl.write(f'-I={args.distMaxScipyAdm}\n')
            if 'compilaConNumba' in dir(args):
                argsFileControl.write(f'-B={args.compilaConNumba}\n')

            for miDasoVar in args.listTxtDasoVars:
                argsFileControl.write(f'{miDasoVar}\n')
    except:
        myLog.warning(f'\nqlidtwins-> No se ha podido crear el fichero de argumentos para linea de comandos: {argsFileName}')

    return argsFileName


# ==============================================================================
def creaConfigDict(
        args,
        tipoEjecucion=0,
    ):
    """
    Se crea el diccionario usando los argumentos leidos en linea de comandos
    o, en su defecto, los valores por defecto del fichero de configuracion
    o, en su defecto, los valores por defecto del modulo clidtwcfg.py
    """
    cfgDict = {}
    # Parametros de configuracion principales
    cfgDict['mainAction'] = args.mainAction

    cfgDict['rutaAscRaizBase'] = getParametroConPath(
        args.rutaAscRaizBase,
        dataBasePath=os.getcwd(),
        nombreParametro='rutaAscRaizBase',
        )

    cfgDict['rutaCompletaMFE'] = getParametroConPath(
        args.rutaCompletaMFE,
        dataBasePath=os.getcwd(),
        nombreParametro='rutaCompletaMFE',
        )
    cfgDict['cartoMFEcampoSp'] = args.cartoMFEcampoSp

    cfgDict['patronVectrName'] = getParametroConPath(
        args.patronVectrName,
        dataBasePath=os.getcwd(),
        nombreParametro='patronVectrName',
        )
    if args.patronLayerName == 'None':
        cfgDict['patronLayerName'] = None
    else:
        cfgDict['patronLayerName'] = args.patronLayerName
    if args.patronFieldName == 'None':
        cfgDict['patronFieldName'] = None
    else:
        cfgDict['patronFieldName'] = args.patronFieldName

    if args.testeoVectrName == '':
        print('qlidtwins-> Se requiere el argumento testeoVectrName')
        sys.exit(0)
    else:
        if ':' in args.testeoVectrName or args.testeoVectrName.startswith('/'):
            # El parametro testeoVectrName es una ruta absoluta
            cfgDict['testeoVectrName'] = args.testeoVectrName
        else:
            # El parametro testeoVectrName es una ruta relativa.
            # Supongo que:
            #   O bien cartolidar se ejecuta con -m o esa ruta esta referida al directorio de trabajo.
            #   O bien se ejecuta directamente qlidtiwns y el directorio de trabajo es el que contiene a ese modulo.
            if '__main__.py' in sys.argv[0]:
                cfgDict['testeoVectrName'] = os.path.abspath(os.path.join(os.getcwd(), 'cartolidar', args.testeoVectrName))
            # elif 'qlidtwins.py' in sys.argv[0]:
            else:
                cfgDict['testeoVectrName'] = os.path.abspath(os.path.join(os.getcwd(), args.testeoVectrName))
    if args.testeoLayerName == 'None':
        cfgDict['testeoLayerName'] = None
    else:
        cfgDict['testeoLayerName'] = args.testeoLayerName

    # print('\nqlidtwins-> Chequeo algunas variables:')
    # print('qlidtwins->->->-> sys.argv[0]:', sys.argv[0])
    # print('qlidtwins->->->-> os.getcwd():', os.getcwd())
    # print('qlidtwins->->->-> args.rutaAscRaizBase:', args.rutaAscRaizBase)
    # print('                                       ', cfgDict['rutaAscRaizBase'])
    # print('qlidtwins->->->-> args.rutaCompletaMFE:', args.rutaCompletaMFE)
    # print('                                       ', cfgDict['rutaCompletaMFE'])
    # print('qlidtwins->->->-> args.patronVectrName:', args.patronVectrName)
    # print('                                       ', cfgDict['patronVectrName'])
    # print('qlidtwins->->->-> args.testeoVectrName:', args.testeoVectrName)
    # print('                                       ', cfgDict['testeoVectrName'])


    if __verbose__ == 3:
        myLog.debug(f'qlidtwins-> args.listTxtDasoVars ({type(args.listTxtDasoVars)}) -> {args.listTxtDasoVars}')
        numElementosPorDasoVarEnArgumentoListTxtDasoVars = len((args.listTxtDasoVars[0]).split(","))
        myLog.debug(f'{TB}El primer argumento posicional tiene {numElementosPorDasoVarEnArgumentoListTxtDasoVars} elementos: {(args.listTxtDasoVars[0]).split(",")}')
        myLog.debug('{:=^80}'.format(''))

    # args.listTxtDasoVars es una lista de cadenas (argumentos posicionales)
    if len((args.listTxtDasoVars[0]).split(',')) == 1:
        # Los argumentos posicionales son simplificados, solo incluyen FileTypeId
        # Los textos de la lista de textos se usa directamente son los FileTypeId
        # cfgDict['listLstDasoVars'] = args.listTxtDasoVars
        cfgDict['listaTxtDasoVarsFileTypes'] = args.listTxtDasoVars
        if __verbose__ == 3 and (tipoEjecucion == 1 or tipoEjecucion == 2):
            myLog.debug(f'\nqlidtwins-> Los argumentos posicionales (listTxtDasoVars) son una secuencia de FileTypeId')
    else:
        args_listLstDasoVars = []
        # Argumentos posicionales completos: FileTypeId,NickName,RangoLinf,RangoLsup,NumClases,Movilidad,Ponderacion
        # La lista de textos se convierte a lista de listas y el primer elemento de esas listas es FileTypeId
        for numDasoVar, txtListaDasovar in enumerate(args.listTxtDasoVars):
            # Los argumentos posicionales son completos:
            # "FileTypeId, NickName, RangoLinf, RangoLsup, NumClases, Movilidad(0-100), Ponderacion(0-10)"
            listDasoVar = [item.strip() for item in txtListaDasovar.split(',')]
            if len(listDasoVar) <= 5:
                myLog.error(f'\nqlidtwins-> ATENCION: el argumento posicional (listTxtDasoVars) debe ser una')
                myLog.error(f'{TB} Secuencia (uno por variable) de cadenas de texto separados por espacios del tipo:')
                myLog.error(f'{TB}     texto1 texto2 ...')
                myLog.error(f'{TB} Los elementos de esta secuencia deben ser:')
                myLog.error(f'{TB}     Opcion a: identificadores de DLVs (FileTypeId). P. ej. alt95 fcc05 fcc03') 
                myLog.error(f'{TB}     Opcion b: una secuencia de cinco elementos separados por comas (sin espacios) del tipo:')
                myLog.error(f'{TB}         FileTypeId,NickName,RangoLinf,RangoLsup,NumClases,Movilidad,Ponderacion')
                myLog.error(f'{TB}         Ejemplo: {GLO.GLBLlistTxtDasoVarsPorDefecto}')
                myLog.error(f'{TB}-> La variable {numDasoVar} ({listDasoVar[0]}) solo tiene {len(listDasoVar)} elementos: {listDasoVar}')
                sys.exit(0)
            listDasoVar[2] = int(listDasoVar[2])
            listDasoVar[3] = int(listDasoVar[3])
            listDasoVar[4] = int(listDasoVar[4])
            listDasoVar[5] = int(listDasoVar[5])
            if len(listDasoVar) > 6:
                listDasoVar[6] = int(listDasoVar[6])
            else:
                listDasoVar.append(10)
            args_listLstDasoVars.append(listDasoVar)
        # La lista de textos se ha convertido a lista de listas
        cfgDict['listLstDasoVars'] = args_listLstDasoVars
    # ==========================================================================

    # ==========================================================================
    # Parametros de configuracion extra
    try:
        cfgDict['menuInteractivo'] = args.menuInteractivo
        cfgDict['marcoCoordMiniX'] = args.marcoCoordMiniX
        cfgDict['marcoCoordMaxiX'] = args.marcoCoordMaxiX
        cfgDict['marcoCoordMiniY'] = args.marcoCoordMiniY
        cfgDict['marcoCoordMaxiY'] = args.marcoCoordMaxiY
        cfgDict['marcoPatronTest'] = args.marcoPatronTest
        cfgDict['nPatronDasoVars'] = args.nPatronDasoVars
        cfgDict['rasterPixelSize'] = args.rasterPixelSize
        cfgDict['radioClusterPix'] = args.radioClusterPix
        cfgDict['nivelSubdirExpl'] = args.nivelSubdirExpl
        cfgDict['outRasterDriver'] = args.outRasterDriver
        cfgDict['outputSubdirNew'] = args.outputSubdirNew
        cfgDict['cartoMFErecorte'] = args.cartoMFErecorte
        cfgDict['varsTxtFileName'] = args.varsTxtFileName
        cfgDict['ambitoTiffNuevo'] = args.ambitoTiffNuevo
        cfgDict['noDataTiffProvi'] = args.noDataTiffProvi
        cfgDict['noDataTiffFiles'] = args.noDataTiffFiles
        cfgDict['noDataTipoDMasa'] = args.noDataTipoDMasa
        cfgDict['umbralMatriDist'] = args.umbralMatriDist
        cfgDict['distMaxScipyAdm'] = args.distMaxScipyAdm
        cfgDict['compilaConNumba'] = args.compilaConNumba
    except Exception as e:
        myLog.error(f'qlidtwins-> args: {list(myArgs for myArgs in dir(args) if not myArgs.startswith("__"))}')
        program_name = 'qlidtwins.py'
        indent = len(program_name) * " "
        sys.stderr.write(f'{program_name}-> {repr(e)}\n')
        if os.path.exists(GLO.configFileNameCfg):
            if 'object has no attribute' in repr(e):
                argumentoNoEncontrado = repr(e)[repr(e).index('object has no attribute') + len('object has no attribute') + 2: -3]
                sys.stderr.write(f'{indent}   Revisar si {GLO.configFileNameCfg} incluye el argumento {argumentoNoEncontrado}\n')
                sys.stderr.write(f'{indent}     {GLO.configFileNameCfg} debe incluir todos los parametros preceptivos (main & extra).\n')
            else:
                sys.stderr.write(f'{indent}   Revisar si el fichero de configuracion {GLO.configFileNameCfg} incluye todos los parametros preceptivos (main & extra).\n')
        else:
            sys.stderr.write(f'{indent}   Error desconocido al leer los parametros de configuracion en linea de argumentos y por defecto.\n')
        sys.stderr.write(f'{indent}   For help use:\n')
        sys.stderr.write(f'{indent}     help with only the main arguments:  python {program_name}.py -h\n')
        sys.stderr.write(f'{indent}     help with main and extra arguments: python {program_name}.py -e 1 -h')
        sys.exit(0)
    # ==========================================================================

    # cfgDict['marcoCoordMiniX'] = 318000
    # cfgDict['marcoCoordMaxiX'] = 322000
    # cfgDict['marcoCoordMiniY'] = 4734000
    # cfgDict['marcoCoordMaxiY'] = 4740000

    return cfgDict


# ==============================================================================
def mostrarConfiguracion(cfgDict):
    # configFileNameCfg = getConfigFileNameCfg()
    configFileNameCfg = GLO.configFileNameCfg

    myLog.info('\n{:_^80}'.format(''))
    myLog.info(f'qlidtwins-> Parametros de configuracion principales:')
    if len(sys.argv) == 3:
        if os.path.exists(configFileNameCfg):
            infoConfiguracionUsada = f'Son valores leidos del fichero de configuracion ({configFileNameCfg}).'
        else:
            infoConfiguracionUsada = 'Son valores "de fabrica" incluidos en codigo (clidtwcfg.py).'
    else:
        infoConfiguracionUsada = 'Incluye valores leidos en linea de comandos (los que no van en linea de comandos, son por defecto).'
    myLog.info(f'{TB}{infoConfiguracionUsada}')

    if 'listLstDasoVars' in cfgDict.keys():
        myLog.info(f'{TB}-> Listado de dasoVars:')
        myLog.info(f'{TB}{TV}-> formato: [fileType, nickName, limInf, limSup, numClases, movilidadInterclases (0-100), ponderacion (0-10)]')
        for numDasoVar, listDasoVar in enumerate(cfgDict['listLstDasoVars']):
            myLog.info(f'{TB}{TV}Variable {numDasoVar}: {listDasoVar}')
    elif 'listaTxtDasoVarsFileTypes' in cfgDict.keys():
        myLog.info(f'{TB}-> Listado de FileTypeId (identificadores de dasoVars):')
        for numDasoVar, FileTypeId in enumerate(cfgDict['listaTxtDasoVarsFileTypes']):
            myLog.info(f'{TB}{TV}Variable {numDasoVar}: {FileTypeId}')

    myLog.info(f'{TB}-> Rango de coordenadas UTM:')
    if cfgDict['marcoPatronTest']:
        if (
            cfgDict['marcoCoordMiniX'] != 0
            or cfgDict['marcoCoordMaxiX'] != 0
            or cfgDict['marcoCoordMiniY'] != 0
            or cfgDict['marcoCoordMaxiY'] != 0
        ):
            myLog.info(f'{TB}{TV}Se adopta la envolvente de las coordenadas sumunistradas y los shapes de referenia (patron) y chequeo (testeo).')
            if (
                cfgDict['marcoCoordMiniX'] != 0
                or cfgDict['marcoCoordMaxiX'] != 0
            ):
                myLog.info(
                    f'{TB}{TV}{TV}X {cfgDict["marcoCoordMiniX"]:07f} - {cfgDict["marcoCoordMaxiX"]:07f} '
                    f'-> {cfgDict["marcoCoordMaxiX"] - cfgDict["marcoCoordMiniX"]:04.0f} m:')
            if (
                cfgDict['marcoCoordMiniY'] != 0
                or cfgDict['marcoCoordMaxiY'] != 0
            ):
                myLog.info(
                    f'{TB}{TV}{TV}Y {cfgDict["marcoCoordMiniY"]:07f} - {cfgDict["marcoCoordMaxiY"]:07f} '
                    f'-> {cfgDict["marcoCoordMaxiY"] - cfgDict["marcoCoordMiniY"]:04.0f} m:')
            myLog.info(f'{TB}{TV}Ver valores de la envolvente mas adelante.')
        else:
            myLog.info(f'{TB}{TV}Se adopta la envolvente de los shapes de referenia (patron) y chequeo (testeo).')
            myLog.info(f'{TB}{TV}Ver valores mas adelante.')
    elif (
        cfgDict['marcoCoordMiniX'] == 0
        or cfgDict['marcoCoordMaxiX'] == 0
        or cfgDict['marcoCoordMiniY'] == 0
        or cfgDict['marcoCoordMaxiY'] == 0
        ):
        myLog.info(f'{TB}{TV}No se han establecido coordenadas para la zona de estudio.')
        myLog.info(f'{TB}{TV}Se adopta la envolvente de los ficheros con variables dasoLidar.')
    else:
        myLog.info(
            '{TB}{TV}{TV}X {:07f} - {:07f} -> {:04.0f} m:'.format(
                cfgDict['marcoCoordMiniX'], cfgDict['marcoCoordMaxiX'],
                cfgDict['marcoCoordMaxiX'] - cfgDict['marcoCoordMiniX']
            )
        )
        myLog.info(
            '{TB}{TV}{TV}Y {:07f} - {:07f} -> {:04.0f} m:'.format(
                cfgDict['marcoCoordMiniY'], cfgDict['marcoCoordMaxiY'],
                cfgDict['marcoCoordMaxiY'] - cfgDict['marcoCoordMiniY']
            )
        )

    myLog.info(f'{TB}-> Ruta base (raiz) y ficheros:')
    myLog.info(f'{TB}{TV}rutaAscRaizBase: {cfgDict["rutaAscRaizBase"]}')
    myLog.info(f'{TB}{TV}patronVectrName: {cfgDict["patronVectrName"]}')
    if type(cfgDict['patronLayerName']) == str and cfgDict['patronLayerName'] != '': 
        myLog.info(f'{TB}{TV}patronLayerName: {cfgDict["patronLayerName"]}')
    if type(cfgDict['patronFieldName']) == str and cfgDict['patronFieldName'] != '': 
        myLog.info(f'{TB}{TV}patronFieldName: {cfgDict["patronFieldName"]}')
    myLog.info(f'{TB}{TV}testeoVectrName: {cfgDict["testeoVectrName"]}')
    if type(cfgDict['testeoLayerName']) == str and cfgDict['testeoLayerName'] != '':
        myLog.info(f'{TB}{TV}testeoLayerName: {cfgDict["testeoLayerName"]}')
    myLog.info(f'{TB}-> Cartografia de cubiertas (MFE):')
    myLog.info(f'{TB}{TV}rutaCompletaMFE: {cfgDict["rutaCompletaMFE"]}')
    myLog.info(f'{TB}{TV}cartoMFEcampoSp: {cfgDict["cartoMFEcampoSp"]}')
    myLog.info('{:=^80}'.format(''))

    if __verbose__ == 3:
        myLog.debug('\n{:_^80}'.format(''))
        # myLog.debug('__verbose__: {}'.format(__verbose__))
        # myLog.debug(f'->-> qlidtwins-> args: {argsConfig}')
        # myLog.info(f'{TB}->> dir(args):', dir(args))
        myLog.debug('->> Lista de dasoVars en formato para linea de comandos:')
        myLog.debug(f'{TB}{argsConfig.listTxtDasoVars}')
        myLog.debug('{:=^80}'.format(''))

    if __verbose__ >= 2:
        if TRNS_LEER_EXTRA_ARGS:
            infoConfiguracionUsada = ' (valores leidos en linea de comandos o, si no van en linea de comandos, valores por defecto)'
        else:
            if os.path.exists(configFileNameCfg):
                infoConfiguracionUsada = f' (valores leidos del fichero de configuracion, {configFileNameCfg})'
            else:
                infoConfiguracionUsada = ' (valores "de fabrica" incluidos en codigo, clidtwcfg.py)'
        myLog.debug('\n{:_^80}'.format(''))
        myLog.debug(f'Parametros de configuracion adicionales{infoConfiguracionUsada}:')
        myLog.debug(f'{TB}-> menuInteractivo: {cfgDict["menuInteractivo"]}')
        myLog.debug(f'{TB}-> marcoCoordMiniX: {cfgDict["marcoCoordMiniX"]}')
        myLog.debug(f'{TB}-> marcoCoordMaxiX: {cfgDict["marcoCoordMaxiX"]}')
        myLog.debug(f'{TB}-> marcoCoordMiniY: {cfgDict["marcoCoordMiniY"]}')
        myLog.debug(f'{TB}-> marcoCoordMaxiY: {cfgDict["marcoCoordMaxiY"]}')
        myLog.debug(f'{TB}-> marcoPatronTest: {cfgDict["marcoPatronTest"]}')
        myLog.debug(f'{TB}-> nPatronDasoVars: {cfgDict["nPatronDasoVars"]}')
        myLog.debug(f'{TB}-> rasterPixelSize: {cfgDict["rasterPixelSize"]}')
        myLog.debug(f'{TB}-> radioClusterPix: {cfgDict["radioClusterPix"]}')
        myLog.debug(f'{TB}-> nivelSubdirExpl: {cfgDict["nivelSubdirExpl"]}')
        myLog.debug(f'{TB}-> outRasterDriver: {cfgDict["outRasterDriver"]}')
        myLog.debug(f'{TB}-> outputSubdirNew: {cfgDict["outputSubdirNew"]}')
        myLog.debug(f'{TB}-> cartoMFErecorte: {cfgDict["cartoMFErecorte"]}')
        myLog.debug(f'{TB}-> varsTxtFileName: {cfgDict["varsTxtFileName"]}')
        myLog.debug(f'{TB}-> ambitoTiffNuevo: {cfgDict["ambitoTiffNuevo"]}')
        myLog.debug(f'{TB}-> noDataTiffProvi: {cfgDict["noDataTiffProvi"]}')
        myLog.debug(f'{TB}-> noDataTiffFiles: {cfgDict["noDataTiffFiles"]}')
        myLog.debug(f'{TB}-> noDataTipoDMasa: {cfgDict["noDataTipoDMasa"]}')
        myLog.debug(f'{TB}-> umbralMatriDist: {cfgDict["umbralMatriDist"]}')
        myLog.debug(f'{TB}-> distMaxScipyAdm: {cfgDict["distMaxScipyAdm"]}')
        myLog.debug(f'{TB}-> compilaConNumba: {cfgDict["compilaConNumba"]}')
        myLog.debug('{:=^80}'.format(''))


# ==============================================================================
def clidtwinsUseCase(
        cfgDict,
        accionPral=None,
    ):
    if accionPral is None:
        accionPral = cfgDict['mainAction']
    else:
        cfgDict['mainAction'] = accionPral

    myLog.debug('\n{:_^80}'.format(''))
    myLog.debug('qlidtwins-> Creando objeto de la clase DasoLidarSource...')

    myDasolidar = DasoLidarSource(LCL_verbose=__verbose__)
    # Resultados a testear:
    # -> Que existe el objeto myDasolidar
    # -> Que tiene como propiedades los argumentos extra y otros adicionales:
    #    GLBLmenuInteractivo, etc.
    #    LOCLmarcoCoordMiniX, etc.
    if __verbose__ == 3 or TRNS_testTwins:
        myLog.debug('qlidtwins-> tests-> Verifica DasoLidarSource')
        myLog.debug(f'{TB}type(myDasolidar): {type(myDasolidar)}')
        myLog.debug(f'{TB}hasattr(myDasolidar, "GLBLmenuInteractivo"): {hasattr(myDasolidar, "GLBLmenuInteractivo")}')
        myLog.debug('{:=^80}'.format(''))

    myLog.debug('\n{:_^80}'.format(''))
    myLog.debug('qlidtwins-> Ejecutando setRangeUTM...')
    myDasolidar.setRangeUTM(
        LCL_marcoCoordMiniX=cfgDict['marcoCoordMiniX'],
        LCL_marcoCoordMaxiX=cfgDict['marcoCoordMaxiX'],
        LCL_marcoCoordMiniY=cfgDict['marcoCoordMiniY'],
        LCL_marcoCoordMaxiY=cfgDict['marcoCoordMaxiY'],
        LCL_marcoPatronTest=cfgDict['marcoPatronTest'],
        LCL_rutaAscRaizBase=cfgDict['rutaAscRaizBase'],
        LCL_patronVectrName=cfgDict['patronVectrName'],
        LCL_patronLayerName=cfgDict['patronLayerName'],
        LCL_testeoVectrName=cfgDict['testeoVectrName'],
        LCL_testeoLayerName=cfgDict['testeoLayerName'],
    )
    # Resultados a testear:
    # -> Que el objeto myDasolidar tiene la propiedad GLBLmarcoPatronTest
    # -> Que el objeto myDasolidar tiene coordenadas del marco definidas
    if __verbose__ == 3 or TRNS_testTwins:
        myLog.debug('qlidtwins-> tests-> Verifica setRangeUTM')
        myLog.debug(f'{TB}myDasolidar.GLBLmarcoPatronTest: {myDasolidar.GLBLmarcoPatronTest}')
        myLog.debug(f'{TB}myDasolidar.LOCLmarcoCoordMiniX: {myDasolidar.LOCLmarcoCoordMiniX}')
        myLog.debug(f'{TB}myDasolidar.LOCLmarcoCoordMaxiX: {myDasolidar.LOCLmarcoCoordMaxiX}')
        myLog.debug(f'{TB}myDasolidar.LOCLmarcoCoordMiniY: {myDasolidar.LOCLmarcoCoordMiniY}')
        myLog.debug(f'{TB}myDasolidar.LOCLmarcoCoordMaxiY: {myDasolidar.LOCLmarcoCoordMaxiY}')
        myLog.debug('{:=^80}'.format(''))

    myLog.debug('\n{:_^80}'.format(''))
    myLog.debug('qlidtwins-> Ejecutando searchSourceFiles...')
    if (
        'listLstDasoVars' in cfgDict.keys()
        and type(cfgDict['listLstDasoVars'][0]) == list
    ):
        # los argumentos listaDasoVars son completos 
        myDasolidar.searchSourceFiles(
            LCL_listLstDasoVars=cfgDict['listLstDasoVars'],
            LCL_nPatronDasoVars=cfgDict['nPatronDasoVars'],  # opcional
            LCL_rutaAscRaizBase=cfgDict['rutaAscRaizBase'],
            LCL_nivelSubdirExpl=cfgDict['nivelSubdirExpl'],  # opcional
            LCL_outputSubdirNew=cfgDict['outputSubdirNew'],  # opcional
        )
    elif (
        'listaTxtDasoVarsFileTypes' in cfgDict.keys()
        and type(cfgDict['listaTxtDasoVarsFileTypes'][0]) == str
    ):
        # Los argumentos posicionales listaDasoVars solo tienen los FileTypeId
        myDasolidar.searchSourceFiles(
            LCL_listaTxtDasoVarsFileTypes=cfgDict['listaTxtDasoVarsFileTypes'],
            LCL_nPatronDasoVars=cfgDict['nPatronDasoVars'],  # opcional
            LCL_rutaAscRaizBase=cfgDict['rutaAscRaizBase'],
            LCL_nivelSubdirExpl=cfgDict['nivelSubdirExpl'],  # opcional
            LCL_outputSubdirNew=cfgDict['outputSubdirNew'],  # opcional
        )

    elif (
        # Esta situacion no debe darse, porque si los argumentos posicionales son de tipo
        # FileTypeId se guardan como listaTxtDasoVarsFileTypes y no como listLstDasoVars
        'listLstDasoVars' in cfgDict.keys()
        and type(cfgDict['listLstDasoVars'][0]) == str
    ):
        myDasolidar.searchSourceFiles(
            LCL_listaTxtDasoVarsFileTypes=cfgDict['listLstDasoVars'],
            LCL_nPatronDasoVars=cfgDict['nPatronDasoVars'],  # opcional
            LCL_rutaAscRaizBase=cfgDict['rutaAscRaizBase'],
            LCL_nivelSubdirExpl=cfgDict['nivelSubdirExpl'],  # opcional
            LCL_outputSubdirNew=cfgDict['outputSubdirNew'],  # opcional
        )
    else:
        myLog.error(f'\nqlidtwins-> Atencion: revisar los argumentos pasados en linea de comandos. sys.argv: <{sys.argv}>')
        sys.exit(0)
    # Resultados a testear:
    # -> Lista de ficheros encontrados:
    if __verbose__ == 3 or TRNS_testTwins:
        myLog.debug('\n{:_^80}'.format(''))
        myLog.debug('qlidtwins-> tests-> Verifica searchSourceFiles')
        # myDasolidar.inFilesListAllTypes
        myLog.debug(f'{TB}len(myDasolidar.inFilesListAllTypes): {len(myDasolidar.inFilesListAllTypes)}')
        for numDasoVarX, listaFileTuplesDasoVarX in enumerate(myDasolidar.inFilesListAllTypes):
            for numFile, [pathFile, nameFile] in enumerate(listaFileTuplesDasoVarX):
                if numFile < 10 or numFile == len(listaFileTuplesDasoVarX) - 1:
                    myLog.debug(f'{TB}{TV}inFilesListAllTypes-> {numDasoVarX}, {numFile}, {pathFile}, {nameFile}')
                elif numFile == 10:
                    myLog.debug(f'{TB}{TV}...')
        myLog.debug('{:=^80}'.format(''))

    myLog.debug('\n{:_^80}'.format(''))
    myLog.debug('qlidtwins-> Ejecutando createMultiDasoLayerRasterFile...')
    myDasolidar.createMultiDasoLayerRasterFile(
        LCL_rutaCompletaMFE=cfgDict['rutaCompletaMFE'],
        LCL_cartoMFEcampoSp=cfgDict['cartoMFEcampoSp'],
        LCL_rasterPixelSize=cfgDict['rasterPixelSize'],
        # LCL_outRasterDriver=cfgDict['outRasterDriver'],
        # LCL_cartoMFErecorte=cfgDict['cartoMFErecorte'],
        # LCL_varsTxtFileName=cfgDict['varsTxtFileName'],
    )
    # Resultados a testear:
    # -> que se ha creado el raster:
    #    myDasolidar.LOCLoutPathNameRuta
    #    myDasolidar.LOCLoutFileNameWExt_mergedUniCellAllDasoVars
    myLog.debug('{:=^80}'.format(''))

    accionesPrincipales = [
        '0. Ninguna accion.',
        '1. qlidtwins - chequearCompatibilidadConTesteoVector: verificar analogia con un determinado patron dasoLidar.',
        '2. qlidtwins - generarRasterCluster: generar raster con presencia de un determinado patron dasoLidar.'
    ]
    if cfgDict['menuInteractivo']:
        accionPorDefecto = 1
        print('\ncartolidar-> Menu de herramientas de cartolidar')
        for opcionPrincipal in accionesPrincipales[1:]:
            print(f'\t{opcionPrincipal}')
        selec = input(f'Elije opcion ({accionPorDefecto}): ')
        if selec == '':
            nAccionElegida = accionPorDefecto
        else:
            try:
                nAccionElegida = int(selec)
            except:
                myLog.error(f'\nATENCION: Opcion elegida no disponible: <{selec}>')
                sys.exit(0)
        myLog.info(f'\nSe ha elegido:\n\t{accionesPrincipales[nAccionElegida]}')
        cfgDict['mainAction'] = nAccionElegida
        if __verbose__:
            myLog.info(f'{TB}-> Ejecutando: {accionesPrincipales[cfgDict["mainAction"] - 1]}')

    myLog.info('\n{:_^80}'.format(''))
    myLog.debug('qlidtwins-> Ejecutando analyzeMultiDasoLayerRasterFile...')

    # tipoDeMasaSelecOk = comprobarTipoMasaDeCapaVectorial(
    (tipoDeMasaField, tipoDeMasaValue, listaTM) = comprobarTipoMasaDeCapaVectorial(
        cfgDict['rutaAscRaizBase'],  # self.LOCLrutaAscRaizBase,
        cfgDict['patronVectrName'],  # self.LOCLpatronVectrName,
        LOCLlayerName=cfgDict['patronLayerName'],  # self.LOCLpatronLayerName,
        LOCLpatronFieldName=cfgDict['patronFieldName'],  # self.LOCLpatronFieldName,
        LOCLtipoDeMasaSelec=None,
        LOCLverbose=False,
    )
    if tipoDeMasaField is None:
        myLog.error('')
        myLog.error(f'qlidtwins-> AVISO: no esta disponible el fichero: {cfgDict["patronVectrName"]}')
        myLog.error(f'{TB}-> Ruta base: { cfgDict["rutaAscRaizBase"]}')
        sys.exit(0)
    # tipoDeMasaFieldOk = tipoDeMasaSelecOk[0]
    # tipoDeMasaValueOk = tipoDeMasaSelecOk[1]
    # listaTM = [None]
    # listaTM = listaTM[1:]
    resultadosFileTxtConPath = os.path.join(myDasolidar.LOCLoutPathNameRuta, 'resultadosComparativa.txt')
    resultadosFileTxtControl = open(resultadosFileTxtConPath, mode='w+')
    resultadosFileTxtControl.write(f'Resultado de la comparativa:\n')
    resultadosFileTxtControl.write(f'La capa con los poligonos de referencia tiene {len(listaTM)} Tipos de masa de referencia:\n')
    myLog.info(f'qlidtwins-> Chequeando listaTM:')
    for numTM, LCL_tipoDeMasaSelec in enumerate(listaTM):
        resultadosFileTxtControl.write(f'{TV}-> TM_{LCL_tipoDeMasaSelec}\n')
        myLog.info(f'{TV}-> TM_{LCL_tipoDeMasaSelec}')
    myLog.info('{:=^80}'.format(''))
    resultadosFileTxtControl.write(f'\nResultados para cada Tipo de masa:\n')
    for numTM, LCL_tipoDeMasaSelec in enumerate(listaTM):
        myLog.info('\n{:_^80}'.format(''))
        myLog.info(f'qlidtwins-> LCL_tipoDeMasaSelec: TM_{LCL_tipoDeMasaSelec}')
        resultadosFileTxtControl.write(f'-> Tipo de masa: TM_{LCL_tipoDeMasaSelec}\n')
        myDasolidar.analyzeMultiDasoLayerRasterFile(
            LCL_patronVectrName=cfgDict['patronVectrName'],
            LCL_patronLayerName=cfgDict['patronLayerName'],
            LCL_patronFieldName=cfgDict['patronFieldName'],
            LCL_tipoDeMasaSelec=LCL_tipoDeMasaSelec,
        )
        if myDasolidar.rasterDatasetAll is None:
            myLog.warning(f'{TB}Se pasa directamente el siguiente Tipo de Masa.')
            myLog.warning('')
            continue

        # Resultados a testear:
        # -> Tipos de bosque mas frecuentes en zona patron:
        #    myDasolidar.pctjTipoBosquePatronMasFrecuente1,
        #    myDasolidar.codeTipoBosquePatronMasFrecuente1,
        #    myDasolidar.pctjTipoBosquePatronMasFrecuente2,
        #    myDasolidar.codeTipoBosquePatronMasFrecuente2,
        # -> Que los rangos son correctos:
        #    myDasolidar.dictHistProb01
        # -> Que se ha creado el txt con los rangos:
        #    myDasolidar.LOCLoutPathNameRuta
        #    myDasolidar.outputRangosFileTxtSinPath
        #    myDasolidar.outputRangosFileNpzSinPath,
        if __verbose__ == 3 or TRNS_testTwins:
            myLog.debug('\n{:_^80}'.format(''))
            myLog.debug(f'{TB}qlidtwins-> tests-> analyzeMultiDasoLayerRasterFile')
            myLog.debug(f'{TB}-> Verifica los tipos de bosque mas frecuentes en zona patron:')
            myLog.debug(f'{TB}pctjTipoBosquePatronMasFrecuente1: {myDasolidar.pctjTipoBosquePatronMasFrecuente1}')
            myLog.debug(f'{TB}codeTipoBosquePatronMasFrecuente1: {myDasolidar.codeTipoBosquePatronMasFrecuente1}')
            myLog.debug(f'{TB}pctjTipoBosquePatronMasFrecuente2: {myDasolidar.pctjTipoBosquePatronMasFrecuente2}')
            myLog.debug(f'{TB}codeTipoBosquePatronMasFrecuente2: {myDasolidar.codeTipoBosquePatronMasFrecuente2}')
            if (
                '0_Alt95_ref' in myDasolidar.dictHistProb01.keys()
                or '2_Fcc3m_ref' in myDasolidar.dictHistProb01.keys()
                or '3_CobMt_ref' in myDasolidar.dictHistProb01.keys()
            ):
                myLog.debug(f'{TB}-> Verifica que los rangos son correctos:')
            if '0_Alt95_ref' in myDasolidar.dictHistProb01.keys():
                myLog.debug(f'{TB}0_Alt95_ref: {myDasolidar.dictHistProb01["0_Alt95_ref"]}')
                myLog.debug(f'{TB}0_Alt95_min: {myDasolidar.dictHistProb01["0_Alt95_min"]}')
                myLog.debug(f'{TB}0_Alt95_max: {myDasolidar.dictHistProb01["0_Alt95_max"]}')
            if '2_Fcc3m_ref' in myDasolidar.dictHistProb01.keys():
                myLog.debug(f'{TB}2_Fcc3m_ref: {myDasolidar.dictHistProb01["2_Fcc3m_ref"]}')
                myLog.debug(f'{TB}2_Fcc3m_min: {myDasolidar.dictHistProb01["2_Fcc3m_min"]}')
                myLog.debug(f'{TB}2_Fcc3m_max: {myDasolidar.dictHistProb01["2_Fcc3m_max"]}')
            if '3_CobMt_ref' in myDasolidar.dictHistProb01.keys():
                myLog.debug(f'{TB}3_CobMt_ref: {myDasolidar.dictHistProb01["3_CobMt_ref"]}')
                myLog.debug(f'{TB}3_CobMt_min: {myDasolidar.dictHistProb01["3_CobMt_min"]}')
                myLog.debug(f'{TB}3_CobMt_max: {myDasolidar.dictHistProb01["3_CobMt_max"]}')
            myLog.debug(f'{TB}-> Verifica que se ha creado el txt con los rangos:')
            myLog.debug(f'{TB}{myDasolidar.LOCLoutPathNameRuta}')
            myLog.debug(f'{TB}{myDasolidar.outputRangosFileTxtSinPath}')
            myLog.debug(f'{TB}{myDasolidar.outputRangosFileNpzSinPath}')
            myLog.info('{:=^80}'.format(''))

        if cfgDict['mainAction'] == 0:
            # No se ejecuta ninguna accion (solo para testing)
            return myDasolidar
        elif cfgDict['mainAction'] == 1:
            myLog.debug('\n{:_^80}'.format(''))
            myLog.debug('qlidtwins-> Ejecutando chequearCompatibilidadConTesteoShape...')
            testeoVectorOk = myDasolidar.chequearCompatibilidadConTesteoVector(
                LCL_testeoVectrName=cfgDict['testeoVectrName'],
                LCL_testeoLayerName=cfgDict['testeoLayerName'],
                )
            if not testeoVectorOk:
                return myDasolidar
            # Resultados a testear:
            #     myDasolidar.tipoBosqueOk,
            #     myDasolidar.nVariablesNoOk,
            #     myDasolidar.distanciaEuclideaMediaPatronTesteo,
            #     myDasolidar.distanciaEuclideaMediaPatronPatron,
            #     myDasolidar.distanciaEuclideaRazon
            #     myDasolidar.pctjPorcentajeDeProximidad,
            #     myDasolidar.matrizDeDistancias,
            if False:
                myLog.info('\n{:_^80}'.format(''))
                myLog.info('qlidtwins-> chequearCompatibilidadConTesteoVector')
                myLog.info(f'{TB}-> tipoBosqueOk:   {myDasolidar.tipoBosqueOk}')
                myLog.info(f'{TB}-> nVariablesNoOk: {myDasolidar.nVariablesNoOk}')
                myLog.info(f'{TB}-> distanciaEuclideaMediaPatronTesteo: {myDasolidar.distanciaEuclideaMediaPatronTesteo:0.1f}')
                myLog.info(f'{TB}-> distanciaEuclideaMediaPatronPatron: {myDasolidar.distanciaEuclideaMediaPatronPatron:0.1f}')
                myLog.info(f'{TB}-> distanciaEuclideaRazon:             {myDasolidar.distanciaEuclideaRazon:0.2f}')
                myLog.info(f'{TB}-> pctjPorcentajeDeProximidad:         {myDasolidar.pctjPorcentajeDeProximidad:0.1f} %')
                myLog.info(f'{"":=^80}')
            if __verbose__ > 2:
                myLog.info('\n{:_^80}'.format(''))
                myLog.info(f'{TB}-> matrizDeDistanciasPatronTesteo: {myDasolidar.matrizDeDistanciasPatronTesteo}')
                myLog.info(f'{TB}-> matrizDeDistanciasPatronPatron: {myDasolidar.matrizDeDistanciasPatronPatron}')
                myLog.info(f'{"":=^80}')
            resultadosFileTxtControl.write(f'{TV}-> tipoBosqueOk:   {myDasolidar.tipoBosqueOk}\n')
            resultadosFileTxtControl.write(f'{TV}-> nVariablesNoOk: {myDasolidar.nVariablesNoOk}\n')
            resultadosFileTxtControl.write(f'{TV}-> distanciaEuclideaMediaPatronTesteo: {myDasolidar.distanciaEuclideaMediaPatronTesteo:0.2f}\n')
            resultadosFileTxtControl.write(f'{TV}-> distanciaEuclideaMediaPatronPatron: {myDasolidar.distanciaEuclideaMediaPatronPatron:0.2f}\n')
            resultadosFileTxtControl.write(f'{TV}-> distanciaEuclideaRazon:             {myDasolidar.distanciaEuclideaRazon:0.2f}\n')
            resultadosFileTxtControl.write(f'{TV}-> pctjPorcentajeDeProximidad:         {myDasolidar.pctjPorcentajeDeProximidad:0.2f}\n')
            if __verbose__ > 1 or True:
                resultadosFileTxtControl.write(f'{TV}-> matrizDeDistanciasPatronTesteo: {myDasolidar.matrizDeDistanciasPatronTesteo}\n')
                resultadosFileTxtControl.write(f'{TV}-> matrizDeDistanciasPatronPatron: {myDasolidar.matrizDeDistanciasPatronPatron}\n')

        elif cfgDict['mainAction'] == 2:
            myLog.debug('\n{:_^80}'.format(''))
            myLog.debug('qlidtwins-> Ejecutando generarRasterCluster...')
            rasterClusterOk = myDasolidar.generarRasterCluster(
                LCL_radioClusterPix=cfgDict['radioClusterPix'],
            )
            if not rasterClusterOk:
                return myDasolidar
            # Resultados a testear:
            #     myDasolidar.pctjTipoBosquePatronMasFrecuente1,
            #     myDasolidar.codeTipoBosquePatronMasFrecuente1,
            #     myDasolidar.pctjTipoBosquePatronMasFrecuente2,
            #     myDasolidar.codeTipoBosquePatronMasFrecuente2,
            #
            #     myDasolidar.LOCLoutPathNameRuta,
            #     myDasolidar.outputClusterAllDasoVarsFileNameSinPath,
            #     myDasolidar.outputClusterTipoBoscProFileNameSinPath,
            #     myDasolidar.outputClusterTipoMasaParFileNameSinPath,
            #     myDasolidar.outputClusterFactorProxiFileNameSinPath,
            #     myDasolidar.outputClusterDistanciaEuFileNameSinPath,
            if __verbose__ == 3 or TRNS_testTwins:
                myLog.info('\n{:_^80}'.format(''))
                myLog.info('qlidtwins-> tests-> generarRasterCluster')
                myLog.info(f'{TB}{myDasolidar.pctjTipoBosquePatronMasFrecuente1}')
                myLog.info(f'{TB}{myDasolidar.codeTipoBosquePatronMasFrecuente1}')
                myLog.info(f'{TB}{myDasolidar.pctjTipoBosquePatronMasFrecuente2}')
                myLog.info(f'{TB}{myDasolidar.codeTipoBosquePatronMasFrecuente2}')
                #
                myLog.info(f'{TB}{myDasolidar.LOCLoutPathNameRuta}')
                myLog.info(f'{TB}{myDasolidar.outputClusterAllDasoVarsFileNameSinPath}')
                myLog.info(f'{TB}{myDasolidar.outputClusterTipoBoscProFileNameSinPath}')
                myLog.info(f'{TB}{myDasolidar.outputClusterTipoMasaParFileNameSinPath}')
                myLog.info(f'{TB}{myDasolidar.outputClusterFactorProxiFileNameSinPath}')
                myLog.info(f'{TB}{myDasolidar.outputClusterDistanciaEuFileNameSinPath}')
                myLog.info('{:=^80}'.format(''))

            # Se identifica el TM mas ajustado para cada pixel, dentro de unos minimos
            if __verbose__:
                myLog.info('\n{:_^80}'.format(''))
                myLog.info('qlidtwins-> Ejecutando asignarTipoDeMasa...')
            myDasolidar.asignarTipoDeMasaConDistanciaMinima(
                LCL_listaTM=listaTM,
                LCL_distMaxScipyAdm=cfgDict['distMaxScipyAdm']
            )
            myLog.debug('{:=^80}'.format(''))
    
        else:
            return None

    resultadosFileTxtControl.close()

    return myDasolidar


# ==============================================================================
def foo():
    pass

# ==============================================================================
if (__name__ == '__main__' or 'qlidtwins' in __name__) and not TRNS_testTwins:

    tiempo0 = time.time()
    timeInicio = time.asctime(time.localtime(time.time()))
    myLog.info(f'\nqlidtwins-> {timeInicio}')

    tipoEjecucion = checkRun()
    testRun()

    argsConfig = leerArgumentosEnLineaDeComandos()
    saveArgs(argsConfig)
    cfgDict = creaConfigDict(argsConfig, tipoEjecucion=tipoEjecucion)
    if __verbose__:
        mostrarConfiguracion(cfgDict)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    _ = clidtwinsUseCase(cfgDict)
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    tiempo1 = time.time()
    timeFin = time.asctime(time.localtime(time.time()))
    if __verbose__:
        myLog.info(f'Tiempo total: : {(tiempo1 - tiempo0):0.0f} segundos ({round((tiempo1 - tiempo0)/60, 1)} minutos)')
        myLog.info(timeFin)

    myLog.info(f'\n{"":_^80}')
    LOCLoutPathNameRuta = os.path.join(cfgDict['rutaAscRaizBase'], cfgDict['outputSubdirNew'])
    myLog.info(f'qlidtwins-> Ver resultados en {LOCLoutPathNameRuta}')
    myLog.info(f'{"":=^80}')


    myLog.info('\nqlidtwins-> Fin.')
    # print(f'qlidtwins-> myLog: {dir(myLog)}')
    # print(f'qlidtwins-> myLog.name: {myLog.name}')
    # print(f'qlidtwins-> myLog.level: {myLog.getEffectiveLevel()}, {myLog.getEffectiveLevel}')
    # print(f'qlidtwins-> myLog.Level: {myLog.Level}')
    if myLog.getEffectiveLevel() >= 30:
        print('\nqlidtwins-> Fin.')
