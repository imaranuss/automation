# funciones.py
import cmath
import math
import socket
import time

import matplotlib.pyplot as plt
import numpy as np
import pyvisa as visa
from robot.errors import RobotError


##########################funciones para encontrar los equipos ip y puertos#######################################################

def find_n5171b():  # generador de señales/funciones
    target_port = 5025  # estandar para comandos scpi
    found = 0 #control de error
    # escanea para encontrar dispositivos en la red ethernet
    for i in range(199, 202):  # rango asignado ya que conozco la ip
        ip_address = f'192.168.12.{i}'  # reemplaza con la ip dentro de rango

        try:
            # intento de conexion con el dispositivo
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)  # tiempo asignado para la conexion
                result = sock.connect_ex((ip_address, target_port))
                if result == 0:
                    print(f"Keysight N5171B found with IP: {ip_address}")
                    found = 1  #control de error
                    return ip_address

        except socket.error:
            print("Keysight N5171B not found.")
            pass
    if found == 0:   #control de error
        raise RobotError(message="Keysight N5171B not found.")


# llamada a la función
# gen_address = find_n5171b()


def find_n9320b():  # analizador de espectros
    target_port = 5025  # estandar para comandos scpi
    found = 0  #control de error
    # escanea para encontrar dispositivos en la red ethernet
    for i in range(183, 189):  # rango asignado ya que conozco la ip
        ip_address = f'192.168.12.{i}'  # reemplaza con la ip dentro de rango

        try:
            # intento de conexion con el dispositivo
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)  # tiempo asignado para la conexion
                result = sock.connect_ex((ip_address, target_port))
                if result == 0:
                    print(f"Keysight N9320B found with IP: {ip_address}")
                    found = 1   #control de error
                    return ip_address

        except socket.error:
            print("Keysight N9320B not found.")
            pass
    if found == 0:   #control de error
        raise RobotError(message="Keysight N9320B not found.")


# llamada a la función
# spectrum_address = find_n9320b()


def find_e5063a():  # VNA analizador de redes vectorial
    target_port = 5025  # estandar para comandos scpi
    found = 0  #control de error
    # escanea para encontrar dispositivos en la red ethernet
    for i in range(205, 211):  # rango asignado ya que conozco la ip
        ip_address = f'192.168.12.{i}'  # reemplaza con la ip dentro de rango

        try:
            # intento de conexion con el dispositivo
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)  # tiempo asignado para la conexion
                result = sock.connect_ex((ip_address, target_port))
                if result == 0:
                    print(f"Keysight E5063a found with IP: {ip_address}")
                    found = 1   #control de error
                    return ip_address

        except socket.error:
            print("Keysight E5063a not found.")
            pass
    if found == 0:   #control de error
        raise RobotError(message="Keysight E5063a not found.")

# llamada a la función
# vectorial_address = find_e5063a()

##############################################funciones para abrir conexión con equipos#######################################################

def connect_to_signal_generator(gen_address):
    try:
        rm_gen = visa.ResourceManager()  # creo una instancia para manegar el instrumento
        instrument_generator = rm_gen.open_resource(f'TCPIP0::{gen_address}::inst0::INSTR')  # abrír conexión con el instrumento
        return instrument_generator
    except visa.VisaIOError as e:
        raise RobotError(message=f"Error connecting with instrument Keysights N5171B: {e}")


def connect_to_vectorial_analyzer(vectorial_address):
    try:
        rm_vect = visa.ResourceManager()  # creo una instancia para manegar el instrumento
        instrument_vectorial_analyzer = rm_vect.open_resource(f'TCPIP0::{vectorial_address}::inst0::INSTR')  # abrír conexión con el instrumento
        return instrument_vectorial_analyzer
    except visa.VisaIOError as e:
        raise RobotError(message=f"Error connecting with instrument Keysights E5063a: {e}")


def connect_to_spectrum_analyzer(spectrum_address):
    try:
        rm_spect = visa.ResourceManager()  # creo una instancia para manegar el instrumento
        instrument_spectrum = rm_spect.open_resource(f'TCPIP0::{spectrum_address}::inst0::INSTR')  # abrír conexión con el instrumento
        return instrument_spectrum
    except visa.VisaIOError as e:
        raise RobotError(message=f"Error connecting with instrument Keysights N9320B: {e}")


###########################################funciones para desconectar instrumentos#######################################################

def disconnect_from_signal_generator(instrument_generator):
    try:
        instrument_generator.close()  # Cierro la conexión
        print("Disconnecting from Keysights N5171B.")
    except visa.VisaIOError as e:
        print(f"Error disconnecting from Keysights N5171B: {e}")


def disconnect_from_vectorial_analyzer(instrument_vectorial_analyzer):
    try:
        instrument_vectorial_analyzer.close()  # Cierro la conexión
        print("Disconnecting from Keysights E5063a.")
    except visa.VisaIOError as e:
        print(f"Error disconnecting from Keysights E5063a: {e}")


def disconnect_from_spectrum_analyzer(instrument_spectrum):
    try:
        instrument_spectrum.close()  # Cierro la conexión
        print("Disconnecting from Keysights N9320B.")
    except visa.VisaIOError as e:
        print(f"Error disconnecting from N9320B: {e}")


##############################################funciones para enviar parametros#######################################################

def generator_barrido(instrument_generator, start_freq=None, stop_freq=None, start_amplitude=None, stop_amplitude=None, N_puntos=None):  # debo de pedir con imput los datos antes de llamar a la funcion
    # comienzo por activar el modo barrido para frecuencia
    instrument_generator.write(":FREQ:MODE LIST")
    time.sleep(2)
    # comienzo por activar el modo barrido para amplitud
    instrument_generator.write(":POWer:MODE LIST")
    time.sleep(2)
    try:
        # Configurar la frecuencia y la amplitud
        #if start_freq is None:
            #start_freq = input('Introduce the starting frecuency value: ')
            instrument_generator.write(f":FREQ:STAR {start_freq}")  # valor de frecuencia de inicio
        #if start_amplitude is None:
            #start_amplitude = input('Introduce the starting amplitude value in dBm´s: ')
            instrument_generator.write(f':POWer:STARt {start_amplitude} dBm')  # valor de amplitud
        #if stop_freq is None:
            #stop_freq = input('Introduce the stop frequency value: ')
            instrument_generator.write(f':FREQ:STOP {stop_freq}')
        #if stop_amplitude is None:
            #stop_amplitude = input("Introduce the stop amplitude value in dBm´s: ")
            instrument_generator.write(f":POWer:STOP {stop_amplitude} dbm")
        #if N_puntos is None:
            #N_puntos = input('Introduce the number of points for the frequency sweep: ')
            instrument_generator.write(f":SWE:POIN {N_puntos}")
            print(f'Los valores ajustados son frecuencia inicio: {start_freq},frecuencia final: {stop_freq}, amplitud inicial: {start_amplitude}, amplitud final: {stop_amplitude}, numero de puntos del barrido: {N_puntos}')
    except visa.VisaIOError as e:
        print(f"Error configuring the function generator: {e}")


