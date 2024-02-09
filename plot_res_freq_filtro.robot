*** Settings ***

Library  ../../modulo/keywords.py

*** Variables ***
${vectorial_address}
${instrument_vectorial_analyzer}
${z0_impedance}     50      # seleccion del valor de impedancia caracteristica interna
${f_min}        40e6       #frecuencia de inicio para visualizar
${f_max}        150e6       #frecuencia de parada para visualizar
${puntos}       2001        #numero de puntos de la medida
*** Test Cases ***

Task 1 Find
    [Documentation]    Find instruments on the network
    [Tags]    Step 00 This step finds the instrument
    ${vectorial_address}=   find_e5063a
    Set Global Variable     ${vectorial_address}
    Log   ${vectorial_address}

Task 2 Connect
    [Documentation]    Connecting to VNA via IP address
    [Tags]    Step 01 This step opens a connection with the instrument
    ${instrument_vectorial_analyzer}=  connect_to_vectorial_analyzer  ${vectorial_address}
    Set Global Variable     ${instrument_vectorial_analyzer}
    Log     ${instrument_vectorial_analyzer}

Task 3 Reset instrument
    [Documentation]    resetting instrument
    [Tags]    Step 02 This step applies a reset to the instrument
    reset_vectorial  ${instrument_vectorial_analyzer}

Task 4 Set internal Impedance
    [Documentation]    performing selection of internal impedance between 50 and 75 ohms
    [Tags]    Step 03 This step sets the impedance value
    set_impedancia  ${instrument_vectorial_analyzer}        ${z0_impedance}

Task 5 Performing main measurement
    [Documentation]    plotting the frequency response of a filter (lp,bp,hp)
    [Tags]    Step 04 This step performs the main task
    plotting_res_freq_filtro  ${instrument_vectorial_analyzer}      ${f_min}       ${f_max}       ${puntos}

Task 6 Disconnecting procedure
    [Documentation]    disconnecting from the VNA
    [Tags]    Step 05 This step ends connection with the instrument
    disconnect_from_vectorial_analyzer     ${instrument_vectorial_analyzer}
