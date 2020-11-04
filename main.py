import json
import streamlit as st
import requests
import os

api = (os.environ.get('api_key'))
st.set_page_config(page_title='Recipe Recommender')



def all_ingredients(x):
    user_ingredients = ','.join(map(str, x))

    f = f"https://www.themealdb.com/api/json/v2/{api}/filter.php?i=" + user_ingredients
    data = json.loads(requests.get(f).text)

    if data["meals"] == None:
        st.write("Sorry we can't find a recipes with these ingredients.")
        st.stop()

    recipes = []
    for item in (data["meals"]):
        try:
            meal = item["idMeal"]
            recipes.append(meal)
        except Exception:
            pass



    return (recipes)



def get_meals(recipes,filter_cat,filter_area):
    if filter_cat != 'No Filter':
        recipes = filer_by_cat(recipes, filter_cat)

    if filter_area != 'No Filter':
        recipes = filer_by_area(recipes, filter_area)

    for item in recipes:
        f_recipes = f"https://www.themealdb.com/api/json/v2/{api}/lookup.php?i=" + item
        r_recipes = json.loads(requests.get(f_recipes).text)

        st.image(r_recipes['meals'][0]['strMealThumb'])
        st.subheader(r_recipes['meals'][0]['strMeal'])

        for item in (range(1, 15)):
            a = 'strMeasure' + str(item)
            b = 'strIngredient' + str(item)
            a = r_recipes['meals'][0][a]
            b = r_recipes['meals'][0][b]

            if a != None and b != None:
                try:
                    st.write(a + " " + b)
                except:
                    st.write(b)
            else:
                break

        st.subheader('Instructions:')
        st.write(r_recipes['meals'][0]['strInstructions'])
        st.write("\n")

        youtube_l = r_recipes['meals'][0]['strYoutube']
        video = f"**Link: **{youtube_l}"

        st.write(video)
        st.write("\n")
        st.write("\n")
        st.write("\n")

    return


@st.cache(suppress_st_warning=True, show_spinner=False, allow_output_mutation=True)
def filer_by_cat(recipes,filter_cat):
    f = f"https://www.themealdb.com/api/json/v2/{api}/filter.php?c={filter_cat}"
    data = json.loads(requests.get(f).text)

    filter_list = []

    for index,item in enumerate(data["meals"]):
        filter_list.append(data["meals"][index]['idMeal'])

    recipes = [x for x in recipes if x in filter_list]

    if len(recipes) == 0:
        st.write(f"Sorry, can't find any recipes filtered by '{filter_cat}'")
        st.stop()

    return recipes


def filer_by_area(recipes,filter_area):
    f = f"https://www.themealdb.com/api/json/v2/{api}/filter.php?a={filter_area}"
    data = json.loads(requests.get(f).text)

    filter_list = []

    for index,item in enumerate(data["meals"]):
        filter_list.append(data["meals"][index]['idMeal'])

    recipes = [x for x in recipes if x in filter_list]

    if len(recipes) == 0:
        st.write(f"Sorry, can't find any recipes filtered by '{filter_area}'")
        st.stop()

    return recipes


@st.cache(suppress_st_warning=True, show_spinner=False, allow_output_mutation=True)
def get_ingredient_list():
    f = f"https://www.themealdb.com/api/json/v2/{api}/list.php?i=list"
    data = requests.get(f)
    data = json.loads(data.text)

    ingredients = []
    for item in (data["meals"]):
        try:
            ing = item["strIngredient"]
            ingredients.append(ing)
        except Exception:
            pass

    ingredients[6:] = sorted(ingredients[6:])

    return ingredients

def get_cat():
    f = f"https://www.themealdb.com/api/json/v2/{api}/categories.php"
    data = requests.get(f)
    data = json.loads(data.text)

    categories = ['No Filter',
                    'Breakfast',
                    'Starter',
                    'Side',
                    'Dessert',
                    'Miscellaneous',
                    'Beef',
                    'Chicken',
                    'Lamb',
                    'Pork',
                    'Seafood',
                    'Pasta',
                    'Vegan',
                    'Vegetarian',
                    'Goat']

    for item in (data["categories"]):
        try:
            ing = item["strCategory"]
            if ing not in categories:
                categories.append(ing)
        except Exception:
            pass

    return categories


def get_area():
    f = f"https://www.themealdb.com/api/json/v1/1/list.php?a=list"
    data = requests.get(f)
    data = json.loads(data.text)

    areas = ['No Filter']

    for item in (data["meals"]):
        try:
            ing = item["strArea"]
            if ing not in areas:
                areas.append(ing)
        except Exception:
            pass

    try:
        areas.remove('Irish')
    except:
        pass

    return areas


def name_search(user_text):
    f = f"https://www.themealdb.com/api/json/v2/{api}/search.php?s=" + str(user_text)
    data = json.loads(requests.get(f).text)


    if data["meals"] == None:
        st.write("Sorry we can't find a recipe with that name.")
        st.stop()

    recipes = []

    for item in (data["meals"]):
        recipes.append(item['idMeal'])

    return recipes


def popular():
    f = f"https://www.themealdb.com/api/json/v2/{api}/popular.php"
    data = json.loads(requests.get(f).text)

    recipes = []

    for item in (data["meals"]):
        recipes.append(item['idMeal'])

    return recipes


def new_meals():
    f = f"https://www.themealdb.com/api/json/v2/{api}/latest.php"
    data = json.loads(requests.get(f).text)

    recipes = []

    for item in (data["meals"]):
        recipes.append(item['idMeal'])

    return recipes


st.header("Shane’s Recipe Recommender")

ingredients = get_ingredient_list()
categories = get_cat()
areas = get_area()


my_expander = st.sidebar.beta_expander('Filters')
filter_cat = my_expander.radio('Filter:', (categories), index=0)
filter_area = my_expander.radio('Filter:', (areas), index=0)


radio = st.radio('', (
'Search by ingredients', 'Search by recipe name', 'Newest recipes', 'Just show me some popular recipes'))

if radio == 'Search by recipe name':
    user_text = st.text_input('Recipe Search', value='', max_chars=None, key=None, type='default')
    if len(user_text) != 0:
        recipes = name_search(user_text)
        get_meals(recipes,filter_cat)

elif radio == 'Search by ingredients':
    user_choice = st.multiselect('Choose your ingredients:', ingredients, [])
    if len(user_choice) != 0:
        recipes = all_ingredients(user_choice)
        get_meals(recipes, filter_cat,filter_area)


elif radio == 'Newest recipes':
    recipes = new_meals()
    get_meals(recipes,filter_cat,filter_area)

else:
    recipes = popular()
    get_meals(recipes,filter_cat,filter_area)