def set_vectorial_analyzer_parameters(instrument_vectorial_analyzer, frequency=None, amplitude=None, points=None,
                                      form=None):
    try:
        # Reset del equipo
        instrument_vectorial_analyzer.write('*RST')
        # Configuración inicial
        if frequency is not None:
            instrument_vectorial_analyzer.write(f'SENS:FREQ:CENT {frequency}')

        if amplitude is not None:
            instrument_vectorial_analyzer.write(f'SENS:CHAN1:POW {amplitude}')

        if points is not None:
            instrument_vectorial_analyzer.write(f'SENS:SWE:POIN {points}')

        if form is not None:
            instrument_vectorial_analyzer.write(f'CALC1:FORM {form}')

        print(f"vectorial analyzer configured - Frequency: {frequency}, Amplitude: {amplitude}")
    except visa.VisaIOError as e:
        print(f"Error configuring the vectorial analyzer: {e}")


def set_spectrum_analyzer_parameters(instrument_spectrum, inicial_frequency=None, n_points=None, stop_frequency=None,
                                     bandwidth=None):
    try:
        # Configurar parametros necesarios del analizador de espectros
        if inicial_frequency is not None:
            instrument_spectrum.write(f"SENS:FREQ:STAR {inicial_frequency}")
        if stop_frequency is not None:
            instrument_spectrum.write(f"SENS:FREQ:STOP {stop_frequency}")
        if n_points is not None:
            instrument_spectrum.write(f"SENSe:SWEep:POINts {n_points}")

        instrument_spectrum.write("INITiate:CONTinuous OFF")  # Configura para una sola medición, no continua
        instrument_spectrum.write("DISPlay:WINDow:TRACe:Y:RLEVel 10")

        # Configuración del instrumento
        instrument_spectrum.write(f"SENSe:BANDwidth {bandwidth}")
        instrument_spectrum.write(":SENSe:ACQuisition:RATe:ANALog 20")
        instrument_spectrum.write(":DISPlay:TRACe:Y:SCALe:RLEVel -10 dBm")
        instrument_spectrum.write(":DISPlay:TRACe:Y:SCALe:PDIVision 10 dB")

        # Selecciona la medición de amplitud y frecuencia en el modo espectro
        instrument_spectrum.write(":SENSe:FUNCtion:ON:SPEctrum:AMPLitude")
        instrument_spectrum.write(":SENSe:FUNCtion:ON:SPEctrum:FREQuency")

        # Realiza la medición y lee los resultados
        instrument_spectrum.write(":INITiate:IMMediate;*WAI")
        frecuencia = instrument_spectrum.query(":SENSe:FREQuency:CENTer?")
        amplitud = instrument_spectrum.query(":CALCulate:MARKer:Y?")

        # Imprime los resultados
        print("Frecuencia: " + frecuencia)
        print("Amplitud: " + amplitud)

        print(
            f"spectrum analyzer configured - Frequency range: ({stop_frequency}-{inicial_frequency}), Nº of points: {n_points}")
    except visa.VisaIOError as e:
        print(f"Error configuring the spectrum analyzer: {e}")


##########################funciones para activar salida#######################################################

# Con estas funciones se persigue el activar la salida rf de los instrumentos si la tuviesen.  En el caso de el generador
# de funciones, por ejemplo.

def activar_salida_signal_generator(instrument_generator):
    try:
        instrument_generator.write(":OUTPut ON")
        print('salida RF activada')
        time.sleep(10)
    except visa.VisaIOError as e:
        print(f"Error activating output on signal generator: {e}")


def activar_salida_vectorial_analyzer(instrument_vectorial_analyzer):
    try:
        instrument_vectorial_analyzer.write(':OUTP ON')
        print('salida RF activada')
    except visa.VisaIOError as e:
        print(f"Error activating output on vectorial analyzer: {e}")


def activar_salida_spectrum_analyzer(instrument_spectrum):
    try:
        instrument_spectrum.write('OUTPUT:ON')
        print('salida RF activada')
    except visa.VisaIOError as e:
        print(f"Error activating output on spectrum analyzer: {e}")


#########################apagar salida RF#########################

def desactivar_salida_signal_generator(instrument_generator):
    try:
        instrument_generator.write(":OUTPut OFf")
        print('Salida RF apagada')
    except visa.VisaIOError as e:
        print(f"Error deactivating output on signal generator: {e}")


def desactivar_salida_vectorial_analyzer(instrument_vectorial_analyzer):
    try:
        instrument_vectorial_analyzer.write(":OUTP OFF")
        print('Salida RF apagada')
    except visa.VisaIOError as e:
        print(f"Error deactivating output on VNA: {e}")


##########################funciones para apagar los equipos #######################################################

def apagar_gen(instrument_generator):
    try:
        instrument_generator.write(":SYST:POFF")
        print('N5171B off')
    except visa.VisaIOError as e:
        print(f"Error shutting down Keysights N5171B: {e}")


def apagar_vectorial_analyzer(instrument_vectorial_analyzer):  # funciona!!
    try:
        instrument_vectorial_analyzer.write(":SYST:POFF")
        print('E5063A off')
    except visa.VisaIOError as e:
        print(f"Error shutting down Keysights E5063a: {e}")


def apagar_spectrum_analyzer(instrument_spectrum):
    try:
        instrument_spectrum.write(":SYST:POFF")
        print('N9320B off')
    except visa.VisaIOError as e:
        print(f"Error shutting down Keysights N9320B: {e}")



