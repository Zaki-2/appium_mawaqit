*** Settings ***
Documentation    Fichier robot contenant l'ensemble des tests connexion.  

Resource    ../ressources/loader.robot

Force Tags    connexion

*** Variables ***
#${ENV}=  AP1

*** Test Cases ***

[Connexion] Se connecter a l'application
    [Documentation]    Lancement de l'application mawaqit
    [Tags]    TEST-001
    [Setup]   Lancer Application mawaqit
    Log To Console  Hello mawaqit

    #[Teardown]    Parcours Teardown    


*** Keywords ***

Parcours Setup TEST-001
    Log To Console  Setup TEST-001


testSetupBrowserstack
    ${remoteUrl}                Set Variable        http://sirocco1:WNCnQTrMgdGYUNWU9k4d@hub.browserstack.com/wd/hub
    Open Application  remote_url=${remoteUrl} 
    ...  os_version=9.0
    ...  device=Samsung Galaxy S10e
    ...  app=bs://bf9ef4f04d63b88e4e1db38c46c8dd430ac11cbb
    ...  browserstack.local=true
