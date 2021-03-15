from app import db


ingredients = db.Table(
    'ingredients',
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipe.id"), primary_key=True),
    db.Column("ingredient_item_id", db.Integer, db.ForeignKey("ingredient_item.id"), primary_key=True)
)


def dictify(obj):
    if issubclass(obj.__class__, Base):
        return obj.dictionary
    if issubclass(obj.__class__, list):
        return [dictify(o) for o in obj]
    try:
        return float(obj)
    except (TypeError, ValueError, SyntaxError):
        pass
    return str(obj)


class Base(db.Model):
    __abstract__ = True
    __items__ = ["id"]

    id = db.Column(db.Integer, primary_key=True)

    def _get_attributes(self) -> dict:
        """Get 'public' attributes to be parsed into JSON response"""
        result = {}
        for attr in self.__items__:
            try:
                result[attr] = self.__getattribute__(attr)
            except AttributeError:
                continue
        return result

    @property
    def dictionary(self):
        """Serialize recursively according to the __items__ attribute."""
        return {
            k: dictify(v) for k, v in self._get_attributes().items()
        }

    def _repr(self, **kwargs):
        """Create repr string."""
        kw = {f"{str(k)}={v}" for k, v in kwargs.items()}
        return f'<{self.__class__.__name__} ({", ".join(kw)})>'

    def __repr__(self):
        """Default for all subclasses: everything 'public'."""
        return self._repr(**self.dictionary)


class Ingredient(Base):
    __items__ = ["id", "name"]

    name = db.Column(db.String(80), nullable=False)
    approx_per_piece = db.Column(db.Float, nullable=True)

    def __repr__(self) -> str:
        return self._repr(id=self.id, name=self.name)


class IngredientItem(Base):
    """
    -> [included in shopping list] <amount> <unit> <ingredient> (<note>)
    -> [x] 400 g tomatoes (roughly chopped)
    """
    __items__ = ["ingredient", "amount", "unit", "note"]

    ingredient_id = db.Column(db.Integer, db.ForeignKey(Ingredient.id))
    ingredient = db.relationship(Ingredient, uselist=False)
    amount = db.Column(db.Float, default=0)
    unit = db.Column(db.String(10), default="pcs")
    note = db.Column(db.String(10), nullable=True)
    exclude = db.Column(db.Boolean(), default=False)


class Recipe(Base):
    __items__ = ["id", "title", "subtitle", "ingredients", "concat", "source"]

    title = db.Column(db.String(80), nullable=False)
    subtitle = db.Column(db.String(50), nullable=True)
    source_name = db.Column(db.String(100), nullable=True)
    source = db.Column(db.String(100), nullable=True)
    ingredients = db.relationship(IngredientItem, secondary=ingredients, lazy="subquery",
                                  backref=db.backref("recipes", lazy=False))

    # HTML content + rich text editor on the frontend
    body = db.Column(db.String(1000), nullable=True)

    @property
    def concat(self):
        if self.body:
            return f"{self.body[:50]}..."
        return None
