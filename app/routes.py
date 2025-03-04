from flask import *
from flask_login import login_required
from .database import SupabaseClient
from .forms import *

routes = Blueprint('routes', __name__)
db = SupabaseClient()

# Função auxiliar para garantir que um aluno está selecionado
def ensure_student_selected():
    if 'act_student' not in session or not session['act_student']:
        if 'students' in session and session['students']:  # Se houver alunos disponíveis
            session['act_student'] = session['students'][0]  # Define o primeiro aluno como padrão
        else:
            flash("Nenhum aluno disponível. Adicione um aluno primeiro.", "warning")
            return redirect(url_for('routes.trocaAluno'))  # Redireciona para escolha do aluno

# Rota Protegida
@routes.route('/ficha')
@login_required
def ficha():
    return render_template('ficha.html')

@routes.route('/hinos', methods=['GET', 'POST'])
@login_required
def hinos():
    check_redirect = ensure_student_selected()
    if check_redirect:
        return check_redirect

    hymns_approved = db.seekApprovedHymns(session['act_student']['id'])

    form_approval_principal_hymn = ApprovalFormPrincipalHymn()
    form_approval_alternative_hymn = ApprovalFormAlternativeHymn()
    cancel_approval_principal = CancelApprovalButtonPrincipal()
    cancel_approval_alternative = CancelApprovalButtonAlternative()

    form_type = request.form.get("form_type")

    if form_type == "principal_hymn" and form_approval_principal_hymn.validate_on_submit():
        date = form_approval_principal_hymn.date.data
        observation = form_approval_principal_hymn.observation.data
        hymn = form_approval_principal_hymn.hymn_number.data
        candidate_id = form_approval_principal_hymn.candidate_id.data
        db.saveApprovalPrincipalHymn(date, observation, hymn, session['user_data']['id'], candidate_id)
        return redirect(url_for('routes.hinos'))
    
    if form_type == "alternative_hymn" and form_approval_alternative_hymn.validate_on_submit():
        date = form_approval_alternative_hymn.date.data
        observation = form_approval_alternative_hymn.observation.data
        hymn = form_approval_alternative_hymn.hymn_number.data
        candidate_id = form_approval_alternative_hymn.candidate_id.data
        db.saveApprovalAlternativeHymn(date, observation, hymn, session['user_data']['id'], candidate_id)
        return redirect(url_for('routes.hinos'))
    
    if form_type == "cancel_principal_hymn" and cancel_approval_principal.validate_on_submit():
        hymn = cancel_approval_principal.hymn_number.data
        candidate_id = cancel_approval_principal.candidate_id.data
        db.cancelApprovalPrincipal(hymn, candidate_id)
        return redirect(url_for('routes.hinos'))
    
    if form_type == "cancel_alternative_hymn" and cancel_approval_alternative.validate_on_submit():
        hymn = cancel_approval_alternative.hymn_number.data
        candidate_id = cancel_approval_alternative.candidate_id.data
        db.cancelApprovalAlternative(hymn, candidate_id)
        return redirect(url_for('routes.hinos'))

    hymns_numbers_principal = [hymn_number['number'] for hymn_number in hymns_approved['principal']]
    hymns_numbers_alternative = [hymn_number['number'] for hymn_number in hymns_approved['alternative']]

    return render_template('hinos.html', 
                           form_approval_principal_hymn=form_approval_principal_hymn,
                           form_approval_alternative_hymn=form_approval_alternative_hymn,
                           cancel_approval_principal=cancel_approval_principal,
                           cancel_approval_alternative=cancel_approval_alternative,
                           hymns=hymns_approved, 
                           list_hymns_principal_approved=hymns_numbers_principal, 
                           list_hymns_alternative_approved=hymns_numbers_alternative,
                           students=session['students'], 
                           act_student=session['act_student'])

