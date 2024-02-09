*** Settings ***

Library  ../../modulo/keywords.py

*** Variables ***
${vectorial_address}
${instrument_vectorial_analyzer}
${value_z0}     50      #valor de z0
${freq_unique}  2.45e9    #valor de frecuencia en un unico punto
*** Test Cases ***

Task 1 Find
    [Documentation]    Find instruments on the network
    [Tags]    Step 00 this step finds the instrument´s IP address
    ${vectorial_address}=   find_e5063a
    Set Global Variable     ${vectorial_address}
    Log     ${vectorial_address}

Task 2 Connect
    [Documentation]    Connecting to a VNA via IP address
    [Tags]    Step 01 This step is connecting to the VNA via IP address
    ${instrument_vectorial_analyzer}=  connect_to_vectorial_analyzer  ${vectorial_address}
    Set Global Variable    ${instrument_vectorial_analyzer}
    Log     ${instrument_vectorial_analyzer}

Task 3 Reset instrument
    [Documentation]    resetting instrument
    [Tags]    Step 02 this step resets the instrument
    reset_vectorial  ${instrument_vectorial_analyzer}

Task 4 Set internal Impedance
    [Documentation]    performing selection of internal impedance between 50 and 75 ohms
    [Tags]    Step 03 this step sets impedance value
    set_impedancia  ${instrument_vectorial_analyzer}        ${value_z0}

Task 5 Performing measurement
    [Documentation]    measuring S11 parameter
    [Tags]    Step 04 this step performs main task
    parametro_s11_sfreq  ${instrument_vectorial_analyzer}       ${freq_unique}

Task 6 Output
    [Documentation]    activating output
    [Tags]    Step 05 this step turns on output
    activar_salida_vectorial_analyzer  ${instrument_vectorial_analyzer}

Task 7 Disconnecting procedure
    [Documentation]    This part is in charged of disconnection
    [Tags]    Step 06 this step ends connection with instrument
    disconnect_from_vectorial_analyzer  ${instrument_vectorial_analyzer}
