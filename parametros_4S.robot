*** Settings ***

Library  ../../modulo/keywords.py

*** Variables ***
# se pueden meter los valores directamente sustituyendo en el valor de la variable, para realizar la medida.
${vectorial_address}
${instrument_vectorial_analyzer}
${F_inicial}    None      #frecuencia inicial de barrido
${F_final}      None      #frecuencia final de barrido
${F_unica}      2.55e9      #Valor de frecuencia en un unico punto
${points}       2   # numeros de puntos que componen el barrido o traza
${value_z0}     50          # valores disponibles de impedancia interna caracteristica
${barrido}      single      #tipo medida con un unico valor de frecuencia o barrido0:  single o sweep
${parametro}    S11        # Nombre del parametro de Scattering a medir:  S11,S12,S21,S22
*** Test Cases ***

Task 1 Find
    [Documentation]    Find instruments on the network
    [Tags]    Step 00 finding the correct instrument to iniciate procedure
    ${vectorial_address}=   find_e5063a
    Set Global Variable     ${vectorial_address}
    Log     ${vectorial_address}

Task 2 Connect
    [Documentation]    Connecting to a VNA via IP address
    [Tags]    Step 01 Opening connection with the instrument
    ${instrument_vectorial_analyzer}=  connect_to_vectorial_analyzer  ${vectorial_address}
    Set Global Variable     ${instrument_vectorial_analyzer}
    Log     ${instrument_vectorial_analyzer}
    Log     ${vectorial_address}

Task 3 Reset instrument
    [Documentation]    resetting instrument
    [Tags]    Step 02 Performing a reset to the instrument to start with no errors
    reset_vectorial  ${instrument_vectorial_analyzer}

Task 4 Set internal Impedance
    [Documentation]    performing selection of internal impedance between 50 and 75 ohms
    [Tags]    Step 03 This step sets the impedance value
    set_impedancia  ${instrument_vectorial_analyzer}        ${value_z0}

Task 5 Performing measurement
    [Documentation]    measuring Scattering parameters
    [Tags]    Step 04 In this step the parameter of scattering is obtained
    parametro_Scattering_sfreq  ${instrument_vectorial_analyzer}    ${barrido}  ${parametro}  ${F_unica}    ${F_inicial}    ${F_final}  ${points}

Task 6 Output
    [Documentation]    activating output
    [Tags]    Step 05 In this step, the output is turned on
    activar_salida_vectorial_analyzer  ${instrument_vectorial_analyzer}

Task 7 Disconnecting procedure
    [Documentation]    This part is in charged of disconnection
    [Tags]    Step 06 Ends the connection with the instrument
    disconnect_from_vectorial_analyzer  ${instrument_vectorial_analyzer}
