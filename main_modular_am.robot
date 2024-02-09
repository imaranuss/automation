*** Settings ***

Library  ../../modulo/keywords.py

*** Variables ***
${gen_address}
${instrument_generator}
${modo}     DEEP    # opciones Deep o Normal
${tipo}     LIN     # opciones lineal o exponencial
${i_mod}    10      #Indice de modulación en dB´s
${shape}    SIN     #forma de onda
${ratio}    400      # ratio de frecuencia
${modulacion_on }    ON      #enciende la modulacion o no
${modulacion_off }    OFF      #enciende la modulacion o no
${frequency}        10e6        # valor de frecuencia de la onda
${amplitude}        -10         # valor de amplitud en dBm´s
*** Test Cases ***

Task 1 Find
    [Documentation]    Finding the instrument on the network
    [Tags]    Step 00 this step finds the instrument´s IP address
    ${gen_address}=   find_n5171b
    Set Global Variable     ${gen_address}
    Log     ${gen_address}

Task 2 Connect
    [Documentation]    Connecting to signal generator via IP address
    [Tags]    Step 01 this step opens a connection
    ${instrument_generator}=  connect_to_signal_generator  ${gen_address}
    Set Global Variable     ${instrument_generator}
    Log     ${instrument_generator}

Task 3 Reset instrument
    [Documentation]    resetting instrument
    [Tags]    Step 02 this step applies a reset
    reset_generador  ${instrument_generator}

Task 4 Performing main task
    [Documentation]    generating a signal
    [Tags]    Step 03 this step performs main task
    genera_onda  ${instrument_generator}        ${frequency}        ${amplitude}

Task 5 Selecting AM modulation
    [Documentation]    selecction of the AM modulation with all the required parameters
    [Tags]    Step 04 this step selects AM modulation
    modulacion_am  ${instrument_generator}      ${modo}    ${tipo}     ${i_mod}      ${shape}     ${ratio}

Task 6 Output on/off
    [Documentation]    turn on or off the output
    [Tags]    Step 06 this step changes state of output
    activar_salida_signal_generator  ${instrument_generator}

Task 7 Modulation on/off
    [Documentation]    turn on or off modulation
    [Tags]    Step 05 this step turns state of modulation
    modulacion_off_on  ${instrument_generator}      ${modulacion_on }
    Sleep   3s

Task 8 Modulation on/off
    [Documentation]    turn on or off modulation
    [Tags]    Step 05 this step turns state of modulation
    modulacion_off_on  ${instrument_generator}      ${modulacion_off }
    Sleep   3s

Task 9 Modulation on/off
    [Documentation]    turn on or off modulation
    [Tags]    Step 05 this step turns state of modulation
    modulacion_off_on  ${instrument_generator}      ${modulacion_on }
    Sleep   3s

Task 10 Modulation on/off
    [Documentation]    turn on or off modulation
    [Tags]    Step 05 this step turns state of modulation
    modulacion_off_on  ${instrument_generator}      ${modulacion_off }
    Sleep   3s

Task 11 Output
    [Documentation]    deactivate output
    [Tags]    Step 07 this step turns off output
    desactivar_salida_signal_generator  ${instrument_generator}

Task 12 Disconnecting procedure
    [Documentation]    This part is in charged of disconnection
    [Tags]    Step 08 this step ends connection with instrument
    disconnect_from_signal_generator  ${instrument_generator}

