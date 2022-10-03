from .pages_mawaqit.Elements  import  BasicWebObject
from robotlibcore import DynamicCore
from .pages_mawaqit import *
from robot.api.deco import keyword
from robot.api import logger


class mawaqit(DynamicCore):
    '''
    Librairie robot framework permettant de réaliser des actions sur l'application mobile'.
    *Sommaire*

    %TOC%

    '''

    ROBOT_LIBRARY_SCOPE = "TEST SUITE"

    __version__ = '0.0.1'
    log = logger

    web_objects = [
        Login(),
        commons(),
        ]

    def __init__(self):        
        self.current_web_object = None
        DynamicCore.__init__(self,self.web_objects)
        self._add_webobjects_documentation()


    def _add_webobjects_documentation(self):
        if self.__doc__ == None: self.__doc__ = ''
        for objet in self.web_objects:
            if objet.__doc__ != None:
                self.__doc__ += f'\n {objet.__doc__}'
        self.__doc__ += '--- '

    def _is_webobject_set(self):
        if self.current_web_object == None: 
            raise Exception("Impossible de réaliser l'action demandée car il n'y a pas de webobject actuellement chargé")
        if  isinstance(self.current_web_object,BasicWebObject) == False:
            raise Exception(f"L'objet actuellement chargé ({self.current_web_object}) n'est pas hérité de la classe BasicWebObject")
           
    
    def _switch_webobject(self,webobject_name):
        '''change de webobjet et lance la méthode _check_object() de celui-ci'''
        self.log.debug(f"recherche de {webobject_name}")  
        self.current_web_object = self._get_web_object(webobject_name)
        try:
            self.current_web_object._check_object()
        except Exception as err:
            raise Exception(f"{webobject_name} n'a pas été détecté: {err}")
        self.log.info(f"{webobject_name} détecté")
        self.log.console(f"\n{webobject_name} détecté")


    def _get_web_object(self,web_object_name):
        for web_object in self.web_objects:
            self.log.debug(f'{web_object} => {web_object.name}')
            if web_object.name != None and str(web_object.name).lower() == str(web_object_name).lower():
                return web_object
        raise Exception(f"l'objet demandé ({web_object_name}) n'a pas été trouvé dans la liste des WebObjects de la librairie")



    @keyword("vérifier la présence de",tags=['global'])
    def verifier_presence_webobject(self,webobject_name):
        '''
        Vérifie que le WebObject demandée est présent.\n
        Un WebObject pouvant être une page, un formulaire, un widget...\n
        Si l'on est bien sur le WebObject, alors devient possible d'effectuer des actions sur ses élements (cliquer, détecter la présence...)
        '''
        self._switch_webobject(webobject_name)

    @keyword(tags=['global'])
    def lister_les_elements(self):
        '''
        Log la liste des éléments contenu dans le WebObject actuellement chargé.
        '''
        self._is_webobject_set()
        self.log.info('\n'.join(self.current_web_object._locators.keys()))

    @keyword(tags=['global'])
    def cliquer_sur(self,element):
        '''
        Recherche l'élément demandé parmi-ceux du WebObject actuel et clic dessus.
        '''
        self._is_webobject_set()
        self.current_web_object.get_and_click_on_element(element)

    @keyword("prendre une capture écran de l'élément",tags=['global'])
    def prendre_une_capture_de(self,element,nom_capture=None):
        '''
        Réalise une capture écran de l'élément demandé.\n
        Si le nom de la capture n'est pas renseigné, on enregistre la capture avec le pattern 'nom_element-{index}.png'
        '''
        self._is_webobject_set()
        self.current_web_object.get_and_capture_element(element,nom_capture)

    @keyword("le texte de l'element \"${element}\" est \"${texte}\"",tags=['global'])
    def _check_element_content(self,element,texte,ignore_case=True,continue_on_failure=True):
        '''
        Vérifie que le contenu de l'élément est bien celui attendu. 
            - element: nom de l'élément à contrôler
            - texte: le texte attendu
            - ignore_case: Indique il faut être sensible à la case ou non
            - continue_on_failure: En cas d'erreur, indique si il faut continuer l'exécution du test en cours. 
        '''
        self._is_webobject_set()
        self.current_web_object.get_and_check_element_content(element,texte,ignore_case,continue_on_failure)
       
    @keyword("vérifier la présence de l'élément",tags=['global'])
    def _check_visible_element(self,element):
        self._is_webobject_set()
        self.current_web_object.get_and_check_visible_element(element)

    @keyword("vérifier l'abscence de l'élément",tags=['global'])
    def _check_not_visible_element(self,element):
        self._is_webobject_set()
        self.current_web_object.get_and_check_not_visible_element(element)

    @keyword("Ecrire \"${texte}\" dans l'élément \"${element}\"")
    def _input_text_into_element(self, texte, element):
        '''
        Ecris le texte indiqué dans l'élément du WebObject actuellement chargé
        '''
        self._is_webobject_set()
        texte = str(texte).strip()
        element = str(element).lower().strip()
        locator = self.current_web_object._get_element(element)
        self.log.info(f"Saisie de \"{texte}\" dans l'élément {element}...")
        try:
            self.current_web_object.get_and_input_text_in_element(
                element, texte)
        except Exception as err:
            self.current_web_object.capture_element(element, texte)
            raise Exception(f"Erreur lors de l'écriture dans l'élément\"{element}\" : {err}")
        self.log.info("Saisi effectuée")

    @keyword("Vérifier que l'élément \"${element}\" est \"${statut}\"")
    def etat_element(self,element, statut='actif'):
        '''
        verification de l'élément est actif ou inactif
        '''
        self._is_webobject_set()
        if statut == 'actif':
            self.current_web_object.get_and_check_element_is_enabled(element)
        else:
            self.current_web_object.get_and_check_element_is_disabled(element)

    @keyword("supprimer le texte de l'élément",tags=['global'])
    def _vider_texte_element(self,element):
        self._is_webobject_set()
        self.current_web_object.get_and_clear_text_element(element)