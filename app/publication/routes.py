from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_required
from .models import Publication
from .services import PublicationService
from app.labyrinth.services import LabyrinthService
from app.labyrinth.algorithms import bfs, matrix_to_graph


publication = Blueprint("publication", __name__, template_folder="templates", url_prefix="/publication")


@publication.route('/', methods=['GET'])
def get_all_publications():
    publications = PublicationService.get_all_publications()
    return render_template('all_publications.html', publications=publications)


@publication.route('/<int:id>', methods=['GET'])
def get_publication(id):
    publication = PublicationService.get_publication_by_id(id)
    if not publication:
        return "Publication not found", 404
    return render_template('publication_detail.html', publication=publication)


@publication.route('/create/<int:id>', methods=['POST'])
@login_required
def publish_labyrinth(id):
    labyrinth = LabyrinthService.get_labyrinth_by_id(id)
    if not labyrinth:
        return "Labyrinth not found", 404
    if labyrinth.user.id != current_user.id:
        return "You don't have permission", 401
    if labyrinth.is_published:
        return "This labyrinth is already published", 400
    solution = bfs(matrix_to_graph(labyrinth.matrix), labyrinth.get_start(), labyrinth.get_end())
    if solution is None:
        return jsonify({"error": "Your labyrinth has no solution."}), 400

    publication = Publication(min_movements=len(solution)-1, labyrinth_id=id)
    publication = PublicationService.create_publication(publication, labyrinth)

    return redirect(url_for('publication.get_publication', id=publication.id))


@publication.route('/solve/<int:id>', methods=['POST'])
def solve_publication(id):
    data = request.json
    path = data["path"]

    publication = PublicationService.get_publication_by_id(id)
    if not publication:
        return "Publication not found", 404

    con1 = path[0] == publication.labyrinth.start and path[-1] == publication.labyrinth.end
    con2 = True
    for coor in path:
        coor = [int(x) for x in coor.split(",")]
        con2 = con2 and publication.labyrinth.matrix[coor[0]-1][coor[1]-1] == 0

    def adjacent(c1, c2):
        x1, y1 = map(int, c1.split(","))
        x2, y2 = map(int, c2.split(","))
        return abs(x1 - x2) + abs(y1 - y2) == 1
    con3 = all(adjacent(c1, c2) for c1, c2 in zip(path, path[1:]))

    if (con1 and con2 and con3):
        return jsonify({"result": "Valid solution in {} steps, best solution in {} steps".format(len(path)-1, publication.min_movements)})
    else:
        return jsonify({"result": "Solution not valid"})