@routes.route('/trocaAluno', methods=['GET', 'POST'])
@login_required
def trocaAluno():
    if session['user_data']['nivel']:
        students = session['students']
        for student in students:
            if student['id'] == int(request.form.get('select_field')):
                session['act_student'] = student
                break
        
        return redirect(url_for('routes.teoria'))
    else:
        return None

@routes.route('/teoria', methods=['GET', 'POST'])
@login_required
def teoria():
    check_redirect = ensure_student_selected()
    if check_redirect:
        return check_redirect

    lessons_approved = db.seekApprovedMsaLessons(session['act_student']['id'])

    form_approval_fixing_exercice = ApprovalFormFixingExercice()
    form_approval_practical_exercice = ApprovalFormPracticalExercice()
    form_cancel_fixing_exercice = CancelApprovalButtonFixing()
    form_cancel_practical_exercice = CancelApprovalButtonPractical()

    form_type = request.form.get("form_type")

    if form_type == 'fixing_exercice_approval' and form_approval_fixing_exercice.validate_on_submit():
        date = form_approval_fixing_exercice.date.data
        lesson = form_approval_fixing_exercice.lesson_number.data
        candidate_id = form_approval_fixing_exercice.candidate_id.data
        db.saveApprovalFixingExercice(date, lesson, session['user_data']['id'], candidate_id)
        return redirect(url_for('routes.teoria'))
    
    if form_type == 'practical_exercice_approval' and form_approval_practical_exercice.validate_on_submit():
        date = form_approval_practical_exercice.date.data
        obs = form_approval_practical_exercice.observation.data
        lesson = form_approval_practical_exercice.lesson_number.data
        candidate_id = form_approval_practical_exercice.candidate_id.data
        if form_approval_practical_exercice.submit_complete.data:
            db.saveApprovalBona(date, obs, lesson, session['user_data']['id'], candidate_id, False)
        elif form_approval_practical_exercice.submit_parcial.data:
            db.saveApprovalBona(date, obs, lesson, session['user_data']['id'], candidate_id, True)
        return redirect(url_for('routes.teoria'))
    
    if form_type == 'fixing_exercice_cancel' and form_cancel_fixing_exercice.validate_on_submit():
        lesson = form_approval_fixing_exercice.lesson_number.data
        candidate_id = form_approval_fixing_exercice.candidate_id.data
        db.cancelApprovalFixing(lesson, candidate_id)
        return redirect(url_for('routes.teoria'))
    
    if form_type == 'cancel_practical_lesson' and form_cancel_practical_exercice.validate_on_submit():
        lesson = form_cancel_practical_exercice.lesson_number.data
        candidate_id = form_cancel_practical_exercice.candidate_id.data
        if form_cancel_practical_exercice.submit_complete.data:
            db.modifyStatusPractical(lesson, candidate_id, False)
        elif form_cancel_practical_exercice.submit_parcial.data:
            db.modifyStatusPractical(lesson, candidate_id, True)
        else:
            db.cancelApprovalPactical(lesson, candidate_id)
        return redirect(url_for('routes.teoria'))

    fixing_lessons_approved_number = [lesson_number['number'] for lesson_number in lessons_approved['fixacao']]
    practical_lessons_approved_number = [lesson_number['number'] for lesson_number in lessons_approved['pratico']]

    return render_template('teoria.html', 
                           form_approval_fixing_exercice=form_approval_fixing_exercice,
                           form_approval_practical_exercice=form_approval_practical_exercice,
                           form_cancel_fixing_exercice=form_cancel_fixing_exercice,
                           form_cancel_practical_exercice=form_cancel_practical_exercice,
                           students=session['students'],
                           act_student=session['act_student'], 
                           fixing_lessons_approved=lessons_approved['fixacao'],
                           practical_lessons_approved=lessons_approved['pratico'],
                           fixing_lessons_approved_number=fixing_lessons_approved_number,
                           practical_lessons_approved_number=practical_lessons_approved_number)
