*** Settings ***
Library    ../libs/EpcSimulationLibrary.py

*** Keywords ***
Reset Simulator
    Log    Czyszczenie srodowiska testowego
    EpcSimulationLibrary.Reset Simulator

Attach UE
    [Arguments]    ${id}
    Log    Rozpoczynam podlaczanie urzadzenia UE o ID: ${id}
    EpcSimulationLibrary.Attach UE    ${id}

Detach UE
    [Arguments]    ${id}
    Log    Odłączam urzadzenie UE o ID: ${id}
    EpcSimulationLibrary.Detach UE    ${id}

Start DL Transfer
    [Arguments]    ${ue_id}    ${speed}    ${bearer_id}=9
    Log    Startuje transfer DL predkosc ${speed} na kanale ${bearer_id} dla UE ${ue_id}
    EpcSimulationLibrary.Start DL Transfer    ${ue_id}    ${speed}    ${bearer_id}

Verify DL Transfer
    [Arguments]    ${ue_id}    ${expected_speed}
    Log    Weryfikuje czy transfer dla UE ${ue_id} to faktycznie ${expected_speed}
    EpcSimulationLibrary.Verify DL Transfer    ${ue_id}    ${expected_speed}

Verify UE Is Connected
    [Arguments]    ${id}
    EpcSimulationLibrary.Verify UE Is Connected    ${id}

Verify UE Is Disconnected
    [Arguments]    ${id}
    EpcSimulationLibrary.Verify UE Is Disconnected    ${id}

Verify Bearer Exists
    [Arguments]    ${ue_id}    ${bearer_id}
    EpcSimulationLibrary.Verify Bearer Exists    ${ue_id}    ${bearer_id}

Add Bearer
    [Arguments]    ${ue_id}    ${bearer_id}
    EpcSimulationLibrary.Add Bearer    ${ue_id}    ${bearer_id}