###########################función de ploteo de una señal con los datos obtenidos con VNA##########################

def plotting_res_freq_filtro(instrument_vectorial_analyzer, f_min, f_max, puntos):
    try:
        # Configurar el instrumento
        instrument_vectorial_analyzer.write(':DISP:SPL D12')  # configura el tipo de division para distintos graficos
        time.sleep(1)
        instrument_vectorial_analyzer.write(':CALC1:PAR:COUN 1')  # configura el numero de traces
        time.sleep(1)
        instrument_vectorial_analyzer.write(':CALC2:PAR:COUN 1')
        time.sleep(1)
        instrument_vectorial_analyzer.write(':CALC1:PAR1:DEF S12')
        time.sleep(1)
        instrument_vectorial_analyzer.write(':CALC2:PAR2:DEF S11')
        time.sleep(1)
        instrument_vectorial_analyzer.write(':CALC2:FORM SMIT')
        time.sleep(1)
        instrument_vectorial_analyzer.write(':SENS1:SWE:TYPE LIN')
        time.sleep(1)
        instrument_vectorial_analyzer.write(f':SENS1:FREQ:STAR {f_min}')  # Frecuencia inicial de barrido
        time.sleep(1)
        instrument_vectorial_analyzer.write(f':SENS2:FREQ:STAR {f_min}')
        time.sleep(1)
        instrument_vectorial_analyzer.write(f':SENS1:FREQ:STOP {f_max}')  # Frecuencia final de barrido
        time.sleep(1)
        instrument_vectorial_analyzer.write(f':SENS2:FREQ:STOP {f_max}')
        time.sleep(1)
        instrument_vectorial_analyzer.write(f':SENS1:SWE:POIN {puntos}')  # Número de puntos de medición
        time.sleep(1)
        instrument_vectorial_analyzer.write(f':SENS2:SWE:POIN {puntos}')
        time.sleep(1)
        instrument_vectorial_analyzer.write(':INIT1:CONT ON')  # permite la medida continua en ambas ventanas
        time.sleep(1)
        instrument_vectorial_analyzer.write(':INIT2:CONT ON')
        time.sleep(1)
        instrument_vectorial_analyzer.write(':INIT:CONT OFF')  # Medición única
        time.sleep(1)
        # Obtener datos de medición
        freqs = np.array(instrument_vectorial_analyzer.query_ascii_values(':SENS1:FREQ:DATA?'))
        value = np.array(instrument_vectorial_analyzer.query_ascii_values(':CALC1:DATA:FDAT?'))
        # Reshape para agrupar de dos en dos (números complejos)
        complex_value = value.reshape(-1, 2)
        # Crear un array de números complejos
        value = complex_value[:, 0] + 1j * complex_value[:, 1]
        print(len(freqs))
        print(len(value))

        plt.plot(freqs, value)
        plt.title('Respuesta en Frecuencia de un filtro')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Potencia (dB)')
        plt.show()
    except visa.VisaIOError as e:
        print(f"Error configuring instrument: {e}")


###############################funcion para caracterizar la impedancia de entrada de un dut############


def caracteriza_dut_sfreq(instrument_vectorial_analyzer, f_i, f_f, puntos, z0):
    try:
        # Configurar instrumento
        instrument_vectorial_analyzer.write(':SENS1:SWE:TYPE LIN')  # Tipo de barrido lineal
        time.sleep(1)
        instrument_vectorial_analyzer.write(':CALC1:FORM SMIT')  # Establecer formato de visualización
        time.sleep(1)
        instrument_vectorial_analyzer.write(f':SENS1:FREQ:STAR {f_i}')  # Frecuencia inicial
        time.sleep(1)
        instrument_vectorial_analyzer.write(f':SENS1:FREQ:STOP {f_f}')  # Frecuencia final
        time.sleep(1)
        instrument_vectorial_analyzer.write(f':SENS1:SWE:POIN {puntos}')  # Número de puntos de medición
        time.sleep(1)
        instrument_vectorial_analyzer.write(":CALC1:PAR1:DEF S11")  # calculo s11 coef reflex in
        time.sleep(1)
        instrument_vectorial_analyzer.write(":INIT:CONT OFF")
        time.sleep(2)
        # instrument_vectorial_analyzer.write(":CALC1:CONV ON")  # enciende el modo conversion para pasar de s a z
        time.sleep(1)
        # instrument_vectorial_analyzer.write(":CALC1:CONV:FUNC ZREF")  # cumple la conversion de S a Z
        instrument_vectorial_analyzer.write(':CALC1:FORM SMIT')  # Establecer formato de visualización
        time.sleep(1)
        instrument_vectorial_analyzer.write(":CALC1:MARK:REF ON")  # ACTIVO MARKER DE INICIO
        instrument_vectorial_analyzer.write(":CALC1:PAR1:SEL")  # SELECCIONO
        instrument_vectorial_analyzer.write(":CALC1:MARK1:ACT")  # activo el marcador 1
        instrument_vectorial_analyzer.write(":CALC1:MARK1:X 0")
        time.sleep(2)
        #instrument_vectorial_analyzer.write(":CALC1:MARK2:ACT")  # activo el marcador 2
        #instrument_vectorial_analyzer.write(":CALC1:MARK2:X 0")
        # Iniciar medición
        while int(instrument_vectorial_analyzer.query('*OPC?')) != 1:  # Esperar a que la medición termine
            pass
        time.sleep(1)
        # Obtener datos de medición
        freqs = np.array(instrument_vectorial_analyzer.query_ascii_values(':SENS1:FREQ:DATA?'))
        S11 = np.array(instrument_vectorial_analyzer.query_ascii_values(':CALC1:DATA:FDAT?'))
        print(f'This array contains all the S11 measurements: {S11}')
        # Reshape para agrupar de dos en dos (números complejos)
        complex_S11 = S11.reshape(-1, 2)
        # Crear un array de números complejos
        S11 = complex_S11[:, 0] + 1j * complex_S11[:, 1]
        print(f'This array contains all the S11 measurements in complex form: {S11}')
        reflections = (1-S11) / (1+S11)
        print(f'This array contains all the coef. reflexion measurements: {reflections}')
        impedances = 50* ((1 + reflections) / (1 - reflections))
        print(f'This array contains all the Zin measurements un-normalized: {impedances}')

        impedance_modulus = np.abs(impedances)
        print(f'This array contains all the Zin values in module for all measurements: {impedance_modulus}')
        # Graficar resultados
        plt.plot(freqs, impedances)
        plt.xscale('linear')
        plt.title('Valores de Impedancia dependientes de frecuencia')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Modulo Impedancia  de entrada')
        plt.show()

    except visa.VisaIOError as e:
        print(f"Error configuring instrument: {e}")


