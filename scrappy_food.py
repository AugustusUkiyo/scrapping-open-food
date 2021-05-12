import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
#from urllib3.packages.six import X

########## Helper functions

# Get score
def get_score(url_produit):
    """
    Helper function allow to get score with selenimum API 
    ['Nutri_Score', 'NOVA', 'Eco_Score']
    """
    DRIVER_PATH = './chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(url_produit)
    el = driver.find_elements_by_xpath("//div[@id='product_summary']//h4")
    Nutri_Score = el[0].text[12:]
    NOVA = el[1].text[5:]
    Eco_Score = el[2].text[10:]
    driver.close()
    return Nutri_Score, NOVA, Eco_Score

# get characteristic produit
def caracteristic_du_produit(soup):
    """
    
    list_caracteristic_produit = ['Quantite', 'Conditionnement', 'Marques', 'Categories', 'Labels_certifications_recompenses',
            'Origine_des_ingredient', 'Lieux_de_fabrication_ou_de_transformation', 'Code_de_tracabilite',
            'Lien_vers_la_page_du_produit_sur_le_site_officiel_du_fabricant', 'Magasins', 'Pays_de_vente']
    """
    characteristic_produit = soup.find('div',{'class':"medium-12 large-8 xlarge-8 xxlarge-8 columns"})
    o_list_characteristic_produit = characteristic_produit.find_all("p")[1:]
    list_characteristic_produit = [elem.text.replace('\xa0', '') for elem in o_list_characteristic_produit]
    
    # Quantite
    current_index = 0
    if 'Quantité' in list_characteristic_produit[current_index]:
        index_0 = list_characteristic_produit[current_index].index(':')
        Quantite = list_characteristic_produit[current_index][index_0 + 2:]
        current_index += 1
    else:
        Quantite = ''
        
    # Conditionnement
    if 'Conditionnement' in list_characteristic_produit[current_index]:
        index_1 = list_characteristic_produit[current_index].index(':')
        Conditionnement = list_characteristic_produit[current_index][index_1 + 2:]
        current_index += 1
    else:
        Conditionnement = ''
        
    # Marques
    if 'Marques' in list_characteristic_produit[current_index]:
        index_2 = list_characteristic_produit[current_index].index(':')
        Marques = list_characteristic_produit[current_index][index_2 + 2:]
        current_index += 1
    else:
        Marques = ''
        
    # Categories
    if 'Catégories' in list_characteristic_produit[current_index]:
        index_3 = list_characteristic_produit[current_index].index(':')
        Categories = list_characteristic_produit[current_index][index_3 + 2:]
        current_index += 1
    else:
        Categories = ''
        
    # Labels_certifications_recompenses
    if 'Labels, certifications, récompenses' in list_characteristic_produit[current_index]:
        index_4 = list_characteristic_produit[current_index].index(':')
        Labels_certifications_recompenses = list_characteristic_produit[current_index][index_4 + 2:]
        current_index += 1
    else:
        Labels_certifications_recompenses = ''
        
    # Origine_des_ingredient
    if 'Origine des ingrédients' in list_characteristic_produit[current_index]:
        index_5 = list_characteristic_produit[current_index].index(':')
        Origine_des_ingredient = list_characteristic_produit[current_index][index_5 + 2:]
        current_index += 1
    else:
        Origine_des_ingredient = ''
        
    # Lieux_de_fabrication_ou_de_transformation
    if 'Lieux de fabrication ou de transformation' in list_characteristic_produit[current_index]:
        index_6 = list_characteristic_produit[current_index].index(':')
        Lieux_de_fabrication_ou_de_transformation = list_characteristic_produit[current_index][index_6 + 2:]
        current_index += 1
    else:
        Lieux_de_fabrication_ou_de_transformation = ''
        
    # Code_de_tracabilite
    if 'Code de traçabilité' in list_characteristic_produit[current_index]:
        index_7 = list_characteristic_produit[current_index].index(':')
        Code_de_tracabilite = list_characteristic_produit[current_index][index_7 + 2:]
        current_index += 1
    else:
        Code_de_tracabilite = ''
        
    # Lien_vers_la_page_du_produit_sur_le_site_officiel_du_fabricant    
    if 'Lien vers la page du produit sur le site officiel du fabricant' in list_characteristic_produit[current_index]:
        index_8 = list_characteristic_produit[current_index].index(':')
        Lien_vers_la_page_du_produit_sur_le_site_officiel_du_fabricant = list_characteristic_produit[current_index][index_8 + 2:]
        current_index += 1
    else:
        Lien_vers_la_page_du_produit_sur_le_site_officiel_du_fabricant = ''
    
    # Magasins
    if 'Magasins' in list_characteristic_produit[current_index]:
        index_9 = list_characteristic_produit[current_index].index(':')
        Magasins = list_characteristic_produit[current_index][index_9 + 2:]
        current_index += 1
    else:
        Magasins = ''
    
    # Pays_de_vente
    if 'Pays de vente' in list_characteristic_produit[current_index]:
        index_10 = list_characteristic_produit[current_index].index(':')
        Pays_de_vente = list_characteristic_produit[current_index][index_10 + 2:]
    else:
        Pays_de_vente = ''
        
    return Quantite, Conditionnement, Marques, Categories, Labels_certifications_recompenses,\
            Origine_des_ingredient, Lieux_de_fabrication_ou_de_transformation, Code_de_tracabilite,\
            Lien_vers_la_page_du_produit_sur_le_site_officiel_du_fabricant, Magasins, Pays_de_vente

