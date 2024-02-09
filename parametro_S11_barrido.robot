*** Settings ***

Library    ../../modulo/keywords.py

*** Variables ***
${vectorial_address}
${instrument_vectorial_analyzer}
${value_z0}     50
${fmin}         1.5e9
${fmax}         3.5e9
${puntos}       20001
*** Test Cases ***

Task 1 Find
    [Documentation]    Find instruments on the network
    [Tags]    Step 00 This step finds the IP address of the instrument
    ${vectorial_address}=   find_e5063a
    Set Global Variable     ${vectorial_address}
    Log    ${vectorial_address}

Task 2 Connect
    [Documentation]    Connecting to a VNA via IP address
    [Tags]    Step 01 This step opens connection with the instrument
    ${instrument_vectorial_analyzer}=  connect_to_vectorial_analyzer  ${vectorial_address}
    Set Global Variable    ${instrument_vectorial_analyzer}
    Log     ${instrument_vectorial_analyzer}

Task 3 Reset instrument
    [Documentation]    resetting instrument
    [Tags]    Step 02 This step applies a reset to the instrument
    reset_vectorial  ${instrument_vectorial_analyzer}


Task 4 Set internal Impedance
    [Documentation]    performing selection of internal impedance between 50 and 75 ohms
    [Tags]    Step 03 This step sets the impedance value
    set_impedancia  ${instrument_vectorial_analyzer}        ${value_z0}

Task 5 Performing measurement
    [Documentation]    measuring S11 parameter in a range of frequencies
    [Tags]    Step 04 This step performs the main task
    parametro_s11_barrido  ${instrument_vectorial_analyzer}     ${fmin}     ${fmax}          ${puntos}

Task 6 Output
    [Documentation]    activating output
    [Tags]    Step 05 This step turns on output
    activar_salida_vectorial_analyzer  ${instrument_vectorial_analyzer}

Task 7 Disconnecting procedure
    [Documentation]    This part is in charged of disconnection
    [Tags]    Step 06 This step ends connection with the instrument
    disconnect_from_vectorial_analyzer  ${instrument_vectorial_analyzer}