def caracteriza_dut(instrument_vectorial_analyzer, f_i, f_f, puntos):
    try:
        # Configurar instrumento
        instrument_vectorial_analyzer.write(':SENS1:SWE:TYPE LIN')  # Tipo de barrido lineal
        time.sleep(1)
        instrument_vectorial_analyzer.write(':CALC1:FORM PLOG')  # Establecer formato de visualización
        time.sleep(1)
        instrument_vectorial_analyzer.write(f':SENS1:FREQ:STAR {f_i}')  # Frecuencia inicial
        time.sleep(1)
        instrument_vectorial_analyzer.write(f':SENS1:FREQ:STOP {f_f}')  # Frecuencia final
        time.sleep(1)
        instrument_vectorial_analyzer.write(f':SENS1:SWE:POIN {puntos}')  # Número de puntos de medición
        time.sleep(1)
        instrument_vectorial_analyzer.write(":CALC1:PAR1:DEF S11")  # calculo s11 coef reflex in
        time.sleep(1)
        instrument_vectorial_analyzer.write(":INIT:CONT OFF")
        time.sleep(2)
        #instrument_vectorial_analyzer.write(":CALC1:CONV ON")  # enciende el modo conversion para pasar de s a z
        time.sleep(1)
        #instrument_vectorial_analyzer.write(":CALC1:CONV:FUNC ZREF")  # cumple la conversion de S a Z
        instrument_vectorial_analyzer.write(':CALC1:FORM SMIT')  # Establecer formato de visualización
        time.sleep(1)
        instrument_vectorial_analyzer.write(":CALC1:MARK:REF ON")  # ACTIVO MARKER DE INICIO
        instrument_vectorial_analyzer.write(":CALC1:PAR1:SEL")  # SELECCIONO
        instrument_vectorial_analyzer.write(":CALC1:MARK1:ACT")  # activo el marcador 1
        instrument_vectorial_analyzer.write(":CALC1:MARK1:X 0")
        time.sleep(5)
        instrument_vectorial_analyzer.write(":CALC1:MARK2:ACT")  # activo el marcador 2
        instrument_vectorial_analyzer.write(":CALC1:MARK2:X 0")
        time.sleep(2)
        # Iniciar medición
        while int(instrument_vectorial_analyzer.query('*OPC?')) != 1:  # Esperar a que la medición termine
            pass
        time.sleep(1)
        # Obtener datos de medición
        freqs = np.array(instrument_vectorial_analyzer.query_ascii_values(':SENS1:FREQ:DATA?'))
        S11 = np.array(instrument_vectorial_analyzer.query_ascii_values(':CALC1:DATA:FDAT?'))
        # Reshape para agrupar de dos en dos (números complejos)
        complex_S11 = S11.reshape(-1, 2)
        # Crear un array de números complejos
        S11 = complex_S11[:, 0] + 1j * complex_S11[:, 1]

        Zin = (1+S11)/(1-S11)
        # Imprimir el array de impedancias complejas
        print(len(S11))
        print(len(freqs))

        # Graficar resultados
        plt.plot(freqs, Zin)
        plt.xscale('linear')
        plt.title('Valores de Impedancia dependientes de frecuencia')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Modulo Impedancia  de entrada')
        plt.show()
    except visa.VisaIOError as e:
        print(f"Error configuring instrument: {e}")


######################################################funcion genera_onda_generador de señales#########################################


def genera_onda(instrument_generator, frequency=None, amplitude=None):
    #if frequency is None:
        #frequency = input('Introduce frequency value: ')
        instrument_generator.write(f":FREQ {frequency}")
        print(f'El valor de frecuencia es: {frequency}')
    #if amplitude is None:
        #amplitude = int(input('Introduce amplitude value: '))
        instrument_generator.write(f":POWer:LEVel:IMMediate:AMPLitude {amplitude} dbm")
        print(f'El valor de amplitud es: {amplitude}dBm´s')


#########################################################funcion para resetear equipos ########################################


def reset_generador(instrument_generator):
    try:
        instrument_generator.write('*RST')
        print('Instrument reset done.')
    except visa.VisaIOError as e:
        print(f"Error resetting Keysights N5171B: {e}")


# @keyword("Reset Vectorial Analyzer")
def reset_vectorial(instrument_vectorial_analyzer):
    try:
        instrument_vectorial_analyzer.write('SYST:PRES')
        print('Instrument reset done.')
    except visa.VisaIOError as e:
        print(f"Error resetting Keysights E5063A: {e}")


def reset_spectrum(instrument_spectrum):
    try:
        instrument_spectrum.write('*RST')
        print('Instrument reset done')
    except visa.VisaIOError as e:
        print(f"Error resetting Keysights N9320B: {e}")


######################################################### funcion para encender o apagar la salida de modulacion

def modulacion_off_on(instrument_generator, state=None):
    #if state is None:
        #state = input("Introduce modulation ON or OFF: ")

        if state.upper() == "ON":
            try:
                instrument_generator.write(":OUTP:MOD ON")
                print("Modulation on.")
            except visa.VisaIOError as e:
                print(f"Error turning on modulation: {e}")
        elif state.upper() == "OFF":
            try:
                instrument_generator.write(":OUTP:MOD OFf")
                print("Modulation off.")
            except visa.VisaIOError as e:
                print(f"Error turning off modulation: {e}")
        else:
            print("Invalid input. Please, introduce 'on' or 'off'.")


##################################funcion que selecciona modulacion AM ####################################

