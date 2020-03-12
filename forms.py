#Used for form setup and validations
from wtforms import Form, BooleanField, StringField, PasswordField, TextAreaField, validators

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])
    confirm = PasswordField('Confirm Password')
	
	
class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])
	
class SearchForm(Form):
    search = StringField('Search')
	
class ReviewForm(Form):
	score = StringField('Score', [validators.DataRequired()])
	review = StringField('Review',  [validators.Length(min=0, max=195)])
  
