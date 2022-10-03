from robot.libraries.BuiltIn import BuiltIn
import  RobotEyes
from robot.api import logger
from robot.errors import ExecutionFailed


class ElementsManipulator():
    '''
    Classe pour les manipulations communes de l'appliation via la librairie appium
    (cliquer, attendre que l'élément soit visible et opérationnel...).
    C'est la classe qui permet de s'interfacer avec la SeleniumLibrary.
    Tout méthode ajoutée ici devient disponible dans l'ensemble des WebObjects.
    '''
    BuiltIn = BuiltIn()
    log = logger

    @property
    def applib(self):
        return self.BuiltIn.get_library_instance('AppiumLibrary')
    
    def click_on_element(self, locator):
        '''
        Réalise un clic sur le locator demandé
        '''
        try:
            self.applib.wait_until_element_is_visible(locator)
            self.applib.click_element(locator)
        except Exception as err:
            self.applib.capture_page_screenshot()
            raise err

    def capture_element(self, locator, filename):
        '''
        Prend une capture écran de l'élément demandé
        '''
        self.applib.wait_until_element_is_visible(locator)
        self.applib.capture_element_screenshot(locator, filename)

    def check_element_content(self, locator, text, ignore_case=True):
        '''
        Récupère le texte contenu dans un élément et vérifie son contenu.
        '''
        try:
            text_found = self.applib.get_text(locator)
        except Exception as err:
            self.applib.capture_page_screenshot()
            raise err
        self.BuiltIn.should_be_equal_as_strings(
            text_found, text, ignore_case=ignore_case, msg="Le texte trouvé n'est pas celui attendu")

    def check_visible_element(self, locator):
        '''
        Vérifie que l'élément demandé est bien visible.
        '''
        try:
            self.applib.wait_until_element_is_visible(locator,timeout="20")
        except Exception as err:
            self.applib.capture_page_screenshot()
            raise err

    def check_not_visible_element(self, locator):
        '''
        Vérifie que l'élément demandé n'est pas visible.
        '''
        try:
            self.applib.wait_until_element_is_not_visible(locator)
        except Exception as err:
            self.applib.capture_page_screenshot()
            raise err
    
    def check_element_is_enabled(self, locator):
        '''
        Vérifie que l'élément demandé est enabled.
        '''
        try:
            self.applib.wait_until_element_is_visible(locator)
            self.applib.element_should_be_enabled(locator)
            
        except Exception as err:
            self.applib.capture_page_screenshot()
            raise err

    def check_element_is_disabled(self, locator):
        '''
        Vérifie que l'élément demandé est disabled.
        '''
        try:
            self.applib.wait_until_element_is_visible(locator)
            self.applib.element_should_be_disabled(locator)
            
        except Exception as err:
            self.applib.capture_page_screenshot()
            raise err

    def input_text(self,locator,text):
        '''
        Saisir un text dans l'element.
        '''
        try:
            self.applib.wait_until_element_is_visible(locator)
            self.applib.input_text(locator, text)
        except Exception as err:
            self.applib.capture_page_screenshot()
            raise err

    def clear_text_element(self,locator):
        '''
        supprimer le texte d'un element.
        '''
        try:
            self.applib.wait_until_element_is_visible(locator)
            self.applib.clear_text(locator)
        except Exception as err:
            self.applib.capture_page_screenshot()
            raise err
            