def modulacion_am(instrument_generator, modo, tipo, i_mod, shape, ratio):
    try:
        instrument_generator.write(':AM1:STAT ON')
    except visa.VisaIOError as e:
        print(f"Error setting AM on: {e}")
        time.sleep(5)

    estado = instrument_generator.query('AM1:STAT?')
    if estado != 0:
        print(f'AM modulation on.')
    elif estado == 0:
        print('AM modulation off')
        time.sleep(2)
    try:
        #modo = input('Introduce AM modulation mode; DEEP o NORM: ')
        instrument_generator.write(f':AM:MODE {modo}')
        print(f'Selected mode: {modo}')
    except visa.VisaIOError as e:
        print(f"Error setting AM mode: {e}")
        time.sleep(2)
    try:
        #tipo = input('Introduce AM modulation type.  Exponencial (EXP) or Lineal (LIN): ')
        instrument_generator.write(f':AM1:TYPE {tipo}')
        print(f'Type of AM modulation: {tipo}')
    except visa.VisaIOError as e:
        print(f"Error setting AM modulation type: {e}")
        time.sleep(2)
    try:
        if tipo == 'LIN':
            #i_mod = input('Introduce deviation index in percentage: ')
            instrument_generator.write(f":AM1 {i_mod}")  # indice de modulacion en porcentage
            print(f'Selection of deviation index to: {i_mod}%')
        else:
            #i_mod = input('Introduce deviation index in dB´s: ')
            instrument_generator.write(f":AM1:EXP {i_mod}")  # indice de modulacion en dB´s
            print(f'Selection of deviation index to: {i_mod} dB´s')
    except visa.VisaIOError as e:
        print(f"Error setting deviation index: {e}")
        time.sleep(2)
    try:
        #shape = input('Introduce type of function shape; SINE for sinusoid|TRI for triangular|SQU for squared y RAMP for step:')
        instrument_generator.write(f":AM1:INT:FUNC1:SHAP {shape}")
        print(f'type of function shape:  {shape}')
    except visa.VisaIOError as e:
        print(f"Error setting AM modulation shape: {e}")
        time.sleep(2)
    try:
        #ratio = input('Introduce the frequency ratio for AM modulation in Hertz: ')
        instrument_generator.write(f":AM1:INT:FUNC1:FREQ {ratio}")
        print(f'frequency ratio adjusted to:  {ratio}Hz')
    except visa.VisaIOError as e:
        print(f"Error setting AM modulation frequency ratio: {e}")
        time.sleep(2)
    try:
        time.sleep(3)
        instrument_generator.write('*TRG')
        print('Initiating modulation')
    except visa.VisaIOError as e:
        print(f"Error setting up the trigger: {e}")


###################################### función para demodular ##################################


def demod_fm(instrument_spectrum,cnt_freq, span):
    try:
        instrument_spectrum.write(f':FREQ:CENT {cnt_freq}')
    except visa.VisaIOError as e:
        print(f"Error setting center frequency: {e}")
    time.sleep(1)
    try:
        instrument_spectrum.write(f':FREQ:SPAN {span}')  # ajusto el span a zero para escuchar demodulación
    except visa.VisaIOError as e:
        print(f"Error setting frequency span: {e}")
    time.sleep(1)
    try:
        instrument_spectrum.write(':CALC:MARK1:STAT ON')  # activo marcador 1
    except visa.VisaIOError as e:
        print(f"Error activating marker: {e}")
    time.sleep(1)
    try:
        instrument_spectrum.write(':CALC:MARK1:MAX')  # se supone que situa el marcador en el pico mayor
        instrument_spectrum.write(':BAND 100e3')
    except visa.VisaIOError as e:
        print(f"Error turning marker on: {e}")
    time.sleep(1)
    try:
        instrument_spectrum.write(':DEM:FM:STAT ON')  # activo demodulación y se escucha el audio transmitido con la raspberry
        print(f'Demodulation centered at: {cnt_freq} Hz')
    except visa.VisaIOError as e:
        print(f"Error demodulation state on: {e}")
    time.sleep(1)


############################################### FUNCIONES PARA PARAMETROS S ###########################################################3

def parametro_s11_sfreq(instrument_vectorial_analyzer, frecuencia):
    instrument_vectorial_analyzer.write(':SYST:PRES')  # hago preset del sistema
    time.sleep(1)
    instrument_vectorial_analyzer.write(":CALC1:PAR1:DEF S11")  # definición del parametro a medir
    time.sleep(1)
    instrument_vectorial_analyzer.write(":SENS1:SWE:TYPE LIN")  # tipo de barrido, lineal, log
    time.sleep(1)
    #frecuencia = input('Introduce frequency value: ')
    instrument_vectorial_analyzer.write(f":SENS1:FREQ:STAR {frecuencia}")  # para una unica frecuencia se pone la misma en ambos inicio y parada
    instrument_vectorial_analyzer.write(f":SENS1:FREQ:STOP {frecuencia}")
    time.sleep(1)
    instrument_vectorial_analyzer.write(":SENS1:SWE:POIN 2")  # numero minimo de puntos, 2 no admite 1
    time.sleep(1)
    instrument_vectorial_analyzer.write(":CALC1:FORM SMIT")  # formato de calculo carta de smith lineal **** he puesto (1) en calc...comprobar
    time.sleep(1)
    instrument_vectorial_analyzer.write(":INIT:CONT OFF")  # cancelo el barrido continuo
    time.sleep(1)
    instrument_vectorial_analyzer.write(":CALC1:MARK1 ON")  # activo el marcador 1
    time.sleep(1)
    instrument_vectorial_analyzer.query('*OPC?')
    time.sleep(1)
    instrument_vectorial_analyzer.write(":CALC1:PAR1:SEL")  # asocia el trace activo a un numero de parametro, en este caso S11
    s11 = instrument_vectorial_analyzer.query_ascii_values(":CALC1:DATA:FDAT?")
    parte_real = s11[0]
    parte_imag = s11[1]
    s11 = complex(parte_real, parte_imag)
    print("Parameter s11 is: ", s11)

    s11_mod, fase = cmath.polar(s11)
    fase = math.degrees(fase)
    print('Module:', s11_mod, 'phase:', fase, 'degrees')

