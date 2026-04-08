*** Settings ***
Documentation    Zestaw testów funkcjonalnych i negatywnych dla symulatora EPC LTE.
Resource         ../resources/EPC_Keywords.robot

# Przed startem całego pliku resetujemy symulator dla pewności
Suite Setup      Reset Simulator

*** Test Cases ***

# TC_01
Successful UE Attach
    [Documentation]    Sprawdza poprawne podłączenie urządzenia (UE) z dozwolonego zakresu ID.
    [Tags]    functional    positive
    Attach UE    id=1
    Verify UE Is Connected    id=1
    [Teardown]    Detach UE    id=1

# TC_02
Default Bearer Assignment Verification
    [Documentation]    Sprawdza, czy po podłączeniu UE automatycznie zostaje mu nadany domyślny bearer o ID 9.
    [Tags]    functional    positive
    Attach UE    id=2
    Verify Bearer Exists    ue_id=2    bearer_id=9
    [Teardown]    Detach UE    id=2

# TC_03
Successful UE Detach
    [Documentation]    Weryfikuje, czy proces odłączania urządzenia działa poprawnie i urządzenie znika z sieci.
    [Tags]    functional    positive
    Attach UE    id=3
    Detach UE    id=3
    Verify UE Is Disconnected    id=3

# TC_04
Dedicated Bearer Addition
    [Documentation]    Testuje możliwość dodania nowego, dedykowanego kanału (bearer) dla podłączonego urządzenia.
    [Tags]    functional    positive
    Attach UE    id=4
    Add Bearer    ue_id=4    bearer_id=1
    Verify Bearer Exists    ue_id=4    bearer_id=1
    [Teardown]    Detach UE    id=4

# TC_05
Downlink Transfer Initiation
    [Documentation]    Weryfikuje poprawne rozpoczęcie przesyłania danych w kierunku Downlink z określoną prędkością.
    [Tags]    functional    positive    traffic
    Attach UE    id=5
    Start DL Transfer    ue_id=5    speed=1000kbps
    Sleep    5s
    Verify DL Transfer    ue_id=5    expected_speed=1000kbps
    [Teardown]    Detach UE    id=5

# TC_06
Out Of Range UE ID Error
    [Documentation]    Test negatywny: Sprawdza, czy system zwróci błąd, gdy podamy ID urządzenia spoza zakresu 0-100.
    [Tags]    negative
    Run Keyword And Expect Error    * Attach UE    id=105

# TC_07
Already Active UE Connection Error
    [Documentation]    Test negatywny: Sprawdza, czy próba podłączenia urządzenia, które jest już podłączone, zakończy się błędem.
    [Tags]    negative
    Attach UE    id=6
    Run Keyword And Expect Error    * Attach UE    id=6
    [Teardown]    Detach UE    id=6

# TC_08
Default Bearer Deletion Block
    [Documentation]    Test negatywny: Weryfikuje, czy system blokuje próbę usunięcia domyślnego bearera (ID 9).
    [Tags]    negative
    Attach UE    id=7
    Run Keyword And Expect Error    * Remove Bearer    ue_id=7    bearer_id=9
    [Teardown]    Detach UE    id=7

# TC_09
Transfer Limit Exceeded Error
    [Documentation]    Test negatywny: Upewnia się, że nie można ustawić prędkości transferu powyżej limitu 100 Mbps.
    [Tags]    negative    traffic
    Attach UE    id=8
    Run Keyword And Expect Error    * Start DL Transfer    ue_id=8    speed=105Mbps
    [Teardown]    Detach UE    id=8

# TC_10
Simulator Reset Clears Environment
    [Documentation]    Test systemowy: Sprawdza, czy funkcja resetu przywraca symulator do stanu początkowego (odłącza wszystkie UE).
    [Tags]    system
    Attach UE    id=9
    Verify UE Is Connected    id=9
    Reset Simulator
    Verify UE Is Disconnected    id=9
