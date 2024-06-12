from flask import Blueprint, render_template, request, redirect, url_for, flash
from application import db
from application.models import Cube  # Ensure this import statement is present
from flask_login import current_user, login_required
drafts = Blueprint('draft', __name__, template_folder='../templates')

@drafts.route('/draft_sim', methods=['GET', 'POST'])
def draft_sim():
    if request.method == 'POST':
        packs = request.form['packs']
        cards_per_pack = request.form['cards_per_pack']
        players = request.form['players']
        cube = request.form['cube']
        # Process form data here if needed
        return redirect(url_for('draft.active_draft'))
    return render_template('drafts/draft_sim.html')

@drafts.route('/active_draft')
def active_draft():
    return render_template('drafts/active_draft.html')

@drafts.route('/create_cube', methods=['POST'])
@login_required
def create_cube():
    cube_name = request.form['cube_name']
    cube_description = request.form['cube_description']
    cube_file = request.files['cube_file']
    cube_text = request.form['cube_text']

    mainboard = []
    sideboard = []

    if cube_file:
        content = cube_file.read().decode('utf-8')
        mainboard, sideboard = parse_cube_file(content)
    elif cube_text:
        mainboard, sideboard = parse_cube_file(cube_text)

    new_cube = Cube(
        creator_id=current_user.id,
        name=cube_name,
        description=cube_description,
        cube_mainboard="\n".join(mainboard),
        cube_sideboard="\n".join(sideboard)
    )

    db.session.add(new_cube)
    db.session.commit()

    flash('Cube created successfully!', 'success')
    return redirect(url_for('users.account'))

def parse_cube_file(content):
    mainboard = []
    sideboard = []
    current_list = None

    for line in content.splitlines():
        line = line.strip()
        if line.startswith('#'):
            if 'mainboard' in line:
                current_list = mainboard
            elif 'sideboard' in line:
                current_list = sideboard
        elif current_list is not None:
            current_list.append(line)

    return mainboard, sideboard