def parametro_s11_barrido(instrument_vectorial_analyzer, fmin, fmax, puntos):

    instrument_vectorial_analyzer.write(":CALC1:PAR1:DEF S11")  # comando para seleccionar el parametro a medir S11
    time.sleep(1)
    instrument_vectorial_analyzer.write(":SENS1:SWE:TYPE LIN")  # tipo de barrido, lineal
    time.sleep(1)
    instrument_vectorial_analyzer.write(f":SENS1:FREQ:STAR {fmin}")  # frecuencia de inicio
    time.sleep(1)
    instrument_vectorial_analyzer.write(f":SENS1:FREQ:STOP {fmax}")  # frecuencia de parada
    time.sleep(1)
    instrument_vectorial_analyzer.write(f":SENS1:SWE:POIN {puntos}")  # numero minimo de puntos de barrido
    time.sleep(1)
    instrument_vectorial_analyzer.write(":CALC:FORM MLOG")  # formato de calculo, smith
    time.sleep(1)
    instrument_vectorial_analyzer.write(":INIT:CONT OFF")  # deberia de dar una unica medida
    time.sleep(3)
    instrument_vectorial_analyzer.query('*OPC?')  # Espera a que acaben todas las operaciones
    # activacion de markers
    instrument_vectorial_analyzer.write(":CALC1:MARK1 ON")  # Enciendo o apago markers
    time.sleep(1)
    instrument_vectorial_analyzer.write(":CALC1:MARK2 ON")  # Enciendo o apago markers
    time.sleep(1)
    instrument_vectorial_analyzer.write(f":CALC1:MARK1:X {fmin}")  # pongo el marcador en el punto de f inicial
    instrument_vectorial_analyzer.write(f":CALC1:MARK2:X {fmax}")  # pongo el marcador en el punto de f final

    # grafico
    # Obtener datos de medición
    freqs = np.array(instrument_vectorial_analyzer.query_ascii_values(':SENS1:FREQ:DATA?'))
    value = np.array(instrument_vectorial_analyzer.query_ascii_values(':CALC1:DATA:FDAT?'))
    # Reshape para agrupar de dos en dos (números complejos)
    complex_value = value.reshape(-1, 2)
    # Crear un array de números complejos
    value = complex_value[:, 0] + 1j * complex_value[:, 1]
    plt.title('Valores de S11 en un rango de frecuencia.')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('dB´s')
    plt.plot(freqs, value)
    plt.show()