# ingredients_analysis
def get_ingredients_analysis(soup):
    """
    ingredients_analysis
    """
    l_s = []
    if soup.find('p', {'id' : "ingredients_analysis"}) is None:
        return l_s
    else:
        for string in soup.find('p', {'id' : "ingredients_analysis"}).find_all('span')[:-1]:
            if string.text != '':
                n_string = string.text.replace('\n', '')
                l_s.append(n_string.replace('\t', ''))
    return l_s
 
# reperes nutritionnels
def get_repere_nutrition(soup):
    """
    
    """
    l_ingredient = []
    ingredients = ["grasses", "Acides", "Sucres", "Sel"]
    try:
        for ingredient in soup.find_all('div', {'class':"small-12 xlarge-6 columns"})[1].text.replace('\n', ';').split(';'):
            if "grasses" in ingredient or "Acides" in ingredient or "Sucres" in ingredient or "Sel" in ingredient:
                l_ingredient.append(ingredient)
        # Matières grasses / Lipides
        current_index = 0
        # Matières grasses / Lipides
        try:
            index_0 = l_ingredient[current_index].index('M')
            Grasses = l_ingredient[current_index][1:index_0 - 1]
            current_index += 1
        except:
            Grasses = ''
        # Acides gras saturés
        try:
            index_1 = l_ingredient[current_index].index('A')
            Acides = l_ingredient[current_index][1:index_1 - 1]
            current_index += 1
        except:
            Acides = ''
        # Sucres
        try:
            index_2 = l_ingredient[current_index].index('S')
            Sucres = l_ingredient[current_index][1:index_2 - 1]
            current_index += 1
        except:
            Sucres = ''
        # Sel
        try:
            index_3 = l_ingredient[current_index].index('S')
            Sel = l_ingredient[current_index][1:index_3 - 1]
        except:
            Sel = ''
    except:
        Grasses, Acides, Sucres, Sel = '', '', '' , ''
    return Grasses, Acides, Sucres, Sel

# Informations nutritionnelles
def get_info_nutri(soup):
    """"""
    try:
        Energie_kJ = soup.find_all('tr', {'id':"nutriment_energy-kj_tr"})[0].find_all('td', {'class':"nutriment_value"})[0].text.replace('\n','').replace('\t','').replace('\xa0','')
    except:
        Energie_kJ = ''
    try :
        Energie_kcal = soup.find_all('tr', {'id':"nutriment_energy-kcal_tr"})[0].find_all('td', {'class':"nutriment_value"})[0].text.replace('\n','').replace('\t','').replace('\xa0','')
    except:
        Energie_kcal = ''
    return Energie_kJ, Energie_kcal

# Impact environnemental
def get_impact_environnemental(soup):
    """
    
    """
    impact = ''
    for elem in soup.find_all('img', {'style':"margin-bottom:1rem;max-width:100%"}):
        if 'Eco-score' in elem['alt']:
            impact = elem['alt'][9:].replace(' ', '')
    return impact

########## Core Functions
def get_page(start=1,end=7981):
    """

    time execution: 0m0,883s
    """
    list_pages = []
    for i in range(start,end):
        list_pages.append('https://fr.openfoodfacts.org/'+str(i))
    return list_pages

def get_list_produits_page(url):
    """
    time execution: 0m1,195s
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    list_produits = soup.find("div", { 'id' : "search_results" })
    list_produit_href = [elem['href'] for elem in list_produits.find_all('a', href=True)]
    return list_produit_href


def get_produit(url_produit):
    """
    time execution: 0m3,005s
    """
    url = 'https://fr.openfoodfacts.org/'+url_produit
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # Name produit
    name = soup.find('h1', {'itemprop' : "name"}).text.replace('\xa0', ' ')
    # Code barre
    code_barre = soup.find('span', {'id' : "barcode"}).text 
    # Nutri_Score, NOVA, Eco_Score
    Nutri_Score, NOVA, Eco_Score = get_score(url)
    # Characteristic produit
    Quantite, Conditionnement, Marques, Categories, Labels_certifications_recompenses, \
    Origine_des_ingredient, Lieux_de_fabrication_ou_de_transformation, Code_de_tracabilite, \
    Lien_vers_la_page_du_produit_sur_le_site_officiel_du_fabricant, Magasins, Pays_de_vente = caracteristic_du_produit(soup)
    # ingredients
    ingredients = ', '.join(get_ingredients_analysis(soup))
    # reperes nutritionnels
    Grasses, Acides, Sucres, Sel = get_repere_nutrition(soup)
    # categories cochees
    if soup.find('label', {'style' : "display:inline;font-size:1rem;"}) is None:
        Categories_cochees = ''
    else:
        Categories_cochees = soup.find('label', {'style' : "display:inline;font-size:1rem;"}).text.replace('\n', '').replace('\t', '')
    # Informations nutritionnelles
    Energie_kJ, Energie_kcal = get_info_nutri(soup)
    # Impact environnemental
    Impact_environnemental = get_impact_environnemental(soup)
    return name, code_barre, Nutri_Score, NOVA, Eco_Score, Quantite, Conditionnement, Marques, Categories, \
        Labels_certifications_recompenses, Origine_des_ingredient, Lieux_de_fabrication_ou_de_transformation, \
        Code_de_tracabilite, Lien_vers_la_page_du_produit_sur_le_site_officiel_du_fabricant, Magasins, Pays_de_vente, \
        ingredients, Grasses, Acides, Sucres, Sel, Categories_cochees, Energie_kJ, Energie_kcal, Impact_environnemental

def main():
    pages = get_page(start=1,end=2)
    list_produit = get_list_produits_page(url=pages[0])
    print(list_produit[10])
    for i in range(0,len(list_produit)):
        print(get_produit(list_produit[i]))

if __name__ == "__main__":
    main()

#print(get_produit(url_produit='produit/3057640257773/naturelle-volcanique-volvic'))
