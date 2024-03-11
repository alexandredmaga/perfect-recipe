from flask import render_template, url_for, redirect, flash
from flask_login import login_required, current_user
from perfect_recipe.models import Recipe, Ingredient, Instruction
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError
from perfect_recipe.ext.database import db

def init_app(app):
    @login_required
    @app.route('/')
    def index():
        return render_template('index.html', user=current_user)

    @app.route('/recipe', methods=['GET', 'POST'])
    @login_required
    def recipe_index():
        recipes = Recipe.query.filter_by(user_id=current_user.id).all()
        return render_template('recipe.html', user=current_user, recipes=recipes)

    @app.route('/recipe/new', methods=['GET', 'POST'])
    @login_required
    def recipe_new():
        form = RecipeForm()

        if form.validate_on_submit():
            recipe = Recipe(title=form.title.data, description=form.description.data, preparation_time=form.preparation_time.data, portion=form.portion.data, user_id=current_user.id)

            for ingredient_form in form.ingredients:
                ingredient_title = ingredient_form.title.data
                ingredient = Ingredient.query.filter_by(title=ingredient_title).first()

                if not ingredient:
                    ingredient = Ingredient(title=ingredient_title)
                    db.session.add(ingredient)
                    db.session.commit()
                recipe.ingredients.append(ingredient)

            for instruction_form in form.instructions:
                instruction_title = instruction_form.title.data
                instruction = Instruction.query.filter_by(title=instruction_title).first()
                if not instruction:
                    instruction = Instruction(title=instruction_title)
                    db.session.add(instruction)
                    db.session.commit()
                recipe.instructions.append(instruction)

            db.session.add(recipe)
            db.session.commit()
            flash('Receita criada com sucesso!', category="success")
            return redirect(url_for('recipe_index'))
        return render_template('recipe_new.html', user=current_user, form=form)

    @app.route('/recipe/edit/<int:recipe_id>', methods=['GET', 'POST'])
    @login_required
    def recipe_edit(recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)

        form = RecipeForm(obj=recipe)

        ingredients = Ingredient.query.filter_by(recipe_id=recipe_id).all()

        ingredients_data = [{'id': ingredient.id, 'title': ingredient.title} for ingredient in ingredients]

        # for ingredient in ingredients:
        #     form.ingredients.append_entry({'title': ingredient.title})

        # for instruction in recipe.instructions:
        #     form.instructions.append_entry({'title': instruction.title})

        if form.validate_on_submit():
            form.populate_obj(recipe)

            for ingredient_form in form.ingredients:
                ingredient_title = ingredient_form.title.data
                ingredient = Ingredient.query.filter_by(title=ingredient_title).first()
                if not ingredient:
                    ingredient = Ingredient(title=ingredient_title)
                    db.session.add(ingredient)
                    db.session.commit()
                recipe.ingredients.append(ingredient)

            for instruction_form in form.instructions:
                instruction_title = instruction_form.title.data
                instruction = Instruction.query.filter_by(title=instruction_title).first()
                if not instruction:
                    instruction = Instruction(title=instruction_title)
                    db.session.add(instruction)
                    db.session.commit()
                recipe.instructions.append(instruction)

            db.session.add(recipe)
            db.session.commit()
            return redirect(url_for('recipe_index'))
        return render_template('recipe_edit.html', user=current_user, form=form, ingredients_data=ingredients_data)


    @app.route('/recipe/show/<int:recipe_id>', methods=['GET', 'POST'])
    @login_required
    def recipe_show(recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)

        ingredients = Ingredient.query.filter_by(recipe_id=recipe_id).all()

        return render_template('recipe_show.html', user=current_user, recipe=recipe, ingredients=ingredients)

    @app.route('/recipe/delete/<int:recipe_id>', methods=['GET', 'POST'])
    @login_required
    def recipe_delete(recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)

        form = RecipeForm(obj=recipe)
        db.session.delete(recipe)
        db.session.commit()

        flash('Receita removida com sucesso!', 'success')
        return redirect(url_for('recipe_index'))


class IngredientForm(FlaskForm):
    title = StringField('Nome do Ingrediente', validators=[DataRequired()])

class InstructionForm(FlaskForm):
    title = StringField('Passo', validators=[DataRequired()])

class RecipeForm(FlaskForm):
    title = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"class": "form-control","placeholder": "Bolo de cenoura"})

    description = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"class": "form-control","placeholder": "Descrição"})

    ingredients = FieldList(FormField(IngredientForm), min_entries=1)

    instructions = FieldList(FormField(InstructionForm), min_entries=1)

    preparation_time = StringField(validators=[InputRequired(), Length(min=4, max=10)], render_kw={"class": "form-control","placeholder": "1 hr"})

    portion = StringField(validators=[InputRequired(), Length(min=4, max=10)], render_kw={"class": "form-control","placeholder": "2 pessoas"})

    submit = SubmitField("Enviar", render_kw={"class": "btn btn-primary"})