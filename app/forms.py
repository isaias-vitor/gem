from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length



# Formulário de Login usando Flask-WTF
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

# Formulário de Aprovação de Hinos (Voz Principal)
class ApprovalFormPrincipalHymn(FlaskForm):
    hymn_number = StringField('numeroHino')
    candidate_id = StringField('idCandidato')
    date = DateField('Data', validators=[DataRequired()])
    observation = TextAreaField('Observação')
    submit = SubmitField('Aprovar')

# Formulário de Aprovação de Hinos (Voz Alternativa)
class ApprovalFormAlternativeHymn(FlaskForm):
    hymn_number = StringField('numeroHino')
    candidate_id = StringField('idCandidato')
    date = DateField('Data', validators=[DataRequired()])
    observation = TextAreaField('Observação')
    submit = SubmitField('Aprovar')

# Formulário de Aprovação de Lição do MSA (Exercícios de Fixação)
class ApprovalFormFixingExercice(FlaskForm):
    lesson_number = StringField('numeroLição')
    candidate_id = StringField('idCandidato')
    date = DateField('Data', validators=[DataRequired()])
    submit = SubmitField('Aprovar')

# Formulário de Aprovação de Lição do MSA (Exercícios Prático)
class ApprovalFormPracticalExercice(FlaskForm):
    lesson_number = StringField('numeroLição')
    candidate_id = StringField('idCandidato')
    date = DateField('Data', validators=[DataRequired()])
    observation = TextAreaField('Observação')
    submit_complete = SubmitField('Aprovar')
    submit_parcial = SubmitField('Aprovar Parcialmente')

# Botão de Cancelamento de Aprovação de Hinos (Voz Principal)
class CancelApprovalButtonPrincipal(FlaskForm):
    hymn_number = StringField('numeroHino')
    candidate_id = StringField('idCandidato')
    cancel = SubmitField('Cancelar Aprovação')

# Botão de Cancelamento de Aprovação de Hinos (Voz Alternativa)
class CancelApprovalButtonAlternative(FlaskForm):
    hymn_number = StringField('numeroHino')
    candidate_id = StringField('idCandidato')
    cancel = SubmitField('Cancelar Aprovação')

# Botão de Cancelamento de Aprovação de Lição do MSA (Exercícios de Fixação)
class CancelApprovalButtonFixing(FlaskForm):
    lesson_number = StringField('numeroLição')
    candidate_id = StringField('idCandidato')
    cancel = SubmitField('Cancelar Aprovação')

# Botão de Cancelamento de Aprovação de Lição do MSA (Exercícios Práticos)
class CancelApprovalButtonPractical(FlaskForm):
    lesson_number = StringField('numeroLição')
    candidate_id = StringField('idCandidato')
    submit_complete = SubmitField('Aprovar')
    submit_parcial = SubmitField('Aprovar Parcialmente')
    cancel = SubmitField('Cancelar Aprovação')
    