def parametro_Scattering_sfreq(instrument_vectorial_analyzer, barrido, parametro, f_unique, f_inicio, f_fin, puntos):
    while True:
        #barrido = input('measure single frequency, or sweep?: ')

        if barrido.lower() == 'single':
            try:
                instrument_vectorial_analyzer.write(f":SENS1:FREQ:STAR {f_unique}")  # para una unica frecuencia se pone la misma en ambos inicio y parada
                instrument_vectorial_analyzer.write(f":SENS1:FREQ:STOP {f_unique}")
                time.sleep(1)
                puntos = 2  # para una unica frecuencia se calcula un unico punto
                instrument_vectorial_analyzer.write(f":SENS1:SWE:POIN {puntos}")
                time.sleep(1)
                if parametro.upper() == 'S11':
                    instrument_vectorial_analyzer.write(':CALC1:FORM SMIT')
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:DEF S11")
                    instrument_vectorial_analyzer.write(":SENS1:SWE:TYPE LIN")
                    time.sleep(1)
                    instrument_vectorial_analyzer.write("INIT:CONT ON")
                    instrument_vectorial_analyzer.query('*OPC?')
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:SEL")  # asocia el trace activo a un numero de parametro, en este caso S11
                    instrument_vectorial_analyzer.write(':CALC1:MARK1 ON')
                    instrument_vectorial_analyzer.write(':CALC1:MARK1:X 0')
                    instrument_vectorial_analyzer.write("INIT:CONT OFf")
                    S11 = np.array(instrument_vectorial_analyzer.query_ascii_values(":CALC1:DATA:FDAT?"))
                    complex_value = S11.reshape(-1, 2)
                    # Crear un array de números complejos
                    S11 = (complex_value[:, 0] + 1j * complex_value[:, 1])
                    print(f'Parameter S11 is {S11[0]} ')
                    break
                elif parametro.upper() == 'S12':
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:DEF S12")
                    time.sleep(1)
                    instrument_vectorial_analyzer.write(':CALC1:FORM PLOG')
                    instrument_vectorial_analyzer.write(":SENS1:SWE:TYPE LIN")
                    time.sleep(1)
                    instrument_vectorial_analyzer.write("INIT:CONT ON")
                    instrument_vectorial_analyzer.query('*OPC?')
                    instrument_vectorial_analyzer.write(':CALC1:MARK1 ON')
                    instrument_vectorial_analyzer.write(':CALC1:MARK1:X 0')
                    instrument_vectorial_analyzer.write("INIT:CONT OFf")
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:SEL")
                    S12 = np.array(instrument_vectorial_analyzer.query_ascii_values(":CALC1:DATA:FDAT?"))
                    #complex_value = S12.reshape(-1, 2)
                    # Crear un array de números complejos
                    #S12 = (complex_value[:, 0] + 1j * complex_value[:, 1])
                    print(f'Parameter S12 is {S12[0]} dB and phase {S12[1]}º degrees')
                    break
                elif parametro.upper() == 'S21':
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:DEF S21")
                    time.sleep(1)
                    instrument_vectorial_analyzer.write(':CALC1:FORM PLOG')
                    instrument_vectorial_analyzer.write(":SENS1:SWE:TYPE LIN")
                    time.sleep(1)
                    instrument_vectorial_analyzer.write("INIT:CONT ON")
                    instrument_vectorial_analyzer.write(':CALC1:MARK1 ON')
                    instrument_vectorial_analyzer.write(':CALC1:MARK1:X 0')
                    instrument_vectorial_analyzer.write("INIT:CONT OFf")
                    instrument_vectorial_analyzer.query('*OPC?')
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:SEL")
                    S21 = np.array(instrument_vectorial_analyzer.query_ascii_values(':CALC1:DATA:FDAT?'))
                    #complex_value = S21.reshape(-1, 2)
                    # Crear un array de números complejos
                    #S21 = (complex_value[:, 0] + 1j * complex_value[:, 1])
                    print(f'Parameter S21 is {S21[0]} dB and phase {S21[1]}º degrees ')
                    break
                elif parametro.upper() == 'S22':
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:DEF S22")
                    time.sleep(2)
                    instrument_vectorial_analyzer.write(':CALC1:FORM SMIT')
                    instrument_vectorial_analyzer.write(":SENS1:SWE:TYPE LIN")
                    time.sleep(4)
                    instrument_vectorial_analyzer.write("INIT:CONT ON")
                    instrument_vectorial_analyzer.query('*OPC?')
                    time.sleep(2)
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:SEL")
                    instrument_vectorial_analyzer.write(':CALC1:MARK1 ON')
                    instrument_vectorial_analyzer.write(':CALC1:MARK1:X 0')
                    instrument_vectorial_analyzer.write("INIT:CONT OFf")
                    S22 = np.array(instrument_vectorial_analyzer.query_ascii_values(':CALC1:DATA:FDAT?'))
                    complex_value = S22.reshape(-1, 2)
                    # Crear un array de números complejos
                    S22 = (complex_value[:, 0] + 1j * complex_value[:, 1])
                    print(f'Parameter S22 is {S22[0]} ')
                    break
            except visa.VisaIOError as e:
                print(f"Error completing measurement: {e}")
                ###### aqui para barrido, arriba single point#################################33

        elif barrido.lower() == 'sweep':
            try:
                instrument_vectorial_analyzer.write(f":SENS1:FREQ:STAR {f_inicio}")  # para una unica frecuencia se pone la misma en ambos inicio y parada
                instrument_vectorial_analyzer.write(f":SENS1:FREQ:STOP {f_fin}")
                time.sleep(1)
                instrument_vectorial_analyzer.write(f":SENS1:SWE:POIN {puntos}")
                time.sleep(1)
                if parametro.upper() == 'S11':
                    instrument_vectorial_analyzer.write(':CALC1:FORM SMIT')
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:DEF S11")
                    instrument_vectorial_analyzer.write(":SENS1:SWE:TYPE LIN")
                    time.sleep(1)
                    instrument_vectorial_analyzer.write("INIT:CONT ON")
                    instrument_vectorial_analyzer.query('*OPC?')
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:SEL")  # asocia el trace activo a un numero de parametro, en este caso S11
                    S11 = np.array(instrument_vectorial_analyzer.query_ascii_values(":CALC1:DATA:FDAT?"))
                    complex_value = S11.reshape(-1, 2)
                    # Crear un array de números complejos
                    S11 = complex_value[:, 0] + 1j * complex_value[:, 1]
                    S11_real = S11.real
                    print(f'Parameter S11 is {S11} ')
                    freqs = np.array(instrument_vectorial_analyzer.query_ascii_values(':SENS1:FREQ:DATA?'))

                    plt.title('Parametro S11')
                    plt.xlabel('Frecuencia (Hz)')
                    plt.ylabel('S11 (Real part)')
                    plt.plot(freqs, S11_real)
                    plt.show()
                    break
                elif parametro.upper() == 'S12':
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:DEF S12")
                    time.sleep(1)
                    instrument_vectorial_analyzer.write(':CALC1:FORM PLOG')
                    instrument_vectorial_analyzer.write(":SENS1:SWE:TYPE LIN")
                    time.sleep(1)
                    instrument_vectorial_analyzer.write("INIT:CONT ON")
                    instrument_vectorial_analyzer.query('*OPC?')
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:SEL")
                    S12 = np.array(instrument_vectorial_analyzer.query_ascii_values(':CALC1:DATA:FDAT?'))
                    S12_dB = [S12[i] for i in range(0, len(S12), 2)]
                    # Obtener datos de medición
                    freqs = np.array(instrument_vectorial_analyzer.query_ascii_values(':SENS1:FREQ:DATA?'))

                    # grafico
                    plt.title('Parametro S12')
                    plt.xlabel('Frecuencia (Hz)')
                    plt.ylabel('S12 (dB´s)')
                    plt.plot(freqs, S12_dB)
                    plt.show()
                    break
                elif parametro.upper() == 'S21':
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:DEF S21")
                    time.sleep(1)
                    instrument_vectorial_analyzer.write(':CALC1:FORM PLOG')
                    instrument_vectorial_analyzer.write(":SENS1:SWE:TYPE LIN")
                    time.sleep(1)
                    instrument_vectorial_analyzer.write("INIT:CONT ON")
                    instrument_vectorial_analyzer.query('*OPC?')
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:SEL")
                    S21 = np.array(instrument_vectorial_analyzer.query_ascii_values(':CALC1:DATA:FDAT?'))
                    S21_dB = [S21[i] for i in range(0, len(S21), 2)]
                    print(f'Parameter S21 is {S21[0]} dB and phase {S21[1]}º degrees ')
                    # grafico
                    # Obtener datos de medición
                    freqs = np.array(instrument_vectorial_analyzer.query_ascii_values(':SENS1:FREQ:DATA?'))
                    plt.title('Parametro S21')
                    plt.xlabel('Frecuencia (Hz)')
                    plt.ylabel('S21 (dB´s)')
                    plt.plot(freqs, S21_dB)
                    plt.show()
                    break
                elif parametro.upper() == 'S22':
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:DEF S22")
                    time.sleep(2)
                    instrument_vectorial_analyzer.write(':CALC1:FORM SMIT')
                    instrument_vectorial_analyzer.write(":SENS1:SWE:TYPE LIN")
                    time.sleep(2)
                    instrument_vectorial_analyzer.write("INIT:CONT ON")
                    instrument_vectorial_analyzer.query('*OPC?')
                    time.sleep(2)
                    instrument_vectorial_analyzer.write(":CALC1:PAR1:SEL")
                    S22 = np.array(instrument_vectorial_analyzer.query_ascii_values(':CALC1:DATA:FDAT?'))
                    complex_value = S22.reshape(-1, 2)
                    S22 = complex_value[:, 0] + 1j * complex_value[:, 1]
                    print(f'Parameter S22 is: {S22} ')
                    freqs = np.array(instrument_vectorial_analyzer.query_ascii_values(':SENS1:FREQ:DATA?'))
                    plt.title('Parametro S22')
                    plt.xlabel('Frecuencia (Hz)')
                    plt.ylabel('S22 (dB´s)')
                    plt.plot(freqs, S22)
                    plt.show()
                    break
            except visa.VisaIOError as e:
                print(f"Error completing measurement: {e}")

        else:
            print('Error: Please, introduce "single" or "sweep".')


