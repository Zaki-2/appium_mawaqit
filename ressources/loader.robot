*** Settings ***
Documentation    Fichier robot contenant l'ensemble des libraires et variables d'environnement à charger.
   
Library    Collections
Library    ../mawaqitLibrary/
Library    AppiumLibrary
Library    ScreenCapLibrary        
Library    Process
Library    ImageHorizonLibrary     ${CURDIR}${/}images
Library    ../mawaqitLibrary/AppiumEnhanceLibrary.py

Resource    commun.robot

Variables    ../config/${OS}.yaml


*** Variables ***

${app}   ${EXECDIR}${/}application${/}${Capabilities.APP}
${images_dir}   ${EXECDIR}${/}ressources/images

