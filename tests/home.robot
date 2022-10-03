*** Settings ***
Documentation    Fichier robot contenant l'ensemble des tests conso.  

Resource    ../ressources/loader.robot

Force Tags    home

Suite Setup   Initialisation

*** Variables ***

*** Test Cases ***

[Home] Etre accueillie chaleureusement
    [Documentation]    Etre accueillie chaleureusement 
    [Tags]    MCARE-619
    [Setup]    Parcours Setup MCARE-619
    Lancer ECM



*** Keywords ***
Parcours Setup MCARE-619
    #RESERVER UN CLIENT MOBILE
    Parcours Setup

    