class BasicWebObject(ElementsManipulator):
    '''
    Class basique de WebObject qui contient les locators, le nom de l'objet ainsi que les méthodes pour récuperer les locators par leur libellé.
    '''
    name = 'Basic WebOject'

    description = None

    _locators = {
        'libelle_element': { 
            'ios':'value_locator', 
            'android': 'value_locator'
            },
        'libelle commun': {
            'commun': 'value_locator'
        }
    }

    @property
    def os(self):
        os = self.BuiltIn.get_variable_value("${OS}")
        os = self._get_normalized_element_name(os)
        return os

    def __init__(self, add_class_name=True):
        #Generation automatique de la documentation des locators
        self._generate_documentation(add_class_name)


    def _generate_documentation(self,add_class_name):
        '''
        Genere automatique la documentation du WebObject.
        A surcharger si vous voulez changer la manière d'alimenter la documentation.
        '''
        if self.__doc__ == None: self.__doc__ = ''
        self.__doc__ += '\n'
        self.__doc__ += '--- '
        self._document_basic_infos(add_class_name)
        self._document_custom_methods()
        self._document_elements()
        
    def _document_basic_infos(self,add_class_name):
        if add_class_name : self.__doc__ += f'\n= {self.__class__.__name__} =\n'        
        self.__doc__ += f'*nom de l\'objet*: "{self.name}"\n\n'        
        self.__doc__ += f'_*description*_ \n\n {self.description}\n\n'

    def _document_elements(self):
        self.__doc__ += f'*liste des éléments manipulables*:\n\n'
        self.__doc__ += "| *element* | *locator selenium* |\n"
        for key in self._locators:
            self.__doc__+= str("| "+key+" | "+str(self._locators[key])+" |\n")
        self.__doc__ += '\n\n'

    def _document_custom_methods(self):
        '''
        detecte les fonctions publiques du WebObject et alimente la documentation en conséquences.
        '''
        kw_list = []
        for item_name, item_type in self.__class__.__dict__.items():
            if '_' not in item_name[0] and type(item_type).__name__ == 'function':
                kw_list.append(f'{item_name}')
        if len(kw_list) != 0:
            self.__doc__ += "*mots-clés liés à l'objet:*\n\n"
            self.__doc__ += '\n '.join(kw_list)
            self.__doc__ += '\n\n'


    def _check_object(self):
        '''
        Méthode pour vérifier que le webobject est bien détecté.
        Par défaut, fait un pass. A surcharger pour faire les détections spécifiques à l'objet recherché.
        '''
        pass

    def _get_element(self, nom_element):
        '''
        Retrouve le locator selenium d'un element contenu par l'objet
        '''
        nom_element = self._get_normalized_element_name(nom_element)
        self.log.debug(f'recherche de {nom_element} ...')
        if nom_element in self._locators.keys():
            self.log.debug(f'{nom_element} trouvé')
            return self._resolve_element(nom_element)
        raise Exception(
            f"l'élement demandé ({nom_element}) ne fait pas partie des éléments contenu dans {self.name}")

    def _resolve_element(self,nom_element):
        '''
        Recupére la valeur en fonction de si l'on est sur du commun ou du scpéfique à l'OS
        '''
        element = self._locators.get(nom_element)
        if 'commun' in element.keys(): 
            return element['commun']

        self.log.debug(f"OS est: {self.os}")
        
        if self.os in ['android','ios']: 
            self.log.debug("test :"+element.get(self.os))
            return element.get(self.os)

        raise Exception(f"Erreur, l'élément {nom_element} n'a pas été trouvé parmis les clés attendues (commun, android, ios) pour l'OS {self.os}")

    def _get_normalized_element_name(self, nom_element):
        '''
        retourne le nom normalisé de l'élément pour palier aux erreurs de saisie utilisateur
        '''
        return str(nom_element).lower().replace(' ', '_')

    def get_and_click_on_element(self, nom_element):
        '''
        Réalise la récupération de l'élément par son label  ( _get_element() ) 
        et clique dessus ( click_on_element() )
        '''
        self.log.info(f'clic sur {nom_element}')
        self.log.console(f'\nclic sur {nom_element}')
        self.click_on_element(self._get_element(nom_element))
        self.log.info("clic effectué")

    def get_and_check_visible_element(self, nom_element):
        '''
        Réalise la récupération de l'élément par son label  ( _get_element() ) 
        et vérifie sa visibilité ( check_visible_element() )        
        '''
        self.log.info(
            f"vérification de la visibilité de l'élement {nom_element}")
        self.check_visible_element(self._get_element(nom_element))
        self.log.info(f"l'élement {nom_element} est visible")
        self.log.console(f'\n{nom_element} trouvé et visible')

    def get_and_capture_element(self, nom_element, nom_capture=None):
        '''
        Réalise la récupération de l'élément par son label  ( _get_element() ) 
        et prend une capture écran de celui-ci ( capture_element() )  
        '''
        if nom_capture == None:
            nom_capture = self._get_normalized_element_name(
                nom_element) + '-{index}.png'
        self.capture_element(self._get_element(nom_element), nom_capture)
        self.log.console(f"\n{nom_element} capturé ({nom_capture})")

    def get_and_check_element_content(self, nom_element, texte, ignore_case=True, continue_on_failure=True):
        '''
        Réalise la récupération de l'élément par son label  ( _get_element() ) 
        et vérifie son contenu  ( check_element_content() )  
        '''
        self.log.info(f"récupération du texte contenu dans {nom_element}")
        try:
            self.check_element_content(
                self._get_element(nom_element), texte, ignore_case)
        except Exception as err:
            erreur = ExecutionFailed(
                f"le contenu de {nom_element} n'est pas celui attendu: " + str(err))
            erreur.continue_on_failure = continue_on_failure
        self.log.info("le contenu correspond bien au texte attendu")

    def get_and_check_not_visible_element(self, nom_element):
        '''
        Réalise la récupération de l'élément par son label  ( _get_element() ) 
        et vérifie sa visibilité ( check_not_visible_element() )        
        '''
        self.log.info(
            f"vérification de la non visibilité de l'élement {nom_element}")
        self.check_not_visible_element(self._get_element(nom_element))
        self.log.info(f"l'élement {nom_element} n'est pas visible")
        self.log.console(f'\n{nom_element} trouvé et est bien non visible')
    
    def get_and_input_text_in_element(self, nom_element,text):
        '''
        Réalise la récupération de l'élément par son label  ( _get_element() ) 
        et ecrire dans l'element       
        '''
        self.log.info(
            f"vérification de la visibilité de l'élement {nom_element}")
        self.input_text(self._get_element(nom_element), text)
        self.log.info(f"Ecrire {text} dans l'élement {nom_element}")

    def get_and_check_element_is_enabled(self, nom_element):
        '''
        Réalise la récupération de l'élément par son label  ( _get_element() ) 
        et vérifier que l'élement est enabled     
        '''
        self.log.info(
            f"vérification de la visibilité de l'élement {nom_element}")
        self.check_element_is_enabled(self._get_element(nom_element))
        self.log.info(f"Vérifier que l'élement {nom_element} est enabled")

    def get_and_check_element_is_disabled(self, nom_element):
        '''
        Réalise la récupération de l'élément par son label  ( _get_element() ) 
        et vérifier que l'élement est disabled    
        '''
        self.log.info(
            f"vérification de la visibilité de l'élement {nom_element}")
        self.check_element_is_disabled(self._get_element(nom_element))
        self.log.info(f"Vérifier que l'élement {nom_element} est disabled")

    def get_and_clear_text_element(self, nom_element):
        '''
        Réalise la suppression du texte de l'élément  ( _get_element() ) 
        '''
        self.log.info(f'vider champ {nom_element}')
        self.clear_text_element(self._get_element(nom_element))
        self.log.info("suppression texte effectué")