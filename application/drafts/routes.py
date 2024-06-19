from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from application import db
from application.models import Cube
from flask_login import current_user, login_required
import random

drafts = Blueprint('draft', __name__, template_folder='../templates')

@drafts.route('/draft_sim', methods=['GET', 'POST'])
@login_required
def draft_sim():
    if request.method == 'POST':
        packs = int(request.form['packs'])
        cards_per_pack = int(request.form['cards_per_pack'])
        players = int(request.form['players'])
        cube_id = int(request.form['cube'])

        # Calculate total number of cards needed
        total_cards_needed = packs * cards_per_pack * players

        # Fetch the selected cube
        selected_cube = Cube.query.get(cube_id)

        if not selected_cube:
            flash('Selected cube not found!', 'danger')
            return redirect(url_for('draft.draft_sim'))

        # Split the mainboard into a list of card names
        mainboard_cards = selected_cube.cube_mainboard.split('\n')

        # Ensure we have enough cards
        if len(mainboard_cards) < total_cards_needed:
            flash('Not enough cards in the mainboard of the selected cube!', 'danger')
            return redirect(url_for('draft.draft_sim'))

        # Randomly select the required number of cards
        selected_cards = random.sample(mainboard_cards, total_cards_needed)

        # Organize the selected cards into packs
        packs_list = []
        for i in range(players):
            for j in range(packs):
                pack_start = (i * packs + j) * cards_per_pack
                pack_end = pack_start + cards_per_pack
                packs_list.append(selected_cards[pack_start:pack_end])

        # Store packs in session to access in active_draft route
        session['packs'] = packs_list

        return redirect(url_for('draft.active_draft'))

    user_cubes = Cube.query.filter_by(creator_id=current_user.id).all()
    return render_template('drafts/draft_sim.html', user_cubes=user_cubes)

@drafts.route('/active_draft', methods=['GET'])
@login_required
def active_draft():
    packs = session.get('packs')
    if not packs:
        flash('No active draft found!', 'danger')
        return redirect(url_for('draft.draft_sim'))

    # Get the first pack
    first_pack = packs[0]

    return render_template('drafts/active_draft.html', first_pack=first_pack)
