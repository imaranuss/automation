*** Settings ***

Library  ../../modulo/keywords.py

*** Variables ***
${gen_address}
${spectrum_address}
${instrument_generator}
${instrument_spectrum}
${frequency}        1.5e9        # valor de frecuencia de la onda
${amplitude}        -10         # valor de amplitud en dBm´s
${Modulation_state}     ON
*** Test Cases ***

Task 1 Find
    [Documentation]    Finding the instrument on the network
    [Tags]    step 00 Finding the IP address of the instrument
    ${gen_address}=   find_n5171b
    Set Global Variable     ${gen_address}
    ${spectrum_address}=  find n9320b
    Set Global Variable     ${spectrum_address}
    Log    ${gen_address}
    Log    ${spectrum_address}

Task 2 Connect
    [Documentation]    Connecting to signal generator and spectrum analyzer via IP address
    [Tags]    step 01 Creating a connection with the instrument
    ${instrument_generator}=  connect_to_signal_generator  ${gen_address}
    Set Global Variable     ${instrument_generator}
    ${instrument_spectrum}=  connect to spectrum analyzer  ${spectrum_address}
    Set Global Variable     ${instrument_spectrum}
    Log     ${instrument_generator}
    Log     ${instrument_spectrum}


Task 3 Reset instrument
    [Documentation]    resetting instrument
    [Tags]    step 02 Apply a reset to the instrument
    reset_generador  ${instrument_generator}
    reset_spectrum  ${instrument_spectrum}


Task 4 Performing main task
    [Documentation]    generating a signal
    [Tags]    step 03 Generating a signal
    genera_onda  ${instrument_generator}    ${frequency}    ${amplitude}


Task 5 Modulation on/off
    [Documentation]    turn on or off modulation
    [Tags]    step 04 selecting modulation state
    modulacion_off_on       ${instrument_generator}     ${Modulation_state}


Task 6 Output on/off
    [Documentation]    turn on or off the output
    [Tags]    step 05 adjusting output state
    activar_salida_signal_generator     ${instrument_generator}


Task 7 Visualice
    [Documentation]    visualice the signal on the spectrum analyzer
    [Tags]    step 06 graph of signal
    visualiza_señal     ${instrument_spectrum}


Task 8 Output
    [Documentation]    de activate output
    [Tags]    step 07 Disconnecting output
    desactivar_salida_signal_generator      ${instrument_generator}


Task 9 Disconnecting procedure
    [Documentation]    This part is in charged of disconnection
    [Tags]    step 08 Ending connection with instrument
    disconnect_from_signal_generator        ${instrument_generator}
    disconnect_from_spectrum_analyzer       ${instrument_spectrum}

