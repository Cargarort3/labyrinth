from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_required
from .repositories import Labyrinth
from .services import LabyrinthService
from .algorithms import matrix_to_graph, bfs, dfs, random_walk, path_movements


labyrinth = Blueprint("labyrinth", __name__, template_folder="templates", url_prefix="/labyrinth")


@labyrinth.route('/solve', methods=['POST'])
def solve_labyrinth():
    data = request.json
    matrix = data["labyrinth"]
    start = tuple(data["start"])
    end = tuple(data["end"])
    algorithm = data.get("algorithm", "bfs")

    graph = matrix_to_graph(matrix)

    if algorithm == "dfs":
        path = dfs(graph, start, end)
    elif algorithm == "rw":
        path = random_walk(matrix, start, end)
    else:
        path = bfs(graph, start, end)

    return jsonify({"path": path_movements(path) if path else None})


@labyrinth.route('/create', methods=['GET', 'POST'])
def create_labyrinth():

    if request.method == 'POST':
        data = request.json
        start = tuple(data["start"])
        end = tuple(data["end"])

        if not data["title"].strip():
            return jsonify({"error": "Title is required"}), 400

        labyrinth = Labyrinth(title=data["title"], description=data["description"], matrix=data["labyrinth"], user_id=current_user.id)
        labyrinth.set_start(start)
        labyrinth.set_end(end)

        labyrinth = LabyrinthService.create_labyrinth(labyrinth)

        return redirect(url_for('labyrinth.my_labyrinths'))

    return render_template('labyrinth_form.html')


@labyrinth.route('/', methods=['GET'])
@login_required
def my_labyrinths():
    labyrinths = LabyrinthService.get_my_labyrinths(current_user.id)
    return render_template('my_labyrinths.html', labyrinths=labyrinths)


@labyrinth.route('/<int:id>', methods=['GET'])
@login_required
def get_labyrinth(id):
    labyrinth = LabyrinthService.get_labyrinth_by_id(id)
    if not labyrinth:
        return "Labyrinth not found", 404
    if labyrinth.user.id != current_user.id:
        return "You don't have permission", 401
    return render_template('labyrinth_detail.html', labyrinth=labyrinth)


@labyrinth.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_labyrinth(id):
    labyrinth = LabyrinthService.get_labyrinth_by_id(id)
    if not labyrinth:
        return "Labyrinth not found", 404
    if labyrinth.user.id != current_user.id:
        return "You don't have permission", 401

    if request.method == 'POST':
        data = request.json
        start = tuple(data["start"])
        end = tuple(data["end"])

        if not data["title"].strip():
            return jsonify({"error": "Title is required"}), 400

        labyrinth.title = data["title"]
        labyrinth.description = data["description"]
        labyrinth.matrix = data["labyrinth"]
        labyrinth.set_start(start)
        labyrinth.set_end(end)

        labyrinth = LabyrinthService.update_labyrinth(labyrinth)

        return redirect(url_for('labyrinth.get_labyrinth', id=labyrinth.id))

    return render_template('labyrinth_edit.html', labyrinth=labyrinth)


@labyrinth.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_labyrinth(id):
    labyrinth = LabyrinthService.get_labyrinth_by_id(id)
    if not labyrinth:
        return "Labyrinth not found", 404

    if labyrinth.user.id == current_user.id:
        LabyrinthService.delete_labyrinth(id)
        return "Labyrinth deleted"
    else:
        return "You don't have permission", 401