def parametro_s12_barrido(instrument_vectorial_analyzer):
    instrument_vectorial_analyzer.write(':SYST:PRES')  # hago reset del sistema
    time.sleep(5)
    try:
        S12 = instrument_vectorial_analyzer.write(":CALC1:PAR1:DEF S12")
        time.sleep(5)
        instrument_vectorial_analyzer.write(":SENS1:SWE:TYPE LIN")
        time.sleep(5)
        instrument_vectorial_analyzer.write("SENS1:SWE:MODE SING")
        time.sleep(5)
        instrument_vectorial_analyzer.write(":SENS1:FREQ:STAR 1000000")
        time.sleep(5)
        instrument_vectorial_analyzer.write(":SENS1:FREQ:STOP 10000000")
        time.sleep(5)
        instrument_vectorial_analyzer.write(":SENS1:SWE:POIN 201")
        time.sleep(5)
        instrument_vectorial_analyzer.write(":CALC:FORM PLOG")
        instrument_vectorial_analyzer.write("INIT:IMM")
        instrument_vectorial_analyzer.query('*OPC?')
    except visa.VisaIOError as e:
        print(f"Error completing measurement: {e}")


def grafico(instrument_vectorial_analyzer):  # ajustar y comprobar esto
    # Graficar los resultados obtenidos
    F_inicio = instrument_vectorial_analyzer.query_ascii_values(":SENS1:FREQ:STAR?")
    F_final = instrument_vectorial_analyzer.query_ascii_values(":SENS1:FREQ:STOP?")
    S11 = instrument_vectorial_analyzer.query_ascii_values(":CALC1:DATA:FDAT?")
    frecuencias = np.linspace(F_inicio, F_final, len(S11))  # Rango de frecuencias
    plt.plot(frecuencias, S11, label='S11')
    plt.xlabel('Frecuencia (GHz)')
    plt.ylabel('S11')
    plt.title('Parameter S11 values in range of frequencies')
    plt.legend()
    plt.grid(True)
    plt.show()


############################### funcion para modificar la impedancia caracteristica#############33333

def set_impedancia(instrument_vectorial_analyzer, z0):
    try:
        #z0 = input("Introduce the desired value of z0: ")
        instrument_vectorial_analyzer.write(f"SENS1:CORR:IMP {z0}")
        print(f"Impedance z0 adjusted to: {z0} Ohms")
    except visa.VisaIOError as e:
        print(f"Error completing action: {e}")


################################### funcion para calcular el retardo de grupo #############################################

def calculo_Gdelay(instrument_vectorial_analyzer, f_in, f_out):
    try:
        instrument_vectorial_analyzer.write(':SYST:PRES')  # Restablecer instrumento a valores por defecto
        instrument_vectorial_analyzer.write(':SENS1:SWE:TYPE LIN')  # Tipo de barrido lineal
        #f_in = input('Introduce inicial frequency: ')
        instrument_vectorial_analyzer.write(f':SENS1:FREQ:STAR {f_in}')  # Frecuencia inicial
        #f_out = input('Introduce final frequency: ')
        instrument_vectorial_analyzer.write(f':SENS1:FREQ:STOP {f_out}')  # Frecuencia final
        instrument_vectorial_analyzer.write(':SENS1:SWE:POIN 201')  # Número de puntos de medición
        instrument_vectorial_analyzer.write(':CALC1:PAR:DEF S21')  # Definir parámetro S21
        instrument_vectorial_analyzer.write(':CALC1:FORM MLOG')  # Establecer formato de visualización

        # Conectar la línea de coaxial al puerto de referencia del analizador
        instrument_vectorial_analyzer.write('SENS1:CORR:COLL:CKIT:PORT:SEL \'PORT1\'')  # Seleccionar el puerto 1 como referencia
        instrument_vectorial_analyzer.write('SENS1:CORR:COLL:CKIT:REMO:TYPE COAX')  # Tipo de kit de calibración
        instrument_vectorial_analyzer.write('SENS1:CORR:COLL:CKIT:REMO')  # Conectar el kit de calibración

        # Configurar medición de retardo de grupo
        instrument_vectorial_analyzer.write(':CALC1:PAR1:DEF GDEL')  # Definir parámetro GDEL
        instrument_vectorial_analyzer.write(':CALC1:FORM MLOG')  # Establecer formato de visualización
        instrument_vectorial_analyzer.write(':SENS1:CORR:LENG:ADJ:OFFS:TYPE DLY')  # Tipo de corrección de longitud de cable
        instrument_vectorial_analyzer.write(':SENS1:CORR:LENG:ADJ:OFFS:TIME 5E-9')  # Tiempo de retardo del cable

        # Iniciar medición
        instrument_vectorial_analyzer.write('*TRG')  # Iniciar medición
        while int(instrument_vectorial_analyzer.query('*OPC?')) != 1:  # Esperar a que la medición termine
            pass

        # Obtener datos de medición
        freqs = np.array(instrument_vectorial_analyzer.query_ascii_values(':SENS1:FREQ:DATA?'))
        gdel_ns = np.array(instrument_vectorial_analyzer.query_ascii_values(':CALC1:DATA:FDAT?'))
        print(len(freqs))
        print(len(gdel_ns))

        # Graficar resultados
        # plt.plot(freqs, gdel_ns)
    # plt.xscale('log')

    except visa.VisaIOError as e:
        print(f"Error completing action: {e}")


def visualiza_señal(instrument_spectrum):
    try:
        instrument_spectrum.write(':CALC1:AUTO')
        time.sleep(1)
        instrument_spectrum.write(':CALC1:MARK1:TRCK ON')
        time.sleep(1)
        instrument_spectrum.write(':INIT:CONT 0')
        time.sleep(1)
        data_str = instrument_spectrum.query(':TRACe:DATA? TRACE1')  # Get data as a string
        time.sleep(1)

# Close the connection
       # instrument_spectrum.close()

        # Parse the Data
        data = np.array([float(val) for val in data_str.split(',')])

        # Plot the Data
        freq_range = np.linspace(1e9, 2e9, len(data))
        plt.plot(freq_range, data)
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Amplitud (dBm)')
        plt.title('Spectrum Analyzer Display')
        plt.grid(True)
        plt.show()
        print('Graph generated.')
        #print(instrument_spectrum.query(':CALC1:MARK1?'))
    except Exception as e:
        print(f"Error completing action: {e}")




