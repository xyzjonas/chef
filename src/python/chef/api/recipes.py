from typing import List

from fastapi import APIRouter
from sqlmodel import Session

from chef.controllers import RecipesController
from chef.schemas import Recipe, CreateOrUpdateRecipe
from chef.models import engine

router = APIRouter()
recipes = RecipesController()


# Store the current recipe id in memory
CURRENT_RECIPES_IDS = []


@router.get("/")
async def get_recipes(category: int = None) -> List[Recipe]:
    with Session(engine()) as session:
        if category:
            return await recipes.get_by_category(session, category)
        h = await recipes.get_all(session)
        return await recipes.get_all(session)


@router.get("/{item_id}")
async def get_recipe(item_id: int) -> Recipe:
    with Session(engine()) as session:
        return await recipes.get_single(session, item_id)


@router.delete("/{item_id}")
async def delete_recipe(item_id: int) -> None:
    with Session(engine()) as session:
        await recipes.delete_single(session, item_id)


@router.post('/', status_code=201)
async def create_recipe(create_data: CreateOrUpdateRecipe) -> Recipe:
    with Session(engine()) as session:
        return await recipes.create(session, create_data)


@router.put('/{item_id}')
async def update_recipe(item_id: int, update_data: CreateOrUpdateRecipe) -> Recipe:
    with Session(engine()) as session:
        return await recipes.update(session, item_id, update_data)

    # created = False
    #
    # if data.get("id"):
    #     recipe = Recipe.query.filter_by(id=data.get("id")).first_or_404()
    #     # a bit hackish :(
    #     for ii in recipe.ingredients:
    #         db.session.delete(ii)
    #     db.session.commit()
    # else:
    #     _assert_request_data(data, required=["title"])
    #     _validate_type(data["title"], str)
    #     recipe = Recipe(title=data["title"])
    #     created = True
    #
    # if data.get("title") and _validate_type(data.get("title"), str):
    #     recipe.title = data["title"]
    # if data.get("subtitle") and _validate_type(data.get("subtitle"), str):
    #     recipe.subtitle = data["subtitle"]
    # if data.get("source_name") and _validate_type(data.get("source_name"), str):
    #     recipe.source_name = data["source_name"]
    # if data.get("source") and _validate_type(data.get("source"), str):
    #     recipe.source = data["source"]
    # if data.get("portions") and _validate_type(data.get("portions"), int):
    #     recipe.portions = data["portions"]
    # if data.get("body") and _validate_type(data.get("body"), str):
    #     recipe.body = data["body"]
    # if data.get("draft") and _validate_type(data.get("draft"), bool):
    #     recipe.draft = data["draft"]
    #
    # # ingredients
    # ingredient_items = []
    # for item in (data.get("ingredients") or []):
    #     if not item.get("ingredient") or not item["ingredient"].get("name"):
    #         raise InvalidUsage(f"Malformed: one of the posted ingredients is missing 'name' field",
    #                            status_code=400)
    #     ingredient_name = item["ingredient"].get("name")
    #     ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
    #     if not ingredient:
    #         ingredient = Ingredient(name=ingredient_name)
    #
    #     # unit (input format is same as output)
    #     if item.get("unit") and item["unit"].get("name"):
    #         unit = Unit.query.filter_by(name=item["unit"]["name"]).first()
    #         if not unit:
    #             unit = Unit(name=item["unit"]["name"])
    #             db.session.add(unit)
    #             db.session.commit()
    #     else:  # default = piece
    #         unit = Unit.query.filter_by(name="pcs").first() or Unit(name="pcs")
    #
    #     ii = IngredientItem(ingredient=ingredient, amount=item.get("amount"),
    #                         unit=unit, note=item.get("note"))
    #     ingredient_items.append(ii)
    # recipe.ingredients = ingredient_items
    #
    # # tags
    # tags = set()
    # for t in (data.get("tags") or []):
    #     tag_name = t.get("name")
    #     if not tag_name:
    #         continue
    #     tag = Tag.query.filter_by(name=tag_name).first()
    #     if not tag:
    #         tag = Tag(name=tag_name)
    #     tags.add(tag)
    # recipe.tags = list(tags)
    #
    # db.session.add(recipe)
    # db.session.commit()
    # if created:
    #     return f"{recipe.title} created.", 201
    # else:
    #     return f"{recipe.title} modified.", 200
