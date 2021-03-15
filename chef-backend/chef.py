from app import create_app, db
from app.models import Recipe, Ingredient, IngredientItem


app = create_app()


chicken = Ingredient(name="chicken")
chicken_item = IngredientItem(ingredient=chicken, amount=1)
recipe = Recipe(title="Whole chicken", subtitle="oh yeah", ingredients=[chicken_item])


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Recipe": Recipe, "Ingredient": Ingredient, "IngredientItem": IngredientItem,
        "r": recipe
    }
