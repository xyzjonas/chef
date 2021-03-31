from app import create_app, db
from app.models import Recipe, Ingredient, IngredientItem, Tag


app = create_app()


chicken = Ingredient(name="chicken")
penne = Ingredient(name="penne")
salt = Ingredient(name="salt")
chicken_item = IngredientItem(ingredient=chicken, amount=1)
penne_item = IngredientItem(ingredient=penne, amount=200, unit="g")
salt_item = IngredientItem(ingredient=penne, amount=4, unit="g")

tags = [
    Tag(name="italian"),
    Tag(name="chicken"),
    Tag(name="main dish"),
]

recipe1 = Recipe(title="Whole chicken", subtitle="oh yeah",
                 ingredients=[chicken_item], tags=[tags[1], tags[2]])
recipe2 = Recipe(title="Penne", subtitle="alla simple",
                 ingredients=[penne_item, salt_item], tags=[tags[0], tags[2]])


def seed_test_db():
    db.session.add(recipe1)
    db.session.add(recipe2)
    for tag in tags:
        db.session.add(tag)
    db.session.commit()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Recipe": Recipe, "Ingredient": Ingredient, "IngredientItem": IngredientItem,
        "seed": seed_test_db
    }
